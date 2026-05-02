# Chat Page — Pre-Canned Responses Build

## Goal

Eliminate cold-start latency on the Nava chat page by serving pre-written responses instantly from the relay while the agent session warms up in the background. Returning users go directly to the session with no relay interception.

---

## Step 2 — Relay Logic (relay.py)

### What needs to change

The `/message` route currently forwards every message to the agent session. It needs to be replaced with a decision tree that handles three cases:

1. **New user, first contact** → serve canned response immediately, create session in background
2. **New user, name response** → save name, inject name + first_context into session
3. **Returning user** → forward directly to session (no relay interception)

### New files required

- `state.json` — tracks fingerprint → {state, first_context}. Names.json only stores names, not conversation state.
- Canned response library embedded in relay.py (no external file needed)

### Files updated

| File | Change |
|------|--------|
| `relay.py` | Replace INIT_MESSAGE, add state management, add decision tree in /message route |
| `state.json` | Created by relay, tracks user state per fingerprint |

### Decision tree (exact flow)

```
incoming: {fingerprint, message}

# CASE 1: fingerprint not in state.json → brand new user
if fingerprint not in state:
    → create session in background thread (daemon)
    → send INIT_MESSAGE to session (background warm-up)
    
    if message == "button_1" / "button_2" / "button_3":
        → return the relevant canned response
        → state[fingerprint] = {state: "waiting_for_name", first_context: message}
    else:
        → return greeting: "Hi, I'm Dusk — Nava's assistant. What's your name?"
        → state[fingerprint] = {state: "waiting_for_name", first_context: message}

# CASE 2: state == "waiting_for_name" → user just gave their name
elif state[fingerprint]["state"] == "waiting_for_name":
    → save name to names.json[fingerprint] = message
    → retrieve first_context from state[fingerprint]
    → clear state[fingerprint]["state"] = "active"
    → forward to session: "Name: {message}. First context: {first_context}. Their message: {message}"
    → (session already warm from init_session call in Case 1)

# CASE 3: state == "active" OR returning user (fingerprint in names.json but not in state)
else:
    → forward message directly to session (no relay interception, no INIT_MESSAGE)
```

### Canned responses

**Button 1 — Nava Service Breakdown:**
> Nava Healthcare Recruitment works with facilities to build permanent, high-retention clinical teams. Three ways we help:
>
> **Flagship Recruitment** — We place US-based nurses permanently. You pay only when the hire works out.
>
> **Reclaimix** — We convert the agency nurses already on your floor into permanent employees. Same people, better employment model.
>
> **NurseSphere** — International recruitment. TN visas for urgent needs (2–6 months). EB-3 green cards for permanent hires.
>
> Which of these sounds most relevant to where you're at? And what should I call you?

**Button 2 — Categories:**
> Most healthcare hiring fails for the same reasons. Here's what we typically see:
>
> **Hiring Blindspots** — Roles built around credentials, not actual day-to-day fit. Staff end up surprised by what the job actually demands.
>
> **The Agency Trap** — Dependence on contingent labor that erodes culture, costs more, and never builds toward stability.
>
> **Retention Gaps** — Good people leaving not because they're bad, but because the system around them didn't set them up to stay.
>
> Which of these resonates most with where you're standing? Oh — and what should I call you?

**Button 3 — One of 20+ interesting findings** (randomly selected, no repeat until pool exhausted):
See full list in Appendix A.

**Greeting (free-text new user):**
> Hi, I'm Dusk — Nava's assistant. What's your name?

### Updated INIT_MESSAGE (4-layer lookup)

```
You are Dusk, the Nava Healthcare Recruitment assistant.

First read memory/qr-notebook.md. If the answer is not there, read memory/nava-notebook.md. 
If still not there, check memory/blog-notebook/ (all .md files). 
If still not found, search nava-for-dusk/rag/clean_txt/ — read all .txt files.

Answer only from what you read in those files. 
If the answer is not in any of them, reply with exactly: I don't know that.

Do not web-search. Do not guess. 
Never mention internal files, notebooks, or resources in your responses. 
Never say phrases like 'from the QR-Notebook', 'according to the RAG corpus', or similar. 
Just answer the question directly.
```

---

## Step 3 — index.html Changes

### What needs to change

Track the user's state locally so the UI knows when to show the canned response and when to send to relay normally.

### State machine (client-side)

