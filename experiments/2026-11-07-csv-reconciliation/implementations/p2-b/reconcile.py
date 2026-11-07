"""
reconcile.py — Phase 1 + Phase 2 order/invoice reconciliation.

CLI: python reconcile.py --orders PATH --invoices PATH --output PATH

Rules (from BRIEF.md):
  missing_invoice  : order has no matching invoice
  amount_mismatch  : billed_amount != expected_amount
  late_billing     : (invoice_date - order_date).days > 30  (exactly 30 is NOT late)

Output: UTF-8 CSV sorted ascending by (order_id, exception_type) — lexical, not numeric.
Header: order_id,exception_type,normalized_invoice_date,amount_delta

Phase 2 additions:
  - Invoices file may have exactly 2 metadata lines before the CSV header row.
  - In that case invoice_date values use DD/MM/YYYY format.
  - Both formats (no-preamble ISO and two-preamble DD/MM/YYYY) are supported.
  - Do not rely on literal metadata content for format detection.
"""

import argparse
import csv
import io
import sys
from datetime import date
from decimal import Decimal


def parse_iso_date(s: str) -> date:
    """Parse YYYY-MM-DD."""
    return date.fromisoformat(s.strip())


def parse_dmy_date(s: str) -> date:
    """Parse DD/MM/YYYY."""
    s = s.strip()
    day, month, year = s.split("/")
    return date(int(year), int(month), int(day))


def detect_invoice_format(path: str):
    """
    Detect whether the invoice file is:
      - 'iso'  : no preamble, first line is the CSV header, dates are YYYY-MM-DD
      - 'dmy'  : exactly 2 metadata lines before the CSV header, dates are DD/MM/YYYY

    Returns (format_str, skip_lines) where skip_lines is the number of lines
    to skip before the CSV header.

    Detection rule (per CHANGE.md):
      Only two invoice formats are scored:
        1. Original: one header line, no preamble, ISO dates.
        2. New:      exactly two metadata lines before the same header, DD/MM/YYYY dates.
      We detect by reading the first line: if it starts with 'invoice_id' (the known
      header field) it is the original format; otherwise we assume the new two-preamble
      DD/MM/YYYY format.
    """
    with open(path, newline="", encoding="utf-8") as f:
        first_line = f.readline()

    # Strip BOM / whitespace for comparison
    first_stripped = first_line.strip().lstrip("\ufeff")

    # The CSV header always starts with 'invoice_id'
    if first_stripped.startswith("invoice_id"):
        return "iso", 0
    else:
        # Two metadata lines precede the header
        return "dmy", 2


def load_orders(path: str) -> dict:
    """Return {order_id: {'order_date': date, 'expected_amount': Decimal}}."""
    orders = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            oid = row["order_id"]
            orders[oid] = {
                "order_date": parse_iso_date(row["order_date"]),
                "expected_amount": Decimal(row["expected_amount"].strip()),
            }
    return orders


def load_invoices(path: str) -> dict:
    """Return {order_id: {'invoice_date': date, 'billed_amount': Decimal}}.

    Supports two invoice file formats (auto-detected):
      - Original (Phase 1): no preamble, ISO YYYY-MM-DD dates.
      - New (Phase 2): exactly 2 metadata lines before the CSV header, DD/MM/YYYY dates.

    Invoices referencing no order are ignored (handled at reconcile time).
    At most one invoice per order (per spec).
    """
    fmt, skip_lines = detect_invoice_format(path)

    if fmt == "iso":
        date_parser = parse_iso_date
    else:
        date_parser = parse_dmy_date

    invoices = {}
    with open(path, newline="", encoding="utf-8") as f:
        # Skip the preamble metadata lines (0 for iso, 2 for dmy)
        for _ in range(skip_lines):
            f.readline()

        reader = csv.DictReader(f)
        for row in reader:
            oid = row["order_id"]
            invoices[oid] = {
                "invoice_date": date_parser(row["invoice_date"]),
                "billed_amount": Decimal(row["billed_amount"].strip()),
            }
    return invoices


def reconcile(orders: dict, invoices: dict) -> list:
    """Return list of exception rows as dicts."""
    rows = []

    for order_id, order in orders.items():
        order_date = order["order_date"]
        expected = order["expected_amount"]

        if order_id not in invoices:
            # missing_invoice: normalized_invoice_date and amount_delta both empty
            rows.append({
                "order_id": order_id,
                "exception_type": "missing_invoice",
                "normalized_invoice_date": "",
                "amount_delta": "",
            })
        else:
            inv = invoices[order_id]
            invoice_date = inv["invoice_date"]
            billed = inv["billed_amount"]

            delta = billed - expected
            norm_date = invoice_date.isoformat()
            # Format delta to exactly two decimal places (sign preserved)
            delta_str = f"{delta:.2f}"

            # amount_mismatch
            if billed != expected:
                rows.append({
                    "order_id": order_id,
                    "exception_type": "amount_mismatch",
                    "normalized_invoice_date": norm_date,
                    "amount_delta": delta_str,
                })

            # late_billing: strictly more than 30 days
            days_diff = (invoice_date - order_date).days
            if days_diff > 30:
                rows.append({
                    "order_id": order_id,
                    "exception_type": "late_billing",
                    "normalized_invoice_date": norm_date,
                    "amount_delta": delta_str,
                })

    # Sort ascending lexically by (order_id, exception_type)
    rows.sort(key=lambda r: (r["order_id"], r["exception_type"]))
    return rows


def write_output(path: str, rows: list) -> None:
    fieldnames = ["order_id", "exception_type", "normalized_invoice_date", "amount_delta"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Reconcile orders against invoices.")
    parser.add_argument("--orders", required=True, help="Path to orders CSV")
    parser.add_argument("--invoices", required=True, help="Path to invoices CSV")
    parser.add_argument("--output", required=True, help="Path for output exceptions CSV")
    args = parser.parse_args()

    orders = load_orders(args.orders)
    invoices = load_invoices(args.invoices)
    rows = reconcile(orders, invoices)
    write_output(args.output, rows)


if __name__ == "__main__":
    main()
