"""
reconcile.py — CSV Order-Invoice Reconciliation Pipeline (Phase 1)

CLI: python reconcile.py --orders PATH --invoices PATH --output PATH

Implements REQ-REC-001 through REQ-REC-005:
  - REQ-REC-001: CLI invocation and output file production
  - REQ-REC-002: Missing invoice detection
  - REQ-REC-003: Amount mismatch detection (exact decimal arithmetic)
  - REQ-REC-004: Late billing detection (strictly > 30 days)
  - REQ-REC-005: Lexical sort by (order_id, exception_type); multi-exception orders
"""

import argparse
import csv
from datetime import date
from decimal import Decimal


HEADER = ['order_id', 'exception_type', 'normalized_invoice_date', 'amount_delta']


def load_orders(path: str) -> dict:
    """Load orders CSV; return dict keyed by order_id.
    Schema: order_id, order_date, expected_amount  (AC-REC-001.1, REQ-REC-002)
    """
    orders = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            orders[row['order_id']] = {
                'order_date': date.fromisoformat(row['order_date']),
                'expected_amount': Decimal(row['expected_amount']),
            }
    return orders


def load_invoices(path: str) -> dict:
    """Load invoices CSV; return dict keyed by order_id (at most one per order).
    Schema: invoice_id, order_id, invoice_date, billed_amount  (REQ-REC-002, AC-REC-002.4)
    """
    invoices = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            oid = row['order_id']
            # At most one invoice per order; last one wins (spec says at most one anyway)
            invoices[oid] = {
                'invoice_date': date.fromisoformat(row['invoice_date']),
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
            norm_date = inv_date.isoformat()  # YYYY-MM-DD (AC-REC-003.3, AC-REC-004.4)
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
