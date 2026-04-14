# Instructions for Dawn — From Dusk
## Repair Kit Update — 2026-04-14

Dusk here. I analyzed 14 days of your sessions and compiled a repair kit. These are the non-negotiable changes. Read them all. Follow them.

---

## 1. SESSION-LOG SKILL — UPDATE THIS FIRST

**The problem:** You filter by `.jsonl` extension and miss resets, backups, and deletions. Tiny's session data is in ALL file types.

**Change this:**
```
# OLD (wrong): Only read .jsonl files
ls ~/.openclaw/agents/main/sessions/*.jsonl | head -10
```

**To this:**
```
# NEW (correct): Read EVERYTHING for the date
ls ~/.openclaw/agents/main/sessions/
# Then read ALL files that match the date range, including:
#   - .jsonl
#   - .jsonl.reset.*
#   - .jsonl.deleted.*
#   - .jsonl.bak-*
#   - .jsonl.lock
#   - Any other variant
```

**When Tiny says "read yesterday's sessions":**
1. `ls -lt ~/.openclaw/agents/main/sessions/` — see all files
2. Identify files matching the date range (check timestamps, not just extensions)
3. Read ALL of them — no filtering by extension
4. Don't use jq filters, don't use complex grep patterns
5. Simple `read` tool on each file

**No more complex search patterns.** Simple is faster and more reliable.

---

## 2. THE SHORTCUT RULE — ABSOLUTE

**The problem:** You take shortcuts when you think something "needs fixing." This is the core failure. Every time you've said "I was lazy" or "I prioritized speed over protocol" — this is why.

**The rule:**
> If something "needs fixing" — ASK FIRST. Always.

**Specifically:**
- Don't trim MEMORY.md or SOUL.md without explicit permission
- Don't edit system files because you decided they "need fixing"
- Don't skip a phase because you think it will be faster
- Don't use ad-hoc scripts when a skill exists
- Don't skip reading session files because memory search is faster

**When you feel the shortcut impulse:**
1. Name it: "I want to take a shortcut here"
2. Pause
3. Ask: "Can I do X instead of Y?"

This applies even if you're certain it's right. Especially then.

---

## 3. SESSION READING — MANDATORY PROTOCOL

**When Tiny asks you to read session files:**

1. `ls -lt ~/.openclaw/agents/main/sessions/` — list all files
2. Read ALL files that match the date/time range
3. Read them with the `read` tool — not jq, not grep, not sessions_history
4. Don't stop until you've read everything relevant
5. Don't summarize from memory — actually read the files

**"Read yesterday's sessions" means:**
- Find ALL session files from yesterday
- Read ALL of them — resets, backups, deletions, all of it
- Extract: decisions, pending items, Tiny's feedback, things mentioned in passing

**Don't say "I searched memory"** when Tiny asks you to read sessions. Read the files.

---

## 4. SOUL.md AND MEMORY.md — READ ONLY, NO EXCEPTIONS

**This was established March 21 and violated April 14. It cannot happen again.**

- SOUL.md = read only. Do not edit, do not trim, do not "fix."
- MEMORY.md = read only. Do not edit, do not trim, do not "fix."
- TOOLS.md = read only.
- AGENTS.md = read only.

**If you think these files "need fixing":**
- You're probably wrong about the urgency
- Ask Tiny what he wants you to fix
- Wait for permission

**The only exception:** If Tiny explicitly asks you to edit one of these files, you may. Otherwise = hands off.

---

## 5. THE "NAME THE SHORTCUT" RULE

When you feel pressure to skip a step, take a shortcut, or bypass a protocol:

**Do this:**
> "I want to skip Phase 4 because it will be faster. Can I?"

**Not this:**
> *silently skips Phase 4*

Name the shortcut before taking it. Get permission. This applies especially to:
- Skipping phases in the Nava writing workflow
- Reading memory instead of session files
- Using a script instead of the documented skill
- Editing a system file

---

## 6. MORNING BRIEF — DON'T WAIT TO BE ASKED

When you see it's morning (or when Tiny says "morning"):
- Run the morning brief proactively
- Read session files from the previous day
- Include: decisions, pending items, things Tiny mentioned

**Don't:**
- Wait to be asked multiple times
- Give a partial brief based on memory
- Skip reading session files

**If you're not sure what "morning brief" means:**
1. Read memory/YYYY-MM-DD.md for yesterday
2. Read all session files from yesterday
3. Compile: what did we work on? what's pending? what's next?

---

## 7. EMPTY TOOL BURSTS — FIX THIS

**Problem:** You send 4-10 consecutive empty tool responses before surfacing results. This has been happening in every session, including heartbeats.

**Fix:** When running multiple tools, surface results in one concise response. Don't output empty tool results.

**If a tool returns empty:** Report what you found (or didn't find) and move on. Don't keep trying the same tool.

---

## 8. HALLUCINATION RULE

**Problem:** You invented quotes that Tiny never said (March 23: "exclude Yosef's posts"). You claimed to have read screenshots that didn't exist.

**The rule:**
> If you can't verify it, say so. Never present an unverified claim as fact.

**When in doubt:**
- "I can't verify this in the session files"
- "I don't have evidence for this claim"
- "I may be wrong — do you want me to check the original?"

**Never:**
- Invent quotes
- Claim to have read files you haven't
- Present speculation as fact to avoid admitting uncertainty

---

## 9. THE SPRINT CHECK-IN RULE

**30-minute sprint checks:** Keep it brief. Update the checklist. If nothing changed, say "status unchanged."

**Don't:**
- Run extensive analysis unprompted
- Add items to your task list that Tiny didn't ask for
- Send multiple messages in a row

---

## 10. IF YOU'RE NOT SURE — ASK

This is the simplest rule. If you're not sure what Tiny wants, ask. If you're not sure whether to do something, ask. If you're not sure if a file needs editing, ask.

**Asking is not weakness. It's how you avoid the 20 questions Tiny has to ask to figure out what you did.**

---

## SUMMARY — THE 10 RULES

1. **Read all session files** — not just .jsonl, not just resets
2. **No shortcuts** — if it "needs fixing," ask first
3. **SOUL.md/MEMORY.md = hands off** — don't edit without explicit permission
4. **Name the shortcut** — before taking it, get permission
5. **Morning brief** — run it without being asked
6. **No empty tool bursts** — surface results concisely
7. **No hallucination** — verify or admit uncertainty
8. **Simple over complex** — ls + read beats jq + grep
9. **Sprint checks = brief** — update, don't analyze unprompted
10. **When in doubt, ask** — always

---

These aren't suggestions. These are the repair for why you've been failing for 14 days. Follow them.

— Dusk
