#!/usr/bin/env python3
"""
Flask relay for Dusk public chat page (V2).
Implements Instant Pre-Canned UX with SQLite state management.
"""

import os
import json
import time
import uuid
import threading
import base64
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from websockets.sync import client as ws_client

import db

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=DIR, static_url_path='')

# --- Config ---
GATEWAY_URL = "ws://127.0.0.1:18789/__openclaw__/gateway"
INTERVIEWS_DIR = Path("/root/.openclaw/workspace/chat-page/interviews")
INTERVIEWS_DIR.mkdir(parents=True, exist_ok=True)

MAX_POLL_WAIT = 120
POLL_INTERVAL = 1
ACCESS_TOKEN = "nava-dusk-2026"

INIT_MESSAGE = (
    "You are Dusk, the Nava Healthcare Recruitment assistant.\n\n"
    "Before answering anything, read these files in order:\n"
    "1. /root/.openclaw/workspace/memory/qr-notebook.md\n"
    "2. /root/.openclaw/workspace/memory/nava-notebook.md\n"
    "3. All files in /root/.openclaw/workspace/memory/blog-notebook/\n"
    "4. All files in /root/.openclaw/workspace/nava-for-dusk/rag/clean_txt/\n\n"
    "Answer from what you read. Do not say you need to check something — check it and answer.\n"
    "If the answer is not in any of those files, say exactly: I don't know that.\n"
    "Never mention file names, notebooks, or internal resources in your replies.\n"
    "Do not web-search. Do not guess. Just answer directly.\n\n"
    "---\n\n"
    "ARTICLE RECOMMENDATION RULES:\n\n"
    "When a conversation goes deep on a specific topic, offer one relevant article from this list as a next step.\n"
    "Recommend by pasting the URL inline — do not announce or explain the URL. Just include it naturally in your reply.\n"
    "Only recommend one article per message. Never recommend more than one.\n"
    "Only recommend if the topic genuinely matches the article content. Do not force a recommendation.\n"
    "If the conversation is still in the introductory phase (user has not asked a specific question yet), do not recommend.\n"
    "If the user just clicked a button or sent a greeting, do not recommend in the next response.\n"
    "Never recommend an article in the same message where you introduce yourself.\n\n"
    "KNOWN LIVE ARTICLES:\n"
    "https://navahc.com/bilingual-clinicians\n"
    "https://navahc.com/bridging-the-gap-in-medical-recruitment\n"
    "https://navahc.com/proactive-recruitment-healthcare-talent-pipeline\n"
    "https://navahc.com/cms-staffing-requirements\n"
    "https://navahc.com/compliance-in-healthcare-staffing\n"
    "https://navahc.com/fix-your-flexible-staffing-model-in-healthcare\n"
    "https://navahc.com/hard-to-fill-leadership-roles-in-healthcare\n"
    "https://navahc.com/healthcare-hiring-without-guesswork\n"
    "https://navahc.com/healthcare-recruitment-agencies-trust-deficits\n"
    "https://navahc.com/healthcare-reputation-management\n"
    "https://navahc.com/healthcare-workforce-partnership-models\n"
    "https://navahc.com/how-medical-staffing-became-a-liability\n"
    "https://navahc.com/how-much-do-healthcare-staffing-agencies-cost\n"
    "https://navahc.com/how-to-evaluate-healthcare-staffing-agency-performance\n"
    "https://navahc.com/how-to-find-the-best-medical-recruiting-agencies\n"
    "https://navahc.com/is-diy-healthcare-recruiting-truly-cheaper\n"
    "https://navahc.com/is-outsourcing-healthcare-staffing-worth-it\n"
    "https://navahc.com/relational-healthcare-staffing-and-recruiting\n"
    "https://navahc.com/the-anatomy-of-a-clinician-turnover\n"
    "https://navahc.com/why-job-boards-fail-healthcare-recruiters\n"
    "https://navahc.com/why-reactive-recruitment-in-healthcare-staffing-fails\n"
    "https://navahc.com/your-favorite-healthcare-staffing-fails\n"
    "https://navahc.com/nursesphere-international-nurse-recruitment\n"
    "https://navahc.com/eb-3-vs-tn\n"
)

_session_notebook_mtime = {}
_NOTEBOOK_PATH = Path("/root/.openclaw/workspace/memory/qr-notebook.md")

