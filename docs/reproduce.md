# Reproduce

## Local (Apple silicon)

Requirements: an Apple-silicon Mac, [uv](https://docs.astral.sh/uv/), and about 70 GB of free disk for the full six-model roster. The smallest model needs 3 GB. Models download into your normal Hugging Face cache, or into `HF_HOME` if you've set it.

```sh
uv sync --all-extras
uv run pytest                                   # should report all tests passing

# 1. Data (deterministic; should reproduce the committed files byte for byte)
uv run python -m local_trust generate
uv run python -m local_trust validate data/test-v1.jsonl   # prints counts + sha256

# 2. Download pinned weights (optional; `run` downloads on first load)
uv run hf download mlx-community/Qwen3.5-4B-MLX-4bit --revision 32f3e8ecf65426fc3306969496342d504bfa13f3

# 3. Run. Resumable: re-running skips completed cases with the same dataset/prompt/scorer/config.
uv run python -m local_trust run --cases data/test-v1.jsonl --out results/runs/test-v1
uv run python -m local_trust run --cases data/test-crowded-v1.jsonl --out results/runs/test-crowded-v1
#    one model:            --models qwen3.5-4b-4bit
#    an extension:         --models qwen3.8-27b-8bit     (ids from configs/models.json)
#    quick check:          --limit 12

# 4. Analyze (tables, JSON and PNG charts written to results/summary/)
uv run python -m local_trust analyze --runs results/runs/test-v1 --cases data/test-v1.jsonl --out results/summary
```

Each model writes `results/runs/<run>/<model>.jsonl`, one row per case: the raw output, the parsed final text, the score, token counts, timings and peak memory. It also writes `<model>.manifest.json` with the pinned revision, chat-template hash, package versions and load time. Ctrl-C stops after the current case, and the next run resumes from there.

Before a timed run, close heavy apps, keep the Mac on AC power, and don't run anything else on the GPU. Only one model is ever loaded at a time.

## Kaggle (hosted models)

```sh
uv tool install kaggle                          # Kaggle CLI ≥ 2.2
kaggle auth login                               # or place an API token as documented by Kaggle
kaggle benchmarks init -y                       # writes model-proxy creds to .env (git-ignored)
kaggle benchmarks tasks models                  # list available hosted models

uv run python -m local_trust export-kaggle --cases data/test-v1.jsonl   # writes kaggle/*.py
kaggle b t push local-trust-test-v1-clean -f kaggle/local-trust-test-v1-clean.py --wait
kaggle b t run  local-trust-test-v1-clean -m <model> --wait
kaggle b t download local-trust-test-v1-clean -o results/kaggle
```

The generated task files are self-contained. The prompt renderer, the scorer and the frozen cases are inlined verbatim, so the hosted runs use the same code as the local runner. `tests/test_kaggle_export.py` executes a generated file against a fake SDK and checks that its aggregate matches the local scorer. A benchmark (a collection of tasks with a leaderboard) is assembled in the Kaggle web UI.
