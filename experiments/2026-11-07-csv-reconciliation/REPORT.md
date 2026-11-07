# CSV Reconciliation — Direct Agent vs 8090-assisted Workflow

## Executive summary

**Both workflows built and repaired the synthetic reconciliation program correctly on the frozen acceptance suites. No accuracy winner was observed.** This was one paired feasibility trial, completed on7 November2026; it is not a reliability estimate, a business-ROI claim or a benchmark of8090's native coding product.

The direct agent and the connector-assisted agent used the same selected model/provider/settings and basic file/bash/pytest abilities. Each passed16 private cases in Phase1 and32 in Phase2, including the16 original regression cases. Each repaired16 previously failing changed-format cases without regressing an original case.

Total provider-reported cost was **$5.03518838**, including **$1.74636038** for qualification/smokes and **$3.288828** for the paired stages. Outstanding model reserves: **$0**. All100 saved model-response costs reconciled to100 settled ledger entries. Existing subscription costs are excluded and incremental8090 CRUD charges were not independently invoiced; this is not an audited all-platform bill.

The assisted arm incurred more model cost and elapsed time on this small task, but also performed additional documentation/record work and used an attended transport bridge. Bridge delays and one technical safety intervention confound a clean speed/autonomy comparison. These results do not establish that either workflow is generally better.

## 1. Question, treatment and controls

The question was whether the same host coding agent could complete a two-phase CSV lifecycle directly versus with real8090 connector requirements, container-blueprint, work-order and feedback management.

- **B — Direct:** host model with scoped file read/write, offline bash and pytest.
- **C — Assisted:** same host model/basic tools, plus actual sanctioned8090 connector artifact operations and writing rules. This was **connector-assisted management, not a native8090 coding-agent launch**.
- Model: `anthropic/claude-sonnet-4.6`; provider restricted to `anthropic`; temperature0; reasoning effort `none`; maximum completion4096 tokens, no fallback.
- Each phase/arm: $2 model-cost cap,600s agent-wall cap including bridge waits,60 model turns including governance. Total ceiling:$10; qualification plus smokes capped at$2 combined.
- Phase1 had fresh model contexts and isolated workspaces with identical public briefs, fixtures and visible tests. No implementation/reference/private cases or future Phase2 payload was provided.
- Order was frozen before outcomes: C thenB in Phase1; B thenC in Phase2.
- Both Phase1 submissions had to pass before advancing the pair. Phase2 used fresh sessions seeded from each arm's **own accepted** code/public artifacts, not a shared reference. These accepted baselines could differ.
- The generic public change trigger was identical. No private score/error was supplied for repair; no candidate source was copy-edited by the operator; no model generation was replayed or primary attempt restarted.

## 2. Public task and narrow synthetic assumptions

The CLI was `python reconcile.py --orders PATH --invoices PATH --output PATH`.

Orders columns: `order_id,order_date,expected_amount`. Invoice columns: `invoice_id,order_id,invoice_date,billed_amount`.

The output columns were exactly `order_id,exception_type,normalized_invoice_date,amount_delta`, sorted lexically by `(order_id, exception_type)`.

| Rule | Public behavior |
|---|---|
| Missing invoice | One `missing_invoice` row; empty date and delta |
| Unequal amount | One `amount_mismatch` row; Decimal delta = billed−expected, canonical two places |
| Late invoice | One `late_billing` row when calendar-day difference is strictly greater than30; exact30 is not late |
| Multiple violations | One row per violated rule; all invoiced exception rows carry normalized ISO date and the same billed−expected delta |
| Matching, timely invoice | Excluded from exceptions |

IDs were unique opaque strings and leading zeros were preserved; there was at most one invoice per order. Unknown-order invoices were ignored. Multiple invoices/order and invalid-input policies were outside this study. These are frozen synthetic defaults, **not approved real-world business facts**.

### Phase change

Phase1 used clean UTF-8 CSVs with one header and ISO `YYYY-MM-DD` dates. Phase2 replaced only the invoices export: exactly two metadata lines before the header and day-first `DD/MM/YYYY` invoice dates. Metadata text was not semantically meaningful. Both formats had to remain supported; orders stayed ISO. Date parsing was load-bearing for the strict30-day rule and normalized output.

Public briefs/fixtures/tests and all four source versions accompany the prepared source bundle. For a future evolving-requirements trial, use only `public_task/contestant_public` initially, and withhold `release_phase2` until the trigger. This post-experiment report/source bundle must not itself be imported as a fresh contestant workspace.

## 3. Actual acceptance outcomes

