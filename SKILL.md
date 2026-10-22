---
name: meta-funnel-coverage-audit
description: Use when Paul asks to audit a Meta ads account (or specific campaigns) for funnel creative coverage — "audit this ads account", "funnel creative coverage report", "which sub-avatar should I focus / which content should I off", "what else to complete the funnel", re-running or updating an earlier coverage report, or adding targets / men-vs-women ROAS to one. Covers Afyaa, Sahiyya+, Wellous, SGLOW and WP-xx accounts in MYR, SGD or IDR.
---

# Meta Funnel Creative Coverage Audit

Paul's question for any ad account: **does every buyer see an ad made for their step in the decision, and does the account follow up the people who showed interest?**

The answer is one HTML report, published as an Artifact. It holds:
- 90 days of creative scored on what it actually sold
- the sub-avatar to focus on
- the live ads mapped by step
- which ads to switch off
- a ranked fix list
- stop rules
- the RM100k @ ROAS 2 target
- men vs women
- a Summary that mirrors the chat recap

It has been used four times: WP-12, WP-09, Afyaa 3 and SGLOW (Oct 2026).

Read `reference/report-spec.md` before writing the report. It has the section-by-section spec, the writing rules and the mistakes already made once.

## Inputs

**Required: the ad account ID.** Ask only if it's missing.

Everything else comes from memory or the data:
- campaign IDs, if the audit is scoped to specific campaigns (e.g. WP-12 = 2 campaigns)
- market and currency
- product and target audience
- the account's scope rule (e.g. WP-12 = diagnosed CKD stage 2–4 only)
- report language: EN by default; ZH or other only on request
- the existing report URL, if this is a re-audit

## Step 0 · Context (before any data)

1. Read `MEMORY.md` in the project memory folder.
2. Open every memory that names this account or product:
   - `*-coverage-audit.md`
   - `ads-account-targets-rm100k-roas2.md`
   - product truth: any `*-product-truth.md` or `*-selling-points.md` for the product
   - `wp12-web-campaigns-true-roas.md`, for known tracking issues such as Purchase double-fires and WhatsApp closes outside Meta
3. Note these from memory:
   - **Scope rules.** What belongs in this campaign, so off-scope angles go to "move", not "gap".
   - **True-ROAS adjustments.**
   - **Decisions Paul already made.** Don't re-litigate them.
   - **Banned claims.**
4. For a re-audit, run `Artifact action:"read"` on the existing URL. Build on the returned file. Never build from a stale local copy.

## Step 1 · Load the Meta tools

Make one ToolSearch call: `select:` + these names, comma-joined. The prefix is `mcp__b163f209-3e26-4e00-97b6-c24c2e03a849__`. If that fails, search `+ads_get_ad_entities` to find the current prefix.

```
ads_get_ad_accounts, ads_get_ad_entities, ads_get_field_context, ads_get_creatives,
ads_get_opportunity_score, ads_insights_performance_trend, ads_insights_industry_benchmark
```

Call rules for every Meta call:
- **Conversation ID.** Generate a 20-character `client_conversation_id` on the first call and reuse it on every call after.
- **Model.** Pass `client_model` = the exact model ID from the system prompt.
- **Request wording.** `advertiser_request` = Paul's own words.
- **Next actions.** Run every `next_actions` item marked `read_only:true`, as the tool contract requires.
- **Unknown fields.** If you're not sure a field exists, check it with `ads_get_field_context`. The names below are verified.

## Step 2 · Pull the data

Use `include_additional_context:false` and `sort:"amount_spent_descending"` unless noted. Save each pull as `<letter>.json` in the scratchpad (A90, A30, A7, B, C, D, E, F, G30, G7, H) so later steps can find it.

