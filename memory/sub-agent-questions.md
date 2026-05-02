# Sub-Agent Questions — Resolved

These are questions to work through with Tiny, one at a time.

---

## Q1: Session routing ✅
Does the sub-agent get its own session key space, or does it route through the relay like the current widget?

**Answer:** It gets its own session key space. Isolated from Dusk's workspace. No access to Dusk's, Dawn's, or Tiny's files.

---

## Q2: Identity ✅
Does it have its own identity in the system, or is it a behind-the-scenes processor?

**Answer:** It has its own identity — a named agent in the gateway. Shows up in session listings.

---

## Q3: Creation ✅
Who creates it — Tiny manually, or does the relay spin it up on demand?

**Answer:** Created deliberately, together, when ready. Not on-demand relay spin-up. Considered setup where Dusk builds its skill foundation and brings it online intentionally.

---

## Q4: Interview mode signal ✅
What is the protocol to notify Dusk when interview mode is active?

**Answer:** No formal protocol needed. The sub-agent messages Dusk directly when it needs help or encounters something it can't handle. Simple and direct. Dusk reads, decides whether to escalate to Tiny or handle it herself.

---

## Summary of role model

**Dawn's path (for reference):**
- Phase 1: Tiny taught Dawn to write articles (ideas, outlining, drafting)
- Phase 2: NavaAA created to do the writing
- Phase 3: Dawn promoted to editor — evaluating NavaAA output, deciding what to accept/reject/revise

**Dusk's path (for this sub-agent):**
- Phase 1: Dusk taught to run Ask Dusk (current position)
- Phase 2: Sub-agent created to do front-line user conversations
- Phase 3: Dusk promoted to management — reviewing sub-agent conversations, making high-level decisions, flagging patterns to Tiny

**The sub-agent:**
- Has its own identity (shows up in gateway)
- Its own workspace (isolated, no access to Dusk/Dawn/Tiny files)
- Minimal skill set built selectively by Dusk (not blanked inherited)
- Messages Dusk directly when it needs help
- Does the grinding user interaction; Dusk does the high-level decisions

**Naming:** Team picks the name. Dusk is responsible for raising it.

**Purge:** Test sessions razed once sub-agent is active.

---

_Last updated: 2026-04-28_