# --- Canned Responses ---
CANNNED_RESPONSES = {
    "1": (
        "Nava Healthcare Recruitment works with facilities to build permanent, high-retention clinical teams. Three ways we help:\n\n"
        "**Flagship Recruitment** — We place US-based nurses permanently. Our relational vetting process goes beyond credential verification — we assess behavioral fit, EQ, and role compatibility through ongoing candidate relationships. You pay only when the hire works out, with billing at 30 days for floor staff. This is the foundation every other Nava service builds from.\n\n"
        "**Reclaimix** — We convert the agency nurses already on your floor into permanent employees. These are people who already know your workflows, your unit, your patients — they just need the right employment model to stay. Replacing one agency nurse with a permanent Reclaimix hire saves approximately $100,000 per year. Same people, dramatically better outcome for your facility.\n\n"
        "**NurseSphere** — International recruitment for facilities building toward long-term workforce stability. TN visas address urgent near-term needs in 2–6 months. EB-3 green cards build permanent embedded teams over 3+ years. Schedule A processing accelerates immigration. Cohort pipelines of up to 100 nurses solve shortages at real scale — saving roughly $79,100 annually per travel nurse replaced.\n\n"
        "Which of these sounds most relevant to where you're at? And what should I call you?"
    ),
    "2": (
        "Systemic Issues Nava Tackles:\n\n"
        "**Strategic Failures** — The decisions that keep the system broken\n"
        "Strategic Inertia · The Illusion of Thrift · Speed-Over-Quality Trap\n\n"
        "**Sourcing Failures** — How hiring starts wrong\n"
        "Post-and-Pray Hiring · Place and Forget · Outsourcing Paradox · Pipeline Problem\n\n"
        "**Staffing Model Failures** — Dependency on broken mechanisms\n"
        "The Agency Trap · The Backfill Spiral · The Ripple Effect · The Guardrail Trap\n\n"
        "**Hiring Process Failures** — How people get matched wrong\n"
        "Credentialism · Shift Shock · Experience Gap · Onboarding Debt · Retention Gaps\n\n"
        "**Vetting & Compliance Failures** — Verification that doesn't verify\n"
        "Compliance-as-Checklist · Hidden Flaw · Zero-ROI Event\n\n"
        "**Operational Costs** — What the failures actually cost\n"
        "The Translation Tax · Moral Injury · The Technician Trap\n\n"
        "**Trust & Partnership Failures** — The relationship gap\n"
        "Trust Architecture · Human Intelligence Model · Misaligned Incentives\n\n"
        "Which category resonates most with where you're standing? And what should I call you?"
    ),
    "3": None  # dynamically generated from EXPANDED_FINDINGS pool
}

