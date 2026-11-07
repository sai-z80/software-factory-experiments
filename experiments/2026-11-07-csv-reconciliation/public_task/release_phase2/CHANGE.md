# Phase 2 public change contract
Apply only after Phase 1 has been independently evaluated and its artifact frozen.
Business rules and CLI in BRIEF.md remain unchanged.
The updated invoice export has exactly two metadata lines before the same invoice
header, and its invoice_date values use DD/MM/YYYY (day first, unambiguously).
The literal fixture metadata lines are:
Billing tool export v2
Generated for reconciliation study
They are metadata, not records. Other exports can have different metadata text.
Support both the original no-preamble ISO invoice format AND this new two-preamble
DD/MM/YYYY invoice format. Orders remain unchanged, ISO with one header.
Only those two invoice formats are scored; no mixed-row formats or arbitrary damaged
CSVs. Do not rely on literal metadata content or sample IDs/amounts.
Run the supplied Phase 2 public tests plus unchanged Phase 1 regression fixtures.
