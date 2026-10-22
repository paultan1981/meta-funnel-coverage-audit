#!/usr/bin/env python3
"""Turn a Meta Ads MCP ads_get_ad_entities result into a clean JSON list.

Large MCP results are saved by the harness to a tool-results/*.txt file whose
content is {"ad_entities": "<JSON string>", ...}. Small results can be pasted
into a file as-is. Either way this writes a list of flat rows with numbers
already parsed:

    python3 mcp_load.py <result.txt|.json> <out.json>

Each row keeps every original key; money fields ({"value": "..", "unit": ".."})
become floats and a `currency` key is added. Missing metrics become 0.
"""
import json
import sys

NUMERIC = {
    "amount_spent", "impressions", "link_click", "landing_page_view",
    "omni_landing_page_view", "omni_add_to_cart", "omni_initiated_checkout",
    "omni_purchase", "purchase_roas", "frequency", "website_ctr",
    "outbound_clicks_ctr", "cpm", "video_play_actions",
    "video_thruplay_watched_actions", "daily_budget", "results",
    "cost_per_result",
}


def to_num(x):
    if isinstance(x, dict) and "value" in x:
        x = x["value"]
    if x in (None, ""):
        return 0.0
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def load(path):
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, dict):
        for key in ("ad_entities", "data", "results"):
            if key in raw:
                raw = raw[key]
                break
    if isinstance(raw, str):
        raw = json.loads(raw)
    if not isinstance(raw, list):
        raise SystemExit(f"Unexpected shape in {path}: {type(raw).__name__}")
    return raw


def clean(rows):
    out = []
    for r in rows:
        row = dict(r)
        unit = None
        for k, v in r.items():
            if isinstance(v, dict) and "unit" in v:
                unit = unit or v["unit"]
            if k in NUMERIC:
                row[k] = to_num(v)
        row["currency"] = unit
        # purchase value is not returned directly; derive it from ROAS × spend
        row["purchase_value"] = row.get("purchase_roas", 0.0) * row.get("amount_spent", 0.0)
        out.append(row)
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    rows = clean(load(sys.argv[1]))
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)
    spend = sum(r.get("amount_spent", 0) for r in rows)
    sales = sum(r.get("omni_purchase", 0) for r in rows)
    value = sum(r["purchase_value"] for r in rows)
    cur = next((r["currency"] for r in rows if r.get("currency")), "")
    print(f"{len(rows)} rows · spend {spend:,.0f} {cur} · sales {sales:,.0f} · "
          f"ROAS {value / spend if spend else 0:.2f} → {sys.argv[2]}")


if __name__ == "__main__":
    main()
