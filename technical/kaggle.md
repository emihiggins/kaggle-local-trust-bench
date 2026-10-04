# Kaggle integration — qualifying path

## Verified SDK patterns

The [official quick start](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/quick_start.md) documents `@kbench.task`, `llm.prompt`, assertion-based pass/fail, `.run()`, `.evaluate()` over data, and `%choose` for the selected notebook task. The [README](https://github.com/Kaggle/kaggle-benchmarks) describes task/run files consumed by benchmark entities and leaderboards. These are research-backed patterns, not executed integration tests in this repository.

## Day-one gate

In Emi's Kaggle account:

1. Open `https://www.kaggle.com/benchmarks/tasks/new`; confirm the SDK-provisioned notebook is available.
2. Record SDK version, actual model registry (e.g. `list(kbench.llms.keys())` if exposed in that version), quotas/reset timing, notebook runtime and Internet restrictions. Keep account secrets private.
3. Run a single tiny task against one free model; inspect produced task/run artifacts and how to save a notebook version.
4. Establish how current UI groups tasks into a Benchmark and makes it public. Prepare a draft where supported. Public publishing awaits Emi's authorization.
5. Record whether local response import is officially supported. If undocumented or rejected, **do not attempt to fabricate hosted runs or leaderboard rows**.

Timebox access/integration exploration to 2 hours. Continue local data/scorer work if blocked; report exact account/UI blocker. The project can produce useful local results without Kaggle, but cannot claim contest eligibility until this path works.

## Shared implementation, separate execution

Define a task that renders one case, calls the provided `llm`, scores its returned text, and asserts strict success. The following is an **illustrative SDK scaffold**, not a tested notebook:

```python
import kaggle_benchmarks as kbench
from local_trust.prompt import render
from local_trust.scoring import score

@kbench.task(name="local_trust_case")
def local_trust_case(llm, case):
    raw = llm.prompt(render(case))
    result = score(case, raw)
    kbench.assertions.assert_true(
        result.strict_success,
        expectation="Exact evidence-grounded JSON answer or correct abstention",
    )
```

Adapt to the installed SDK's serialization/argument limits. Case fields containing gold are scorer inputs only; only `render(case)` goes into the model prompt. Do not pass `schema=` in primary track: enforced output structure would differ from the local unenforced JSON test.

Use the documented dataset evaluation patterns for the corpus, but first inspect assertion failure semantics: a model being wrong is an expected graded failure, not a reason to abort the whole study. Do not blindly copy `max_attempts > 1` in a way that retries semantic failures. Task wrappers should preserve per-case scores/outputs and correct infrastructure failure accounting. A pilot with deliberately wrong output must still yield an interpretable aggregate.

Prefer eight named task slices (four strata × clean/injected) with each task evaluating its frozen slice and returning a documented scalar aggregate if supported. Verify leaderboard scalar aggregation in the installed version. Otherwise use one documented aggregate task with per-case artifacts and publish slice tables as supporting outputs. Select the intended top-level task with `%choose` when needed; never assume a tuple/dict is ranked the way you intend. Assert the displayed leaderboard score agrees with offline aggregation on a small known fixture before full runs.

Shared renderer/scorer/corpus must be vendored or packaged into the notebook so execution does not require private GitHub authentication. Pin the scorer and corpus hashes. Replaying identical saved text through local and hosted scoring must yield identical results; live generation across backends need not match.

## Comparison and publication

Run at least two actually available free hosted models using identical frozen cases. If controls differ, record effective settings and label comparisons as deployment configurations. Never claim Kaggle executed MLX on Emi's hardware. Mac results are an independently reproducible companion study and can be linked/attached as public result artifacts; do not insert them into Kaggle-native leaderboards unless officially supported and correctly labeled.

Quota ledger: initial allowance, pilot use, primary projected calls/tokens, retry allowance and remaining balance. Set hosted concurrency 1 initially, bounded retries and explicit run timeout. Disable response-cache reuse for independent stability repeats; cached resumptions may avoid repeat billing but are not fresh samples. Stop on free quota exhaustion; no paid fallback.

With publication authorization: create/save benchmark, execute selected models, publish all required dependencies, verify the exact benchmark URL signed out, and capture dated evidence. A notebook URL alone or CSV upload is not sufficient. Recheck challenge rules and current UI rather than guessing platform API routes.
