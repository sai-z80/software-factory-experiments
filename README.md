# Software factory experiments

A shared home for controlled experiments on software delivery and maintenance. Each experiment has its own dated folder; this index links reports without mixing workloads or hiding limitations.

## Experiment index

| Date | Experiment | Main observed outcome | Report and evidence | Drive |
|---|---|---|---|---|
|7 November2026|CSV reconciliation lifecycle: direct vs8090-assisted|Both passed both phases; n=1 correctness tie, no general winner/ROI claim|[Report](experiments/2026-11-07-csv-reconciliation/REPORT.md) · [Aggregate results](experiments/2026-11-07-csv-reconciliation/results.summary.json) · [Public source/tests](experiments/2026-11-07-csv-reconciliation/)|[Google Doc](https://docs.google.com/document/d/1JG-gYKTrIQMduO0rao_-cXfu469Gb1d0FflBYW2FZmw/edit)|

The CSV results are proposed on a review branch, not automatically merged. The assisted workflow is connector-assisted management by the same host model, **not native8090 coding**. Extra artifact work, attended transport latency, one technical safety intervention and pending drafts limit causal efficiency/autonomy claims. Provider-settled spend is not an audited all-platform invoice.

## Repository conventions

- One folder under `experiments/YYYY-MM-DD-short-name/` per experiment.
- Reports state sample size, task/model/tools, cost/time, independent evaluation and limitations.
- Public sources/tests are separated from private evaluator/oracles and from later-phase releases.
- A published experiment folder is not a clean agent workspace. Scope future agents to the correct initial starter only.
- No private answer keys, credentials, raw transcripts, personal data or native project/artifact identifiers.
- New experiments are added through separate pull requests. This publication does not add previous experiments or run new ones.

No new repository licence has been selected or asserted.
