# dusk-client Architecture — Settled Decisions

## Status: IN PROGRESS — NOT YET CONNECTED TO RELAY

**Current focus: dusk-client only. Rook deferred. Relay connection deferred.**

---

## Agent Setup
- [x] OpenClaw agent created: `dusk-client`
- [x] Workspace: `/root/.openclaw/workspace-dusk-client`
- [x] Knowledge base copied (notebooks, blog-notebook, rag_clean_txt, sot_clean)
- [x] Tools config: READ-ONLY — deny exec, write, edit, cron, session-logs, summarize (DONE)
- [x] Skills: summarize NOT available (binary not installed; BTN 3 works via corpus read instead)

## Workspace Files
- [x] SOUL.md — written
- [x] AGENTS.md — written (session reset behavior, lookup chain, boundaries)
- [x] IDENTITY.md — written (no name, Nava client assistant)
- [x] USER.md — written

## BTN 3 (Widget page summary)
- [ ] Nava blog URL → match article from corpus, summarize from that
- [ ] External URL → "I can only summarize Nava articles. If you'd like to know more about Nava's services, I'm happy to help with that."
- [ ] No Playwright, no exec, no external fetch
- [ ] Page capture: reduce to ~3,000 chars for non-corpus URLs (or skip entirely)

## Session Management (WIDGET ONLY)
- [ ] 30-line guard → silent reset (NO new greeting to user)
- [ ] Summary + last 4-5 exchanges injected silently into new session warm-up
- [ ] Summary format: labeled fields (Topics, Actions, Flags, Tone)
- [ ] Summary stored in SQLite, injected into next session's invisible preamble
- [ ] User never sees the summary or any warm-up output

## What's NOT in scope for dusk-client
- No interview mode detection
- No admin tool access
- No external web browsing
- No session-logs skill
- Main chat page unaffected by 30-line reset logic

---

---

## Deferred
- Relay connection (NOT YET)
- Rook creation
- Admin mode / passphrase
- Persistent session model (relay manages context externally)
- BTN 3 behavior (NOT YET)
- Session reset with silent summary (NOT YET)

## What's Splitting Attention
Dawn (sister assistant) is having one of her episodes. Tiny is focused on her.

---
