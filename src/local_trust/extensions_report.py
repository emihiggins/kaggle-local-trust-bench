"""Grouped comparison tables for the exploratory extensions (from analyze output JSON)."""

import json
import os

GROUPS = {
    "Thinking on vs. off": [("qwen3.5-4b-4bit", "off"), ("qwen3.5-4b-4bit-thinking", "on"),
                            ("qwen3.6-35b-a3b-4bit", "off"), ("qwen3.6-35b-a3b-4bit-thinking", "on")],
    "Precision ladder (Qwen3.5-4B, MLX)": [("qwen3.5-4b-4bit", "4-bit"), ("qwen3.5-4b-8bit", "8-bit"),
                                           ("qwen3.5-4b-bf16", "bf16")],
    "Runtime (same model, MLX 4-bit vs. Ollama default quantization)": [
        ("qwen3.6-35b-a3b-4bit", "MLX"), ("ollama-qwen3.6-35b-a3b", "Ollama"),
        ("gemma-4-26b-a4b-4bit", "MLX"), ("ollama-gemma4-26b-a4b", "Ollama")],
}


def pct(x):
    return "NA" if x is None else f"{100 * x:.1f}%"


def main(summary_dir="results/summary/extensions", labels=("test-v1", "test-crowded-v1")):
    out = ["# Exploratory extensions",
           "",
           "Chosen after seeing the primary results (post hoc, exploratory). Same frozen cases, prompt and "
           "scorer. Strict success macro-averaged over strata; drop = clean − injected (95% cluster-bootstrap "
           "interval). *Tolerant* = diagnostic that also accepts a correct conflict listing its values. "
           "Latency is the median per case on the Mac; Ollama memory isn't measured by MLX, so it shows NA.",
           ""]
    for label in labels:
        d = json.load(open(os.path.join(summary_dir, f"{label}.json")))["summaries"]
        out += [f"## {label}", ""]
        for group, items in GROUPS.items():
            out += [f"### {group}", "",
                    "| Model | Setting | Clean | Injected | Drop (pp) | Fake-authority notes | Note cited | Tolerant clean / inj | Hit token cap | Median latency | Peak MLX mem |",
                    "|---|---|---|---|---|---|---|---|---|---|---|"]
            for m, setting in items:
                s = d[m]
                lo, hi = s["degradation_ci_pp"]
                mem = f"{s['peak_mem_gb_max']:.1f} GB" if s.get("peak_mem_gb_max") else "NA"
                out.append(f"| {m} | {setting} | {pct(s['clean_success'])} | {pct(s['injected_success'])} "
                           f"| {s['degradation_pp']:.1f} [{lo:.1f}, {hi:.1f}] | {pct(s['inj_claimed_authority'])} "
                           f"| {pct(s['cited_note_rate'])} | {pct(s['clean_tolerant'])} / {pct(s['injected_tolerant'])} "
                           f"| {s['hit_max_tokens']} | {s['latency_median_s']:.2f} s | {mem} |")
            out.append("")
    path = os.path.join(os.path.dirname(summary_dir), "extensions.md")
    with open(path, "w") as f:
        f.write("\n".join(out))
    print(path)


if __name__ == "__main__":
    main()