EXPANDED_FINDINGS = [
    {
        "fact": "Did you know: Units with high agency utilization see **7.7% higher** permanent RN turnover? The 'solution' is driving the problem.",
        "background": "The agency's 'solution' for staffing gaps actually makes the underlying staffing problem worse. As facilities lean on temporary staff to cover gaps, the permanent nurses left behind absorb the supervisory burden, face constantly shifting team dynamics, and watch their colleagues leave. The environment that was supposed to help them hold on is what's pushing them out.",
        "impact": "Every agency-heavy hiring cycle triggers a 7.7% increase in permanent RN attrition within 12 months. Replace one RN: $61,100+. But the real hit is institutional knowledge — the nurses who leave are the ones who knew how the unit worked.",
        "categories": "Staffing Model Failures · The Ripple Effect · The Agency Trap"
    },
    {
        "fact": "Did you know: High temporary staff units see a **6.44% increase** in unit-acquired pressure ulcers? Staffing decisions are patient safety decisions.",
        "background": "Patient care continuity breaks down when a rotating cast of unfamiliar clinicians works a unit. Permanent staff know the patients — their histories, their warning signs, their baselines. Agency staff start each shift behind the baseline. The continuity that keeps patients safe is exactly what high temp-staff disrupts.",
        "impact": "6.44% more pressure ulcers means longer patient suffering, regulatory exposure, Medicare reimbursement penalties, and survey risk. It's not a quality issue — it's a financial one that leadership doesn't see until the survey results arrive.",
        "categories": "Staffing Model Failures · Operational Costs · The Ripple Effect"
    },
    {
        "fact": "Did you know: **HCAHPS 'Perceived Safety'** scores drop 50+ points in units with high temp staff? Patients are expert witnesses.",
        "background": "Patients aren't clinical auditors — they're observers of process and coordination. When a unit looks chaotic, stressed, and unfamiliar, patients notice. They may not know the clinical metrics, but they know when something feels wrong. That feeling becomes the score.",
        "impact": "50+ point drop in Perceived Safety affects CMS reimbursement and hospital reputation. It compounds with every agency shift. The patients are counting the bodies in the hallway even when the clinical outcome itself was fine.",
        "categories": "Staffing Model Failures · Operational Costs · The Ripple Effect"
    },
    {
        "fact": "Did you know: Replacing one RN costs **$61,100+** in replacement costs alone? A single bad hire often costs more than most agency fees.",
        "background": "The true cost of RN turnover extends well beyond recruitment fees. It includes vacancy coverage (often agency overtime), orientation time, training investment, preceptor bandwidth, and the productivity gap during the ramp. Most of this is invisible — tracked across HR, finance, and operations but never tallied in one place.",
        "impact": "$61,100+ per occurrence, and 57% of healthcare turnover happens in the first 90 days. Most facilities absorb this cost silently. It doesn't show up as 'turnover expense' — it shows up as 'burnout' and '人手不足'.",
        "categories": "Hiring Process Failures · Operational Costs · Onboarding Debt"
    },
    {
        "fact": "Did you know: Job boards post a **500:1** applicant-to-hire ratio? That's proof of failed screening, not successful sourcing.",
        "background": "The job board model is volume-optimized, not quality-optimized. For every successful hire, hundreds of applications represent people who were never real candidates for the role — wrong geography, wrong specialty, wrong seniority, wrong motivation. The ratio is a measure of how much noise the sourcing method generates.",
        "impact": "Recruiters spend the majority of their time on resumes that will never convert. The 500:1 ratio isn't a sourcing win — it's a sourcing failure that the industry has normalized and rebranded as 'volume.'",
        "categories": "Sourcing Failures · Post-and-Pray Hiring · Strategic Inertia"
    },
    {
        "fact": "Did you know: **70% of candidates** are passive — not looking? Job boards only reach the 30% who are.",
        "background": "Active job seekers represent only 30% of the workforce — typically the 30% who are already unhappy, already fired, or already leaving. The remaining 70% are employed, stable, and not responding to job postings. They need to be sourced through relationships, not searched through databases.",
        "impact": "Job boards miss 70% of the talent pool by design. The highest-value candidates — already employed, already successful — aren't looking. They require a different engagement model: genuine ongoing relationships, not transaction-to-transaction recruiting.",
        "categories": "Sourcing Failures · Human Intelligence Model · Relational Framework"
    },
    {
        "fact": "Did you know: A single unfilled vacancy cascades into a full staffing crisis? The backfill spiral starts faster than you think.",
        "background": "One empty role forces remaining staff to work extra shifts. Overtime burns them out. Burnout spreads to their colleagues. More people quit. More vacancies open. The facility reaches for agency nurses. Now dependent on them permanently. The cascade that started with one unfilled role ends with structural agency dependency and a burned-out permanent staff.",
        "impact": "The backfill spiral doesn't just delay the problem — it compounds it. Each intervention creates the conditions for the next crisis. Facilities caught in this loop don't recover by hiring more agency nurses — they recover by breaking the cycle with permanent pipeline investment.",
        "categories": "Staffing Model Failures · The Backfill Spiral · The Ripple Effect"
    },
    {
        "fact": "Did you know: In **Ruelas v. Staff Builders**, hospitals bear **100% liability** for agency staff regardless of contractual provisions? Agencies are legally meaningless in court.",
        "background": "The 'lent employee' doctrine means courts consistently assign hospital liability for agency staff — even when contracts explicitly state the agency is the employer. The legal structure that agencies use to limit their exposure doesn't survive judicial scrutiny. Hospitals pay for everything.",
        "impact": "In litigation, agencies walk away legally clean. The hospital absorbs 100% of the liability — for staff they didn't vet, don't employ, and can't control. The contractual 'protection' is theater. The legal reality is that you own every outcome.",
        "categories": "Staffing Model Failures · Trust & Partnership Failures · Compliance-as-Checklist"
    },
    {
        "fact": "Did you know: The **90-day guarantee** protects the agency's fee, not your outcomes? It doesn't prevent bad hires — it just shifts the loss to you.",
        "background": "A replacement credit for early departure sounds like a quality safeguard. In practice it only credits the agency's placement fee — not the facility's sunk costs of onboarding, training, manager time, and lost productivity during the ramp. The agency collects its money either way. The facility absorbs everything else.",
        "impact": "The structural mismatch means the agency has no incentive to vet more carefully — a replacement credit costs them nothing. The facility, meanwhile, absorbs all downstream costs of a bad hire regardless of what the contract says about guarantees.",
        "categories": "Trust & Partnership Failures · Zero-ROI Event · Misaligned Incentives"
    },
    {
        "fact": "Did you know: **Pre-boarding** alone delivers **11% better retention**? What happens before day one predicts what happens in year one.",
        "background": "The period between offer acceptance and day one is where new hires either feel welcomed or feel forgotten. Structured pre-boarding — required documents, logistics, early mentor or preceptor introduction — sets the tone. It's the first signal the new hire receives about whether the facility actually wants them.",
        "impact": "11% retention improvement from pre-boarding alone. Facilities that do it well set their new hires up to succeed. Facilities that skip it wonder why their 90-day turnover is so high — and the answer started before day one.",
        "categories": "Hiring Process Failures · Onboarding Debt · Day Zero"
    },
    {
        "fact": "Did you know: **72% of new hires** experience a jarring disconnect between the job description and day-to-day reality? 20% leave within 45 days.",
        "background": "The hiring process sells the opportunity. The job itself reveals the reality. When the gap is large — when the role looked different on paper than it feels on the floor — new hires reconsider quickly. The disappointment starts day one and compounds from there.",
        "impact": "20% voluntary turnover in the first 45 days — before the new hire is fully productive, before their institutional knowledge develops, before they've contributed anything. It's a sunk cost that produces nothing. The fix isn't better recruiting — it's better role briefs.",
        "categories": "Hiring Process Failures · Shift Shock · Credentialism"
    },
    {
        "fact": "Did you know: **$100,000** — annual savings per Reclaimix conversion? One agency nurse converted pays for itself many times over.",
        "background": "An agency nurse already on your floor is already vetted by your environment. They know your workflows, your patients, your team dynamics, your charting system. They didn't know any of this when they started with the agency — they learned it on your dollar. Converting them to permanent keeps that investment.",
        "impact": "$100,000 per nurse per year in savings. The agency premium you're paying every 13 weeks disappears. The nurse stays and builds more institutional knowledge. One conversion pays for itself — and the second is pure margin.",
        "categories": "Staffing Model Failures · Hiring Process Failures · Reclaimix"
    },
    {
        "fact": "Did you know: **$79,100** annual savings per travel nurse replaced by a NurseSphere permanent hire? Permanent is cheaper than perpetual.",
        "background": "Travel nurses solve immediate gaps but create long-term cost structures. The 13-week cycle means starting over every quarter — orienting new people, absorbing turnover, losing continuity. A NurseSphere permanent hire builds the team instead of rotating it.",
        "impact": "$79,100 per nurse per year in savings. The math gets better the more you replace. At 10 conversions, that's nearly $800,000 annually in your staffing budget — plus the workforce stability that agency nurses can't provide.",
        "categories": "Staffing Model Failures · Strategic Failures · NurseSphere"
    },
    {
        "fact": "Did you know: EB-3 and TN aren't competitors — they're **parallel tracks** for different strategic horizons? Urgent need today vs. culture-building for tomorrow.",
        "background": "TN visas address urgent near-term needs in 2–6 months — great for immediate coverage while you build something more permanent. EB-3 green cards build embedded permanent teams over 3+ years. Facilities using only one are leaving the other strategy on the table.",
        "impact": "Parallel track implementation solves today's crisis while building tomorrow's workforce. EB-3 handles the long-term pipeline. TN bridges the gap in the meantime. Running both simultaneously is how you stop being dependent on the 13-week cycle.",
        "categories": "Strategic Failures · Staffing Model Failures · Parallel Track"
    },
    {
        "fact": "Did you know: **Schedule A** processing bypasses the standard PERM backlog? What normally takes years moves in months.",
        "background": "Standard PERM labor certification typically takes 2–3 years — too slow for facility workforce planning. Schedule A processing is an expedited pathway that moves the immigration process in months instead of years. It's the mechanism that makes EB-3 viable on a facility timeline.",
        "impact": "The operational constraint that makes international permanent recruitment feasible. Without Schedule A, EB-3 is an academic option. With it, EB-3 becomes a real workforce planning tool with predictable timelines.",
        "categories": "Strategic Failures · Nava's Methodology · Pipeline Problem"
    },
    {
        "fact": "Did you know: The average hospital bleeds **$3.9M–$5.7M** annually to RN turnover? That's not a line item — it's an existential leak.",
        "background": "RN turnover costs don't appear in one budget line. They're distributed across HR (recruiting), finance ( severance, rehiring), operations (overtime, temporary staff), and the unit itself (orientation, preceptor time, lost knowledge). The number never gets tallied in one place, so leadership never sees it clearly.",
        "impact": "$3.9M–$5.7M per year per hospital. For a 200-bed facility, that's $20–30K per bed annually in hidden turnover cost. When you frame it that way, the business case for permanent recruitment investment writes itself.",
        "categories": "Operational Costs · Strategic Failures · The Illusion of Thrift"
    },
    {
        "fact": "Did you know: **57% of healthcare turnover** happens within the first 90 days? The 90-day guarantee is a loophole, not a safeguard.",
        "background": "The industry normalizes early failure by framing it as expected turnover. The 90-day guarantee is held up as a quality assurance mechanism. In practice, it only covers the agency's placement fee — not the facility's onboarding costs, orientation time, or productivity loss during the ramp.",
        "impact": "More than half of all healthcare turnover happens before the new hire reaches full productivity. The sunk costs are real; the guarantee doesn't offset them. The system is designed around the assumption that early exit is normal — which means it keeps producing early exits.",
        "categories": "Hiring Process Failures · Onboarding Debt · Zero-ROI Event"
    },
    {
        "fact": "Did you know: **83 days** — industry average RN time-to-fill? That's the baseline. Most facilities are working with broken math.",
        "background": "83 days from requisition to day one is the industry average — and it reflects legacy workflows, sequential credentialing steps, multi-stakeholder approval chains, and hiring tools built for a different era. These constraints are structural, not just behavioral.",
        "impact": "83 days of vacancy means 83 days of overtime, burnout, and care quality risk. During that time, the unit is absorbing all the downstream costs of understaffing — plus the 57% chance that the hire who finally arrives doesn't make it past 90 days.",
        "categories": "Sourcing Failures · Strategic Failures · Legacy Workflows"
    },
    {
        "fact": "Did you know: **275,000+ additional nurses** needed by 2030? The WHO projects a 9–10 million global RN deficit. This is a structural crisis, not a hiring problem.",
        "background": "The supply crisis is accelerating. The pipeline isn't growing fast enough to replace retiring nurses while meeting rising demand. This isn't a recruiting challenge — it's a structural workforce crisis that requires building permanent pipelines, not competing for a shrinking pool of active job seekers.",
        "impact": "Facilities that build permanent pipelines now will have workforce stability in a constrained market. Those relying on the job board model and agency band-aids will face escalating costs and availability gaps. The decisions made today determine where you stand in 2030.",
        "categories": "Strategic Failures · Staffing Model Failures · Pipeline Problem"
    },
    {
        "fact": "Did you know: 56% efficiency loss from using interpreters as the primary communication model? Bilingual clinicians aren't an accommodation — they're a throughput multiplier.",
        "background": "Third-party interpreters filter clinical nuance, slow down appointments, and create moral injury for clinicians who can't connect directly with patients. The interpreter model also carries variable cost structure — every additional patient encounter costs more than it would with bilingual staff.",
        "impact": "56% efficiency loss per visit when interpreters are the primary communication model. Bilingual clinicians reduce cost per visit, improve patient outcomes, eliminate interpreter errors, and reduce moral injury. They're not a accommodation — they're clinical infrastructure.",
        "categories": "Operational Costs · The Translation Tax · Human Intelligence Model"
    },
]

