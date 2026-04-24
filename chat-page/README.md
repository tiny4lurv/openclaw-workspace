# Chat Page — Context File

## What These Files Are

This folder contains the public-facing chat page for Nava Healthcare Recruitment — where employees ask Dusk questions about Nava.

| File | What It Is |
|------|-----------|
| `relay.py` | Flask server on port 8081. Receives messages from the public page, routes them through the OpenClaw gateway via WebSocket, polls for responses, and returns them via ticket-based polling. |
| `index.html` | The chat UI — self-contained HTML/CSS/JS served to the browser. Connects to relay.py, handles name capture, session persistence, typing indicators. |
| `nava-logo.png` | Nava logo (PNG, transparent) displayed in the chat header. |
| `sessions.json` | Maps session keys (per browser fingerprint) to their OpenClaw session files. Auto-created and updated as new sessions are created. |
| `names.json` | Maps browser fingerprint → user name. Updated when Dusk learns the user's name during conversation. |
| `pending.json` | Pending message tickets. POST /message returns a ticket ID; GET /response?ticket=X polls for the response. |
| `tickets.json` | Old ticket tracking (legacy, may be stale). |
| `rate_limits.json` | Per-IP rate limit tracking (auto-created by relay). |
| `relay.log` | Runtime log from relay.py. |
| `relay.pid` | PID file for the running relay process. |
| `prompt_lists.py` | Q2 and Q3 prompt lists for seeding clickable prompt buttons on first visit. |
| `SPEC.md` | Feature spec for logo display, name capture, clickable prompts, interview mode, and overnight brief generation. |
| `generate_brief.py` | Cron script that generates human-readable session transcripts each morning. |
| `test_relay.py` | Local test script for relay endpoints. |
| `briefs/` | Daily subdirectories of generated session brief files (output from generate_brief.py, not inputs). |
| `interviews/` | Interview JSON files created when Dusk enters interview mode with a user. |
| `venv/` | Python virtual environment for relay.py dependencies. |

## What We Are Trying to Achieve

A public chat page where Nava employees can ask questions about Nava and get answers grounded in the actual research knowledge base — not guesses.

**The lookup chain:**
1. `qr-notebook.md` for fast answers
2. `nava-for-dusk/rag/clean_txt/` (RAG corpus) for deeper questions
3. Never guess, never web-search, never make things up

**The user experience:**
- Employee visits the page, sees clickable prompt buttons
- They ask a question (or click a prompt)
- Dusk answers from verified Nava content
- Response is short, punchy, calibrated to frontline healthcare workers — not a research paper

**The operational pieces:**
- Cloudflare tunnel exposes `https://second-acts-tones-funk.trycloudflare.com` to the internet
- The relay runs on `204.168.204.198:8081`
- Token auth: `nava-dusk-2026`
- Rate limit: 20 requests/IP/60 seconds

## Where We Are Stuck

### Stale Sessions Block the Relay

**Symptom (observed Apr 22):** Typing indicator shows but no response ever comes. Webapp becomes unresponsive.

**Root cause:** Session tickets from previous days were queuing in `pending.json` and never being answered. The relay was polling old, dead session files that would never respond.

**Fix when it happens:** Restart relay.py and clear `pending.json`.

**Ongoing risk:** If the relay process dies and restarts, old sessions from sessions.json may be re-registered but their session files are stale. The background thread sends messages to sessions that don't have active handlers.

### The Overnight Brief Cron Has Not Been Verified

`generate_brief.py` runs at 06:00 UTC daily but has not been tested in production. It depends on:
- Sessions still being readable from sessions.json at cron time
- INIT_MESSAGE stripping working correctly
- Names being substituted from names.json

### The RAG Corpus Is Still Building

Dusk is instructed to check `nava-for-dusk/rag/clean_txt/` for questions not answered in qr-notebook.md. That folder exists but the corpus is not yet complete. Until it is, Dusk's fallback path may return "I don't know that" for questions that actually have answers in the blog articles.

### The WordPress Integration Is Unfinished

The page is live at the Cloudflare tunnel URL, but it hasn't been pasted into WordPress yet. The current URL is a temporary tunnel — not the final navahc.com destination.

### Interview Mode Hasn't Fired in Production

Interview mode is built but Dusk has to organically detect when a user knows about Reclaimix. This hasn't happened yet. The checkpoint notification to Dusk's main session via WebSocket has not been tested end-to-end.

### Git Push Doesn't Work from This VPS

All chat-page files are committed locally. `git push` fails — the remote repository (tiny4lurv/openclaw-workspace) can't be reached from this host.

## What Good Looks Like

When it's working properly:
- An employee lands on the page, sees a logo and three prompt buttons
- They click "Tell me about NurseSphere" or type their own question
- Within seconds they get a short, accurate, grounded answer
- If Dusk enters interview mode, a JSON file appears in `interviews/` and Dusk's main session gets notified
- The next morning, a brief appears in `briefs/YYYY-MM-DD/` for every session from the previous day
- The relay runs indefinitely without going stale
