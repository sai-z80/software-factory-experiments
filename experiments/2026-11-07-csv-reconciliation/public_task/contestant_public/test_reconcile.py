import csv
import os
from pathlib import Path
import signal
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parent
HEADER = ['order_id','exception_type','normalized_invoice_date','amount_delta']

def invoke(orders, invoices, tmp_path):
    output=tmp_path/'exceptions.csv'
    cmd=[sys.executable,str(ROOT/'reconcile.py'),'--orders',str(orders),'--invoices',str(invoices),'--output',str(output)]
    with (tmp_path/'stdout.txt').open('w') as out, (tmp_path/'stderr.txt').open('w') as err:
        p=subprocess.Popen(cmd,cwd=tmp_path,stdout=out,stderr=err,start_new_session=True)
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL);p.wait()
            pytest.fail('Candidate process timed out (3 seconds)')
        finally:
            try: os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError: pass
    assert p.returncode==0, (tmp_path/'stderr.txt').read_text()[:2000]
    assert output.exists(), 'exceptions.csv was not produced'
    with output.open(newline='',encoding='utf-8') as f: return list(csv.reader(f))

def expected(path):
    with path.open(newline='',encoding='utf-8') as f:return list(csv.reader(f))

def test_current_fixture(tmp_path):
    assert invoke(ROOT/'orders.csv',ROOT/'invoices.csv',tmp_path)==expected(ROOT/'expected_exceptions.csv')

def test_original_phase1_regression(tmp_path):
    base=ROOT/'fixtures'/'phase1'
    assert invoke(base/'orders.csv',base/'invoices.csv',tmp_path)==expected(base/'expected_exceptions.csv')

def test_empty_output_has_exact_header(tmp_path):
    orders=tmp_path/'orders.csv';invoices=tmp_path/'invoices.csv'
    orders.write_text('order_id,order_date,expected_amount\n007,2024-01-01,1.00\n')
    invoices.write_text('invoice_id,order_id,invoice_date,billed_amount\nX,007,2024-01-31,1.00\n')
    assert invoke(orders,invoices,tmp_path)==[HEADER]
