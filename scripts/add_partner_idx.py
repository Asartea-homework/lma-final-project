import argparse
from consistency.partner_index import add_partner_columns

p = argparse.ArgumentParser()
p.add_argument("--inp", required=True)
p.add_argument("--out", required=True)
p.add_argument("--offset", type=int, default=0)
a = p.parse_args()

add_partner_columns(a.inp, a.out, offset=a.offset)