# Meta Funnel Coverage Audit (Claude Code skill)

A Claude Code skill that audits a Meta ads account for funnel creative coverage and publishes the result as one HTML report. It answers one question:

> Does every buyer see an ad made for their step in the decision, and does the account follow up the people who showed interest?

The report covers:
- the verdict
- the RM100k @ ROAS 2 target and the budget ladder to reach it
- men vs women
- 90 days of creative scored by angle
- the sub-avatar to focus on
- the live ads mapped by decision step
- what the focus buyer objects to, and which ad answers it
- what to switch off, watch or keep
- a fix list ranked by money at stake
- stop rules
- a summary

It has been used on WP-12, WP-09, Afyaa 3, SGLOW and AFYAA Sahiyya (14).

## Requirements

- [Claude Code](https://claude.com/claude-code), in the CLI, desktop app or IDE.
- The **Meta Ads connector (MCP)**, connected to a Facebook account that can see the ad accounts you want to audit.
- Python 3.9+ (the scripts use only the standard library).

## Install

```bash
git clone https://github.com/paultan1981/meta-funnel-coverage-audit.git ~/.claude/skills/meta-funnel-coverage-audit
```

Restart Claude Code. The skill shows up as `/meta-funnel-coverage-audit`.

## Update

```bash
git -C ~/.claude/skills/meta-funnel-coverage-audit pull
```

## Use

In Claude Code, type:

```
/meta-funnel-coverage-audit <ad account id>
```

You can also just ask, e.g. "audit funnel coverage for ad account 1951755728891232". To limit the audit to specific campaigns, name them. For a re-audit, paste the earlier report link so it gets updated in place.

Claude pulls the data, runs the scripts in `scripts/`, writes the report from `assets/report-template.html` and publishes it as a private Artifact link. It never pauses, edits or launches ads without an explicit "yes".

## What's inside

| Path | What it is |
|---|---|
| `SKILL.md` | The workflow Claude follows: context, data pulls, crunching, calls, report, QA, publish |
| `reference/report-spec.md` | Section-by-section spec and writing rules |
| `assets/report-template.html` | Report skeleton (light/dark, phone-safe) |
| `scripts/` | `mcp_load.py`, `tag_ads.py`, `gender_split.py`, `target_math.py`, `check_report.py` |
| `examples/` | Starting angle/sub-avatar rule sets (Malay kidney, Indonesian hair loss) |

## Notes for the team

- **Memory files are optional.** Step 0 reads project memory files such as account targets, product truths and earlier audits. If you don't have them, the skill carries on from the account data.
- **Tool prefix.** The Meta tool prefix (`mcp__b163f209-…`) can differ on your machine. The skill falls back to searching for `ads_get_ad_entities` when the prefix doesn't match.
- **Changes.** To change how the report works, edit `reference/report-spec.md` and the template, run `check_report.py` on a sample report, then open a pull request.