| # | Purpose | Call |
|---|---|---|
| A | Campaigns, 90/30/7 days | `level:"campaign"`, filter `campaign.amount_spent GREATER_THAN ["0"]`. Fields: `id, name, effective_status, objective, amount_spent, link_click, landing_page_view, omni_add_to_cart, omni_initiated_checkout, omni_purchase, purchase_roas, frequency`. Three calls: `last_90d`, `last_30d`, `last_7d`. |
| B | Live ad sets: structure | `level:"adset"`, filter `adset.effective_status IN ["ACTIVE"]`, `last_30d`. Fields: `id, name, campaign_id, effective_status, daily_budget, optimization_goal, destination_type, promoted_object, learning_stage_info, targeting, amount_spent, frequency, link_click, landing_page_view, omni_purchase, purchase_roas` |
| C | Live ads, lifetime | `level:"ad"`, filter `ad.effective_status IN ["ACTIVE","PENDING_REVIEW","IN_PROCESS","WITH_ISSUES"]`, `date_preset:"maximum"`, `limit:300`. Fields: `id, name, adset_name, campaign_id, effective_status, creative_id, amount_spent, impressions, website_ctr, link_click, landing_page_view, omni_add_to_cart, omni_purchase, purchase_roas, video_play_actions, video_thruplay_watched_actions` |
| D | Live ad copy | `ads_get_creatives`, `creative_ids` from C. Fields: `id, name, object_type, body, title, description, link_url, call_to_action_type, video_id, image_url, thumbnail_url` |
| E | All ads, 90 days | `level:"ad"`, filter `ad.amount_spent GREATER_THAN ["0"]`, `last_90d`, `limit:1000`. Fields: as in C, minus `website_ctr` and thruplays. |
| F | Age × gender, 90 days | `level:"ad_account"`, `breakdowns:["age","gender"]`, `last_90d`. Fields: `amount_spent, link_click, omni_add_to_cart, omni_purchase, purchase_roas` |
| G | Gender, 30 and 7 days | Same as F with `breakdowns:["gender"]`, `last_30d` and `last_7d`. |
| H | Placements | Same as F with `breakdowns:["publisher_platform"]`, `last_90d`. |
| I | Meta's own view | `ads_get_opportunity_score` (account) and `ads_insights_performance_trend` (`analysis_level:"AD"`, `conversation_intent:"INCREASE_VOLUME_OF_RESULTS"`, `conversation_topic:"CREATIVE"`, `hide_ui:true`) |

**Campaign-scoped audits** (like WP-12):
- Use `level:"campaign"` with `object_ids:[…]` for A, F, G and H.
- Filter C and E by `campaign_id`.
- Use `--by name` in gender_split to split markets.
- For a campaign younger than 90 days, "90 days" means since launch; say so in the report.

**WhatsApp / CTWA accounts** (like WP-09):
- Purchases are closes pushed from the CRM.
- Add-to-cart is meaningless.
- Clicks per sale is the close-rate metric.

**Non-MYR accounts:** look up today's FX rate (WebSearch) and cite the source in the reply.

**Large results** are saved to a `tool-results/*.txt` file. Never hand-copy numbers from them; convert with:

```bash
python3 ~/.claude/skills/meta-funnel-coverage-audit/scripts/mcp_load.py <tool-result.txt> <scratchpad>/E.json
```

For a small inline result, write the returned JSON to a file first, then run mcp_load on it. It accepts both shapes.

## Step 3 · Crunch (scripts only; no mental math)

Work in the session scratchpad. `S=~/.claude/skills/meta-funnel-coverage-audit/scripts`.

1. **Angles and sub-avatars.**
   - Write `rules.json` in the ads' language. Start from `examples/rules-sahiyya-ckd-ms.json` (Malay, kidney) or `examples/rules-sglow-hairloss-id.json` (Indonesian, hair).
   - Run `python3 $S/tag_ads.py E.json rules.json --out tagged.json`.
   - Add rules until the "Other" bucket is under ~20% of spend.
   - Judge concepts (the same creative across ad sets), not single copies.
2. **Men vs women.** Convert F and G with mcp_load, then run:
   `python3 $S/gender_split.py --d90 F.json --d30 G30.json --d7 G7.json [--by name]`
