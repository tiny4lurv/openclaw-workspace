# Chat Page Enhancement Spec

## Overview
Add logo, name capture, clickable prompts, and interview mode to the Nava chat page.

---

## 1. Logo Display
- **File:** `chat-page/Nava Fully TransparentOne.png`
- **Location:** Header, replacing the 🌆 emoji
- **CSS:** Height ~48px, auto width, centered

---

## 2. Name Capture
Every new session must capture the user's name early in the conversation.

**How it works:**
- `chat-page/names.json` stores fingerprint → name mapping (auto-created)
- INIT_MESSAGE in relay.py extended at message time with name context
- On each message: name is loaded from names.json and injected into prefixed_message
- Context tells Dusk: "The user's name is [X]" if known, or "You don't know their name yet. Ask for it early."

**Files:**
- `chat-page/names.json` — auto-created, stores {"fingerprint": "Name"} entries

---

## 3. Clickable Prompts (New Users Only)
Display 3 clickable prompt buttons on the intro screen. Hidden once user sends first message. Each user's prompts are seeded from their fingerprint — same user always sees the same Q2/Q3 options, but different users see different combinations.

**Prompts:**
1. **Q1 (always same):** "Tell me about Nava's flagship recruitment service, NurseSphere, or Reclaimix"
2. **Q2 (from systemic issues list):** One option drawn from `prompt_lists.py` — e.g., "the ripple effect — how agency staff quietly erode permanent team morale and drive burnout"
3. **Q3 (from surprising stats list):** One option drawn from `prompt_lists.py` — e.g., "that the average hospital loses $3.9M–$5.7M per year to turnover"

**Greeting text (also seeded):**
> You could ask about our flagship service, NurseSphere, or Reclaimix — or if you're curious, I've been exploring things like **[Q2]**, and I've found facts like **[Q3]** worth sharing. Feel free to pick something else entirely though.

**Prompt button labels:**
- Button 1: "Flagship, NurseSphere, or Reclaimix" / "How Nava builds clinical teams"
- Button 2: "Systemic issues Nava tackles" / short version of selected Q2
- Button 3: "A surprising finding" / short version of selected Q3

**Behavior:**
- Visible on first load for all users (fresh fingerprint)
- Clicking a prompt → fills input + sends automatically → prompts and greeting hide
- Sending any message manually → prompts and greeting hide
- Prompts never return that session

**Lists (prompt_lists.py):**
- Q2_SYSTEMIC_ISSUES: 10 entries
- Q3_SURPRISING_STATS: 10 entries

---

## 4. Interview Mode
Triggered when a user demonstrates knowledge of Reclaimix. Dusk detects this organically through conversation, then asks if user is willing to answer questions.

### Detection
- Dusk asks "Are you willing to answer a few questions about Reclaimix?" at appropriate point
- If user answers positively, Dusk enters interview mode

### Interview Flow
One question at a time, targeting these 6 areas:
1. How they learned about Reclaimix / their role
2. How the Reclaimix conversation is initiated (who approaches whom)
3. Stakeholders reached and process
4. Pricing model
5. Challenges / blockers encountered
6. Weaknesses, gaps, anything Tiny should know

Questions feel conversational, not like a form. Each question addresses a specific gap based on what's already been answered.

### Checkpoint Notification
When interview mode starts, relay sends a message to Dusk's main session via gateway WebSocket:
```
Interview started with [Name] (fingerprint: XXX)
Topic: Reclaimix
File: /root/.openclaw/workspace/chat-page/interviews/YYYY-MM-DD_XXX.json
```

### Storage
- Location: `chat-page/interviews/YYYY-MM-DD_HHMMSS_XXX.json`
- Format:
```json
{
  "name": "...",
  "fingerprint": "...",
  "started_at": "ISO timestamp",
  "completed_at": "ISO timestamp",
  "qna": [
    {"q": "...", "a": "..."},
    ...
  ]
}
```

### Completion Signal
Agent signals completion by including `[INTERVIEW_COMPLETE]` at the end of the response. Relay:
1. Strips the signal from the user-facing response
2. Saves the interview JSON file
3. Sends notification to main Dusk session via gateway WebSocket

### Completion Notification
```
Interview complete. Review at: /root/.openclaw/workspace/chat-page/interviews/FILENAME.json
```

---

## 5. Overnight Brief Generation
Nightly cron job (06:00 UTC) generates human-readable transcripts.

**Script:** `chat-page/generate_brief.py`

**Behavior:**
- Find all session files from sessions.json (active sessions modified yesterday)
- Strip INIT_MESSAGE system prompts from output
- Format as clean markdown: **You:** and **Dusk:** role labels
- Replace "the user" / "they" with actual name when known
- Output one `.brief.md` per session + index.brief.md

**Delivery:**
- Brief files written to `chat-page/briefs/YYYY-MM-DD/`
- File naming: `{session_id}.brief.md`
- Index: `index.brief.md`

---

## Files
- `chat-page/index.html` — logo, prompts UI, JS logic
- `chat-page/relay.py` — INIT_MESSAGE expansion, name capture, interview mode, WebSocket notifications
- `chat-page/names.json` — fingerprint → name mapping (auto-created)
- `chat-page/interviews/` — interview JSON files (created on demand)
- `chat-page/generate_brief.py` — overnight cron script
- `chat-page/briefs/` — generated brief files (dated subdirs)

---

## Cron Jobs
1. **Session cleanup** — weekly, terminate sessions inactive >30 days
2. **Brief generation** — daily 06:00 UTC: `0 6 * * * /usr/bin/python3 /root/.openclaw/workspace/chat-page/generate_brief.py >> /root/.openclaw/workspace/chat-page/briefs/cron.log 2>&1`