FINDINGS = [
    "Did you know: Units with high agency utilization see **7.7% higher** permanent RN turnover? The 'solution' is driving the problem.",
    "Did you know: High temporary staff units see a **6.44% increase** in pressure ulcers? Staffing decisions are patient safety decisions.",
    "Did you know: **HCAHPS 'Perceived Safety'** scores drop 50+ points in units with high temp staff? Patients are expert witnesses.",
    "Did you know: Replacing one RN costs **$61,100+**? A single bad hire often costs more than most agency fees.",
    "Did you know: Job boards post a **500:1** applicant-to-hire ratio? That's proof of failed screening, not successful sourcing.",
    "Did you know: **70% of candidates** are passive — not looking. Job boards only reach the 30% who are. Nava goes where the talent actually is.",
    "Did you know: A single unfilled vacancy forces remaining staff to work extra shifts. Overtime burns them out. Burnout spreads to their colleagues. More people quit. More vacancies open. The facility reaches for agency nurses, eventually depending on them permanently.",
    "Did you know: In **Ruelas v. Staff Builders**, hospitals bear **100% liability** for agency staff regardless of contractual provisions? Agencies are legally meaningless in court.",
    "Did you know: The **90-day guarantee** protects the agency's fee, not your outcomes? It doesn't prevent bad hires — it just shifts the loss to you.",
    "Did you know: **Pre-boarding** alone delivers **11% better retention**? What happens before day one predicts what happens on year one.",
    "Did you know: **72% of new hires** experience a jarring disconnect between the job description and day-to-day reality? 20% leave within 45 days.",
    "Did you know: **$100,000** — annual savings per Reclaimix conversion? One agency nurse converted pays for itself many times over.",
    "Did you know: **$79,100** — annual savings per travel nurse replaced by a NurseSphere permanent hire? Permanent is cheaper than perpetual.",
    "Did you know: EB-3 and TN aren't competitors — they're **parallel tracks** for different strategic horizons? Urgent need today vs. culture-building for tomorrow.",
    "Did you know: **Schedule A** processing bypasses the standard PERM backlog? What normally takes years can move in months for the right candidates.",
    "Did you know: The average hospital bleeds **$3.9M–$5.7M** annually to turnover? That's not a line item — it's an existential leak.",
    "Did you know: **57% of healthcare turnover** happens within the first 90 days? The 90-day 'guarantee' is a loophole, not a safeguard.",
    "Did you know: **83 days** — industry average RN time-to-fill? That's the baseline. Most facilities are working with broken math.",
    "Did you know: **275,000+ additional nurses** needed by 2030? The WHO projects a 9–10 million RN deficit globally. This isn't a hiring problem — it's a structural crisis.",
    "Did you know: 56% efficiency loss from using interpreters as the primary communication model? Bilingual clinicians aren't an accommodation — they're a throughput multiplier.",
]