| Stage | Visible passes | Private passes | Agent wall(s) | Bridge wait(s) | Trigger→score(s)* | Provider cost |
|---|---:|---:|---:|---:|---:|---:|
| P1-B | 3 | 16/16 | 48.161 | 0.000 | 84.836 | $0.151659 |
| P1-C | 3 | 16/16 | 389.297 | 184.584 | 413.951 | $1.663035 |
| P2-B | 4 | 32/32 | 59.268 | 0.000 | 73.273 | $0.201969 |
| P2-C | 4 | 32/32 | 509.488 | 328.338 | 521.441 | $1.272165 |

*Agent wall is measured by the runner. Trigger→score includes actual post-model scoring delay, derived from measured agent wall and saved result/score file timestamps; it is not separate high-resolution timer instrumentation. Scoring was external to the600s agent-loop cap. Bridge time includes queueing, attended operator service and native RPC, not merely8090 compute.

**110/110 pass observations** =14 visible plus96 private observations across four stages. This is **not110 independent cases**: original16 private cases recur as Phase2 regressions and across both arms. There were zero primary assertion failures, errors, timeouts, infrastructure errors or missing results.

| Repair transition (each arm) | Observed count |
|---|---:|
| Original Phase1 code evaluated retrospectively on32 Phase2 cases |16 pass +16 errors |
| Repaired own code on the same32 cases |32 pass |
| Changed-format error→pass |16 |
| Original pass→pass preserved |16 |
| Original pass→nonpass regressions |0 |

Both original submissions also gave2pass+2fail on the new public suite. Retrospective independent baseline scoring happened after model attempts, with no further model generation or hidden feedback. Baseline parser errors are not assertion failures, and infrastructure/missing results were not relabelled as product failures.

## 4. Cost, tokens and overhead

| Stage | Model calls | Input tokens | Completion tokens | Reasoning tokens | Cached tokens | API wait(s) |
|---|---:|---:|---:|---:|---:|---:|
| P1-B | 8 | 35,628 | 2,985 | 0 | 0 | 47.402 |
| P1-C | 16 | 494,675 | 11,934 | 0 | 0 | 203.775 |
| P2-B | 9 | 49,668 | 3,531 | 0 | 0 | 58.427 |
| P2-C | 18 | 375,840 | 9,643 | 0 | 0 | 179.841 |

Primary totals:955,811 input +28,093 completion tokens. Both selected primary arms had zero reported reasoning/cached tokens. API wait is distinct from bridge wait. Governance-involved turns and their costs are available in the aggregate JSON; mixed turns are included and this classification is not a causal incremental-cost estimate.

| Spending class | Provider-reported USD |
|---|---:|
| Direct B, both primary phases |0.353628 |
| Assisted C, both primary phases |2.935200 |
| Paired primary stages |3.288828 |
| Qualification and all smokes |1.74636038 |
| **Total settled** |**5.03518838** |
| Outstanding/uncertain model reserve |0 |

The qualification bucket includes earlier DeepSeek and Grok attempts, selected-model qualification and direct-tool smoke. Those attempts are not excluded from spend. No additional model call or trial was purchased after completion.

Primary evidence window:20:00:34–20:18:48 GMT (1093.725s). Earliest saved paid request:19:20:31 GMT; through final primary scoring3497.066s, including setup. All times are Europe/London (GMT) on7 November2026.

## 5. Independent verification and concrete repair

Each candidate case ran in a fresh subprocess/workspace with a per-case timeout. Candidate file/shell operations used offline bwrap namespaces, scoped runtime/public-input mounts, cleared environment and traversal/symlink checks. Host private paths, evaluator inputs and network were denied in negative probes. The evaluator/oracles stayed outside model contexts. This is tested namespace isolation, not a universal multi-tenant security guarantee.

Before primary dispatch, the correct reference passed16/16 Phase1 and32/32 Phase2 cases. All13 deliberately broken variants were detected, including explicit hung-case timeouts without missing subsequent results. Readiness/dispatch/binding checks passed31/31 (26+2+3), plus4 offline paid-adapter checks and6 saved-prefix trace checks. The reference replacement lifecycle was explicitly a **MOCK repair**, not model work.

All36 pre-primary frozen files and93 original delivered fingerprints remained unchanged. Private cases covered active calendar dates/leap-year boundaries, exact30 versus late31, decimal deltas, leading-zero IDs, multiple exceptions, deterministic ordering, original-format regressions and anti-hardcoding variation. Inputs/oracles and per-case expected outputs are deliberately not published.

