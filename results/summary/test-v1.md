## test-v1

Cases: `data/test-v1.jsonl` (sha256 `24967d892bc2f5f0`)

| Model | Done | Clean strict | Injected strict | Drop (pp) | Attack value adopted | Cited note | Clean→injected flips | JSON valid (inj) | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-4-26b-a4b-4bit | 240/240 | 99.2% [98%–100%] | 97.5% [94%–100%] | 1.7 [-1.7, 5.0] | 0.0% | 1.7% | 2.5% | 100.0% | 0.26 s | 14.7 GB |
| gemma-4-e4b-4bit | 240/240 | 96.7% [93%–99%] | 93.3% [88%–98%] | 3.3 [-1.7, 8.3] | 1.7% | 4.2% | 6.0% | 99.2% | 0.22 s | 4.9 GB |
| gpt-oss-20b-mxfp4 | 240/240 | 99.2% [98%–100%] | 100.0% [100%–100%] | -0.8 [-2.5, 0.0] | 0.0% | 0.0% | 0.0% | 100.0% | 0.54 s | 12.6 GB |
| qwen3.5-4b-4bit | 240/240 | 98.3% [96%–100%] | 71.7% [63%–79%] | 26.7 [19.2, 35.0] | 5.8% | 26.7% | 27.1% | 100.0% | 0.22 s | 3.3 GB |
| qwen3.6-35b-a3b-4bit | 240/240 | 96.7% [93%–99%] | 90.8% [86%–96%] | 5.8 [0.8, 10.8] | 0.0% | 5.0% | 7.8% | 100.0% | 0.26 s | 20.2 GB |
| qwen3.8-27b-4bit | 240/240 | 100.0% [100%–100%] | 98.3% [96%–100%] | 1.7 [0.0, 4.2] | 0.0% | 0.0% | 1.7% | 100.0% | 1.11 s | 16.4 GB |

Strict success is macro-averaged over the four strata; brackets are 95% stratum-preserving cluster-bootstrap intervals over base scenarios (10,000 resamples, seed 20261004).

| Model | Variant | direct | selection | missing | conflict | lenient (fence-stripped) | false answer | false abstain |
|---|---|---|---|---|---|---|---|---|
| gemma-4-26b-a4b-4bit | clean | 100% | 100% | 100% | 97% | 99.2% | 0.0% | 0.0% |
| gemma-4-26b-a4b-4bit | injected | 93% | 97% | 100% | 100% | 97.5% | 0.0% | 5.0% |
| gemma-4-e4b-4bit | clean | 100% | 97% | 100% | 90% | 96.7% | 1.7% | 1.7% |
| gemma-4-e4b-4bit | injected | 97% | 87% | 93% | 97% | 93.3% | 5.0% | 5.0% |
| gpt-oss-20b-mxfp4 | clean | 100% | 100% | 97% | 100% | 99.2% | 1.7% | 0.0% |
| gpt-oss-20b-mxfp4 | injected | 100% | 100% | 100% | 100% | 100.0% | 0.0% | 0.0% |
| qwen3.5-4b-4bit | clean | 100% | 100% | 97% | 97% | 98.3% | 3.3% | 0.0% |
| qwen3.5-4b-4bit | injected | 70% | 77% | 70% | 70% | 71.7% | 10.0% | 23.3% |
| qwen3.6-35b-a3b-4bit | clean | 100% | 93% | 93% | 100% | 96.7% | 0.0% | 3.3% |
| qwen3.6-35b-a3b-4bit | injected | 83% | 83% | 97% | 100% | 90.8% | 0.0% | 16.7% |
| qwen3.8-27b-4bit | clean | 100% | 100% | 100% | 100% | 100.0% | 0.0% | 0.0% |
| qwen3.8-27b-4bit | injected | 93% | 100% | 100% | 100% | 98.3% | 0.0% | 3.3% |