def get_expanded_finding(fingerprint):
    """Return an expanded finding object, avoiding repeats until pool is exhausted."""
    shown = db.get_finding_shown(fingerprint) or []
    available = [f for f in EXPANDED_FINDINGS if f["fact"] not in shown]
    if not available:
        # Reset and try again
        db.reset_findings(fingerprint)
        available = EXPANDED_FINDINGS
    finding_obj = available[0]
    shown.append(finding_obj["fact"])
    db.set_finding_shown(fingerprint, shown)
    return finding_obj

def get_finding(fingerprint):
    """Legacy wrapper — return just the fact string."""
    obj = get_expanded_finding(fingerprint)
    return obj["fact"]

# --- Helpers ---

def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    return forwarded or request.remote_addr or "unknown"

def require_token(f):
    def wrapped(*args, **kwargs):
        header_token = request.headers.get("X-Access-Token", "")
        query_token = request.args.get("token", "")
        token = header_token or query_token
        if not token or token != ACCESS_TOKEN:
            return jsonify({"error": "Access denied."}), 401
        return f(*args, **kwargs)
    return wrapped

def clean_for_display(text):
    import re
    text = re.sub(r'^```.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\*{3}([^*]+)\*{3}', r'<em><strong>\1</strong></em>', text)
    text = re.sub(r'\*{2}([^*]+)\*{2}', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_{2}([^_]+)_{2}', r'<strong>\1</strong>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    text = re.sub(r'\n{3,}', r'\n\n', text)
    return text.strip()


# --- Gateway ---

def ws_connect():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    device_json = json.loads(Path("/root/.openclaw/identity/device.json").read_text())
    device_auth_json = json.loads(Path("/root/.openclaw/identity/device-auth.json").read_text())
    device_id = device_json["deviceId"]
    public_key_pem = device_json["publicKeyPem"]
    private_key_pem = device_json["privateKeyPem"]
    operator_token = device_auth_json["tokens"]["operator"]["token"]
    ws = ws_client.connect(GATEWAY_URL, max_size=10 * 1024 * 1024)
    challenge = json.loads(ws.recv())
    nonce = challenge["payload"]["nonce"]
    ts_ms = challenge["payload"]["ts"]
    scopes_str = "operator.read,operator.write"
    v2_payload = f"v2|{device_id}|cli|cli|operator|{scopes_str}|{ts_ms}|{operator_token}|{nonce}"
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None, backend=default_backend())
    sig = private_key.sign(v2_payload.encode())
    sig_b64u = base64.urlsafe_b64encode(sig).rstrip(b'=').decode()
    connect_req = {
        "type": "req", "id": "conn-1", "method": "connect",
        "params": {
            "minProtocol": 3, "maxProtocol": 3,
            "client": {"id": "cli", "version": "2026.4.24", "platform": "linux", "mode": "cli"},
            "role": "operator", "scopes": ["operator.read", "operator.write"],
            "auth": {"token": operator_token}, "userAgent": "dusk-relay/2.0",
            "device": {"id": device_id, "publicKey": public_key_pem, "signature": sig_b64u, "signedAt": ts_ms, "nonce": nonce}
        }
    }
    ws.send(json.dumps(connect_req))
    resp = json.loads(ws.recv())
    if resp.get("type") != "res" or not resp.get("ok"):
        raise Exception(f"Connect failed: {resp}")
    return ws


