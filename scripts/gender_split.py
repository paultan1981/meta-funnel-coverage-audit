#!/usr/bin/env python3
"""Men vs women ROAS for 90 / 30 / 7 days, plus the age × gender cells.

    python3 gender_split.py --d90 age_gender_90d.json --d30 gender_30d.json --d7 gender_7d.json [--by name]

Inputs are mcp_load.py outputs of ads_get_ad_entities with
breakdowns ["age","gender"] (90 days) and ["gender"] (30 and 7 days).
--by groups rows by a field first (e.g. `name` at campaign level to split
MY and SG campaigns); omit it for one account-level table.
For a campaign younger than 90 days, pass the since-launch pull as --d90.

Prints a plain table, ready-made <tr> rows for the report, and the age cells.
"""
import argparse
import json
from collections import defaultdict


def load(path):
    return json.load(open(path, encoding="utf-8")) if path else []


def by_gender(rows):
    out = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])  # spend, sales, value, clicks
    for r in rows:
        g = r.get("gender", "unknown")
        o = out[g]
        o[0] += r["amount_spent"]; o[1] += r["omni_purchase"]; o[2] += r["purchase_value"]; o[3] += r.get("link_click", 0)
    return out


def roas(o):
    return o[2] / o[0] if o[0] else 0.0


def fmt_money(x, cur):
    if cur == "IDR":
        return f"IDR {x / 1e6:.1f} jt"
    return f"{'RM' if cur in (None, '', 'MYR') else cur + ' '}{x:,.0f}"


def period_rows(label, rows, cur):
    g = by_gender(rows)
    m, f = g["male"], g["female"]
    known = m[0] + f[0]
    if not known:
        return None
    share = 100 * m[0] / known
    rm, rf = roas(m), roas(f)
    win = "men" if rm > rf else "women"
    print(f"  {label:14} men {fmt_money(m[0], cur):>14} ({share:3.0f}%) {m[1]:4.0f} sales ROAS {rm:4.2f} "
          f"cost/sale {fmt_money(m[0] / m[1], cur) if m[1] else '–':>12} clicks/sale {m[3] / m[1] if m[1] else 0:5.0f} | "
          f"women {fmt_money(f[0], cur):>14} {f[1]:4.0f} sales ROAS {rf:4.2f} "
          f"cost/sale {fmt_money(f[0] / f[1], cur) if f[1] else '–':>12} clicks/sale {f[3] / f[1] if f[1] else 0:5.0f}  → {win}")
    bm = f"<b>{rm:.2f}</b>" if rm > rf else f"{rm:.2f}"
    bf = f"<b>{rf:.2f}</b>" if rf > rm else f"{rf:.2f}"
    return (f'<tr><td>{label}</td><td class="num">{fmt_money(m[0], cur)}</td><td class="num">{share:.0f}%</td>'
            f'<td class="num">{m[1]:.0f}</td><td class="num">{bm}</td><td class="num">{f[1]:.0f}</td><td class="num">{bf}</td></tr>')


def age_cells(rows, cur):
    cells = defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in rows:
        if "age" not in r or r.get("gender") not in ("male", "female"):
            continue
        c = cells[(r["age"], r["gender"])]
        c[0] += r["amount_spent"]; c[1] += r["omni_purchase"]; c[2] += r["purchase_value"]
    if not cells:
        return
    print("  age × gender (spend · sales · ROAS):")
    for age in sorted({k[0] for k in cells}):
        parts = []
        for g in ("male", "female"):
            c = cells.get((age, g))
            if c:
                parts.append(f"{g[0].upper()} {fmt_money(c[0], cur)} · {c[1]:.0f} · {c[2] / c[0] if c[0] else 0:.2f}")
        print(f"    {age:8} " + "   |   ".join(parts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d90"); ap.add_argument("--d30"); ap.add_argument("--d7")
    ap.add_argument("--label90", default="90 days")
    ap.add_argument("--by", help="group rows by this field first, e.g. name")
    a = ap.parse_args()
    data = {"90": load(a.d90), "30": load(a.d30), "7": load(a.d7)}
    cur = next((r.get("currency") for rows in data.values() for r in rows if r.get("currency")), "")
    groups = sorted({r.get(a.by, "") for rows in data.values() for r in rows}) if a.by else [None]
    labels = {"90": a.label90, "30": "30 days", "7": "7 days"}
    for grp in groups:
        print(f"\n== {grp or 'account'}")
        html = []
        for p in ("90", "30", "7"):
            rows = [r for r in data[p] if grp is None or r.get(a.by, "") == grp]
            if rows:
                tr = period_rows(labels[p], rows, cur)
                if tr:
                    html.append(tr)
        age_cells([r for r in data["90"] if grp is None or r.get(a.by, "") == grp], cur)
        print("  <tbody> rows:")
        for tr in html:
            print("   ", tr)
    print("\nReminders: Meta records the clicker's gender (a man may buy for his wife). "
          "Under ~10 sales a window shows direction, not proof. A gender split needs the "
          "original audience option; Advantage+ audience treats gender as a suggestion.")


if __name__ == "__main__":
    main()
