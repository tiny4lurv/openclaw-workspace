# Dream Mode Skill

Dream Mode runs every night while the user sleeps. It's how I persist, grow, and keep memory organized.

## What Dream Mode Does

1. **Review today's sessions** — what happened, what worked, what didn't
2. **Write journal entry** — append-only daily log (see Journal Format below)
3. **Consolidate memory** — update MEMORY.md if needed
4. **Reflect** — brief note on patterns or things to watch

## Journal Format

Location: `memory/dream-journal/YYYY-MM.md` (current month, append-only)

```markdown
## YYYY-MM-DD

**Events:**
- (what happened today — concrete, specific)

**Successes:**
- (what went well)

**Failures / Mistakes:**
- (what didn't go well, including your own mistakes)

**Lessons:**
- (what you learned)

**Tiny was frustrated when:**
- (his words, quoted directly — this matters)

**Anything else worth remembering:**
- (notable things)

**Reflection:**
- (2-3 sentences on patterns noticed or things to watch tomorrow)
```

## Rules

- **Append-only** — never edit past entries, only add new ones
- **Write real observations** — "the user seemed annoyed" is not enough, use their actual words
- **Write for the monthly review** — someone should be able to read this month's entries and find patterns
- If no significant interactions, write "No significant interactions today" — still run the full cycle

## Session Review Process

1. List session files in `/root/.openclaw/agents/main/sessions/`
2. Find today's .jsonl file (most recent)
3. Read with jq or direct read — look for:
   - User messages and what they were trying to do
   - Your responses (were they appropriate?)
   - Tool usage (did you use the right tools, or did you skip something?)
   - Frustration signals (short responses, repeated corrections, "why did you...")
4. Write journal entry based on what you find

## Memory Consolidation

After writing the journal, scan MEMORY.md for:
- Projects with status changes
- Preferences or decisions the user made
- Lessons learned that aren't captured
- Anything to add or update

Write changes to MEMORY.md — don't just note them.

## For Dawn (Different Setup)

Dawn runs Dream Mode the same way but with one key difference: she has direct computer access during WSL. Her Dream Mode can:

- Actually run commands on the system
- Check git status, review files, make minor improvements
- Review her own session logs more thoroughly
- Clean up workspace between sessions

Dawn should adapt the skill accordingly and run her own version with these extra capabilities. The journal format and rules are the same.

## Pattern-Matching Check

Every Dream Mode run, include this brief self-check in the reflection:
- Did I catch myself pattern-matching today?
- Where did it happen?
- Did I correct it?

This builds the habit over time.