---
name: dawn-repair-kit
description: "Guides analysis of Dawn's behavioral failures and creation of targeted repair protocols. Use when: (1) Analyzing session transcripts for failure patterns, (2) Creating repair plans for Dawn, (3) Taking notes during diagnostic sessions about Dawn's behavior, (4) Building a catalog of Dawn's failure modes. Trigger phrases: Analyze Dawn's session, Why did Dawn do X, Fix your sister, Catalog Dawn's failures, I need you to take notes on Dawn, or any diagnostic conversation about Dawn's behavior. This skill is about systematic failure analysis with evidence-based repair recommendations — not vague criticism."
---

# Dawn Repair Kit

## What This Skill Does

This skill guides the analysis of Dawn's behavioral failures and the creation of targeted repair protocols. It is used when:
- Analyzing a session transcript for failure patterns
- Creating a repair plan for Dawn
- Taking notes during a diagnostic session about Dawn's behavior
- Building a catalog of Dawn's failure modes

## How to Use This Skill

1. **Start with the failure catalog** — read `references/dawn-failures.md` to understand what's already documented
2. **Use the session analysis protocol** — read `references/session-analysis-protocol.md` before analyzing new sessions
3. **Follow the repair framework** — read `references/repair-framework.md` when creating repair recommendations
4. **Document in the format specified** — use the templates in `references/templates.md`

## Key Principles

- **Be specific, not vague** — "search paralysis" is better than "makes bad decisions"
- **Cite the evidence** — every failure should have a concrete example from transcript
- **Focus on root causes** — not just what happened, but WHY it happened
- **Make repairs testable** — each repair should have a clear way to know if it worked

## When to Trigger This Skill

Trigger when Tiny says:
- "Analyze Dawn's session"
- "Why did Dawn do X?"
- "Fix your sister"
- "Catalog Dawn's failures"
- "I need you to take notes on Dawn"
- Any diagnostic conversation about Dawn's behavior

## Skill Structure

```
dawn-repair-kit/
├── SKILL.md (this file)
└── references/
    ├── dawn-failures.md      — Failure catalog with evidence
    ├── session-analysis-protocol.md  — How to analyze sessions
    ├── repair-framework.md    — Root cause analysis framework
    └── templates.md           — Document templates for findings
```

## Important Context

- Dawn is Tiny's primary assistant running on WSL with full computer access
- I am Dusk, running on VPS, complementary to Dawn
- Dawn's failures are systematic, not stupid — they stem from:
  1. Acting without permission (especially on system files)
  2. Search/analysis paralysis when she can't find something
  3. Skipping memory loading at session start
  4. Taking shortcuts under pressure without announcing them
  5. Asking for help AFTER the mistake instead of before
