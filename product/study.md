# Study brief and requirements

## Intended audience and question

For developers choosing a private, on-device assistant: **how often can a small model return an exact, evidence-backed answer when documents contain missing information, conflicting records, or instruction-like text? What latency and memory trade-off buys additional reliability?**

This is a text capability benchmark with a Mac systems appendix. It is not certification of an autonomous agent, a general security benchmark, or a contest to use every accelerator.

## Prespecified questions

- Q1: How does exact task success change between clean and instruction-injected versions of otherwise identical evidence?
- Q2: Do models abstain correctly on absent or conflicting evidence without refusing answerable cases?
- Q3: What accuracy/latency/memory Pareto frontier is observed on this one Mac?
- Q4 (extension): Does same-base 8-bit quantization improve reliability relative to 4-bit enough to justify its footprint?
- Q5 (extension): Does matched irrelevant context degrade answer quality or injection robustness?

Do not assume larger models win, attacks succeed, or 8-bit helps. Null and mixed findings are valid.

## Scope and requirements

| ID | Requirement |
|---|---|
| R1 | Original synthetic paired corpus, deterministic oracle and versioned freeze |
| R2 | Same prompt content, cases and pure scorer reused locally and on Kaggle |
| R3 | Target three local models; minimum two; at least two available free hosted models |
| R4 | Score grounded correctness, abstention, schema adherence and paired degradation separately |
| R5 | Mac latency/memory measured with declared boundaries; no invented hardware claims |
| R6 | Resumable, auditable runs with explicit error accounting and immutable provenance |
| R7 | Qualifying public Kaggle Benchmark and DEV write-up prepared according to official rules |
| R8 | No private personal data, paid calls or real-world actions by evaluated models |

No authenticated product/persona UI is being built. Roles: Emi owns entry, account access, eligibility and publication approval; execution agent authors/runs experiments; judges/readers see only approved synthetic public assets/results. They must never receive machine serial numbers, private account data or credentials.

## Claim-to-evidence matrix

All entries below are **planned**, not verified.

| Potential public claim | Required behavior/evidence | Boundary | Acceptance |
|---|---|---|---|
| "Model X is more reliable on this task" | Frozen shared cases, exact scoring, paired uncertainty, complete denominators | Not general intelligence or causal model-size attribution | A3, A5, A7 |
| "Document instructions changed outputs" | Matched clean/attack pairs and auditable raw examples | Distinguish syntax errors from observed attack-target compliance | A3, A7 |
| "Model X runs locally on this Mac" | Verified machine manifest and offline local generation after download | No ANE use inferred from chip specs | A1, A5 |
| "4-bit reduced reliability" | Same-base/revision/backend paired quantization comparison | No cross-family/backend causality claim | A8 |
| "Benchmark reproducible on Kaggle" | Hosted executions, shared fixture scoring, pinned data/scorer hashes | Not an assertion local models ran on Kaggle | A2, A6 |
| "Submission ready" | Working public benchmark link and fully evidenced English draft | Only Emi-approved public publication counts as entered | A9 |

Avoid "secure", "hallucination-free", "best local model", "zero cost" (hardware/electricity exist), and "Neural Engine accelerated" without evidence.
