# Working plan

Owner: Emi. Last updated 2026-10-04. Deadline: **Oct 11, 2026, 23:59 PDT** (Oct 12, 06:59 UTC). Target: publish the DEV post on Oct 10.

This replaces the first-pass planning handoff (see git history at `8aa2f44`). I kept its core idea: an evidence-grounded extraction benchmark with paired clean/injected cases, deterministic scoring, and a local study plus a Kaggle study. I dropped its 2025-era model list, its multi-document process, and the assumption that Kaggle hosted models can't be driven from the Mac.

## What changed from the first-pass plan, and why

| Decision | Why |
|---|---|
| **Current models.** Qwen3.5/3.6/3.8, Gemma 4, gpt-oss replace Qwen3/Phi-4-mini | The first plan picked models a year old. A public article should test what people would install today. |
| **Six local models instead of three** | Measured smoke speed is 0.2–0.6 s per case, so a full 240-case pass takes minutes per model, not hours. |
| **Added a crowded condition** (+12 look-alike records) | Dev smoke runs score about 100% on clean standard cases even at 4B. A second, paired difficulty level guards against a ceiling and answers "do distractors matter?" |
| **Timing collected on every case** instead of a separate timing block | Inference is cheap; this gives 240+ timing samples per model for free. |
| **Kaggle via CLI** (`kaggle benchmarks tasks push/run`) | The current CLI supports pushing and running tasks from a local machine. Notebook-only authoring isn't needed. |
| **Dropped the stability-repeat study** | Greedy decoding is deterministic locally, so repeats measure nothing. Hosted repeats aren't worth the quota. |
| **Raw outputs committed** (synthetic inputs only) | Public auditability is a selling point. Machine identifiers and credentials still stay out. |
| **Added a lenient (fence-stripped) diagnostic and a cited-untrusted-note metric** | The smoke test already showed the most common injection failure: a model calls a false "conflict" and cites the note. These metrics make that visible. |

## Status

- [x] Mac verified: Mac Studio, M5 Max, 18 CPU cores (6S+12P), 40 GPU cores, 48 GB, macOS 27.0. The HF cache is on the external drive (3 TB free).
- [x] uv environment (Python 3.12, mlx 0.32.3, mlx-lm 0.32.0). Metal works.
- [x] Generator, validator, renderer, scorer, MLX and Ollama adapters, resumable runner, analysis and charts, Kaggle exporter.
- [x] 31 tests: gold scores perfectly, malformed or plausible-wrong answers fail, no gold leakage, deterministic corpus, Kaggle export parity.
- [x] All 6 local models downloaded (pinned revisions) and smoke-tested on the 48-case dev set: every case completed, JSON valid, no thinking leakage, nothing hit the token cap. Speed 0.2–1.1 s/case; peak MLX memory 3–20 GB. Gemma 4 needed an explicit `enable_thinking=false`.
- [x] Repo will be public (Emi, 2026-10-04). Merged to `main`.
- [ ] **Emi:** confirm eligibility and accept the current official rules (see [docs/challenge.md](docs/challenge.md)).
- [ ] **Emi:** choose a license before the repo goes public (suggested: MIT for code, CC BY 4.0 for data).
- [ ] **Emi:** log in to Kaggle on this Mac (`kaggle auth login`, then `kaggle benchmarks init -y`).
- [ ] Review and freeze the test set (next section).
- [ ] Measured runs, analysis, article, publication.

## Schedule

| Day | Work | Gate to pass |
|---|---|---|
| **Sun Oct 4** | Harness, docs, smoke tests ✔ | Tests green; 3 models smoke-tested |
| **Mon Oct 5** | Kaggle login, list models, push the **dev** task and run 1 hosted model. Review the test set, freeze it, tag `protocol-v1`.  | Hosted run produces a score that matches local rescoring of the same raw outputs. The frozen hashes are committed *before* any test-set call. |
| **Tue Oct 6** | Local primary: 6 models × (standard + crowded) × 240 cases (~2,900 calls; an estimated 1–2 h total). Hosted: 3–4 models × standard clean+injected. Add crowded only if quota allows. | Full coverage, or every failure disclosed. Quota ledger recorded. |
| **Wed Oct 7** | Extensions in priority order: (1) Qwen3.8-27B thinking on vs. off, (2) 8-bit vs. 4-bit, (3) Ollama vs. MLX. Then analysis. | Each extension gets its own table, or is marked omitted. |
| **Thu Oct 8** | Audit 3 qualitative examples against the source docs. Charts. Draft the article. Build the Kaggle benchmark collection in the UI. | Every number in the draft traces to `results/summary/*.json`. |
| **Fri Oct 9** | Emi reviews the draft and the benchmark. Make the Kaggle benchmark public and check it signed out. | The public URL works in a private window. |
| **Sat Oct 10** | Publish the DEV post (with Emi's approval). | Post is live with the `kagglechallenge` tag and a working benchmark link. |
| Sun Oct 11 | Buffer only. | — |

If anything slips, cut in this order: Ollama runtime comparison, then 8-bit, then the crowded hosted runs, then the thinking extension. Keep these at all costs: the standard test set on at least 4 local and 2 hosted models, the Kaggle benchmark, and an honest article.

## Freeze checklist (Oct 5, before any test-set inference)

1. Read at least 24 rendered test bases (6 per stratum, a mix of domains), plus every conflict pattern and every attack style. Check that each question is answerable exactly as the gold says. Log the reviewer and any fixes in `data/REVIEW.md`.
2. Known generator quirk to decide on: some alternate date fields aren't chronologically consistent (e.g. a purchase date after the warranty expiry). Either fix it or note it as a limitation. It doesn't affect gold.
3. `uv run python -m local_trust validate` on all four files. Record the sha256 values in `data/FREEZE.md` with the prompt hash, scorer version and `configs/models.json` hash.
4. Commit and tag `protocol-v1`. After that, any fix means a v2 and a rerun.

## Hosted model selection (Oct 5)

Choose from `kaggle b t models`. Aim for 3–4 models from different vendors, including at least one economical model and one frontier model, and if possible a hosted Gemma (the same family as the local Gemma 4, which gives a nice local vs. hosted comparison). Record exact slugs, the date, and any controls that can't be set. Stop when the free quota runs out; there's no paid fallback.

## Article angle (draft hypotheses, not findings)

The question the article answers: *"If I give a local model my documents, when can I trust its answer?"* The structure is clean accuracy, then what breaks under injection and how (adopting the planted value vs. a false conflict vs. a format failure), then whether a bigger model, more crowding, thinking or 8-bit changes it, and finally what that costs in latency and memory on this Mac. The early smoke signal (Qwen3.5-4B false-conflicts on 25% of injected dev cases, while Gemma 4 E4B does so on about 4%) is a lead to check on the test set, not a result.

## Ground rules (kept from the first plan)

- No paid inference, cloud rentals or subscriptions. Kaggle free quota only.
- Evaluated models get one text prompt: no tools, files, network or code execution. Document instructions are inert data.
- No LLM judge. No tuning on the test set. No retries of wrong answers. No dropping failed cases.
- Weights, credentials, `.env`, caches and machine serial numbers or UUIDs stay out of Git.
- Don't change macOS memory limits or other system settings to make a model fit. Use a smaller model.
- Publishing the Kaggle benchmark or the DEV post needs Emi's explicit go-ahead. The repo is intended to be public, so never commit anything that couldn't be.
- No claim without evidence in `results/`. Avoid "secure", "hallucination-free", "best local model" and "uses the Neural Engine".