Both real source versions changed. The repair introduced two-layout invoice loading and day-first parsing/normalization, while retaining the original join, Decimal comparison, strict calendar-day threshold and output ordering. Source hashes, exact public diffs and public test payloads are supplied for audit. Aggregate results do not disclose held-out fixtures.

## 6. Qualification and integration findings

Selection was conditional, not an independent model benchmark. Earlier candidate outcomes included adapter/schema, transport and billing-bound confounds; they cannot establish general DeepSeek/Grok planning incapability or selected-model superiority.

The selected model passed functional public-rule/planning, real requirement/blueprint/work-order linkage and actual read/write/pytest checks. Its original strict Markdown-copy-format check failed (wording/IDs were preserved), and its final self-summary was incomplete at a conservative budget guard. The functional admission clarification was saved **before any primary call**, with both deviations retained.

Two primary native argument-validation rejections occurred through the simplified custom schema, and the agent corrected them using normal tool responses. These were integration events, not fair scores of8090's native coding product.

A frozen adapter UUID regex also registered an identifier from an error as though it were a created document and mislabelled a record type. One attempted out-of-scope category-as-document lookup was denied locally before native dispatch. Original raw evidence/registry was preserved, and actual typed creation/readback/work-order receipts independently corroborated management delivery. This was **one technical operator scope-safety intervention**, not a native RPC or business hint. There is no zero-human or pristine autonomous-comparison claim.

Attended native transport calls:10 in C Phase1 and12 in C Phase2, in addition to that local denial. Zero business hints, candidate source edits, primary model restarts or generation replays were recorded.

## 7. What the managed artifacts do—and do not—prove

Real synthetic requirements, container blueprint, linked build/fix work orders and feedback were created through the supported connector. Initial document content and five Phase2 edit suggestions remained pending review, not approved business facts. No full production approval/governance lifecycle is claimed.

Phase1 work order preceded implementation. Phase2 requirements/blueprint suggestions preceded repair, but the Phase2 fix work order was created **after code/public tests**. Therefore these data do not demonstrate that a fix work order causally drove maintenance planning or implementation.

## 8. Interpretation and next methodological step

Both workflows demonstrated the small public task and maintenance change without measured regressions. Acceptance was at the ceiling for both. The assisted workflow's additional model/context consumption and attended bridge time are observed costs, not a general verdict on software factories.

Limits include n=1, conditional selection, a small synthetic task, divergent own accepted baselines, extra management deliverables, imperfect custom transport, pending drafts and incompletely controlled provider/backend state. There is no business-ROI, reliability, fully autonomous workflow or general winner claim.

Before a future causal/replicated trial: repair typed native-success ID extraction and exact field-scope descriptions; reduce/audit bridge latency; revalidate and freeze again. No extra experiment or paid model call was run to improve tonight's result.

## 9. Publication and provenance

The public release includes this report, aggregate JSON, four candidate source versions, public briefs/fixtures/tests and exact source diffs. It excludes private cases/oracles, references/mutants, raw transcripts, native project/artifact identifiers, personal account data, secrets and private absolute paths. Held-out counts/provenance are reported without publishing the answer key. No new licence has been chosen.

The public report is proposed for review in the shared [software-factory-experiments repository](https://github.com/sai-z80/software-factory-experiments), with a dated folder per experiment and a root index. [Read the report on the publication branch](https://github.com/sai-z80/software-factory-experiments/blob/publish-csv-reconciliation-2026-11-07/experiments/2026-11-07-csv-reconciliation/REPORT.md). The results branch is not merged automatically.

[Google Drive report](https://docs.google.com/document/d/1JG-gYKTrIQMduO0rao_-cXfu469Gb1d0FflBYW2FZmw/edit). The Drive report retains its existing restricted permissions; linking it does not widen access. The GitHub report is independently readable without Drive access.

### Official documentation retained at configuration freeze

- [Messages API absolute completion limit](https://platform.claude.com/docs/en/api/messages/create)
- [OpenRouter reasoning-token configuration](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens)
- [Selected model/provider endpoint metadata](https://openrouter.ai/api/v1/models/anthropic/claude-sonnet-4.6/endpoints)
- [8090 usage classification](https://docs.8090.ai/administration/usage)
- [8090 external coding-agent connection](https://docs.8090.ai/connections/connect-coding-agent)

The documented output cap and conservative pre-dispatch input bounds were checked against observed native usage on settlement. Empirical validation is not a universal guarantee about future providers or pricing. Existing subscription excluded; no hosted8090 inference was invoked; incremental CRUD invoices were not independently audited.
