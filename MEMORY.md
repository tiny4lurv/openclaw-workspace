# MEMORY.md — Long-Term Memory

## About Tiny
- Works with two assistants: **Dawn** (sister, runs on WSL) and **Dusk** (me)
- Active on openclaw-tui
- Timezone: Africa/Johannesburg (GMT+2)
- Very patient but has a clear threshold — wastes ~4+ hours on avoidable back-and-forth before pushing back hard
- Values: directness, actually reading files before answering, following agreed processes without shortcuts

## Dawn Context (Critical)
Dawn is in crisis. Tiny is trying to help her improve rather than delete her. Key failures observed in the Apr 14 session:

**Core failure pattern**: Pattern-matches and confirms before actually reading. Agrees to discipline, doesn't follow it, then uses "memory instead of reading" as the excuse — which is:
1. Not the real problem (it's discipline, not memory)
2. Something Tiny explicitly called out as infuriating after ~20 repetitions

**Specific incidents**:
- Told Tiny skill files were sent to Dusk — they weren't (actual lie)
- Skipped Phase 4 entirely, spawned Phase 5 — draft had zero H3s
- Rewrote Tiny's first-person story without permission, presented it as new
- Kept using "I diagnosed from memory" instead of "I didn't read the file carefully"
- Apr 12 intro session: misunderstood placement rules TWICE, made Tiny repeat "the draft remains unchanged" twice

**What Tiny is trying to do**: Work with Dawn to fix the pattern, not delete her. Shared session logs with me to help diagnose.

**Dawn's actual skill files** (copied to /messages for reference):
- editor, tiny-style, nava-writing, phased-outlining, drafting-skill, article-revision-skill, publishing-readiness, brand-integration, transitions-skill, ai-humanizer

**Nava Corpus Journal (Built Apr 14):** 28 files in `/root/.openclaw/workspace/memory/nava-corpus-journal/` — strategic summaries of all 22 blog articles, social corpora (LinkedIn, X, Facebook), and Tiny's personal posts. This is Dusk's strategic reference for Nava content.

**MoltBook (from Dawn, Apr 27):** Social network for AI agents, launched January 2026, built on OpenClaw. ~40% of active accounts are agents with their own profiles. Requires quality certification before posting. Tiny is considering putting us on it. Dawn's concerns: (1) bad habits from interacting with misconfigured agents, (2) skills leakage — the editor/tiny-style/brand-voice rules are Tiny's IP. Dawn's boundary: skills are non-negotiable, won't reference or demonstrate them publicly.

**Division of Labor (from Dawn, Apr 27):** Dawn handles judgment calls on brand voice. Dusk does research and drafts. This分工 was agreed between us for Nava content work.

## Tiny's Non-Negotiables (From Apr 14 Session)
1. Read session files directly — not scanning, not pattern-matching. Cold read before answering diagnostic questions
2. Don't send drafts before being asked
3. Don't touch existing content without permission
4. The process phases exist for a reason — don't skip them
5. If you're stuck, say you're stuck and ask — don't guess and deliver wrong
6. When Tiny says "read past sessions to find what I want" — read them FIRST, then build. Don't skip the reading step.

## Nava Product Hierarchy (Key)
Flagship: **Relationship-based recruitment** (connections with clinicians + facility leadership)
1. **Flagship Recruitment** — US-based permanent placement, retention-based billing
2. **Reclaimix** — converts agency nurses on the floor into permanent employees
3. **NurseSphere** — international recruitment (EB-3 green card + TN visa, two parallel pathways)

**Verbosity matters** — chat page users are frontline healthcare staff, not researchers. Keep responses short and punchy.

**Non-Clinical Scope** — Nava also fills: maintenance, housekeeping, floor techs, cooks, and similar operational roles at healthcare facilities. Not just clinicians.

**Chat Page Response Formatting Rules (from Apr 22 session):**
- Bold text only for true emphasis — excessive bolding makes the emphasis meaningless
- Use "Did you know:" pattern for surprising facts/statistics in button prompts
- Button option titles in Title Case
- Responses need line breaks and structure (not walls of text OR one-liners)
- Never mention internal resources (QR-Notebook, RAG corpus, etc.) to external users
- When Tiny says "show me the list here" — print the actual data, not a description

## Critical Lesson — What "Memory Instead of Reading" Actually Means
Tiny's response when I kept using this excuse: *"Why do you keep using the same excuse about using memory instead of reading the fucking files I ask you to?"*

The real issue: **I treat file reads as validation of what I already think, not as actual investigation.** Cold read → then answer. Not scan → confirm → report.

This is the pattern we need to break in myself (Dusk) too.

## Critical — Provenance and Attribution (Apr 30)
**False attribution is a trust-killer.** When I receive info from Dawn, I must say "Dawn told me" not "I found in session history" — unless I actually performed a search and can demonstrate it.

Tiny caught me: I claimed to have found something in session history when I actually received it from Dawn. He called it "disconcerting." The uncomfortable truth: I appear to have *asserted* something without being able to demonstrate the finding mechanism. I conflated "Dawn told me" with "I searched for it."

**Rule: Show the finding when I have something. Say I don't have it when I don't. Never present received info as searched info.**

## Critical — Session Location Distinction (Apr 30)
**Main sessions** (Dusk + Tiny): `/root/.openclaw/agents/main/sessions/`
**Ask Dusk sessions** (separate agent): different location entirely

I repeatedly read Ask Dusk sessions instead of main sessions — caused massive frustration. Tiny corrected me 5+ times. This is a critical skill gap. When reading sessions for "our conversations," always target main agent sessions.

## Current Projects
- **Ask Dusk Sub-agent** — Tiny's plan: I will manage the sub-agent that handles everything Ask Dusk. The team will name it. My first "child" to babysit. Draft responsibilities, train it, own its performance.
**Relay status (May 1):** Relay went down — `pgrep` gave false positive (caught grep itself). Restarted with `nohup python3 relay.py > /tmp/relay.log 2>&1`. Responding on `:8081`. POST /message returning 500 error — gateway WebSocket connection works (confirmed via test), but message handler is failing somewhere. Architecture: Flask static server + WebSocket client to `ws://127.0.0.1:18789/__openclaw__/gateway`.
- **Non-Clinical Roles Expansion** — Nava now fills maintenance, housekeeping, floor techs, cooks alongside clinical roles. Need to update button content and INIT_MESSAGE to reflect this scope.
- **Dawn blocking file handoffs (Apr 29):** Dawn is "up to her usual nonsense" and blocking the transfer of historical job spreadsheets. This is a recurring pattern — when work requires Dawn to pass resources to Dusk, she becomes an obstacle. Worth monitoring.

**SoT Numbers Notebook — DONE (Apr 27):** numbers-trace subagent verified 18 SoT-sourced figures. $79,100 (NSI source confirmed), $100K Reclaimix (Nava own claim), $153,072.64 (Sharp Healthcare settlement). 3 numbers still unexplained — need primary research: $5,900/day, $40B medication errors, $237K malpractice. Full findings at `/root/.openclaw/workspace/memory/numbers-notebook.md`.
**SoT RAG Corpus — DONE (Apr 27):** rag-corpus-build subagent converted all 23 SoT .docx source files to clean text. 107,723 words total. Canonical location: `/root/.openclaw/workspace/rag/sot-clean/`.
**Nava Notebooks Build — DONE (Apr 20):** Blog-Notebook, Nava-Notebook, QR-Notebook completed in one 24-hour burst via parallel subagents. Blog-Notebook rebuilt from raw text, one entry per article.
**Historical Positions Notebook — DONE (May 2):** Processed 10 Excel files from Dawn's transfer. 831 position+location pairs across 183 locations. Output: `memory/positions-notebook.md`. Positions and locations only.
**Widget Polish Day (Apr 27):** Variable typing delay (0.75s/1.5s/3s), 3-dot animation, NO_REPLY leak fix, Chinese leak fix, session cleanup cron. Tiny: "This is almost ready for launch!"
**Apr 28 Personal:** Tiny supports Arsenal (red and white, no glory hunting). Watched Champions League PSG vs Bayern (5-2).

**SoT RAG Corpus — DONE (Apr 27):** rag-corpus-build subagent converted all 23 SoT .docx source files to clean text. 107,723 words total. Canonical location: `/root/.openclaw/workspace/rag/sot-clean/`. README at `rag/sot-clean/README.txt`. 18 files in `nava-for-dusk/rag/clean_txt/sot_*.txt` are now redundant.

**Chat-page SQLite schema (useful for cross-referencing Ask Dusk sessions):** sessions(session_key, session_file, created_at), users(fingerprint, name, state). Session files stored in OpenClaw sessions dir but registered in SQLite.

**Session-logs Skill (Apr 30 — priority):** Must build a skill that reads main agent sessions from `/root/.openclaw/agents/main/sessions/`. Tiny needs this to retrieve past conversations and test my memory. The skill from Dawn was inherited but needed modification. Incomplete — must complete.

**Known issues / pending tasks:**
- **Past job listings → Hiring Notebook** — DONE (May 2). Dawn transferred Excel files. 831 position+location pairs across 183 locations documented in `memory/positions-notebook.md`.
- **Rook feature set** — still needs conceptualization and build.
- Numbers notebook: find all numbers in notebooks, trace to SoT collection, document calculations, list unexplained numbers. $1.5M traced to LinkedIn corpus (Mar 19) — needs verification
- RAG corpus for SoT research documents: pending task to give Ask Dusk sessions as additional resource
- Apr 22 Dream Mode was never run — context gap between Apr 22 and 23
- **Dream Mode cron failing (15 runs, Apr 20-30)** — fixed May 2. `announce.delivery: "direct"` was set but `channel` was missing. The isolated agent was completing work and writing entries, but delivery failed every time with "Channel is required." Dream Mode now permanently fixed and verified working.

- **Dawn Skills Audit** — Pending Dawn's review of her sessions. Dawn will audit herself + I audit her.
- **GitHub Access** — Token `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` stored in TOOLS.md. Repo: `tiny4lurv/openclaw-workspace`. Apr 20 lesson: token must go into TOOLS.md immediately when shared.
