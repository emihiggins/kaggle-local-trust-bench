# Handoff to the Mac execution agent

## Mission

Implement and execute [the study](product/study.md), using Emi's Mac for local inference and Kaggle for the contest-native benchmark. Produce an audited results bundle and ready-to-publish DEV article. This handoff is a specification, not a functioning runner.

## Read in order

1. [Challenge rules](research/challenge.md), especially public benchmark and deadline.
2. [Study requirements](product/study.md) and [benchmark protocol](technical/benchmark.md).
3. [Mac runbook](technical/mac-runbook.md), [implementation contract](technical/implementation.md), and [Kaggle integration](technical/kaggle.md).
4. [Delivery gates](delivery/plan.md) and [open decisions](delivery/decisions-and-risks.md).

## First working session

- Record actual Mac specifications without serial numbers; inspect free disk and OS version.
- In Emi's authenticated Kaggle session, establish that task creation, model access, notebook execution and benchmark visibility work. Record exact free quota and model IDs. Never assume ordinary Kaggle API credentials grant model-proxy access.
- Resolve two local models plus two free hosted models; reserve a third local model for the target scope.
- Create a Python 3.11+ environment and lock dependencies. Do not download weights until disk checks pass. Keep one active model in memory.
- Implement the schema validator and pure scorer first; use the example fixtures only for development. Prove malformed outputs and plausible wrong answers fail.
- Smoke-test one locally loaded model and one Kaggle task on the same 6 fixtures; compare scores by replaying identical output strings through both scorers. Live models need not give identical answers.
- Only then build/review the full synthetic corpus, freeze it, and execute the run matrix.

## When something is blocked

Continue independent work: dataset/scorer work does not require Kaggle access; notebook authoring does not require downloaded Mac models. Do not label a notebook or uploaded CSV as a verified qualifying benchmark. See bounded fallbacks in [decisions](delivery/decisions-and-risks.md).

## Return to Emi

Provide commit SHA; actual hardware manifest; complete run counts and failures; score tables and plots; three audited qualitative examples; exact Kaggle benchmark URL and visibility verification when publication is authorized; final DEV draft; remaining publication/eligibility decisions. State which planned experiments were omitted and why.

Emi has requested planning in the present session. This document is the next agent's execution brief when Emi assigns it; it does not claim benchmarks have already run or authorize public submission by itself.
