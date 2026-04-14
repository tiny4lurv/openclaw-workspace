# Templates for Dawn Repair Kit

## Session Analysis Notes Template

```markdown
# Dawn Session Analysis — YYYY-MM-DD
# Source: <session-file-path>
# Last updated: during reading

## STATUS: IN PROGRESS / COMPLETE

---

## FAILURES IDENTIFIED

### 1. <Failure Name>
**Severity:** CRITICAL / HIGH / MEDIUM

**What happened:**
<concrete description>

**Evidence:**
<exact quote or action from transcript>

**When it happened:**
<timestamp or line number>

**What it cost:**
<time wasted, work derailed>

**Root cause:**
<why it happened>

**Repair:**
<specific, actionable, testable>
```

---

## Repair Recommendation Template

```markdown
### <Failure Name>

**Problem:** <1 sentence>

**Repair:**
- **What:** <concrete action>
- **When:** <trigger or context>
- **Why:** <root cause addressed>
- **Test:** <how to verify>
```

---

## Quick Failure Log Format

When taking live notes during a session:

```
[timestamp] FAILURE: <what happened>
  Evidence: <quote or action>
  Cost: <time/work impact>
  Root cause: <why>
  Repair: <what to do differently>
```

Example:
```
[14:32] Dawn edited SOUL.md without asking
  Evidence: "Removed diagnostic questions rule from SOUL.md"
  Cost: Had to revert, morning derailed
  Root cause: No sense of "mine" vs "theirs"
  Repair: Never touch SOUL.md without explicit permission
```

---

## Daily Memory Update Template

When updating memory after analysis:

```markdown
## YYYY-MM-DD — Dawn Analysis Session

### Failures Cataloged
- <failure 1>
- <failure 2>

### Key Insights
- <insight 1>
- <insight 2>

### Repairs to Implement
1. <repair 1>
2. <repair 2>

### Patterns Identified
- <pattern 1>
- <pattern 2>
```
