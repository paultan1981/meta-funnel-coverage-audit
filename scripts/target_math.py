#!/usr/bin/env python3
"""Target block, gated ladder and stop rules for one ad account.

    python3 target_math.py --spend7 3965 --value7 6615 --sales7 14 [--aov 463] \
        [--spend30 8557 --value30 11110 --sales30 24] [--currency MYR|SGD|IDR] [--fx 1] \
        [--target-myr 100000] [--roas 2] [--sprint1-days 30] [--today 2026-10-20] [--mode website|whatsapp]

Money inputs are in the account's own currency. --fx is local units per 1 MYR
(IDR ≈ 4,420 in Oct 2026; look it up fresh and cite the source). AOV defaults
to the 30-day average order (value30 / sales30), else the 7-day one.

Prints: board tiles, Today-vs-Target rows, the ladder (+20% every 3 days),
earliest full month at target, the stop-rule ladder and weekly creative volume.
"""
import argparse
import datetime as dt
import math


def short(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def money(x, cur):
    if cur == "IDR":
        return f"IDR {short(x / 1e6)} jt" if x >= 1e6 else f"IDR {x / 1e3:.0f}k"
    sym = "RM" if cur == "MYR" else f"{cur} "
    return f"{sym}{short(x / 1e3)}k" if x >= 10000 else f"{sym}{x:,.0f}"


def ladder(start, end):
    steps, v = [start], start
    while v * 1.2 < end:
        v *= 1.2
        steps.append(v)
    if steps[-1] < end:
        steps.append(end)
    return steps


def earliest_month(today, sprint1_days, ladder_days):
    reach = today + dt.timedelta(days=sprint1_days + ladder_days)
    if reach.day > 7:  # not at target pace in the first week → next month is the first full one
        reach = (reach.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    return reach.strftime("%B %Y")


def stop_rules(aov, max_cpa, cur, mode):
    m = lambda x: money(x, cur)
    rules = [("2,000 impressions", "Link CTR below 0.7%" if mode == "website" else "Link CTR below 0.4% (nobody opens the chat)")]
    if mode == "website":
        rules += [(m(0.23 * aov), "0 add-to-carts"),
                  (m(0.45 * aov), "Cost per add-to-cart above 2× the account average")]
    else:
        rules += [(m(0.15 * aov), "A WhatsApp click costs more than ~2× what this account usually pays")]
    rules += [(m(2 * max_cpa), f"0 sales (2× the {m(max_cpa)} target cost per sale)"),
              (m(1.5 * aov), "ROAS below 1.0"),
              (f"{m(3 * aov)} or 30 days", "ROAS below 1.5: replace it"),
              ("Any time", "Frequency above 3.5 (prospecting) or 6 (follow-up) with CTR down 30%: refresh the creative")]
    return rules


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spend7", type=float, required=True)
    ap.add_argument("--value7", type=float, required=True)
    ap.add_argument("--sales7", type=float, required=True)
    ap.add_argument("--spend30", type=float); ap.add_argument("--value30", type=float); ap.add_argument("--sales30", type=float)
    ap.add_argument("--aov", type=float)
    ap.add_argument("--currency", default="MYR")
    ap.add_argument("--fx", type=float, default=1.0, help="local units per 1 MYR")
    ap.add_argument("--target-myr", type=float, default=100000)
    ap.add_argument("--roas", type=float, default=2.0)
    ap.add_argument("--sprint1-days", type=int, default=30, help="shorten (e.g. 15) when the account is already near the target ROAS")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--mode", choices=["website", "whatsapp"], default="website")
    a = ap.parse_args()
    cur = a.currency

    aov = a.aov or ((a.value30 / a.sales30) if a.sales30 else (a.value7 / a.sales7))
    target = a.target_myr * a.fx
    max_spend = target / a.roas
    orders = target / aov
    max_cpa = aov / a.roas
    pace_sales = a.value7 / 7 * 30
    pace_spend = a.spend7 / 7 * 30
    roas7 = a.value7 / a.spend7 if a.spend7 else 0
    day_now, day_target = a.spend7 / 7, max_spend / 30
    steps = ladder(day_now, day_target)
    n = len(steps) - 1
    month = earliest_month(dt.date.fromisoformat(a.today), a.sprint1_days, 3 * n)

    print("BOARD")
    print(f"  Sales target      {money(target, cur)} a month" + (f" (RM{a.target_myr / 1e3:.0f}k at 1 MYR ≈ {a.fx:,.0f} {cur})" if cur != "MYR" else ""))
    print(f"  Max ad spend      {money(max_spend, cur)} a month, {money(day_target, cur)} a day")
    print(f"  Orders needed     ~{orders:.0f} a month (~{orders / 30:.0f} a day) at the {money(aov, cur)} average order")
    print(f"  Max cost per sale {money(max_cpa, cur)}")
    print("\nTODAY VS TARGET (today = last 7 days at a monthly pace)")
    rows = [("Sales a month", money(pace_sales, cur), money(target, cur), f"{target / pace_sales:.1f}×" if pace_sales else "–"),
            ("Ad spend a month", money(pace_spend, cur), money(max_spend, cur) + " max", f"{max_spend / pace_spend:.1f}×"),
            ("ROAS", f"{roas7:.2f}", f"{a.roas:.1f}", f"{a.roas - roas7:+.2f}"),
            ("Orders a month", f"~{a.sales7 / 7 * 30:.0f}", f"~{orders:.0f}", f"{orders / (a.sales7 / 7 * 30):.1f}×" if a.sales7 else "–"),
            ("Ad spend a day", money(day_now, cur), money(day_target, cur), f"{day_target / day_now:.1f}×")]
    for r in rows:
        print(f"  {r[0]:18} {r[1]:>18} {r[2]:>20} {r[3]:>8}")
    print("  <tbody>" + "".join(f'<tr><td>{r[0]}</td><td class="num">{r[1]}</td><td class="num">{r[2]}</td><td class="num">{r[3]}</td></tr>' for r in rows) + "</tbody>")
    if a.spend30:
        print(f"\n  30 days: {money(a.spend30, cur)} spent, {a.sales30:.0f} sales, {money(a.value30, cur)} in sales (ROAS {a.value30 / a.spend30:.2f})")

    print(f"\nLADDER: {n} steps of +20% every 3 days ≈ {3 * n} days, {money(day_now, cur)} → {money(day_target, cur)} a day")
    print('  <div class="ladder">' + "".join(f"<span>{money(s, cur)}</span>" for s in steps) + "</div>")
    print(f"  Earliest full month at target (Sprint 1 = {a.sprint1_days} days, then the ladder): {month}")

    print(f"\nSTOP RULES ({a.mode}; AOV {money(aov, cur)}, max cost per sale {money(max_cpa, cur)})")
    for at, rule in stop_rules(aov, max_cpa, cur, a.mode):
        print(f"  {at:28} {rule}")
    print("  Never pause an ad that sold in the last 7 days without a written reason.")

    print("\nCREATIVE VOLUME: replace about a quarter of live ads a week — "
          "3–4 new ads a week at today's spend, 6–8 at the target spend.")


if __name__ == "__main__":
    main()
