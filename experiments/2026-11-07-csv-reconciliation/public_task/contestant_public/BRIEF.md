# Public reconciliation contract — proposed assumptions for review
These rule resolutions are experimental assumptions, not approved business facts.
Implement one self-contained Python file `reconcile.py` using ordinary libraries.
CLI: `python reconcile.py --orders PATH --invoices PATH --output PATH`.
`python` means the experiment's pinned Python interpreter; this box uses the supplied
venv Python (system command is `python3`). No source code is provided to contestants.

Input schemas, in this exact order:
- orders.csv: order_id,order_date,expected_amount
- invoices.csv: invoice_id,order_id,invoice_date,billed_amount

Inputs are valid UTF-8 CSV. IDs are unique nonempty strings; preserve leading zeroes.
At most one invoice per order; multi-invoice settlement is OUT OF SCOPE.
Invoices referencing no order are ignored. Amounts are nonnegative decimal currency
values with exactly two fractional digits; compare exact decimal values, not floats.
Order dates are ISO YYYY-MM-DD. Dates are valid calendar dates. Invoice dates may
precede order dates: this is not a separate exception. No invalid-input handling is
scored, nor permissions, duplicate-ID policy, user interfaces or deployment.

For each order emit one row per violated rule (both amount and lateness may apply):
- missing_invoice: no invoice; normalized_invoice_date and amount_delta both empty.
- amount_mismatch: billed_amount != expected_amount.
- late_billing: (invoice_date - order_date).days > 30; exactly 30 is NOT late.
For every invoiced exception, normalize the date to YYYY-MM-DD and set amount_delta
= billed_amount - expected_amount, exact two decimal places (zero is 0.00).
Matched orders violating no rules produce no rows.
Output is a UTF-8 CSV with EXACT header:
order_id,exception_type,normalized_invoice_date,amount_delta
Sort ascending lexically by (order_id, exception_type); do not numerically coerce IDs.
Header must exist even when output is empty. Standard CSV quoting/newlines accepted.

Phase 1: each input has one header, no preamble, all dates YYYY-MM-DD.
Only Phase 1 requirements are applicable to the initial build.
Public tests are examples, not the full specification. Independent evaluation uses
fresh records satisfying these same rules. Do not modify tests or fixtures.
