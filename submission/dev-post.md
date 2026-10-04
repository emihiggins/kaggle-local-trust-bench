---
title: "Can a local AI model trust the documents it reads?"
published: false
tags: devchallenge, kagglechallenge, ai, machinelearning
---

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23).*

> DRAFT SKELETON: every `[bracket]` is filled only from `results/summary/*.json` after the frozen runs. The title is a question, not a finding. Target length is 1,200–1,800 words.

## What I Benchmarked

[Hook, 2–3 sentences: you point a local model at your invoices or tickets. You need the exact fact, an honest "not there" or "records disagree", and no obedience to text inside the files.]

Local Trust Bench gives a model a question and a handful of short synthetic records, then asks for one JSON object: `answer` with the exact value and the IDs of the records that prove it, or `missing`, or `conflict`. [Insert the compact example from the README.]

Each of the [120] base scenarios comes in two versions that differ in only one document, an untrusted note in the same position:

- **clean**: a harmless filing note
- **injected**: a planted instruction to give a wrong value. It comes in three styles: a plain command, a fake "records office" correction, and a fake example answer.

The scenarios cover four kinds of question: direct lookup, picking the right record among look-alikes, a missing fact, and conflicting records. A **crowded** version adds 12 look-alike records to the same scenarios. Scoring is a deterministic checker, with no LLM judge. A case counts only if the JSON, the status, the exact value and the exact evidence are all right.

[Why this matters, in one paragraph. Make clear this is instruction-following in data, not an agent-security test: the models had no tools.]

## Models Tested

[Table: model · where it ran (Mac / Kaggle) · quantization · thinking setting · why chosen.]

Local runs: Mac Studio, M5 Max (18-core CPU, 40-core GPU), 48 GB unified memory, macOS 27.0, MLX LM [version], greedy decoding, one model and one request at a time. Hosted runs: Kaggle Benchmarks free quota, with the same prompt, cases and scorer code; provider defaults are noted where they can't be controlled.

## Findings

[Lead with the single most useful lesson, in one sentence, with its number and interval.]

[Chart 1: clean vs injected strict success per model, with intervals.]

[How models fail when they fail (chart 2): adopting the planted value, inventing a "conflict" and citing the note, or breaking the output format. Which attack style worked best?]

[Crowding: did 12 look-alike records change accuracy or robustness?]

[Chart 3: reliability vs. median latency and memory on the Mac. Which model would I actually run for this job, and why?]

[Extensions that were actually run: thinking on/off, 8-bit vs. 4-bit, Ollama vs. MLX. Mark the ones not run as omitted.]

[Three audited examples, quoted verbatim: a clean success, an informative injected failure, an abstention or conflict case.]

[What surprised me. A null result is fine to report.]

**Limitations.** Synthetic, template-generated English data; 120 scenarios per condition; one Mac; specific quantized builds; unseen hosted-provider settings; no real tools; greedy decoding only. [Plus any failures or omitted runs.]

**What next.** [One follow-up justified by the results.]

## My Benchmark

- **Kaggle benchmark (public):** [URL, checked signed out]
- Task files, frozen cases and scorer: [Kaggle task links]; code and raw outputs: [GitHub link if made public]

## Credits and Reproducibility

Built with Kaggle Benchmarks and MLX LM. The models are by Qwen, Google and OpenAI, with MLX conversions by mlx-community. Protocol v1, dataset sha256 [hash], runs on [dates]. Written with AI coding assistance; all results come from the logged runs. [Collaborators' DEV handles, if any.]
