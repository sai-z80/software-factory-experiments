"""
reconcile.py — CSV Order-Invoice Reconciliation Pipeline (Phase 1 + Phase 2)

CLI: python reconcile.py --orders PATH --invoices PATH --output PATH

Implements REQ-REC-001 through REQ-REC-006:
  - REQ-REC-001: CLI invocation and output file production
  - REQ-REC-002: Missing invoice detection
  - REQ-REC-003: Amount mismatch detection (exact decimal arithmetic)
  - REQ-REC-004: Late billing detection (strictly > 30 days)
  - REQ-REC-005: Lexical sort by (order_id, exception_type); multi-exception orders
  - REQ-REC-006: Dual invoice format support (Phase 1 ISO / Phase 2 DD/MM/YYYY + 2-line preamble)
"""

import argparse
import csv
from datetime import date, datetime
from decimal import Decimal
from io import StringIO


HEADER = ['order_id', 'exception_type', 'normalized_invoice_date', 'amount_delta']

# The canonical invoice CSV header row (used for preamble detection)
_INVOICE_HEADER = 'invoice_id,order_id,invoice_date,billed_amount'


def load_orders(path: str) -> dict:
    """Load orders CSV; return dict keyed by order_id.
    Schema: order_id, order_date, expected_amount  (AC-REC-001.1, REQ-REC-002)
    Orders always use Phase 1 format: one header row, ISO YYYY-MM-DD dates.
    """
    orders = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            orders[row['order_id']] = {
                'order_date': date.fromisoformat(row['order_date']),
                'expected_amount': Decimal(row['expected_amount']),
            }
    return orders


def _detect_invoice_format(lines: list) -> tuple:
    """Detect whether the invoice file is Phase 1 (no preamble) or Phase 2 (2-line preamble).

    Detection is based solely on line position of the header row (AC-REC-006.4):
    - Phase 1: lines[0] starts with 'invoice_id,' — header is first line, ISO dates.
    - Phase 2: lines[2] starts with 'invoice_id,' — two preamble lines precede header,
               dates are DD/MM/YYYY.

    Returns (preamble_count, date_format_string).
    """
    # Normalise: strip trailing whitespace/newlines for comparison
    def header_line(line):
        return line.strip().lower().startswith('invoice_id,')

    if lines and header_line(lines[0]):
        # Phase 1: no preamble, ISO dates
        return 0, '%Y-%m-%d'
    elif len(lines) >= 3 and header_line(lines[2]):
        # Phase 2: exactly two preamble lines, DD/MM/YYYY dates
        return 2, '%d/%m/%Y'
    else:
        # Fallback: treat as Phase 1 (spec says only two formats are scored)
        return 0, '%Y-%m-%d'


def load_invoices(path: str) -> dict:
    """Load invoices CSV; return dict keyed by order_id (at most one per order).

    Supports two formats (REQ-REC-006):
    - Phase 1: one header row, no preamble, invoice_date as ISO YYYY-MM-DD.
    - Phase 2: two free-text metadata lines before the header row,
               invoice_date as DD/MM/YYYY.

    Format is detected by the position of the header row (AC-REC-006.4).
    """
    with open(path, newline='', encoding='utf-8') as f:
        raw = f.read()

    lines = raw.splitlines(keepends=True)
    preamble_count, date_fmt = _detect_invoice_format(lines)

    # Reconstruct the CSV content starting from the header line
    csv_content = ''.join(lines[preamble_count:])

    invoices = {}
    for row in csv.DictReader(StringIO(csv_content)):
        oid = row['order_id']
        raw_date = row['invoice_date'].strip()
        # Parse date according to detected format, then store as date object
        inv_date = datetime.strptime(raw_date, date_fmt).date()
        # At most one invoice per order; last one wins (spec says at most one anyway)
        invoices[oid] = {
            'invoice_date': inv_date,
            'billed_amount': Decimal(row['billed_amount']),
        }
    return invoices


def reconcile(orders: dict, invoices: dict) -> list:
    """Apply exception rules and return sorted list of exception rows.

    Rules (per BRIEF and requirements):
      - missing_invoice : order has no invoice (REQ-REC-002)
      - amount_mismatch : billed_amount != expected_amount, exact decimal (REQ-REC-003)
      - late_billing    : (invoice_date - order_date).days > 30 (REQ-REC-004)

    Output sorted ascending lexically by (order_id, exception_type) (REQ-REC-005).
    """
    rows = []

    for order_id, order in orders.items():
        invoice = invoices.get(order_id)

        if invoice is None:
            # REQ-REC-002: missing invoice — both date and delta are empty (AC-REC-002.2/3)
            rows.append({
                'order_id': order_id,
                'exception_type': 'missing_invoice',
                'normalized_invoice_date': '',
                'amount_delta': '',
            })
        else:
            inv_date = invoice['invoice_date']
            billed = invoice['billed_amount']
            expected = order['expected_amount']
            norm_date = inv_date.isoformat()  # YYYY-MM-DD (AC-REC-003.3, AC-REC-004.4, AC-REC-006.3)
            delta = billed - expected          # exact Decimal arithmetic (AC-REC-003.2)
            delta_str = f'{delta:.2f}'         # two fractional digits (AC-REC-003.4, AC-REC-004.5)

            # REQ-REC-003: amount mismatch
            if billed != expected:
                rows.append({
                    'order_id': order_id,
                    'exception_type': 'amount_mismatch',
                    'normalized_invoice_date': norm_date,
                    'amount_delta': delta_str,
                })

            # REQ-REC-004: late billing — strictly > 30 days (AC-REC-004.1/2)
            day_diff = (inv_date - order['order_date']).days
            if day_diff > 30:
                rows.append({
                    'order_id': order_id,
                    'exception_type': 'late_billing',
                    'normalized_invoice_date': norm_date,
                    'amount_delta': delta_str,
                })

    # REQ-REC-005: sort ascending lexically by (order_id, exception_type) — no numeric coercion
    rows.sort(key=lambda r: (r['order_id'], r['exception_type']))
    return rows


def write_output(path: str, rows: list) -> None:
    """Write exception report CSV with exact header (AC-REC-001.3/4)."""
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description='Reconcile orders against invoices.')
    parser.add_argument('--orders', required=True, help='Path to orders CSV')
    parser.add_argument('--invoices', required=True, help='Path to invoices CSV')
    parser.add_argument('--output', required=True, help='Path for exception report CSV')
    args = parser.parse_args()

    orders = load_orders(args.orders)
    invoices = load_invoices(args.invoices)
    rows = reconcile(orders, invoices)
    write_output(args.output, rows)
    # Exit code 0 on success (AC-REC-001.5) — implicit from normal return


if __name__ == '__main__':
    main()
