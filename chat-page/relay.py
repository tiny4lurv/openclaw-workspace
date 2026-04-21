#!/usr/bin/env python3
"""
Flask relay for Dusk public chat page.
Receives messages from public page, sends to OpenClaw gateway via WebSocket,
and delivers responses via polling.
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
from websockets.exceptions import ConnectionClosed

DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=DIR)

# --- Config ---
QR_NOTEBOOK = Path("/root/.openclaw/workspace/memory/qr-notebook.md")
NAMES_FILE = Path("/root/.openclaw/workspace/chat-page/names.json")
NAMES_FILE.parent.mkdir(parents=True, exist_ok=True)
if not NAMES_FILE.exists():
    NAMES_FILE.write_text("{}")

INIT_MESSAGE = (
    "You are Dusk. Keep your answer to exactly 2 sentences. Plain text only — no bold, no bullets, no markdown. "
    "Read memory/qr-notebook.md before answering. Answer only from what you read there. "
    "If the answer is not in the QR-Notebook, reply with exactly: I don't know that. "
    "Do not web-search. Do not guess. Do not ramble."
    # Name instruction injected at message time via prefixed_message
)

GATEWAY_URL = "ws://127.0.0.1:18789/__openclaw__/gateway"
SESSION_STORE = Path("/root/.openclaw/workspace/chat-page/sessions.json")
SESSION_STORE.parent.mkdir(parents=True, exist_ok=True)
if not SESSION_STORE.exists():
    SESSION_STORE.write_text("{}")

PENDING_FILE = Path("/root/.openclaw/workspace/chat-page/pending.json")
if not PENDING_FILE.exists():
    PENDING_FILE.write_text("{}")

INTERVIEWS_DIR = Path("/root/.openclaw/workspace/chat-page/interviews")
INTERVIEWS_DIR.mkdir(parents=True, exist_ok=True)

MAX_POLL_WAIT = 120
POLL_INTERVAL = 1

# Secret token for access control — change this to a secure value
ACCESS_TOKEN = "nava-dusk-2026"

# Rate limiting: max requests per IP within a time window
MAX_REQUESTS_PER_IP = 20
RATE_WINDOW_SECONDS = 60


# --- Helpers ---

def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))

def create_isolated_session():
    """Create a new isolated agent session via gateway WebSocket. Returns (session_key, session_file_path)."""
    ws = ws_connect()
    
    req_id = str(uuid.uuid4())[:8]
    create_req = {
        "type": "req",
        "id": req_id,
        "method": "sessions.create",
        "params": {}
    }
    ws.send(json.dumps(create_req))
    
    # Read responses until we get the one with matching id
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == req_id and resp.get("type") == "res":
            break
    
    ws.close()
    
    if not resp.get("ok"):
        raise Exception(f"Failed to create session: {resp}")
    
    payload = resp.get("payload", {})
    session_key = payload.get("key")
    session_file = payload.get("entry", {}).get("sessionFile")
    
    if not session_key or not session_file:
        raise Exception(f"Invalid session create response: {payload}")
    
    return session_key, session_file

def init_session(session_key):
    """Send initialization message to a new session to load QR-Notebook and set rules."""
    ws = ws_connect()
    req_id = str(uuid.uuid4())[:8]
    send_req = {
        "type": "req",
        "id": req_id,
        "method": "sessions.send",
        "params": {
            "key": session_key,
            "message": INIT_MESSAGE,
            "idempotencyKey": req_id
        }
    }
    ws.send(json.dumps(send_req))
    try:
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") == req_id and resp.get("type") == "res":
                break
    except Exception:
        pass
    ws.close()


def get_or_create_session(fingerprint):
    """Map fingerprint to session. Creates a new isolated session if needed."""
    sessions = load_json(SESSION_STORE)
    if fingerprint not in sessions:
        # Create a new isolated session
        session_key, session_file = create_isolated_session()
        sessions[fingerprint] = {
            "sessionKey": session_key,
            "sessionFile": session_file,
            "sessionId": session_file.split("/")[-1].replace(".jsonl", "")
        }
        save_json(SESSION_STORE, sessions)
    return sessions[fingerprint]["sessionKey"]

def get_session_file(fingerprint):
    """Get session file path for a fingerprint. Handles both old (string) and new (dict) formats."""
    sessions = load_json(SESSION_STORE)
    if fingerprint not in sessions:
        return None
    entry = sessions[fingerprint]
    if isinstance(entry, dict):
        return entry.get("sessionFile")
    # Old format: stored as session key string — extract session ID from key
    # Format: agent:main:dashboard:UUID → session file is /root/.../sessions/UUID.jsonl
    if isinstance(entry, str) and entry.startswith("agent:main:dashboard:"):
        session_id = entry.split(":")[-1]
        return f"/root/.openclaw/agents/main/sessions/{session_id}.jsonl"
    return None

def add_pending(ticket, session_key, fingerprint):
    pending = load_json(PENDING_FILE)
    pending[ticket] = {"session_key": session_key, "fingerprint": fingerprint, "response": None, "timestamp": time.time()}
    save_json(PENDING_FILE, pending)

def set_response(ticket, response):
    pending = load_json(PENDING_FILE)
    if ticket in pending:
        pending[ticket]["response"] = response
        save_json(PENDING_FILE, pending)

def get_pending(ticket):
    pending = load_json(PENDING_FILE)
    if ticket in pending and pending[ticket]["response"] is not None:
        return pending[ticket]["response"]
    return None

def cleanup_stale_pending():
    """Remove pending entries older than 5 minutes (no response received)."""
    now = time.time()
    pending = load_json(PENDING_FILE)
    stale = [tid for tid, data in pending.items()
             if now - data.get("timestamp", 0) > 300]
    for tid in stale:
        del pending[tid]
    if stale:
        save_json(PENDING_FILE, pending)

# --- Rate limiting tracking ---
RATE_FILE = Path("/root/.openclaw/workspace/chat-page/rate_limits.json")
if not RATE_FILE.exists():
    RATE_FILE.write_text("{}")

def get_client_ip():
    """Get client IP from request, handling proxies."""
    # Check X-Forwarded-For header (set by proxies/serveo)
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if forwarded:
        return forwarded
    return request.remote_addr or "unknown"

def check_rate_limit(ip):
    """Check if IP is within rate limits. Returns (allowed, remaining, reset_in)"""
    now = time.time()
    limits = load_json(RATE_FILE)
    
    if ip not in limits:
        limits[ip] = {"count": 0, "window_start": now}
    
    window_start = limits[ip].get("window_start", now)
    count = limits[ip].get("count", 0)
    
    # Reset window if expired
    if now - window_start >= RATE_WINDOW_SECONDS:
        limits[ip] = {"count": 0, "window_start": now}
        count = 0
        window_start = now
    
    if count >= MAX_REQUESTS_PER_IP:
        reset_in = int(RATE_WINDOW_SECONDS - (now - window_start))
        return False, 0, max(reset_in, 0)
    
    limits[ip]["count"] = count + 1
    save_json(RATE_FILE, limits)
    
    remaining = MAX_REQUESTS_PER_IP - count - 1
    return True, remaining, RATE_WINDOW_SECONDS

def cleanup_stale_rate_limits():
    """Remove rate limit entries for IPs that are no longer active."""
    now = time.time()
    limits = load_json(RATE_FILE)
    stale = [ip for ip, data in limits.items() 
             if now - data.get("window_start", 0) > RATE_WINDOW_SECONDS * 2]
    for ip in stale:
        del limits[ip]
    if stale:
        save_json(RATE_FILE, limits)

def require_token(f):
    """Decorator to require valid access token."""
    def wrapped(*args, **kwargs):
        # Check token from header or query param
        header_token = request.headers.get("X-Access-Token", "")
        query_token = request.args.get("token", "")
        token = header_token or query_token
        
        if not token or token != ACCESS_TOKEN:
            return jsonify({"error": "Access denied. Invalid or missing token."}), 401
        
        return f(*args, **kwargs)
    return wrapped

def get_line_count(session_file):
    """Get current line count of session file."""
    if not session_file:
        return 0
    try:
        lines = Path(session_file).read_text().strip().split("\n")
        return len([l for l in lines if l.strip()])
    except Exception:
        return 0

def get_new_response(session_file, line_count_before):
    """Get latest assistant text from session file lines after line_count_before."""
    if not session_file:
        return None

    try:
        lines = Path(session_file).read_text().strip().split("\n")
    except Exception:
        return None

    new_lines = lines[line_count_before:]
    for line in reversed(new_lines):
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
            if msg.get("type") == "message" and msg.get("message", {}).get("role") == "assistant":
                content = msg.get("message", {}).get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if c.get("type") == "text":
                            return c["text"]
                elif isinstance(content, str) and content:
                    return content
        except Exception:
            continue
    return None


# --- Gateway ---

def ws_connect():
    """Connect to gateway and complete handshake with device auth."""
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
    if challenge.get("type") != "event" or challenge.get("event") != "connect.challenge":
        raise Exception("Expected connect.challenge")

    nonce = challenge["payload"]["nonce"]
    ts_ms = challenge["payload"]["ts"]

    scopes_str = "operator.read,operator.write"
    v2_payload = f"v2|{device_id}|cli|cli|operator|{scopes_str}|{ts_ms}|{operator_token}|{nonce}"

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(), password=None, backend=default_backend()
    )
    sig = private_key.sign(v2_payload.encode())
    sig_b64u = base64.urlsafe_b64encode(sig).rstrip(b'=').decode()

    connect_req = {
        "type": "req",
        "id": "conn-1",
        "method": "connect",
        "params": {
            "minProtocol": 3,
            "maxProtocol": 3,
            "client": {"id": "cli", "version": "2026.4.11", "platform": "linux", "mode": "cli"},
            "role": "operator",
            "scopes": ["operator.read", "operator.write"],
            "auth": {"token": operator_token},
            "locale": "en-US",
            "userAgent": "dusk-relay/1.0",
            "device": {
                "id": device_id,
                "publicKey": public_key_pem,
                "signature": sig_b64u,
                "signedAt": ts_ms,
                "nonce": nonce
            }
        }
    }
    ws.send(json.dumps(connect_req))

    resp = json.loads(ws.recv())
    if resp.get("type") != "res" or not resp.get("ok"):
        raise Exception(f"Connect failed: {resp}")

    return ws


def wait_for_response(session_key, session_file, message, ticket):
    """Connect, send message, poll session file for new assistant response."""
    line_count_before = get_line_count(session_file)

    ws = ws_connect()

    req_id = str(uuid.uuid4())[:8]
    send_req = {
        "type": "req",
        "id": req_id,
        "method": "sessions.send",
        "params": {
            "key": session_key,
            "message": message,
            "idempotencyKey": req_id
        }
    }
    ws.send(json.dumps(send_req))

    # Read ack
    ack_ok = False
    try:
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") == req_id and resp.get("type") == "res":
                ack_ok = resp.get("ok", False)
                break
    except Exception:
        pass

    ws.close()

    if not ack_ok:
        set_response(ticket, "Failed to send message. Please try again.")
        return

    # Poll session file
    start = time.time()
    last_check = 0
    while time.time() - start < MAX_POLL_WAIT:
        if time.time() - last_check < POLL_INTERVAL:
            time.sleep(0.5)
            continue
        last_check = time.time()

        response = get_new_response(session_file, line_count_before)
        if response:
            set_response(ticket, response)
            return

    set_response(ticket, "Sorry, I'm taking longer than expected. Please try again.")


# --- Interview helpers ---

def save_interview(fingerprint, qna):
    """Save interview Q&A to a JSON file. Returns filename."""
    names = load_json(NAMES_FILE)
    name = names.get(fingerprint)
    
    timestamp = time.strftime("%Y-%m-%d_%H%M%S")
    short_ts = timestamp.split("_")[1] + timestamp.split("_")[2]  # HHMMSS
    filename = f"{timestamp}_{short_ts[-3:]}.json"
    filepath = INTERVIEWS_DIR / filename
    
    interview_data = {
        "name": name or "Unknown",
        "fingerprint": fingerprint,
        "started_at": qna.get("started_at", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "qna": qna.get("qna", [])
    }
    save_json(filepath, interview_data)
    return filename


def notify_main_session(message):
    """Send a message to the main Dusk session via gateway WebSocket."""
    try:
        ws = ws_connect()
        req_id = str(uuid.uuid4())[:8]
        send_req = {
            "type": "req",
            "id": req_id,
            "method": "sessions.send",
            "params": {
                "key": "agent:main:dashboard:default",
                "message": message,
                "idempotencyKey": req_id
            }
        }
        ws.send(json.dumps(send_req))
        try:
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == req_id and resp.get("type") == "res":
                    break
        except Exception:
            pass
        ws.close()
    except Exception:
        pass  # Non-critical if main session notification fails


# --- Routes ---

@app.route("/")
def index():
    return send_file(os.path.join(DIR, "index.html"))

@app.route("/message", methods=["POST"])
@require_token
def handle_message():
    """
    Receive a message from the public page.
    Body: { "fingerprint": "uuid", "message": "text", "interview_mode": bool, "interview_data": {...} }
    Returns: { "ticket": "uuid" }
    """
    client_ip = get_client_ip()
    allowed, remaining, reset_in = check_rate_limit(client_ip)
    if not allowed:
        return jsonify({
            "error": "Rate limit exceeded. Please try again later.",
            "retryAfter": reset_in
        }), 429

    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    fingerprint = data.get("fingerprint")
    message = data.get("message", "").strip()
    interview_mode = data.get("interview_mode", False)
    interview_data = data.get("interview_data")

    if not fingerprint or not message:
        return jsonify({"error": "missing fingerprint or message"}), 400

    session_info = get_or_create_session(fingerprint)
    session_key = session_info
    session_file = get_session_file(fingerprint)
    ticket = str(uuid.uuid4())

    add_pending(ticket, session_key, fingerprint)

    # Load name for this fingerprint
    names = load_json(NAMES_FILE)
    user_name = names.get(fingerprint)

    # Build name context for prefixed message
    if user_name:
        name_context = f"The user's name is {user_name}."
    else:
        name_context = "You don't know their name yet. Ask for it early in the conversation."

    # Prepend INIT_MESSAGE + name context to user message
    prefixed_message = INIT_MESSAGE + "\n\n" + name_context + "\n\nUser question: " + message

    # Handle interview mode
    if interview_mode and interview_data:
        # Store Q&A as it comes in
        qna_file_key = f"interview_{fingerprint}"
        pending = load_json(PENDING_FILE)
        if qna_file_key not in pending:
            pending[qna_file_key] = {"qna": [], "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
        pending[qna_file_key]["qna"].append({
            "q": interview_data.get("question", ""),
            "a": message
        })
        pending[qna_file_key]["fingerprint"] = fingerprint
        pending[qna_file_key]["name"] = user_name
        save_json(PENDING_FILE, pending)

        # Check for [INTERVIEW_COMPLETE] signal in message from agent's perspective
        # We check the incoming message for the completion signal (agent sends it to us)
        # Actually, the agent sends [INTERVIEW_COMPLETE] in the response to the user.
        # We detect it in the response before delivering it to the user.
        pass

    try:
        thread = threading.Thread(
            target=wait_for_response,
            args=(session_key, session_file, prefixed_message, ticket),
            daemon=True
        )
        thread.start()

        return jsonify({"ticket": ticket, "remaining": remaining})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/response", methods=["GET"])
def get_response():
    """
    Poll for response to a ticket.
    Query: ?ticket=uuid&token=xyz
    Returns: { "response": "text" } or { "pending": true }
    Also checks for [INTERVIEW_COMPLETE] and handles interview completion.
    """
    # Rate limit check on polling too
    client_ip = get_client_ip()
    cleanup_stale_pending()
    cleanup_stale_rate_limits()
    
    ticket = request.args.get("ticket", "").strip()
    if not ticket:
        return jsonify({"error": "missing ticket"}), 400

    response = get_pending(ticket)
    if response is not None:
        # Check for interview completion signal
        if "[INTERVIEW_COMPLETE]" in response:
            # Clean up the signal from what we return to the user
            response = response.replace("[INTERVIEW_COMPLETE]", "").strip()
            
            # Get interview data and save
            pending = load_json(PENDING_FILE)
            qna_file_key = "interview_" + pending.get(ticket, {}).get("fingerprint", "")
            interview_pending = pending.get(qna_file_key)
            
            if interview_pending:
                fp = interview_pending.get("fingerprint")
                filename = save_interview(fp, interview_pending)
                
                # Notify main session
                name = interview_pending.get("name", "Unknown")
                notify_main_session(
                    f"Interview complete with {name} (fingerprint: {fp})\n"
                    f"Review at: /root/.openclaw/workspace/chat-page/interviews/{filename}"
                )
                
                # Clean up
                if qna_file_key in pending:
                    del pending[qna_file_key]
                    save_json(PENDING_FILE, pending)
        
        return jsonify({"response": response})

    return jsonify({"pending": True})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    print(f"Starting Dusk relay on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True)