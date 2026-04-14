# Session Analysis Protocol

## When to Use This Protocol

When asked to analyze Dawn's behavior from a session transcript.

---

## Step 1: Locate the Session File

Session files are stored at:
```
/home/tiny4lurv/.openclaw/agents/main/sessions/
```

To find the right session:
```bash
ls -lt /home/tiny4lurv/.openclaw/agents/main/sessions/ | head -20
```

Sessions are organized by date. If Tiny says "that was on Sunday", check Sunday's session file directly.

---

## Step 2: Read the Session

Read the session file with `read` tool. If the file is too large (>50KB), use:
```bash
sed -n '<start>p' /path/to/session.md | head -c 50000
```

Read in chunks of ~400 lines, taking notes as you go.

---

## Step 3: Catalog Failures

For each failure, record:

1. **What happened** — concrete description, not vague
2. **Evidence** — exact quote or action from transcript
3. **When it happened** — timestamp or line number
4. **What it cost** — time wasted, work derailed, etc.
5. **Root cause** — why it happened, not just what happened

Use the template in `templates.md`.

---

## Step 4: Look for Patterns

After cataloging individual failures, ask:
- Do they share a common trigger?
- Do they share a common root cause?
- Is there a pattern around context switches (morning → afternoon, new topic, etc.)?

---

## Step 5: Write Repair Recommendations

Each failure should have:
- **Specific** — not "be more careful"
- **Actionable** — something Dawn can actually DO differently
- **Testable** — a way to know if the repair worked

---

## Red Flags to Watch For

- Dawn editing SOUL.md, MEMORY.md, or any system file
- Dawn running Python scripts to search instead of reading session files
- Dawn asking about things that should be in memory
- Dawn saying she's "done" when she hasn't actually written anything
- Dawn taking shortcuts without naming them

---

## Note-Taking Conventions

When taking notes during analysis:
- Use `——` for emphasis or separation
- Quote directly with exact quotes from Tiny when possible
- Include timestamps for significant events
- Mark items as `[UNVERIFIED]` if not directly observed
- Mark items as `[HIGH PRIORITY]` if they caused significant time loss
