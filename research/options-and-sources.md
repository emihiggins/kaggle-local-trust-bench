# Research, existing solutions and experiment choice

Research date: 2026-10-04. Sources are primary unless noted. Branch URLs are mutable; pin dependency/model revisions during execution. Access and hardware behavior not observed on the Mac remain unverified.

## Candidate benchmarks — planning judgment, not measured results

| Candidate | Insight/novelty potential | Mac fit | Delivery risk | Decision |
|---|---|---|---|---|
| Evidence-grounded JSON extraction with missing facts, conflicts and document injection | High: shows when a local assistant is trustworthy and what breaks it | Excellent: short text, exact scoring, modest models | Low–medium | **Primary** |
| Same-model 4-bit versus 8-bit reliability | High when paired with actual task outcomes | Excellent on a modest model | Low | First extension |
| Longer context / distractor dilution | High, exposes reliability beyond clean prompts | Good at bounded context | Medium: tokenization and KV memory | Second extension |
| MLX versus llama.cpp throughput | Useful systems appendix; less original alone | Excellent | Medium: quantization parity confound | Optional appendix |
| SQL generation against synthetic SQLite datasets | High, executable oracle | Good CPU/GPU balance | Medium: sandboxing and semantic scoring | Alternative if domain preference changes before freeze |
| Multi-turn tool-use recovery | High practical relevance | Good model fit | High: tool schemas, state, retry semantics | Defer |
| Receipt/screenshot extraction | Interesting multimodal task | Plausible with small VLMs | High: image assets, OCR scoring, model adapters | Defer |
| Generic MMLU/HumanEval/leaderboard replication | Low originality without a new hypothesis | Possible | Familiar but weak challenge narrative | Sanity check only, not main entry |
| ANE versus GPU inference | Hardware-interesting | Depends on Core ML model conversion | High: backend support and unequal models | Out of scope |

Recommendation: one coherent benchmark with interpretable slices, not unrelated mini-benchmarks. No guarantee of contest success.

## Existing solutions preflight

- **Kaggle Benchmarks SDK**: required hosted integration; tasks, assertions, datasets and run artifacts already exist. Reuse these instead of building a leaderboard platform. [README](https://github.com/Kaggle/kaggle-benchmarks), [quick start](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/quick_start.md), [cookbook](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md). Observed `ci` revision: `fb51e8b242563c6cece48d052dbf5375b9bee4c5`.
- **MLX LM**: Apple-silicon Python inference, quantization, streaming and model loading. Best primary local backend because scorer and runner are Python. MIT; repository active on research date. [README](https://github.com/ml-explore/mlx-lm). Observed revision: `5cfec4cb39deba54210b3ff4d86f2337c7bc10b5`.
- **llama.cpp / llama-bench**: reuse for optional Metal/CPU and prompt/decode throughput; no bespoke timing engine for that appendix. Its measurements exclude tokenization and sampling, unlike end-to-end application timing. [tool documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md). Observed revision: `2ca15f5404760548c39e7b92bd43116a09414a1a`.
- **lm-evaluation-harness**: maintained general task/backends/metrics framework; valuable for existing benchmarks, but extra abstraction for this tiny, paired corpus and Kaggle export. Reconsider if implementing the runner exceeds one day. [Repository](https://github.com/EleutherAI/lm-evaluation-harness).
- **Ollama / LM Studio**: plausible convenience alternatives, not selected as primary; avoid adding another runtime and undocumented defaults. No need for a paid platform.

Custom work is justified only for this original dataset, scorer, minimal adapters, resume ledger and analysis. Do not build authentication, UI, hosted APIs, or a general experiment-management platform.

## Platform findings

[Google's announcement](https://blog.google/innovation-and-ai/technology/developers-tools/kaggle-community-benchmarks/) confirms free model access within quotas, tasks grouped into benchmarks, recorded interactions and leaderboard results.

The public Kaggle page returned a reCAPTCHA/browser-check page during research. Therefore account access, exact model roster, quota, current publication clicks and local-result import support are **not verified**.

The SDK's [local development guide](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/local_development.md) explicitly says local development via its model proxy is for the internal Kaggle team. Do not promise that an ordinary Kaggle token enables remote model calls from the Mac. Hosted notebooks plus an independent MLX runner are the supported planning path. No requirement to expose a local server to Kaggle.

## Model evidence and selection

Primary model cards:

- [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B): Apache-2.0; small family baseline.
- [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B): Apache-2.0; 8.2B parameters; explicit thinking/non-thinking modes; native context 32,768 tokens. Its card documents MLX LM and llama.cpp support. Default thinking must not accidentally enter the non-thinking comparison.
- [Qwen3-30B-A3B](https://huggingface.co/Qwen/Qwen3-30B-A3B): Apache-2.0; 30.5B total / 3.3B active parameters. **All weights still need storage and memory**, not just active parameters. Stretch model, not a fit guarantee.
- [Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct): MIT; useful non-Qwen family contrast. Exact MLX artifact/tokenizer compatibility must pass a smoke test.
- [Gemma 3 12B IT](https://huggingface.co/google/gemma-3-12b-it): card fetch gated (401). Optional only after Emi accepts applicable terms and compatible artifacts are verified; not on critical path.
- [Ministral 8B 2410](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410): research-license conditions in model card; not chosen over easier permissively licensed candidates.

These are researched, feasible baseline candidates, not a claim that they are the newest/best models in October 2026. Execution may replace a candidate with a better available same-size model **before protocol freeze**, logging rationale, license, revisions and resource fit. Do not spend the week continually chasing releases.

## Verified downloadable candidate metadata

Hugging Face API and each artifact's `config.json` were checked on 2026-10-04. All five candidates below were ungated, declared the matching base model, and declared group size 64. Metadata verification is not a successful Mac inference test or proof that two conversions used the identical base weight revision.

| MLX artifact | Observed immutable revision | Bits |
|---|---|---|
| [Qwen3-4B-4bit](https://huggingface.co/mlx-community/Qwen3-4B-4bit) | `4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25` | 4 |
| [Qwen3-8B-4bit](https://huggingface.co/mlx-community/Qwen3-8B-4bit) | `545dc4251c05440727734bcd94334791f6ab0192` | 4 |
| [Phi-4-mini-instruct-4bit](https://huggingface.co/mlx-community/Phi-4-mini-instruct-4bit) | `ac1c269cb4222a4e136a3d09edad301056c1f36a` | 4 |
| [Qwen3-8B-8bit](https://huggingface.co/mlx-community/Qwen3-8B-8bit) | `48a0b75b1ae72503e21e1558d040bc227510ff06` | 8 |
| [Qwen3-30B-A3B-4bit](https://huggingface.co/mlx-community/Qwen3-30B-A3B-4bit) | `d388dead1515f5e085ef7a0431dd8fadf0886c57` | 4 |

Start with these revisions rather than an unpinned `main`. Inspect license/provenance and hash downloaded files, then smoke-test. For a causal quantization comparison, additionally establish identical original weight revision and conversion recipe apart from bit width; otherwise describe it as a comparison of distributed artifacts. If artifacts are incompatible, select alternatives before freeze and document the replacement.
