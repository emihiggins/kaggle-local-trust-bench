# Decisions, uncertainties and fallback rules

## Adopted design decisions

- D1: One original evidence-grounding benchmark with clean/injected pairs; local performance is supporting evidence. Rationale: strong practical question and direct contest fit.
- D2: Deterministic scoring; no LLM-as-judge expense or judge-model bias.
- D3: MLX LM primary backend; Kaggle-native hosted benchmark separately. No unverified local proxy dependency.
- D4: Small/medium quantized models first; no ANE/Core ML work, training or 70B runs.
- D5: Plans/repo private; only synthetic reviewed entry artifacts become public with Emi's approval.
- D6: No paid services. Model selection and optional expansions bounded by observed resources/free quota.
- D7: Frozen test set and explicit errors; no best-of-N answer selection, prompt tuning on holdout, hidden retries or unsupported claims.

## Assumptions versus blockers

| Item | State | Resolution / fallback |
|---|---|---|
| Reported M5 Max Mac Studio configuration | User supplied, not physically verified | Inventory first; use actual specs in analysis; no need to block planning |
| 48 GB available to models | Not assumed; OS consumes part | Respect runtime memory gate; use smaller models/context |
| Kaggle task/model access | Unverified, UI browser check during research | Day-one authenticated smoke; actual blocker to qualifying publication if unavailable |
| Public benchmark creation/results visibility | Workflow must be tested | 2-hour spike; record blocker, do not substitute a notebook link |
| Kaggle local-result import | Not confirmed | Companion Mac results outside native leaderboard; hosted models supply qualifying runs |
| Free quota for target | Not confirmed | Reduced balanced corpus/models selected before freeze; do not buy calls |
| MLX artifacts | IDs, revisions, ungated access and quantization metadata verified | Download hashes, original weight provenance and Mac smoke still required |
| Hardware/OS runtime compatibility | Not tested | Small MLX smoke; supported llama.cpp fallback if MLX blocked; rerun common protocol, label backend |
| Eligibility/accounts/team status | Emi must confirm before entry | Independent technical work can proceed; no public entry until resolved |
| Exact current best model | Not claimed | Stable baseline roster; substitution before freeze only |

## Risks and bounded responses

- **Deadline:** integrate Kaggle first, not after a week of Mac-only runs. If behind, two local + two hosted models, reduced 60-base dataset, no extensions. If even this cannot finish, report incomplete submission honestly.
- **Weak dataset validity:** structured oracle plus rendered review; don't count trivial JSON compliance alone as trustworthiness. Verify missing/conflict definitions explicitly.
- **Format confound:** no constrained JSON primary track. Report semantic and schema dimensions separately; models unable to comply are valid observed failures, not parser repairs.
- **Reasoning default confound:** inspect Qwen hard-disabled template. If unsupported, select compatible artifact rather than changing primary response budget silently.
- **Kaggle differences:** same prompt content/scorer/data, logged provider defaults. Do not claim precision/backend equivalence or Mac-vs-cloud hardware performance.
- **Swapping or disk exhaustion:** measure before download/run; one model; pause on limits; choose smaller model. No deletion of personal files or system tuning.
- **Model licensing/gated downloads:** select Apache/MIT baselines; third-party conversion provenance still checked. No automatic acceptance of gated terms.
- **Privacy:** wholly synthetic documents. No actual email/calendar/repository contents in cases. Treat injection strings as inert data; evaluated models have no real tools.
- **Overclaiming from small N:** paired bootstrap and clear exploratory labels; no universal security/performance conclusions.
- **Transient API errors:** bounded transport-only retries and explicit coverage; no indefinite polling and no silent case dropping.

## Out of scope / deliberately unresolved

No runnable harness, actual Mac measurement, model download, cloud call, account connection, live task creation or public post is performed by this planning repository. Candidate MLX IDs/revisions are researched; installed runtime versions, downloaded hashes, compatibility and hosted roster/quota remain execution discoveries. No estimated throughput is represented as an observed result. No license for redistribution of third-party model weights is granted by this repo. Original code/data licensing can be chosen before releasing those artifacts; preserve dependency notices.