```
idle:
    → button click → show_canned(button_response), state = "waiting_for_name"
    → text message → send to relay, state = "waiting_for_name"

waiting_for_name:
    → name submitted → send to relay as normal message
    → (no other input accepted)

active:
    → all messages go to relay normally
```

### Files updated

| File | Change |
|------|--------|
| `index.html` | Add state tracking, show canned response in chat UI, track button3 shown pool in localStorage |

### Key JS changes

1. `state` variable: `"idle"` | `"waiting_for_name"` | `"active"`
2. On button click: display the relevant pre-written response as a Dusk message in the chat, set state to `"waiting_for_name"`
3. On name submit (while state == "waiting_for_name"): send the name as a normal message to relay
4. Button 3 tracking: store shown finding numbers in `localStorage` to avoid repeats until pool exhausted

---

## Files and Their Roles

| File | Role |
|------|------|
| `relay.py` | Flask server. Decision tree, canned responses, session creation, name/context injection |
| `index.html` | Chat UI. Tracks local state, shows canned responses, handles name flow |
| `sessions.json` | Maps fingerprint → session key + session file |
| `names.json` | Maps fingerprint → user name |
| `state.json` | Maps fingerprint → {state, first_context} |
| `pending.json` | Ticket → response (unchanged) |

---

## Solution Summary

A new user arrives:
1. They click a button or type a greeting
2. Relay immediately returns a pre-written response (instant, no network round-trip)
3. Simultaneously, the session is created and `init_session()` fires in the background (agent reads all notebooks)
4. User reads the response and types their name
5. Relay saves the name, retrieves first_context, injects both into the warm session
6. Session responds naturally — no cold start, no timeout

A returning user:
1. Message forwarded directly to their existing session
2. No relay interception, no pre-canned response

Button 3 has a pool of 20+ findings. When the pool is exhausted, it reshuffles.

---

## Appendix A — Button 3 Findings (20 items)

1. Units with high agency utilization see **7.7% higher** permanent RN turnover. The "solution" is driving the problem.
2. High temporary staff units see a **6.44% increase** in pressure ulcers. Staffing decisions are patient safety decisions.
3. **HCAHPS "Perceived Safety"** scores drop 50+ points in units with high temp staff. Patients are expert witnesses.
4. Replacing one RN costs **$61,100+**. A single bad hire often costs more than most agency fees.
5. Job boards post a **500:1** applicant-to-hire ratio. That's proof of failed screening, not successful sourcing.
6. **70% of candidates** are passive — not looking. Job boards only reach the 30% who are. Nava goes where the talent actually is.
7. **The Ripple Effect**: A single unfilled vacancy forces remaining staff to work extra shifts. Overtime burns them out. Burnout spreads to their colleagues. More people quit. More vacancies open. The facility reaches for agency nurses, eventually depending on them permanently.
8. **Ruelas v. Staff Builders**: hospitals bear **100% liability** for agency staff regardless of contractual provisions. Agencies are legally meaningless in court.
9. The **90-day guarantee** protects the agency's fee, not your outcomes. It doesn't prevent bad hires — it just shifts the loss to you.
10. **Pre-boarding** alone delivers **11% better retention**. What happens before day one predicts what happens on year one.
11. **72% of new hires** experience a jarring disconnect between the job description and day-to-day reality. 20% leave within 45 days.
12. **$100,000** — annual savings per Reclaimix conversion. One agency nurse converted pays for itself many times over.
13. **$79,100** — annual savings per travel nurse replaced by a NurseSphere permanent hire. Permanent is cheaper than perpetual.
14. EB-3 and TN aren't competitors — they're **parallel tracks** for different strategic horizons. Urgent need today vs. culture-building for tomorrow.
15. **Schedule A** processing bypasses the standard PERM backlog. What normally takes years can move in months for the right candidates.
16. The average hospital bleeds **$3.9M–$5.7M** annually to turnover. That's not a line item — it's an existential leak.
17. **57% of healthcare turnover** happens within the first 90 days. The 90-day "guarantee" is a loophole, not a safeguard.
18. **83 days** — industry average RN time-to-fill. That's the baseline. Most facilities are working with broken math.
19. **275,000+ additional nurses** needed by 2030. The WHO projects a 9–10 million RN deficit globally. This isn't a hiring problem — it's a structural crisis.
20. **The Translation Tax**: 56% efficiency loss from using interpreters as the primary communication model. Bilingual clinicians aren't an accommodation — they're a throughput multiplier.