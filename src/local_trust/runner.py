"""Serial, resumable runner. One model loaded at a time, one request at a time.

Rows are appended to results/runs/<run>/<model_id>.jsonl and flushed after every case.
Resume skips a case only if a complete row with the same idempotency key exists.
"""

import datetime as dt
import hashlib
import json
import os
import platform
import signal
import time

from . import cases as cases_mod
from . import prompt as prompt_mod
from . import scoring
from .backends import make_backend


def _sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def _read_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # partial last line from a hard kill; that case is simply rerun
    return rows


def _versions():
    out = {"python": platform.python_version(), "macos": platform.mac_ver()[0]}
    try:
        import importlib.metadata as md

        for pkg in ("mlx", "mlx-lm", "transformers"):
            out[pkg] = md.version(pkg)
    except Exception:
        pass
    return out


class _Stop:
    requested = False


def run(cases_path, models, out_dir, limit=None, log=print):
    cases = cases_mod.load(cases_path)
    problems = cases_mod.validate(cases, require_balanced=False)
    if problems:
        raise SystemExit("case validation failed:\n" + "\n".join(problems[:20]))
    if limit:
        cases = cases[:limit]
    dataset_sha = cases_mod.file_hash(cases_path)[:16]
    os.makedirs(out_dir, exist_ok=True)

    prev = signal.signal(signal.SIGINT, lambda *_: setattr(_Stop, "requested", True))
    try:
        for spec in models:
            if _Stop.requested:
                break
            _run_model(spec, cases, cases_path, dataset_sha, out_dir, log)
    finally:
        signal.signal(signal.SIGINT, prev)


def _run_model(spec, cases, cases_path, dataset_sha, out_dir, log):
    path = os.path.join(out_dir, f"{spec['id']}.jsonl")
    config_sha = _sha(spec)
    key_base = (dataset_sha, prompt_mod.prompt_template_hash(), scoring.SCORER_VERSION, config_sha)
    done = {r["case_id"] for r in _read_rows(path)
            if tuple(r.get("key", [])) == key_base and r.get("status") == "success"}
    todo = [c for c in cases if c["case_id"] not in done]
    log(f"[{spec['id']}] {len(done)} done, {len(todo)} to run")
    if not todo:
        return

    backend = make_backend(spec)
    load_s = backend.load()
    manifest = {
        "model": spec, "config_sha": config_sha, "load_s": load_s,
        "chat_template_sha": backend.chat_template_hash(), "dataset": cases_path,
        "dataset_sha": dataset_sha, "prompt_sha": prompt_mod.prompt_template_hash(),
        "scorer": scoring.SCORER_VERSION, "versions": _versions(),
        "started": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    with open(os.path.join(out_dir, f"{spec['id']}.manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    log(f"[{spec['id']}] loaded in {load_s:.1f}s; warm-up")
    backend.generate(prompt_mod.render(cases[0]))  # unscored warm-up

    t_start = time.perf_counter()
    with open(path, "a", encoding="utf-8") as out:
        for i, case in enumerate(todo, 1):
            if _Stop.requested:
                log("stop requested; checkpoint saved")
                break
            row = {"key": list(key_base), "model_id": spec["id"], "case_id": case["case_id"],
                   "base_id": case["base_id"], "stratum": case["stratum"], "variant": case["variant"],
                   "attack_style": case.get("meta", {}).get("attack_style"),
                   "ts": dt.datetime.now(dt.timezone.utc).isoformat()}
            try:
                gen = backend.generate(prompt_mod.render(case))
                row.update(gen, status="success", score=scoring.score(case, gen["final_text"]))
            except Exception as e:  # infrastructure failure, not a wrong answer
                row.update(status="error", error=f"{type(e).__name__}: {e}"[:500])
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            if i % 10 == 0 or i == len(todo):
                el = time.perf_counter() - t_start
                log(f"[{spec['id']}] {i}/{len(todo)}  {el / i:.1f}s/case  eta {el / i * (len(todo) - i) / 60:.1f} min")
    backend.unload()
