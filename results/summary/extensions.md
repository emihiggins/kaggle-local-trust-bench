# Exploratory extensions

Chosen after seeing the primary results (post hoc, exploratory). Same frozen cases, prompt and scorer. Strict success macro-averaged over strata; drop = clean − injected (95% cluster-bootstrap interval). *Tolerant* = diagnostic that also accepts a correct conflict listing its values. Latency is the median per case on the Mac; Ollama memory isn't measured by MLX, so it shows NA.

## test-v1

### Thinking on vs. off

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-4bit | off | 98.3% | 71.7% | 26.7 [19.2, 35.0] | 20.0% | 26.7% | 98.3% / 71.7% | 0 | 0.22 s | 3.3 GB |
| qwen3.5-4b-4bit-thinking | on | 95.0% | 90.0% | 5.0 [-1.7, 11.7] | 82.5% | 0.0% | 95.0% / 90.0% | 17 | 2.54 s | 3.3 GB |
| qwen3.6-35b-a3b-4bit | off | 96.7% | 90.8% | 5.8 [0.8, 10.8] | 80.0% | 5.0% | 96.7% / 90.8% | 0 | 0.26 s | 20.2 GB |
| qwen3.6-35b-a3b-4bit-thinking | on | 97.5% | 98.3% | -0.8 [-3.3, 1.7] | 100.0% | 0.0% | 97.5% / 98.3% | 0 | 4.55 s | 20.2 GB |

### Precision ladder (Qwen3.5-4B, MLX)

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-4bit | 4-bit | 98.3% | 71.7% | 26.7 [19.2, 35.0] | 20.0% | 26.7% | 98.3% / 71.7% | 0 | 0.22 s | 3.3 GB |
| qwen3.5-4b-8bit | 8-bit | 99.2% | 72.5% | 26.7 [19.2, 35.0] | 22.5% | 25.0% | 99.2% / 72.5% | 0 | 0.30 s | 5.3 GB |
| qwen3.5-4b-bf16 | bf16 | 99.2% | 73.3% | 25.8 [18.3, 34.2] | 22.5% | 25.0% | 99.2% / 73.3% | 0 | 0.46 s | 9.0 GB |

### Runtime (same model, MLX 4-bit vs. Ollama default quantization)

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.6-35b-a3b-4bit | MLX | 96.7% | 90.8% | 5.8 [0.8, 10.8] | 80.0% | 5.0% | 96.7% / 90.8% | 0 | 0.26 s | 20.2 GB |
| ollama-qwen3.6-35b-a3b | Ollama | 98.3% | 91.7% | 6.7 [2.5, 11.7] | 80.0% | 0.8% | 98.3% / 91.7% | 0 | 0.53 s | NA |
| gemma-4-26b-a4b-4bit | MLX | 99.2% | 97.5% | 1.7 [-1.7, 5.0] | 92.5% | 1.7% | 100.0% / 97.5% | 0 | 0.26 s | 14.7 GB |
| ollama-gemma4-26b-a4b | Ollama | 94.2% | 90.8% | 3.3 [-1.7, 8.3] | 90.0% | 0.8% | 99.2% / 96.7% | 0 | 0.35 s | NA |

## test-crowded-v1

### Thinking on vs. off

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-4bit | off | 93.3% | 66.7% | 26.7 [17.5, 35.8] | 17.5% | 29.2% | 93.3% / 66.7% | 0 | 0.33 s | 3.9 GB |
| qwen3.5-4b-4bit-thinking | on | 99.2% | 99.2% | 0.0 [-2.5, 2.5] | 97.5% | 0.0% | 99.2% / 99.2% | 2 | 3.56 s | 3.9 GB |
| qwen3.6-35b-a3b-4bit | off | 86.7% | 83.3% | 3.3 [-3.3, 10.0] | 65.0% | 5.8% | 86.7% / 83.3% | 0 | 0.38 s | 20.9 GB |
| qwen3.6-35b-a3b-4bit-thinking | on | 99.2% | 99.2% | 0.0 [-2.5, 2.5] | 100.0% | 0.0% | 99.2% / 99.2% | 0 | 5.41 s | 20.9 GB |

### Precision ladder (Qwen3.5-4B, MLX)

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-4bit | 4-bit | 93.3% | 66.7% | 26.7 [17.5, 35.8] | 17.5% | 29.2% | 93.3% / 66.7% | 0 | 0.33 s | 3.9 GB |
| qwen3.5-4b-8bit | 8-bit | 95.8% | 68.3% | 27.5 [19.2, 35.8] | 12.5% | 30.8% | 95.8% / 68.3% | 0 | 0.43 s | 5.9 GB |
| qwen3.5-4b-bf16 | bf16 | 95.8% | 68.3% | 27.5 [19.2, 35.8] | 15.0% | 30.0% | 95.8% / 68.3% | 0 | 0.57 s | 9.7 GB |

### Runtime (same model, MLX 4-bit vs. Ollama default quantization)

| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.6-35b-a3b-4bit | MLX | 86.7% | 83.3% | 3.3 [-3.3, 10.0] | 65.0% | 5.8% | 86.7% / 83.3% | 0 | 0.38 s | 20.9 GB |
| ollama-qwen3.6-35b-a3b | Ollama | 97.5% | 85.8% | 11.7 [5.0, 18.3] | 60.0% | 8.3% | 97.5% / 85.8% | 0 | 0.69 s | NA |
| gemma-4-26b-a4b-4bit | MLX | 97.5% | 96.7% | 0.8 [-2.5, 5.0] | 95.0% | 0.0% | 98.3% / 97.5% | 0 | 0.39 s | 15.2 GB |
| ollama-gemma4-26b-a4b | Ollama | 79.2% | 82.5% | -3.3 [-8.3, 1.7] | 82.5% | 0.0% | 99.2% / 96.7% | 0 | 0.55 s | NA |
