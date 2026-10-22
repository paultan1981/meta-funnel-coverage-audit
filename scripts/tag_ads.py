#!/usr/bin/env python3
"""Tag 90-day ads by angle and sub-avatar, then score each group on what it sold.

    python3 tag_ads.py <ads.json from mcp_load.py> <rules.json> [--out tagged.json]

rules.json (write one per account, in the ads' own language):
{
  "angles":  [["Hero static: Poster 6", "^poster 6"], ["Safety / side effects", "efek samping|aman"], ...],
  "avatars": [["Tried other products", "produk lain|ganti-ganti"], ...],
  "fields":  ["name", "adset_name"]          # optional: text the regexes search (default name + adset_name)
}

First match wins, so order rules from most to least specific. Ads that match no
angle land in "Other"; the script prints the biggest of them so you can add
rules until "Other" is under ~20% of spend.

Also prints concepts: the same ad name with " – Copy", "(2)" etc. stripped, so a
creative running in several ad sets is judged once.
"""
import argparse
import json
import re
from collections import defaultdict

COPY_SUFFIX = re.compile(r"(\s*[–-]\s*copy(\s*\d+)?|\s*\(\d+\)|\s+copy(\s*\d+)?)+\s*$", re.I)


def concept_name(name):
    return COPY_SUFFIX.sub("", name or "").strip()


def first_match(text, rules, default):
    for label, rx in rules:
        if re.search(rx, text, re.I):
            return label
    return default


def aggregate(rows, key):
    groups = defaultdict(lambda: {"ads": 0, "spend": 0.0, "sales": 0.0, "value": 0.0, "atc": 0.0, "clicks": 0.0})
    for r in rows:
        g = groups[r[key]]
        g["ads"] += 1
        g["spend"] += r["amount_spent"]
        g["sales"] += r["omni_purchase"]
        g["value"] += r["purchase_value"]
        g["atc"] += r.get("omni_add_to_cart", 0)
        g["clicks"] += r.get("link_click", 0)
    return sorted(groups.items(), key=lambda kv: -kv[1]["spend"])


def print_table(title, groups, total, cur):
    print(f"\n{title}")
    print(f"  {'group':44} {'ads':>4} {'spend':>14} {'share':>6} {'sales':>6} {'ROAS':>5} {'cost/sale':>12} {'ATC':>6}")
    for label, g in groups:
        roas = g["value"] / g["spend"] if g["spend"] else 0
        cps = g["spend"] / g["sales"] if g["sales"] else 0
        flag = "" if g["sales"] >= 10 else "  (direction, not proof)"
        print(f"  {label[:44]:44} {g['ads']:4d} {g['spend']:14,.0f} {100 * g['spend'] / total:5.0f}% "
              f"{g['sales']:6.0f} {roas:5.2f} {cps:12,.0f} {g['atc']:6.0f}{flag}")
    print(f"  currency: {cur}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ads")
    ap.add_argument("rules")
    ap.add_argument("--out", default="tagged.json")
    ap.add_argument("--top-other", type=int, default=20)
    a = ap.parse_args()

    ads = json.load(open(a.ads, encoding="utf-8"))
    rules = json.load(open(a.rules, encoding="utf-8"))
    fields = rules.get("fields", ["name", "adset_name"])
    cur = next((r.get("currency") for r in ads if r.get("currency")), "")

    rows = []
    for r in ads:
        text = " | ".join(concept_name(str(r.get(f, ""))) if f == "name" else str(r.get(f, "")) for f in fields)
        rows.append({**r,
                     "concept": concept_name(r.get("name", "")),
                     "angle": first_match(text, rules.get("angles", []), "Other"),
                     "avatar": first_match(text, rules.get("avatars", []), "—")})
    json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)

    total = sum(r["amount_spent"] for r in rows) or 1
    sales = sum(r["omni_purchase"] for r in rows)
    value = sum(r["purchase_value"] for r in rows)
    print(f"{len(rows)} ads · spend {total:,.0f} {cur} · {sales:.0f} sales · ROAS {value / total:.2f}")

    print_table("BY ANGLE", aggregate(rows, "angle"), total, cur)
    print_table("BY SUB-AVATAR", aggregate(rows, "avatar"), total, cur)
    print_table("TOP CONCEPTS (same creative across ad sets)", aggregate(rows, "concept")[:25], total, cur)

    other = [r for r in rows if r["angle"] == "Other"]
    share = 100 * sum(r["amount_spent"] for r in other) / total
    print(f"\nOTHER bucket: {len(other)} ads, {share:.0f}% of spend" + ("  ← add rules" if share > 20 else ""))
    for r in sorted(other, key=lambda r: -r["amount_spent"])[: a.top_other]:
        print(f"  {r['amount_spent']:12,.0f}  {r['omni_purchase']:3.0f} sales | {r.get('name', '')[:70]} | {str(r.get('adset_name', ''))[:40]}")
    print(f"\ntagged rows → {a.out}")


if __name__ == "__main__":
    main()
