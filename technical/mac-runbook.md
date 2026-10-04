# Mac execution and experiment matrix

## 1. Verify the host

The user reports M5 Max / Mac Studio / 18 CPU cores / 40 GPU cores / 16 Neural Engine cores / 48 GB unified RAM / 512 GB disk. Treat that as provided context, not measured fact. On the Mac run read-only inventory:

```sh
uname -m
sw_vers
sysctl -n machdep.cpu.brand_string
sysctl -n hw.memsize
sysctl -n hw.physicalcpu
sysctl -n hw.logicalcpu
sysctl hw.perflevel0.physicalcpu hw.perflevel1.physicalcpu
df -h .
sysctl vm.swapusage
vm_stat
```

Use `system_profiler SPDisplaysDataType` locally to check GPU. Some sysctl keys can be absent; log unavailable rather than fail. If using SPHardwareDataType, redact serial number and hardware UUID before storing/sharing. Verify chip/model designation in About This Mac and correct article wording if it differs. Do not publish inferred memory bandwidth, TOPS or ANE activity.

Run native arm64 Python (not Rosetta). Check MLX release support for installed macOS/chip, then perform a tiny Metal inference. Baseline uses GPU/CPU through MLX; it does **not** target the Neural Engine. Full 18-core CPU utilization is not a goal; leave resources for OS/tokenization.

## 2. Resource policy — conservative planning limits

- One loaded model, one inference request at a time. No concurrent model benchmarks.
- Prefer combined model/KV/working memory under **32 GiB** on the reported 48 GB host, leaving OS/application headroom. This is a planning ceiling, not a claim about Apple's exact allocatable GPU limit.
- Start at ≤4,096 input tokens plus ≤512 generated tokens. Check the actual backend allocation limit; reduce model/context on failure. No rotating/truncated KV cache in the main study because it changes task semantics.
- Pause if memory pressure is yellow/red or swap grows by >1 GiB above the pre-run baseline across a block. Archive affected rows as resource-confounded, cool down/close ordinary apps, rerun entire affected timing block after recovery. Quality output is retained and labeled.
- Check **actual free space**, not nominal 512 GB capacity. Reserve ≥60 GiB free after downloads and aim for ≤80 GiB total project/model cache. If initially constrained, select only two small models and a ≤30 GiB cache. Never delete unrelated user files.
- Set one project-owned Hugging Face cache location; avoid duplicate GGUF and MLX copies unless running the backend appendix. No 70B model or full-precision 30B experiment.
- No sudo, wired-memory changes, paid APIs or automatic license acceptance. If a model needs remote executable code, choose a supported alternative first.

## 3. Model order and matrix

Candidate MLX artifact IDs/revisions and base IDs are verified in [research](../research/options-and-sources.md); use that pinned shortlist, then verify downloaded hashes and Mac compatibility. Estimates below are rough **4-bit weight storage** including a modest allowance, not runtime peak measurements.

| Order | Base model | Role | Rough weight size | Scope |
|---|---|---|---|---|
| 1 | Qwen/Qwen3-4B | Fast family baseline | 2.5–4 GiB | Required candidate |
| 2 | Qwen/Qwen3-8B | Same-family scale comparison | 4.5–7 GiB | Required candidate |
| 3 | microsoft/Phi-4-mini-instruct | Independent family contrast | 2.5–4 GiB | Target, smoke-gated |
| 4 | Qwen/Qwen3-30B-A3B | Sparse larger-model frontier | 16–22 GiB | Stretch only, measured memory gate |

For every chosen artifact record HF repo and commit, base revision/provenance, quantization bits/group size/method, actual files and SHA-256, license, tokenizer/chat-template hash, backend version and generation config. "4-bit" is not a complete format description. Avoid downloading original full-precision weights solely to create a quantization when a trustworthy compatible artifact exists.

Primary local generation: native templates, Qwen `enable_thinking=False`, temperature 0 (greedy), max output 512, stop on model EOS, batch 1, fresh KV state per case, no prefix cache. This is a deliberate reproducibility setting, not the Qwen card's recommended sampling recipe. Document it. Validate hard non-thinking switch in rendered prompt; `/no_think` alone is not equivalent. If another model cannot use the protocol, replace it before freeze or label a separate track.