3. **Target and stop rules.**
   - Run `python3 $S/target_math.py --spend7 … --value7 … --sales7 … --spend30 … --value30 … --sales30 … --today YYYY-MM-DD [--aov …] [--currency IDR --fx 4420] [--mode whatsapp] [--sprint1-days 15]`.
   - Take spend, sales and value from the account totals of A7 and A30. Value = ROAS × spend; mcp_load adds it as `purchase_value`.
   - Pass `--aov` only when the true average order differs from Meta's (e.g. WhatsApp closes). Otherwise it defaults to the 30-day value ÷ sales.
   - Use `--sprint1-days 15` when the account is already near ROAS 2.
4. **Coverage map.**
   - Place every live ad (C + D) on a decision step, using the step list in report-spec §6.
   - Read the actual copy. Count the live ads that share a primary text.
   - Check whether each ad names its person in the first line or first 3 seconds.
5. **Objections (section 6b).**
   - Take the 1–2 sub-avatars that sell from tag_ads (the Focus row plus the next best in scope).
   - For each of the 6–8 standard objections in report-spec §6b, decide from the live copy (D) whether a live ad answers it: proven, partial or none.
   - Search E's ad names for objection words (`lama|kesan|doktor|ubat|mahal|bazir|harga|promo|ori|farmasi|selamat|sesuai|cod|pakej`) to find a paused or past ad that can fill each gap.
   - Count how many gaps are a copy or a move, and how many need a new shoot.
6. **Structure.** From B, check:
   - Is there a retargeting ad set? Are buyers excluded?
   - Advantage+ audience on or off?
   - How many ad sets have one ad, and how many have the same broad audience?
   - Learning-limited ad sets.
   - Placement winners and losers (H).
   - Any fragmentation warning from I.

## Step 4 · Make the calls

- **Focus sub-avatar.** Pick the best ROAS group with ≥10 sales that fits the account's scope. If the data contradicts the team's plan, say so plainly.
- **Off.** Off = past a stop line from target_math, counted per concept.
- **Watch.** Watch = under the line; give the exact line where it gets stopped.
- **Keep.** Keep = sold within the rules. Flag any fatigue that I shows.
- **Fix list.** Rank by money at stake each month, e.g. unconverted add-to-carts × average order, or spend on losers. The usual top three:
  1. a follow-up layer that holds the objection ads
  2. the checkout or close-rate leak
  3. a hero refresh that keeps its copy structure
- **The lever.** Name the one number that must move before the budget ladder starts.

## Step 5 · Build the report

1. **Publish rules first.** Follow the Artifact tool's current rules for a new page. The template already meets the page contract: light/dark tokens with both guards, Archivo + IBM Plex Mono, phone-safe tables.
2. **Copy the template.** Copy `assets/report-template.html` to `<scratchpad>/<account>-coverage.html`.
   - Title: `<Account> Funnel Coverage`.
   - Header: eyebrow, lede, meta line, and the "How this account sells" note.
3. **Fill the sections** in order per `reference/report-spec.md`:
   Verdict → Target → Men vs women → What sells → Sub-avatar → Coverage map → **Objections (6b)** → Off/watch/keep → Complete the funnel → Stop rules/SOP → **Summary last**.
4. **Paste script output.** Use the `<tbody>`, `<tr>` and ladder output exactly as the scripts printed it.
5. **ZH (or BM/ID) version on request only.** See the spec's ZH notes, and cross-link the two pages.

## Step 6 · QA (all must pass before publishing)

- [ ] `python3 $S/check_report.py <file>` prints OK.
  - It checks section order, the Summary tline, tag balance, dark-mode guards and leftover `{{…}}`.
