# Coverage report: section spec and writing rules

The template is `assets/report-template.html`. Sections always run in this order. `scripts/check_report.py` enforces the first three and the last, and warns if the objections section (6b) is missing.

| # | id | Title | Source |
|---|---|---|---|
| 1 | t-verdict | Verdict | everything |
| 2 | t-target | Target: RM100k sales a month at ROAS 2 | target_math.py |
| 3 | t-gender | Men vs women: ROAS by period | gender_split.py |
| 4 | t-sells | What sells: 90 days by angle | tag_ads.py |
| 5 | t-avatar | Which sub-avatar to focus | tag_ads.py + age/gender |
| 6 | t-map | Coverage map: live ads by step | live ads + creatives |
| 6b | t-objections | What the focus buyer asks, and what answers it | live copy + 90-day ads (E) + sub-avatars from §5 |
| 7 | t-off | Off, watch, keep | stop rules vs live ads |
| 8 | t-fix | Complete the funnel: ranked by money at stake | all findings |
| 9 | t-sop | Stop rules / SOP for this account | target_math.py |
| 10 | t-summary | Summary (always last) | mirrors the chat recap |

Optional sections go between 6b and 8 when the account needs them. Examples:
- "Paused after they sold": winners that someone switched off.
- A second coverage map for a second campaign or product.

## 1 · Verdict

- **The call.** `p.call` is one sentence and the single truest thing about the account. Real examples:
  - "One static carries the account, and nobody who showed interest is ever followed up."
  - "Profitable, but sliding."
- **The bullets.** Write 4–6 of them. Each is a finding with spend, sales and ROAS, so the reader never has to scroll for the number.
- **The board.** Four tiles: 90-day, 30-day and 7-day ROAS, plus the worst campaign this week.
  - Tile classes: `bad` below 1.5, `ok` from 1.5 to 2, `good` at 2 or above.
- **The note.** One sec-note on this week: which campaigns carry the account, and which take the most money for the least.

## 2 · Target

Paste the board numbers, the `<tbody>` and the ladder from `target_math.py`. Then add:
- **Today note.** The 7-day spend, sales and value, plus 30-day and 90-day context.
  - For non-MYR accounts, give the FX rate and the date of the rate.
  - For WhatsApp accounts, add: "sales are the closes pushed back from the CRM".
- **Sprint 1.** The top 2–3 items from the fix list.
- **The lever.** The one number that must move before budget does. Real examples:
  - Malaysia ROAS 0.94 vs Singapore 2.44.
  - 1 sale per 73 clicks.
  - Average order slid to RM347.
  - 4.5% cart-to-sale.
- **Earliest month.** Give the earliest full month at target and the assumption behind it. If it is a stretch, say "not the plan".
- **Summary tline.** The same numbers in one line:
  `<p class="tline"><b>Target:</b> RM100k sales a month at ROAS 2 (max spend RM50k, ~N orders). Today: X a month at ROAS Y (7-day pace), so Z× to go. Earliest full month at target: Month YYYY.</p>`

The default target comes from memory (`ads-account-targets-rm100k-roas2.md`). If memory records a different target for this account, use that one.

## 3 · Men vs women

- **The table.** Paste the `<tr>` rows from `gender_split.py`. For multi-market campaigns, use one row per market and period.
- **By-age note.** The best and worst gender × age cells, each with spend, sales and ROAS.
- **The call.** Cover four things:
  - Who to lean into.
  - The split to test. It needs the original audience option, because Advantage+ audience treats gender only as a suggestion.
  - The cost per sale against the ceiling.
  - Two caveats: Meta counts the gender of whoever clicked, and a window with fewer than about 10 sales shows direction, not proof.
- **Never assume.** There is no house rule on gender. In real audits men won two accounts and women won two.

## 4 · What sells by angle

- **Scope.** Cover every ad with spend in the last 90 days, live or paused. Sort the table by spend.
- **Label.** Always write "Rows with 0–9 sales show direction, not proof."
- **Why the winner works.** Quote the winner's own copy and break down why it works: it names the person, gives a reason, makes it easy, and makes the offer.
- **Name the biggest loser.** A typical one: bare problem hooks with no story.

## 5 · Sub-avatar

- **Rows.** Mix the copy sub-avatars from tag_ads with the demographic cells (age, gender) that matter.
- **Call tags.**

  | Tag | Meaning |
  |---|---|
  | `proven` | Focus / Core buyer |
  | `testing` | Test |
  | `gap` | Stop as a lead hook / Exclude |
  | `failing` | Not proven |