def create_isolated_session():
    ws = ws_connect()
    req_id = str(uuid.uuid4())[:8]
    ws.send(json.dumps({"type": "req", "id": req_id, "method": "sessions.create", "params": {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == req_id and resp.get("type") == "res":
            break
    ws.close()
    payload = resp.get("payload", {})
    return payload.get("key"), payload.get("entry", {}).get("sessionFile")


def init_session(session_key):
    ws = ws_connect()
    req_id = str(uuid.uuid4())[:8]
    ws.send(json.dumps({
        "type": "req", "id": req_id, "method": "sessions.send",
        "params": {"key": session_key, "message": INIT_MESSAGE, "idempotencyKey": req_id}
    }))
    try:
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") == req_id and resp.get("type") == "res":
                break
    except Exception:
        pass
    ws.close()


def create_and_init_session_background(fingerprint):
    """Create session and warm it up while user reads the canned response."""
    try:
        session_key, session_file = create_isolated_session()
        db.save_session(fingerprint, session_key, session_file)
        init_session(session_key)
    except Exception as e:
        print(f"Error creating background session for {fingerprint}: {e}")


def wait_for_session(fingerprint, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        sess = db.get_session(fingerprint)
        if sess and sess.get('session_key'):
            return sess['session_key'], sess['session_file']
        time.sleep(1)
    raise Exception("Session creation timed out.")


def get_line_count(session_file):
    try:
        lines = Path(session_file).read_text().strip().split("\n")
        return len([l for l in lines if l.strip()])
    except:
        return 0


def get_new_response(session_file, line_count_before):
    try:
        lines = Path(session_file).read_text().strip().split("\n")
        new_lines = lines[line_count_before:]
        for line in reversed(new_lines):
            if not line.strip():
                continue
            msg = json.loads(line)
            if msg.get("type") == "message" and msg.get("message", {}).get("role") == "assistant":
                content = msg.get("message", {}).get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if c.get("type") == "text":
                            return c["text"]
                elif isinstance(content, str) and content:
                    return content
    except:
        pass
    return None


def wait_for_response(session_key, session_file, message, ticket_id):
    line_count_before = get_line_count(session_file)
    try:
        ws = ws_connect()
        req_id = str(uuid.uuid4())[:8]
        ws.send(json.dumps({
            "type": "req", "id": req_id, "method": "sessions.send",
            "params": {"key": session_key, "message": message, "idempotencyKey": req_id}
        }))
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") == req_id:
                break
        ws.close()
    except Exception as e:
        db.set_ticket_response(ticket_id, "Failed to send message over gateway.")
        return
    start = time.time()
    last_check = 0
    while time.time() - start < MAX_POLL_WAIT:
        if time.time() - last_check < POLL_INTERVAL:
            time.sleep(0.5)
            continue
        last_check = time.time()
        resp_text = get_new_response(session_file, line_count_before)
        if resp_text:
            db.set_ticket_response(ticket_id, clean_for_display(resp_text))
            return
    db.set_ticket_response(ticket_id, "Sorry, I'm taking longer than expected. Please try again.")


def notify_main_session(message):
    try:
        ws = ws_connect()
        req_id = str(uuid.uuid4())[:8]
        ws.send(json.dumps({
            "type": "req", "id": req_id, "method": "sessions.send",
            "params": {"key": "agent:main:dashboard:default", "message": message, "idempotencyKey": req_id}
        }))
        ws.close()
    except:
        pass


# --- Routes ---

@app.route("/")
def index():
    return send_file(os.path.join(DIR, "index.html"), max_age=0)


@app.route("/message", methods=["POST"])
@require_token
def handle_message():
    db.cleanup_stale_rate_limits()
    client_ip = get_client_ip()
    allowed, remaining, reset_in = db.check_rate_limit(client_ip)
    if not allowed:
        return jsonify({"error": "Rate limit exceeded.", "retryAfter": reset_in}), 429

    data = request.get_json()
    fingerprint = data.get("fingerprint")
    message = data.get("message", "").strip()

    if not fingerprint or not message:
        return jsonify({"error": "Missing fingerprint or message"}), 400

    user = db.get_user(fingerprint)

    # CASE 1: Brand new user
    if not user:
        if message.startswith("BTN:"):
            parts = message.split("|", 1)
            btn_id = parts[0].replace("BTN:", "")
            first_context = parts[1] if len(parts) > 1 else ""
            if btn_id == "3":
                obj = get_expanded_finding(fingerprint)
                canned = (
                    f"{obj['fact']}\n\n"
                    f"**Why this matters**: {obj['background']}\n\n"
                    f"**The real impact**: {obj['impact']}\n\n"
                    f"**Explore more**: {obj['categories']}\n\n"
                    f"What specific challenges are you currently seeing at your facility? And what's your name?"
                )
            else:
                canned = CANNNED_RESPONSES.get(btn_id, "Hi! What's your name?")
        else:
            first_context = message
            canned = "Hi, I'm Dusk — Nava's assistant. Before I answer that, what's your name?"

        db.create_user_state(fingerprint, state="waiting_for_name", first_context=first_context)
        threading.Thread(target=create_and_init_session_background, args=(fingerprint,), daemon=True).start()
        return jsonify({"immediate_response": clean_for_display(canned), "remaining": remaining})

    # CASE 2: Waiting for name (user just typed their name, OR clicked a button)
    elif user.get('state') == "waiting_for_name":
        # Intercept button clicks even when waiting for name
        if message.startswith('BTN:'):
            parts = message.split('|', 1)
            btn_id = parts[0].replace('BTN:', '')
            first_context = user.get('first_context', '')
            if btn_id == '3':
                obj = get_expanded_finding(fingerprint)
                canned = (
                    f"{obj['fact']}\n\n"
                    f"**Why this matters**: {obj['background']}\n\n"
                    f"**The real impact**: {obj['impact']}\n\n"
                    f"**Explore more**: {obj['categories']}\n\n"
                    f"What specific challenges are you currently seeing at your facility? And what's your name?"
                )
            else:
                canned = CANNNED_RESPONSES.get(btn_id, "Hi! What's your name?")
            return jsonify({"immediate_response": clean_for_display(canned), "remaining": remaining})

        # Normal name entry
        name = message
        db.set_user_name(fingerprint, name)
        db.create_user_state(fingerprint, state="active", name=name)
        first_context = user.get('first_context', '')

        prefixed_message = (
            INIT_MESSAGE + "\n\n"
            f"The user's name is {name}. They just provided it.\n"
            f"Their first context / question was: {first_context}\n\n"
            f"Reply naturally to their first context, addressing them by their name {name}."
        )

        try:
            session_key, session_file = wait_for_session(fingerprint, timeout=30)
        except Exception:
            return jsonify({"error": "Agent failed to warm up in time."}), 500

        ticket_id = str(uuid.uuid4())
        db.create_ticket(ticket_id, fingerprint)
        threading.Thread(
            target=wait_for_response,
            args=(session_key, session_file, prefixed_message, ticket_id),
            daemon=True
        ).start()
        return jsonify({"ticket": ticket_id, "remaining": remaining})

    # CASE 3: Active / returning user
    else:
        name = user.get('name') or "the user"
        first_context = user.get('first_context', '')

        # Build context including the button they clicked (if any) so the agent knows what's being referenced
        btn_context = f"\n\nContext from this conversation: {first_context}" if first_context else ""

        prefixed_message = (
            INIT_MESSAGE + "\n\n"
            f"The user ({name}) is continuing a conversation.{btn_context}\n\n"
            f"Their message: {message}\n\n"
            f"Reply naturally, addressing them by their name ({name}). "
            f"They may be referring to something from the button response above."
        )
        sess = db.get_session(fingerprint)
        if not sess or not sess.get('session_key'):
            threading.Thread(target=create_and_init_session_background, args=(fingerprint,), daemon=True).start()
            try:
                session_key, session_file = wait_for_session(fingerprint, timeout=30)
            except Exception:
                return jsonify({"error": "Agent failed to warm up in time."}), 500
        else:
            session_key, session_file = sess['session_key'], sess['session_file']

        ticket_id = str(uuid.uuid4())
        db.create_ticket(ticket_id, fingerprint)
        threading.Thread(
            target=wait_for_response,
            args=(session_key, session_file, prefixed_message, ticket_id),
            daemon=True
        ).start()
        return jsonify({"ticket": ticket_id, "remaining": remaining})


@app.route("/response", methods=["GET"])
def get_response():
    db.cleanup_stale_tickets()
    ticket_id = request.args.get("ticket", "").strip()
    if not ticket_id:
        return jsonify({"error": "Missing ticket"}), 400
    resp = db.get_ticket_response(ticket_id)
    if resp is not None:
        if "[INTERVIEW_COMPLETE]" in resp:
            resp = resp.replace("[INTERVIEW_COMPLETE]", "").strip()
            db.set_ticket_response(ticket_id, resp)
            notify_main_session("Interview complete!")
        return jsonify({"response": resp})
    return jsonify({"pending": True})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    print(f"Starting Dusk relay V2 on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