- [ ] Every count in the page was recounted against script output after the last edit (`grep` the claims).
- [ ] The objections table (6b) has one column per selling sub-avatar (or market), and every "Fill from" names a real ad from E with its numbers or says "New shoot". The "N of M need a copy, not a shoot" count matches the rows.
- [ ] No recommendation contradicts a table on the same page.
- [ ] Off-scope angles are marked "move", not "gap".
- [ ] Rows with fewer than 10 sales are labelled "direction, not proof".
- [ ] Ad names are exactly as they appear in Ads Manager.
- [ ] The Summary matches the Verdict, the Fix list and the chat recap.

## Step 7 · Publish, recap, remember

1. **Publish.**
   - New report: `Artifact` with `icon:"map"` and a one-sentence `description`.
   - Re-audit: pass `url` to update in place, so the link Paul shared keeps working.
2. **Recap in chat.** Mirror the Summary:
   - the target line
   - What we found (bold claim + number)
   - Focus
   - Turn off · watch
   - To complete the funnel
   - the report link, plus a note if the page is private ("share from the page's Share menu")
3. **Memory.**
   - Write or update `<account>-coverage-audit.md` (type project): account ID, how it sells, key findings with numbers, report URL + version, open offers.
   - Add or refresh its line in `MEMORY.md`.
   - Update this account's row in `ads-account-targets-rm100k-roas2.md`.
4. **Offer one next action.** Examples:
   - build the retargeting or gender-split ad sets as paused drafts
   - set a daily stop-gates check
   - make a ZH/BM version

   **Never pause, edit or launch live ads without an explicit "yes" for that action.**

## Common mistakes (all happened once)

| Mistake | Fix |
|---|---|
| Counts drifted after edits (13 vs 9 off-target ads, 55 vs 57 to switch off) | Recount from tagged.json after every edit |
| Briefed "stage-named + family testimonials" when the 90-day data said they lost | Recommendations follow the data; re-read the angle table before writing the fix list |
| Judged each "– Copy" duplicate separately | Judge concepts; stop lines apply per concept |
| Objection ads called failures when they had only run cold | Judge objection ads in retargeting; recommend moving them there |
| Briefed new shoots for objections an old paused ad already answered | Search E's names for objection words before writing "New shoot" (spec §6b) |
| Assumed women buy beauty and men buy for themselves | Pull gender per account; SGLOW men won, WP-12 SG women won |
| Trusted Meta ROAS on an account with known tracking bugs | Read memory for true-ROAS notes (WhatsApp closes, double-fires) and state which number the page uses |
| Summary forgotten or placed mid-page | The Summary is always the last section; check_report enforces this |
| Updated a report from a stale local file | Read the live artifact first on any re-audit |
| Hand-copied a big inline MCP result (error-prone, slow) | Pull it back out of the session transcript jsonl: find the last line containing a unique marker plus `"toolUseResult"`, `raw_decode` from `{"next_actions"`, then `json.loads(obj["ad_entities"])` (WP-12, 21 Oct) |
| Missed rejected ads, which deliver nothing but leave a step empty | Add `"DISAPPROVED"` to pull C. `ads_get_errors` does not return rejection reasons, so read them in the standalone ad editor (`…/ads/edit/standalone?act=…&selected_ad_ids=…`) and add a "Rejected by Meta" section |
| A campaign younger than 90 days printed "90 days / 30 days" labels | Pull `maximum` / `last_14d` / `last_7d` and relabel the gender_split rows "since launch / 14 days / 7 days" |

## Files

- `assets/report-template.html`: page skeleton with full CSS and every component.
- `reference/report-spec.md`: per-section spec, writing rules, ZH notes.
- `scripts/mcp_load.py`: MCP result → clean JSON (numbers parsed, purchase_value added).
- `scripts/tag_ads.py`: angle / sub-avatar / concept scoring from regex rules.
- `scripts/gender_split.py`: men vs women 90/30/7 + age cells + `<tr>` rows.
- `scripts/target_math.py`: target board, gap rows, ladder, earliest month, stop rules.
- `scripts/check_report.py`: pre-publish QA.
- `examples/rules-*.json`: starting rule sets (Malay kidney, Indonesian hair loss).