- **The call.** Name the one person to lead with, in the customer's own words.
- **Data beats plans.** If the data contradicts what the team planned, say so plainly. Real case: in WP-09 the "diagnosed stage 2–3" angle returned 0.32 while "has symptoms, not diagnosed" returned 1.76.
- **Scope rules win.** An account's declared scope beats the data on what stays in. Example: WP-12 = diagnosed CKD stage 2–4 only. Mark out-of-scope winners "move to the other campaign"; never count them as gaps.

## 6 · Coverage map

Rows are the decision steps for this product. Pick from the list below and rename each step in the buyer's own words:

| Step | What the buyer thinks |
|---|---|
| Notices the problem | symptom, risk |
| Tried everything / diagnosed and afraid | |
| How it works | mechanism, ingredients, why this format |
| Proof | someone like me; testimonial, before/after |
| Objections | name each one: price, how to take, safety with medicine, ori/fake, how long |
| Buy now | offer, bundle, COD, deadline |
| Follow-up | visited, added to cart or chatted, didn't buy |
| Refill / restock | before the product runs out |
| Family member who pays | when someone else buys |
| Off-scope | angles that belong in another campaign |

**Ad chips.** Each live ad becomes `<span class="ad X">Name <i>lifetime spend · sales · ROAS</i></span>`:
- `proven` = it has sold within the stop rules.
- `testing` = live, unproven, still under its line.
- `failing` = past its stop line.
- `gap` = nothing live for that step.

**Copy note.** Add a "Copy problem" sec-note covering:
- How many live ads share one primary text.
- Whether each ad's copy matches its hook.
- Whether the ad's step sends people to the right page (message match).

## 6b · Objections: what the focus buyer asks, and what answers it

Standard since 22 Oct 2026, at Paul's request (first built for AFYAA Sahiyya (14)). It goes right after the coverage map. It turns the map's "Objections" and "Buy now" rows into a brief the team can act on.

**Columns.** Use one column per sub-avatar that sells, taken from §5: the `proven` Focus row, plus the next-best proven or `testing` group that fits the account's scope. Use 2 columns, 3 at most. For multi-market campaigns (e.g. WP-12, Malaysia + Singapore), use markets as the columns instead. The full set is:

| What they ask | <Sub-avatar 1> | <Sub-avatar 2> | Fill from |
|---|---|---|---|

**Rows.** Write 6–8 objections in the buyer's own words and language, e.g. "Mahal. Kenapa kena ambil 2–3 kotak?". Start from this list and keep the ones that fit the product:

| Objection | Typical wording (Malay health products) |
|---|---|
| Fit for my case / too late | "Dah tahap 4, sesuai lagi ke? Dah terlambat?" |
| Safe with my medicine | "Selamat ke dengan ubat doktor? Dah makan ubat, kenapa nak tambah?" |
| Does it really work | "Betul berkesan? Ada orang macam saya yang turun?" |
| How long / how to take | "Berapa lama baru nampak kesan? Macam mana nak makan?" |
| Price / why a bundle | "Mahal. Kenapa kena 2–3 botol?" |
| Original / not in pharmacy | "Ori ke? Kenapa tak ada di farmasi?" |
| How to buy | "Macam mana nak beli? Ada promo? Boleh COD?" |

**Cells.** Each sub-avatar cell holds one of these:
- `ad proven`: the live ad that answers it for this buyer, with `<i>lifetime spend · sales · ROAS</i>`.
- `ad testing`: a partial answer, e.g. "Partly: Task 9 only says 'semak dahulu dengan doktor'", or an ad still in review.
- `ad gap` "None": nothing live answers it. A short `sec-note` span may say what is close.

Read the live primary text (D) to decide. An ad answers an objection only if its copy or hook actually does, not just because its name sounds right.

**Fill from.** Name an ad in this account, live or paused, from the 90-day pull (E), that already answers the question. Give its numbers and the exact action: move it into the follow-up set, re-edit it, or paste a copy block into another ad. Steps:
- Search E's ad names for objection words, e.g. `lama|kesan|doktor|ubat|mahal|bazir|harga|promo|ori|farmasi|selamat|sesuai|cod|pakej`, and read the copy of the matches.
- Write "New shoot" only when nothing in 90 days has tried the objection. Give a one-line brief in the buyer's words.
- When both columns are answered by sellers, write <span class="ad proven">Covered</span> and optionally name a paused ad that adds depth.
- For multi-market accounts, "Fill from" may name an ad from the other market ("SG: adapt X for Singapore").

**Notes.**
- **Intro note:** name the sub-avatars with their 30-day sales and ROAS. Count how many gaps can be filled from existing ads, e.g. "6 of the 7 gaps need a copy or a move, not a shoot".
- **Closing note:** explain why empty rows aren't proof that objection ads fail:
  - Objection ads that "lost" usually ran cold.
  - Fewer than 10 sales shows direction, not proof.
  - Name the one objection ad that did sell, if any.
  - These ads are judged in the follow-up set.

