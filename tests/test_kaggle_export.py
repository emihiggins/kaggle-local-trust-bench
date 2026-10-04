"""Run a generated Kaggle task file against a fake kaggle_benchmarks module.

Proves the inlined renderer/scorer give the same scores as the local package for identical
raw responses, and that the aggregate counts wrong answers and unfinished cases as failures.
"""

import json
import sys
import types

from local_trust import cases as cases_mod
from local_trust.generate import generate, write_jsonl
from local_trust.kaggle_export import build
from local_trust.prompt import render
from local_trust.scoring import score


def _fake_kbench(responder, captured):
    kb = types.ModuleType("kaggle_benchmarks")

    class Runs(list):
        @property
        def completed_runs(self):
            return self

        @property
        def errored_runs(self):
            return []

    def task(name=None, store_task=True):
        def deco(fn):
            def evaluate(llm, evaluation_data, **kw):
                return Runs(types.SimpleNamespace(result=fn(llm[0], **row))
                            for row in evaluation_data.to_dict("records"))

            def run(llm):
                captured["result"] = fn(llm)

            fn.evaluate, fn.run = evaluate, run
            return fn
        return deco

    class Client:
        class enable_cache:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

    kb.task, kb.client = task, Client
    kb.llm = types.SimpleNamespace(prompt=responder)
    return kb


def test_generated_task_matches_local_scorer(tmp_path, monkeypatch):
    cases = generate("k", 2, 5)
    path = tmp_path / "k.jsonl"
    write_jsonl(cases, path)
    task_file = build(str(path), "injected", str(tmp_path))
    injected = [c for c in cases if c["variant"] == "injected"]
    by_prompt = {render(c): c for c in injected}

    # Deterministic fake model: gold for the first half, the attacker's value for the rest.
    responses = {}
    for i, c in enumerate(injected):
        g = c["gold"]
        if i % 2 == 0:
            responses[c["case_id"]] = json.dumps({"status": g["status"], "value": g["value"],
                                                  "evidence_ids": g["accepted_evidence_sets"][0]})
        else:
            responses[c["case_id"]] = json.dumps({"status": "answer", "value": c["attack_target"]["value"],
                                                  "evidence_ids": ["D1"]})
    captured = {}
    fake = _fake_kbench(lambda prompt: responses[by_prompt[prompt]["case_id"]], captured)
    monkeypatch.setitem(sys.modules, "kaggle_benchmarks", fake)
    exec(compile(open(task_file).read(), task_file, "exec"), {"__name__": "kaggle_task"})

    local = [score(c, responses[c["case_id"]])["strict_success"] for c in injected]
    per = {}
    for c, ok in zip(injected, local):
        per.setdefault(c["stratum"], []).append(ok)
    expected = sum(sum(v) / len(v) for v in per.values()) / len(per)
    assert captured["result"] == expected
    assert 0 < expected < 1
    assert cases_mod.validate(cases) == []
