# CSV reconciliation lifecycle —7 November2026

One paired feasibility trial: direct agent B versus the same host agent using actual8090 connector-assisted artifact management. **Correctness tie; not a benchmark of native8090 coding or a general ROI/reliability claim.**

- [Full report](REPORT.md) — methods, counts, cost/time/token tables and limitations.
- [Aggregate machine-readable results](results.summary.json).
- [Exact public-source/content hashes](SOURCE_HASHES.json).
- [Google Drive report](https://docs.google.com/document/d/1JG-gYKTrIQMduO0rao_-cXfu469Gb1d0FflBYW2FZmw/edit) — existing permissions unchanged.

Both arms passed Phase1 (3visible+16private) and Phase2 (4visible+32private), with zero regressions.110pass observations are not110 independent cases: original16 private cases recur in Phase2. Provider-settled cost$5.03518838 includes qualification/smokes; incremental8090 CRUD invoice was not independently audited.

The assisted arm's extra artifact work, attended bridge latency, one technical scope-safety intervention and pending native drafts limit causal comparison. Phase2 fix work order followed code/public tests. There is no zero-human/autonomy or work-order-causality claim.

## Layout

- `implementations/p1-b`, `p1-c`, `p2-b`, `p2-c`: exact submitted single-file programs.
- `source_diff_b.patch`, `source_diff_c.patch`: own accepted Phase1→Phase2 changes.
- `public_task/contestant_public`: clean Phase1 starter; no implementation.
- `public_task/release_phase2`: separately released change, trigger, invoice replacement and visible tests.
- `PUBLIC_VALIDATION.json`: publication-source public smoke checks, not another model experiment.

## Release boundary

This is a **post-experiment public record, not an agent workspace**. For a new evolving-requirements run, copy ONLY `public_task/contestant_public` into the initial isolated workspace. Do not expose this report, aggregate results, implementations or `release_phase2` to a Phase1 agent. Release Phase2 only after accepting that agent's own Phase1 code. Never use a reference implementation to replace the arm's own baseline.

Private cases/oracles, references/mutants, raw transcripts, native project/artifact IDs, private paths and personal account data are intentionally not published. Public tests alone cannot reproduce the independent held-out acceptance verdict. No new licence is asserted.

## Public-test reproduction

For a trusted, reviewed source snapshot, assemble a temporary workspace from the Phase1 starter and one implementation, then run `python3 -m pytest -q`. For Phase2, overlay the separate release first. Use offline sandboxing when executing untrusted candidate code; the original verification used scoped bwrap namespaces rather than merely separate folders. No model/API call is necessary to run these public checks.