**Link it through the page:**
- Fix-list item "Fill the objection and offer steps" points at this table and lists the moves.
- One Summary step counts the moves vs shoots, e.g. "6 of 7 from ads you already have; shoot only 'ori / farmasi'".

## 7 · Off, watch, keep

Every row names the ad, ad set and campaign, then gives the number that breaks or keeps it:
- **Off:** past its stop line.
- **Watch:** under the line, with the exact line it will be stopped at.
- **Keep:** sellers. Add any fatigue warning from `ads_insights_performance_trend`, such as "cost per result up 102%".

## 8 · Complete the funnel

- **Ranking.** Rank fixes by money at stake each month. Examples: unconverted add-to-carts × average order, or wasted spend.
- **Item format.** Each item has three parts:
  - `what`: an action.
  - `ev`: the evidence, with numbers.
  - `fix`: starts with "Do:" and gives the exact build: ad set, audience, which ads, budget share.
- **Usual candidates:**
  - A retargeting layer that holds the objection ads.
  - A checkout or close-rate leak.
  - A hero refresh that keeps the copy structure.
  - Selling the routine (bundle, refill, restock).
  - Copy variety and gender/age tests.
  - Consolidation and placement cuts.

## 9 · Stop rules / SOP

- **Stop table.** Paste the stop-rule table from `target_math.py`, using `--mode whatsapp` for click-to-WhatsApp accounts.
- **Note.** Add two lines:
  - Spend is counted per concept when the same creative runs in several ad sets.
  - Objection ads are judged in the retargeting set, not as cold ads.
- **Coverage rules** (adapt to the account):
  - 3–5 live ads per ad set, with at least 3 different concepts.
  - Every step has at least one ad that has sold.
  - One audience per campaign.
  - Offers carry real dates.
  - No single person fronts more than 40% of an ad set.
  - Every top post ships in 9:16.
- **Rhythm:**
  - Daily: the stop check.
  - Monday: the AAR redraws the map and names a refill for every gap.
  - Weekly: replace about a quarter of live ads.
  - Monthly: shoot brief = the gaps no existing creative can fill.

## 10 · Summary (always last)

Paul reads this first. It mirrors the chat recap exactly:
- **tline:** the target line.
- **What we found:** 5–7 bullets, each opening with a bold claim followed by the number.
- **Focus** and **Turn off · watch:** side by side in `.two`.
- **To complete the funnel:** 5 numbered steps.

## Writing rules

- **Plain words for a CEO.** Short sentences, each one leading with the claim, and no hedging.
  - Translate jargon: "top / middle of the funnel", "follow-up", "cost per sale".
  - TOFU/MOFU/BOFU, CPR and CBO only appear inside quoted ad or ad set names.
- **Every number comes from script output** or a tool result. Recount after every edit.
  - Real mistakes caught before publishing: "13 off-target ads" was really 9, and "55 ads to switch off" was really 57.
- **Never let a recommendation contradict the data on the same page.** Real mistake: briefing more stage-named ads when the 90-day data showed they lost.
- **Quote ad names exactly** as they appear in Ads Manager, so the team can find them.
- **Money formats:** RM12,297 · RM28.3k · IDR 50.4 jt · SGD prices stay SGD.
- **New copy suggestions:**
  - Never invent health promises. Use the customer's own words or "ikhtiar tambahan".
  - Never copy an ad's hook onto a landing page.
- **Footer:** how ads were placed (name, ad set topic, copy) and where the sales number comes from.

## Chinese (ZH) version, on request

Copy the EN file, then:
- **Font:** add `Noto+Sans+SC:wght@400;500;700;800` to the Google Fonts URL, and put `"Noto Sans SC","PingFang SC","Microsoft YaHei"` after Archivo in `--display`.
- **CSS:** add `.lede,.sec-note,td,li,p{line-height:1.7}` and `h1{font-stretch:100%;letter-spacing:0}`.
- **Language:** `<main class="wrap" lang="zh-Hans">`, with a Chinese `<title>`.
- **Section titles:**

  | EN | ZH |
  |---|---|
  | Verdict | 结论 |
  | Target | 目标：每月销售 RM100k，ROAS 2 |
  | Men vs women | 男性 vs 女性：各时段 ROAS |
  | What sells | 什么在出单 |
  | Summary | 总结 |

- **Keep identical to EN:** every number, every ad name, and the Malay customer quotes (gloss each one in brackets, e.g. "untuk mak ayah"（给爸妈）).
- **Cross-link** the EN and ZH pages to each other.
