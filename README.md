# Local Trust Bench

**Status: researched planning handoff, 2026-10-04. No benchmark implementation, model runs, measured results, Kaggle publication, or DEV submission yet.**

Can a model running on a personal Mac reliably extract facts, admit missing evidence, and ignore instructions embedded in the documents it reads? Measure this with an original, mechanically scored benchmark; publish the same tasks on Kaggle; add a local accuracy/latency/memory study.

Target: Emi's reported M5 Max Mac Studio, 18-core CPU, 40-core GPU, 16-core Neural Engine, 48 GB unified memory, 512 GB storage. Hardware identity and available resources must be verified on the actual machine. This planning host is not the benchmark machine.

## Start here

Give the executing agent [START_HERE.md](START_HERE.md). It contains the task order and boundaries. The repo is private by default; the contest requires a **public Kaggle benchmark and published DEV article**, not a public GitHub repo.

## Canonical plan map

| Document | Owns |
|---|---|
| [Challenge requirements](research/challenge.md) | Official rules, deadline, eligibility and submission criteria |
| [Research and options](research/options-and-sources.md) | Sources, tooling preflight, candidate ranking and model evidence |
| [Study brief](product/study.md) | Research questions, scope, requirements and intended claims |
| [Benchmark specification](technical/benchmark.md) | Dataset, prompt, scoring, metrics and statistical protocol |
| [Mac execution](technical/mac-runbook.md) | Hardware discovery, models, resource budgets and run matrix |
| [Implementation contract](technical/implementation.md) | Modules, data formats, interfaces, resume and test behavior |
| [Kaggle integration](technical/kaggle.md) | Hosted task flow, platform discovery and parity gates |
| [Delivery plan](delivery/plan.md) | Sequence, dates, acceptance criteria and completion evidence |
| [Decisions and risks](delivery/decisions-and-risks.md) | Assumptions, choices, fallbacks and blockers |
| [DEV draft](submission/dev-post.md) | Submission structure; intentionally no fabricated findings |
| [Example fixtures](examples/cases.jsonl) | Illustrative development cases, not the final study dataset |

Next action: verify Kaggle task creation/model quota and the Mac inventory, then implement the portable scorer and a tiny end-to-end smoke run before creating the full dataset.
