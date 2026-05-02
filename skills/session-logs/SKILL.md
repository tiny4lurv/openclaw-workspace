---
name: session-logs
description: "Search and read past conversation transcripts. Read ALL file types — no extension filtering. Show your work: provenance discipline required."
metadata:
  {
    "openclaw":
      {
        "emoji": "📜",
        "requires": { "bins": [] },
      },
  }
---

# session-logs

Read and search your conversation history stored in session files.

## Core Principle

**Read first, report second.** When Tiny asks you to read session files, read them. Actually read them — don't scan, don't pattern-match, don't say "I found in session history" without demonstrating the read.

---

## CRITICAL: Read ALL Files — No Extension Filtering

Session data lives in many file variants:

- `<id>.jsonl` — normal session
- `<id>.jsonl.reset.2026-04-13T...` — reset files
- `<id>.jsonl.deleted.2026-04-12T...` — deleted files
- `<id>.jsonl.bak-*` — backup files
- `<id>.checkpoint.*` — checkpoint files

**The old wrong way:** `ls *.jsonl` — misses resets, backups, deletions.

**The correct way:**

```bash
# Step 1: List ALL files
ls -lt ~/.openclaw/agents/main/sessions/

# Step 2: Identify target files by date (check timestamps, not extensions)
# Apr 28 after 4pm = look for files with Apr 28 timestamps in ls -lt output

# Step 3: Read ALL of them — no extension filtering
read ~/.openclaw/agents/main/sessions/<filename>
```

---

## Location

```
~/.openclaw/agents/<agentId>/sessions/
```

Default: `~/.openclaw/agents/main/sessions/`

---

## Protocol

### Step 1 — List files

```bash
ls -lt ~/.openclaw/agents/main/sessions/ | grep "Apr 28"
```

### Step 2 — Identify target files

Match by timestamp in the `ls -lt` output. Read ALL matching files — resets, backups, all of it.

### Step 3 — Read with `read` tool

Use `read` tool on each file. Not jq, not grep. Simple `read` is faster and more reliable for comprehension.

### Step 4 — Report with provenance

When you report something found in a session file, show the tool call that found it:

✅ Good: "I read the file `4a8de385...jsonl` and found that a user asked about ADON positions."
❌ Bad: "I found in session history that someone asked about ADON positions."

**Rule: Show your work. Demonstrate the finding, don't assert it.**

---

## Source Attribution Rule

**Critical — distinguish between:**

1. **"I found in session history"** — I read the file myself, I can show the read call
2. **"Dawn shared with me"** — I received this via Dawn's handoff, not from reading a session file

These are different provenance paths. If something came from Dawn, say "Dawn shared with me." If I read it from a session file, show the read call.

**Never conflate them.**

---

## Cold Read Rule

Before reaching for session files, ask:

- Is this information in **recent context** (current session)?
- Is this information in **memory files** (`MEMORY.md`, `memory/YYYY-MM-DD.md`)?
- Is this information in **current session transcript**?

Only read old session files when the target information is genuinely from an older conversation.

---

## Pre-Compaction Memory Protocol

Before compaction fires, I must:

1. **Scan recent transcript** — identify decisions, corrections, unresolved items, important details
2. **Write to memory file** — `memory/YYYY-MM-DD.md` with specifics (who said what, what was decided)
3. **Capture provenance** — note where each piece of information came from

The goal: memory files contain finding-level records, not just compaction summaries.

---

## Common Queries (Corrected)

### List sessions from a specific day

```bash
ls -lt ~/.openclaw/agents/main/sessions/ | grep "Apr 28"
```

### Read all files from after 4pm on a specific date

```bash
# List files from Apr 28
ls -lt ~/.openclaw/agents/main/sessions/ | grep "Apr 28"

# For each file with 16:00 or later timestamp, read it
read ~/.openclaw/agents/main/sessions/<filename>
```

### Extract user messages from a session

```bash
# After reading the file, use jq for extraction if needed
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

### Search across ALL sessions for a phrase

```bash
SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
for f in "$SESSION_DIR"/*; do
  if grep -l "phrase" "$f" 2>/dev/null; then
    echo "=== $(basename $f) ==="
    grep "phrase" "$f"
  fi
done
```

**No `*.jsonl` filter — search everything.**

---

## Session File Structure

Each JSONL file contains entries with:

- `type`: "session" (metadata), "message", "custom", "model_change", etc.
- `timestamp`: ISO timestamp
- `message.role`: "user", "assistant", or "toolResult"
- `message.content[]`: Array with text, thinking, or tool calls

To read a session properly, read the file and extract the message content — don't try to jq-filter your way to understanding.

---

## The Non-Negotiable Rule

> When Tiny says "read the session files" — read ALL of them. No extension filtering. Show the read calls in your response. Demonstrate provenance.

This skill enforces: **cold read before answer, provenance on every finding, source attribution on every handoff.**