"""Local inference adapters. Each returns the raw output, the final text to score, and timing.

Test models get a single user message and nothing else: no tools, files or network.
"""

import hashlib
import json
import re
import time
import urllib.request

_THINK = re.compile(r"\A\s*<think>(.*?)</think>\s*", re.DOTALL)
_HARMONY_FINAL = "<|channel|>final<|message|>"
_GEMMA_THOUGHT = re.compile(r"\A\s*<\|channel>thought(.*?)<channel\|>\s*", re.DOTALL)


def split_reasoning(raw):
    """Frozen final-answer parser for reasoning formats: (reasoning_text, final_text).

    Qwen-style `<think>...</think>` prefix, Gemma 4 `<|channel>thought...<channel|>` prefix,
    or gpt-oss harmony final channel. Anything else
    is returned unchanged as the final text. Never used to repair JSON.
    """
    if _HARMONY_FINAL in raw:
        reasoning, final = raw.rsplit(_HARMONY_FINAL, 1)
        for end in ("<|return|>", "<|end|>"):
            if final.endswith(end):
                final = final[: -len(end)]
        return reasoning, final
    m = _THINK.match(raw) or _GEMMA_THOUGHT.match(raw)
    if m:
        return m.group(1), raw[m.end():]
    return None, raw


class MLXBackend:
    def __init__(self, spec):
        self.spec = spec
        self.model = self.tokenizer = None

    def load(self):
        import mlx.core as mx
        from mlx_lm import load

        t0 = time.perf_counter()
        self.model, self.tokenizer = load(self.spec["repo"], revision=self.spec.get("revision"))
        mx.synchronize()
        return time.perf_counter() - t0

    def chat_template_hash(self):
        tpl = getattr(self.tokenizer, "chat_template", None) or ""
        return hashlib.sha256(tpl.encode()).hexdigest()[:16]

    def render(self, prompt):
        kwargs = self.spec.get("template_kwargs", {})
        return self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], add_generation_prompt=True, tokenize=False, **kwargs
        )

    def generate(self, prompt):
        import mlx.core as mx
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler

        text = self.render(prompt)
        ids = self.tokenizer.encode(text, add_special_tokens=False)
        mx.clear_cache()
        mx.reset_peak_memory()
        sampler = make_sampler(temp=0.0)
        pieces, first, last = [], None, None
        t0 = time.perf_counter()
        for resp in stream_generate(self.model, self.tokenizer, ids,
                                    max_tokens=self.spec["max_tokens"], sampler=sampler):
            if first is None:
                first = time.perf_counter()
            pieces.append(resp.text)
            last = resp
        t1 = time.perf_counter()
        raw = "".join(pieces)
        reasoning, final = split_reasoning(raw)
        gen_tokens = last.generation_tokens if last else 0
        return {
            "raw_output": raw,
            "final_text": final,
            "reasoning_chars": len(reasoning) if reasoning else 0,
            "rendered_prompt_sha": hashlib.sha256(text.encode()).hexdigest()[:16],
            "prompt_tokens": last.prompt_tokens if last else len(ids),
            "output_tokens": gen_tokens,
            "finish_reason": last.finish_reason if last else None,
            "latency_s": t1 - t0,
            "ttft_s": (first - t0) if first else None,
            "decode_tps": ((gen_tokens - 1) / (t1 - first)) if first and gen_tokens > 1 and t1 > first else None,
            "prefill_tps": last.prompt_tps if last else None,
            "peak_mem_gb": mx.get_peak_memory() / 1e9,
        }

    def unload(self):
        import gc
        import mlx.core as mx

        self.model = self.tokenizer = None
        gc.collect()
        mx.clear_cache()


class OllamaBackend:
    """Runtime-comparison track only. Uses the local Ollama server on localhost."""

    def __init__(self, spec):
        self.spec = spec
        self.url = spec.get("url", "http://127.0.0.1:11434")

    def _post(self, path, body, timeout=900):
        req = urllib.request.Request(self.url + path, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())

    def load(self):
        t0 = time.perf_counter()
        self._post("/api/generate", {"model": self.spec["tag"], "prompt": "", "keep_alive": "30m"})
        return time.perf_counter() - t0

    def chat_template_hash(self):
        info = self._post("/api/show", {"model": self.spec["tag"]})
        return hashlib.sha256(info.get("template", "").encode()).hexdigest()[:16]

    def generate(self, prompt):
        body = {
            "model": self.spec["tag"],
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": self.spec.get("think", False),
            "keep_alive": "30m",
            "options": {"temperature": 0, "seed": 0, "num_predict": self.spec["max_tokens"],
                        "num_ctx": self.spec.get("num_ctx", 8192)},
        }
        t0 = time.perf_counter()
        r = self._post("/api/chat", body)
        t1 = time.perf_counter()
        content = r["message"].get("content", "")
        thinking = r["message"].get("thinking") or ""
        reasoning, final = split_reasoning(content)
        ev, evd = r.get("eval_count", 0), r.get("eval_duration", 0)
        pe, ped = r.get("prompt_eval_count", 0), r.get("prompt_eval_duration", 0)
        return {
            "raw_output": (f"<think>{thinking}</think>" if thinking else "") + content,
            "final_text": final,
            "reasoning_chars": len(thinking) + (len(reasoning) if reasoning else 0),
            "rendered_prompt_sha": None,
            "prompt_tokens": pe,
            "output_tokens": ev,
            "finish_reason": r.get("done_reason"),
            "latency_s": t1 - t0,
            "ttft_s": ped / 1e9 if ped else None,  # server-reported prefill time, not client TTFT
            "decode_tps": ev / (evd / 1e9) if evd else None,
            "prefill_tps": pe / (ped / 1e9) if ped else None,
            "peak_mem_gb": None,
        }

    def unload(self):
        self._post("/api/generate", {"model": self.spec["tag"], "prompt": "", "keep_alive": 0})


def make_backend(spec):
    return {"mlx": MLXBackend, "ollama": OllamaBackend}[spec["backend"]](spec)
