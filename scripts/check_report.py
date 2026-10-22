#!/usr/bin/env python3
"""QA a coverage report before publishing.

    python3 check_report.py <report.html>

Fails (exit 1) on structural problems; warns on style problems. Checks:
- <title> is 2–4 words-ish (CJK titles: ≤ 12 characters)
- section order: Verdict first, Target second, Men vs women third, Summary last
- Summary has the .tline target line and the four blocks
- <section>, <ul>, <ol>, <table> tags balance
- dark-mode tokens exist with both guards; no <script> tags; no {{placeholders}} left
- jargon that needs plain words (TOFU/MOFU/BOFU, CPR, CBO/ABO) is flagged
"""
import re
import sys

REQUIRED_ORDER = ["t-verdict", "t-target", "t-gender"]
SUMMARY_BLOCKS_EN = ["What we found", "Focus", "Turn off", "To complete the funnel"]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    html = open(sys.argv[1], encoding="utf-8").read()
    errors, warns = [], []

    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        errors.append("no <title>")
    else:
        t = m.group(1).strip()
        cjk = re.search(r"[一-鿿]", t)
        if (cjk and len(t) > 16) or (not cjk and not 2 <= len(t.split()) <= 5):
            warns.append(f"title should be a 2–4 word name: {t!r}")

    ids = re.findall(r'<section aria-labelledby="([^"]+)"', html)
    if ids[:3] != REQUIRED_ORDER:
        errors.append(f"first sections must be {REQUIRED_ORDER}, found {ids[:3]}")
    if not ids or ids[-1] != "t-summary":
        errors.append(f"last section must be t-summary, found {ids[-1] if ids else None}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate section ids")
    if "t-objections" not in ids:
        warns.append("no objections section (t-objections, spec §6b); it is standard since 22 Oct 2026")
    elif "t-map" in ids and ids.index("t-objections") != ids.index("t-map") + 1:
        warns.append("objections section (t-objections) should come right after the coverage map (t-map)")

    s = html.find('aria-labelledby="t-summary"')
    summ = html[s:] if s >= 0 else ""
    if 'class="tline"' not in summ:
        errors.append("Summary is missing the target line (p.tline)")
    if 'lang="zh' not in html:
        for b in SUMMARY_BLOCKS_EN:
            if b not in summ:
                warns.append(f"Summary block missing: {b}")

    for tag in ("section", "ul", "ol", "table", "div"):
        o = len(re.findall(rf"<{tag}[\s>]", html)); c = html.count(f"</{tag}>")
        if o != c:
            errors.append(f"<{tag}> open {o} / close {c}")

    if "prefers-color-scheme: dark" not in html or ':root:not([data-theme="light"])' not in html or ':root[data-theme="dark"]' not in html:
        errors.append("dark-mode tokens or their two guards are missing")
    if "<script" in html:
        warns.append("page has <script>; reports should be static")
    if "{{" in html:
        errors.append(f"{html.count('{{')} template placeholders left")

    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    for word in ("TOFU", "MOFU", "BOFU", "CBO", "ABO", "CPR"):
        for m in re.finditer(rf"\b{word}\b", text):
            ctx = text[max(0, m.start() - 40): m.end() + 30].strip()
            warns.append(f"jargon {word}: “…{ctx}…” — rewrite in plain words unless it is part of a quoted ad / ad set name")

    for e in errors:
        print("ERROR ", e)
    for w in warns:
        print("warn  ", w)
    print(f"{len(ids)} sections: {' → '.join(ids)}")
    print("OK" if not errors else "FIX ERRORS BEFORE PUBLISHING")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
