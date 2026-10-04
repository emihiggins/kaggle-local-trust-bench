# Delivery plan and acceptance gates

## Schedule (UTC, planning targets)

Dates are a suggested workback, not an automated schedule. Official deadline is owned by [challenge requirements](../research/challenge.md).

| Phase | Target | Depends on | Reviewable outcome |
|---|---|---|---|
| P0 Access/hardware | Oct 4–5 | Mac + authenticated Kaggle | Redacted inventory, quota/registry, 1 hosted task run, model shortlist |
| P1 Vertical slice | Oct 5 | P0 for live smoke; scorer work independent | Tested renderer/scorer, 6 local+hosted fixtures, parity evidence |
| P2 Corpus/protocol freeze | Oct 6 | P1 | Reviewed dev/holdout corpus, selected model revisions, immutable protocol/hash manifest |
| P3 Primary inference | Oct 7–8 | P2 | Local + hosted completed runs, ledger, declared failure counts |
| P4 Analysis/draft | Oct 9 | P3 | Auditable tables, plots, uncertainty, examples, English article draft |
| P5 Publication/review | Oct 10 | P4 + Emi approval | Public Kaggle benchmark checked signed out; DEV post published and checked |
| Buffer | Oct 11 | Any repairs | Broken link/run fixes and final submission verification before deadline |

If starting late, use reduced scope and skip extensions before sacrificing integration, scoring tests or article quality. Stop new optional experiments by Oct 9. Target final review by Oct 10, 18:00 UTC.

## Dependency lanes

- **Corpus/scoring lane:** schema → examples/tests → generator/review → freeze. Can advance while account access is unresolved.
- **Mac lane:** inventory → environment/model smoke → adapter instrumentation. Joins frozen corpus for runs.
- **Kaggle lane:** account/quota discovery → tiny task → packaging/parity → hosted primary results. Joins corpus and scorer at freeze.
- **Evidence lane:** aggregation tests → tables/charts → example audits → article → authorized publication.

These are sequencing opportunities for one executing agent, not a requirement to spawn agents or run model benchmarks concurrently. Inference on the Mac is serial. Each phase should yield one coherent tested commit rather than many micro-PRs.

## Acceptance criteria

Planning artifacts are present now; execution criteria remain unchecked until evidence exists.

- [ ] **A1 / R5:** Actual arm64 chip, memory, CPU/GPU, OS and disk manifest recorded without serial/UUID; MLX Metal smoke succeeds; observed inventory discrepancy, if any, resolved in labels.
- [ ] **A2 / R2,R7:** Real Kaggle task executes, outputs inspectable result artifacts; two available free models and quota recorded; public benchmark workflow established, not guessed.
- [ ] **A3 / R1,R4:** Dataset has exactly chosen full/reduced count, balanced four strata, both variants per base, no leakage; all cases schema/oracle checked; review evidence and hashes committed before final inference.
- [ ] **A4 / R2,R6:** At least 20 identical raw-response fixtures yield identical local/notebook score objects; malformed/wrong answers fail; timeout/resume/error tests pass; scorer inputs never leak through renderer.
- [ ] **A5 / R3,R5,R6:** At least two local models (target three) finish the frozen primary set or disclose unresolved failures; artifacts/revisions/configs pinned; latency/memory units and sample count valid; every result traced to raw output hash.
- [ ] **A6 / R2,R3,R7:** At least two hosted models execute the shared set/subset; visible benchmark aggregate agrees with local recomputation; effective generation differences and coverage disclosed.
- [ ] **A7 / R4,R6:** Reports include clean/injected score counts and intervals, paired deltas, abstention/schema/evidence/attack-target slices, denominators and errors; three qualitative examples independently checked against source evidence.
- [ ] **A8 / optional:** Any quantization/context/backend claims include matched design, pinned configurations and their own comparison tables; omitted extensions marked omitted, not failed or completed.
- [ ] **A9 / R7,R8:** Emi has reviewed eligibility and authorized publication; public benchmark/tasks open signed out; English DEV post matches required structure/tag, links actual benchmark, attributes prior work and includes only actual findings; final URLs/timestamp saved.

## Results manifest expected at handoff

Create `artifacts/study-manifest.json` during execution: project Git SHA, protocol/data/scorer/prompt hashes, actual hardware, environment lock/hash, selected model manifests, planned/completed/error counts, raw-output bundle hash, analysis outputs, Kaggle task/benchmark URLs and notebook versions, DEV draft/public URL, omitted experiments and unresolved limitations. Use null plus an explanation for not-yet-published URLs; never fabricated placeholders that resemble valid results.

## Validation and recovery

Before publishing: run scorer/runner/analysis tests; reconcile run counts; recompute tables from immutable responses; inspect staged changes and secret scan; clear sensitive notebook output; validate links. Preserve originals if a result is corrected, bump version, add amendment and rerun affected comparisons. Never silently edit the frozen gold labels.

Before/after Git pushes: inspect branch, diff, remote and clean state; no weights in Git. Publish results only from reviewed artifacts. If external publication fails, preserve draft and exact error, retry boundedly, and inform Emi; local completion is not publication success.
