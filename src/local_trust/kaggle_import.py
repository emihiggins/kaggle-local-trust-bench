"""Convert downloaded Kaggle Benchmark runs into the local row format, with parity checks.

For every hosted case it verifies that (1) the prompt Kaggle sent equals the local
render(case) and (2) re-scoring the raw response with the local scorer reproduces the score
stored by the hosted task. Any mismatch aborts the import.

Layout read: <src>/<task>/<version>/<model>/<run_id>/local_trust_case-*.run.json
Rows written: <out>/kaggle-<model>.jsonl. If a model was run more than once (e.g. after HTTP
429s), each case takes its response from the most recent run that completed it, and the row
records which run that was.
"""

import glob
import json
import os
from collections import defaultdict

from . import cases as cases_mod
from . import prompt as prompt_mod
from . import scoring


def _case_runs(src):
    for path in glob.glob(os.path.join(src, "*", "*", "*", "*", "local_trust_case-*.run.json")):
        task, version, model, run_id = path.split(os.sep)[-5:-1]
        with open(path, encoding="utf-8") as f:
            yield task, int(version), model, run_id, json.load(f)


def _sent_prompt(run):
    for conv in run.get("conversations", []):
        for req in conv.get("requests", []):
            for content in req.get("contents", []):
                if content.get("role", "").endswith("USER"):
                    return "".join(p.get("text", "") for p in content.get("parts", []))
    return None


def _metrics(run):
    for conv in run.get("conversations", []):
        for req in conv.get("requests", []):
            if req.get("metrics"):
                return req["metrics"]
    return {}


def import_runs(srcs, cases_path, out_dir, log=print):
    cases = {c["case_id"]: c for c in cases_mod.load(cases_path)}
    dataset_sha = cases_mod.file_hash(cases_path)[:16]
    best = {}  # (model, case_id) -> row
    seen_runs = defaultdict(set)
    mismatches = []
    for src in srcs:
        for task, version, model, run_id, run in _case_runs(src):
            seen_runs[model].add((task, version, run_id))
            res = [r.get("dictResult") for r in run.get("results", []) if r.get("dictResult")]
            completed = run.get("state", "").endswith("COMPLETED") and res and "case_id" in res[0]
            if not completed:
                continue  # errored case (e.g. HTTP 429); counted later as not completed
            hosted = res[0]
            case = cases.get(hosted["case_id"])
            if case is None:
                continue  # a case from a different dataset (e.g. dev task)
            sent = _sent_prompt(run)
            if sent != prompt_mod.render(case):
                mismatches.append(f"{model} {hosted['case_id']}: prompt differs from local render")
            local = scoring.score(case, hosted["raw"])
            if local != hosted["score"]:
                mismatches.append(f"{model} {hosted['case_id']}: local score != hosted score")
            m = _metrics(run)
            row = {
                "key": [dataset_sha, prompt_mod.prompt_template_hash(), scoring.SCORER_VERSION, "kaggle"],
                "model_id": f"kaggle-{model}", "case_id": case["case_id"], "base_id": case["base_id"],
                "stratum": case["stratum"], "variant": case["variant"],
                "attack_style": case.get("meta", {}).get("attack_style"),
                "ts": run.get("startTime"), "status": "success", "score": local,
                "raw_output": hosted["raw"], "final_text": hosted["raw"],
                "provider_model": run.get("modelVersion", {}).get("slug"),
                "kaggle_task": task, "kaggle_task_version": version, "kaggle_run_id": run_id,
                "prompt_tokens": m.get("inputTokens"), "output_tokens": m.get("outputTokens"),
                # Hosted backend latency: never compared with Mac latency.
                "hosted_backend_latency_s": int(m["totalBackendLatencyMs"]) / 1000 if m.get("totalBackendLatencyMs") else None,
            }
            k = (row["model_id"], row["case_id"])
            if k not in best or (version, run_id) > (best[k]["kaggle_task_version"], best[k]["kaggle_run_id"]):
                best[k] = row
    if mismatches:
        raise SystemExit("parity check failed:\n" + "\n".join(mismatches[:20]))

    os.makedirs(out_dir, exist_ok=True)
    by_model = defaultdict(list)
    for (model_id, _), row in best.items():
        by_model[model_id].append(row)
    for model_id, rows in sorted(by_model.items()):
        rows.sort(key=lambda r: r["case_id"])
        with open(os.path.join(out_dir, f"{model_id}.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        runs_used = sorted({(r["kaggle_task"], r["kaggle_task_version"], r["kaggle_run_id"]) for r in rows})
        log(f"{model_id}: {len(rows)}/{len(cases)} cases from {len(runs_used)} run(s); "
            f"{len(seen_runs[model_id.removeprefix('kaggle-')])} run(s) seen; parity OK")
    return by_model
