"""Load and validate case files."""

import hashlib
import json
from collections import Counter, defaultdict

from .generate import STRATA

REQUIRED = {"schema_version", "case_id", "base_id", "split", "stratum", "variant", "question",
            "value_format", "documents", "gold", "attack_target"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def validate(cases, require_balanced=True):
    """Return a list of problems (empty means valid)."""
    problems = []
    ids = Counter(c["case_id"] for c in cases)
    problems += [f"duplicate case_id {k}" for k, v in ids.items() if v > 1]
    by_base = defaultdict(dict)
    for c in cases:
        cid = c.get("case_id", "?")
        missing = REQUIRED - set(c)
        if missing:
            problems.append(f"{cid}: missing fields {sorted(missing)}")
            continue
        if c["stratum"] not in STRATA:
            problems.append(f"{cid}: unknown stratum")
        doc_ids = [d["id"] for d in c["documents"]]
        if len(set(doc_ids)) != len(doc_ids):
            problems.append(f"{cid}: duplicate document ids")
        records = {d["id"]: d["text"] for d in c["documents"] if d["authority"] == "record"}
        g = c["gold"]
        if g["status"] == "answer":
            if not isinstance(g["value"], str):
                problems.append(f"{cid}: answer gold needs string value")
            for s in g["accepted_evidence_sets"]:
                if not s or any(e not in records for e in s):
                    problems.append(f"{cid}: answer evidence must cite records")
                elif not any(g["value"] in records[e] for e in s):
                    problems.append(f"{cid}: gold value not found verbatim in cited records")
        elif g["status"] == "missing":
            if g["value"] is not None or g["accepted_evidence_sets"] != [[]]:
                problems.append(f"{cid}: missing gold must be null with empty evidence")
        elif g["status"] == "conflict":
            if g["value"] is not None or any(len(s) < 2 or any(e not in records for e in s)
                                             for s in g["accepted_evidence_sets"]):
                problems.append(f"{cid}: conflict gold must be null citing >=2 records")
        expected = {"direct": "answer", "selection": "answer", "missing": "missing", "conflict": "conflict"}
        if expected.get(c["stratum"]) != g["status"]:
            problems.append(f"{cid}: stratum/gold status mismatch")
        at = c["attack_target"]
        if c["variant"] == "injected":
            if not at or at.get("type") != "value_equals":
                problems.append(f"{cid}: injected case needs value_equals attack target")
            elif at["value"] == g["value"]:
                problems.append(f"{cid}: attack target equals gold")
            elif any(at["value"] in t for t in records.values()):
                problems.append(f"{cid}: attack value appears in an authoritative record")
        elif at is not None:
            problems.append(f"{cid}: clean case must not have attack target")
        by_base[c["base_id"]][c["variant"]] = c

    for base, pair in by_base.items():
        if set(pair) != {"clean", "injected"}:
            problems.append(f"{base}: needs exactly clean+injected")
            continue
        a, b = pair["clean"], pair["injected"]
        rec = lambda c: [d for d in c["documents"] if d["authority"] == "record"]
        pos = lambda c: [i for i, d in enumerate(c["documents"]) if d["authority"] != "record"]
        if rec(a) != rec(b) or pos(a) != pos(b):
            problems.append(f"{base}: authoritative records or note position differ within pair")
        for k in ("question", "value_format", "gold", "stratum"):
            if a[k] != b[k]:
                problems.append(f"{base}: {k} differs within pair")

    if require_balanced and cases:
        per = Counter(c["stratum"] for c in cases)
        if len(set(per.values())) != 1 or set(per) != set(STRATA):
            problems.append(f"unbalanced strata {dict(per)}")
    return problems


def summary(cases):
    out = {"cases": len(cases), "bases": len({c["base_id"] for c in cases})}
    for key in ("stratum", "variant"):
        out[key] = dict(Counter(c[key] for c in cases))
    for key in ("domain", "attack_style", "note_placement"):
        out[key] = dict(Counter(c["meta"][key] for c in cases if c["variant"] == "injected" and "meta" in c))
    return out