Hosted models: choose two available free instruction models from distinct families in the current Kaggle registry; add a third only if quota permits. Prefer one economical model and one stronger model. Do not hardcode historical model IDs from documentation as currently available. Record unsupported sampling controls; never claim exact configuration parity where the provider hides it.

### Required vs extension runs

| Experiment | Cases / configuration | Purpose |
|---|---|---|
| Smoke | 6 example fixtures × 1 local + 1 hosted | Prove end-to-end plumbing |
| Primary quality | 240 cases × 3 target local models + 2 hosted | 1,200 requests total; 480 hosted |
| Minimum quality | 120 cases × 2 local + 2 hosted | 480 requests total; 240 hosted |
| Stability | 48 cases × 3 fresh repeats per selected model | Separate variability study, quota-gated |
| Timing | Fixed 24-case balanced slice × 5 repetitions per local model | Warm latency distribution, separate from main accuracy |
| Quantization | Qwen3-8B 4-bit vs 8-bit, same base revision/backend, all frozen cases | Paired quality/resource effect |
| Context | Fixed 24 base pairs at approx. 1k/4k/8k input budgets | Distractor robustness; separate dataset version |
| Backend appendix | Same base model in MLX and GGUF; 512/2048 prompt and 128 decode; 5 repeats | Systems comparison with conversion/quantization caveat |

Run the primary and delivery gates before extensions. If 8-bit has different base provenance, do not call it an isolated quantization experiment. Select context cases once, use identical text for all models, report actual per-tokenizer lengths; ensure the longest rendering plus output fits all tested windows. Add irrelevant content only, preserve authoritative evidence and freeze placements. Do not silently truncate inputs.

## 4. Timing, memory and operating conditions

Close background heavy apps; record power mode, power source, macOS, ambient/thermal observations if available, and start/end timestamps. No claim of controlled laboratory temperature. Use one unscored warm-up after each load; record model load time separately. Rotate model block order deterministically across repeated timing sessions to reduce order/thermal bias.

Use monotonic wall clocks around generation; synchronize MLX computation for meaningful timing (consult installed API). Definitions:

- Warm end-to-end latency: rendered request tokenization/start through complete generated response, excluding model load.
- TTFT: same start until first generated token is available; streaming chunk delivery is not necessarily an exact token timestamp. Label client-observed first-chunk latency if that's all the adapter exposes.
- Decode throughput: generated tokens after first token divided by time from first to last token; NA for ≤1 token. Include reasoning tokens if measuring an optional reasoning track, and disclose counts.
- Record prompt/decode token counts from actual tokenizer/backend, not character estimates. Compare end-to-end latency primarily across different tokenizers.
- Peak MLX allocated memory using available MLX allocator metrics, plus peak process RSS and swap delta. They describe different things; don't add overlapping counters or call RSS total unified GPU memory.
- Report median and p95 timing over the 120 observations per local model in the fixed slice, with workload/sample size; do not promise an SLA. Preserve per-case values and length distributions.

Energy is optional only with a working, documented meter/sampler; do not infer joules from TDP, CPU percentage or estimated TOPS. A backend appendix's llama-bench tokens/sec excludes tokenization and sampling; keep it separate from application latency.

## 5. Time forecast and resumability

After pilot, estimate `cases × repeats × observed median_seconds / 3600`, plus model loads, downloads, 50% slack and analysis. Example planning arithmetic: 720 local primary requests at 10 s each is 2 hours; at 60 s each, 12 hours. These are scenarios, **not predictions or measurements**. Recalculate from real pilot results before leaving a long run.

Default per-case hard timeout 180 s; model load timeout 600 s; primary per-model wall budget 8 h. Enforce in a worker process that can be terminated without corrupting the ledger. Persist after every case. Retry transport errors at most twice with bounded backoff; never retry wrong answers or silently expand max tokens. Record all attempts. Manual reruns get a new run ID. No LLM polling cron jobs.
