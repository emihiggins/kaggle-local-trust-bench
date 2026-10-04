"""CLI: python -m local_trust {generate,validate,run,analyze,export-kaggle}"""

import argparse
import json

from . import cases as cases_mod
from . import generate as gen


def _models(config, ids):
    cfg = json.load(open(config))
    pool = {m["id"]: m for m in cfg["models"] + cfg.get("extensions", [])}
    if not ids:
        return cfg["models"]
    unknown = [i for i in ids if i not in pool]
    if unknown:
        raise SystemExit(f"unknown model ids: {unknown}")
    return [pool[i] for i in ids]


def main():
    p = argparse.ArgumentParser(prog="local_trust")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate", help="write dev and test case files")
    g.add_argument("--out-dir", default="data")
    v = sub.add_parser("validate")
    v.add_argument("cases")
    r = sub.add_parser("run", help="run local models over a case file (resumable)")
    r.add_argument("--cases", required=True)
    r.add_argument("--config", default="configs/models.json")
    r.add_argument("--models", nargs="*", help="model ids (default: primary roster)")
    r.add_argument("--out", required=True, help="results directory, e.g. results/runs/test-v1")
    r.add_argument("--limit", type=int)
    a = sub.add_parser("analyze")
    a.add_argument("--runs", nargs="+", required=True, help="results directories")
    a.add_argument("--cases", required=True)
    a.add_argument("--out", default="results/summary")
    k = sub.add_parser("export-kaggle", help="build self-contained Kaggle task files")
    k.add_argument("--cases", required=True)
    k.add_argument("--out-dir", default="kaggle")
    args = p.parse_args()

    if args.cmd == "generate":
        variants = [(split, n, seed, suffix, extra)
                    for split, n, seed in (("dev", 6, 7), ("test", 30, 20261004))
                    for suffix, extra in (("", 0), ("-crowded", gen.CROWDED_EXTRA))]
        for split, n, seed, suffix, extra in variants:
            cs = gen.generate(split, n, seed, extra=extra)
            problems = cases_mod.validate(cs)
            if problems:
                raise SystemExit("\n".join(problems))
            path = f"{args.out_dir}/{split}{suffix}-{gen.GENERATOR_VERSION}.jsonl"
            gen.write_jsonl(cs, path)
            print(path, json.dumps(cases_mod.summary(cs)))
    elif args.cmd == "validate":
        cs = cases_mod.load(args.cases)
        problems = cases_mod.validate(cs)
        print("\n".join(problems) or "ok")
        print(json.dumps(cases_mod.summary(cs), indent=1))
        print("sha256", cases_mod.file_hash(args.cases))
        raise SystemExit(1 if problems else 0)
    elif args.cmd == "run":
        from . import runner
        runner.run(args.cases, _models(args.config, args.models), args.out, limit=args.limit)
    elif args.cmd == "analyze":
        from . import analysis
        analysis.main(args.runs, args.cases, args.out)
    elif args.cmd == "export-kaggle":
        from . import kaggle_export
        kaggle_export.main(args.cases, args.out_dir)


if __name__ == "__main__":
    main()
