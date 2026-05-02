import sqlite3
import time
import json
from pathlib import Path

DB_PATH = Path("/root/.openclaw/workspace/chat-page/chat.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    fingerprint TEXT PRIMARY KEY,
    name TEXT,
    state TEXT,
    first_context TEXT,
    created_at REAL,
    updated_at REAL
);

CREATE TABLE IF NOT EXISTS sessions (
    fingerprint TEXT PRIMARY KEY,
    session_key TEXT,
    session_file TEXT,
    session_ready INTEGER DEFAULT 0,
    warmup_lines INTEGER DEFAULT NULL,
    created_at REAL
);

CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    fingerprint TEXT,
    response TEXT,
    partial TEXT,
    timestamp REAL
);

CREATE TABLE IF NOT EXISTS rate_limits (
    ip TEXT PRIMARY KEY,
    count INTEGER,
    window_start REAL
);

CREATE TABLE IF NOT EXISTS pending_interviews (
    fingerprint TEXT PRIMARY KEY,
    name TEXT,
    qna TEXT,
    started_at TEXT
);

CREATE TABLE IF NOT EXISTS findings (
    fingerprint TEXT PRIMARY KEY,
    shown TEXT
);
"""


def get_db():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


# --- Users ---

def get_user(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE fingerprint = ?", (fingerprint,)).fetchone()
        return dict(row) if row else None


def create_user_state(fingerprint, state, first_context=None, name=None):
    now = time.time()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO users (fingerprint, name, state, first_context, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(fingerprint) DO UPDATE SET
               state=excluded.state,
               first_context=COALESCE(excluded.first_context, users.first_context),
               name=COALESCE(excluded.name, users.name),
               updated_at=excluded.updated_at""",
            (fingerprint, name, state, first_context, now, now)
        )
        conn.commit()


def set_user_name(fingerprint, name):
    now = time.time()
    with get_db() as conn:
        conn.execute("UPDATE users SET name = ?, updated_at = ? WHERE fingerprint = ?", (name, now, fingerprint))
        conn.commit()


# --- Sessions ---

def save_session_warmup_lines(fingerprint, warmup_lines):
    with get_db() as conn:
        conn.execute(
            "UPDATE sessions SET warmup_lines=? WHERE fingerprint=?",
            (warmup_lines, fingerprint)
        )
        conn.commit()


def save_session(fingerprint, session_key, session_file, ready=0):
    now = time.time()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO sessions (fingerprint, session_key, session_file, session_ready, created_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(fingerprint) DO UPDATE SET
               session_key=excluded.session_key,
               session_file=excluded.session_file,
               session_ready=excluded.session_ready""",
            (fingerprint, session_key, session_file, ready, now)
        )
        conn.commit()


def mark_session_ready(fingerprint):
    with get_db() as conn:
        conn.execute("UPDATE sessions SET session_ready=1 WHERE fingerprint=?", (fingerprint,))
        conn.commit()


def get_session_warmup_lines(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT warmup_lines FROM sessions WHERE fingerprint=?", (fingerprint,)).fetchone()
        return row[0] if row else None


def is_session_ready(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT session_ready FROM sessions WHERE fingerprint=?", (fingerprint,)).fetchone()
        return row and row[0] == 1


def get_session(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE fingerprint = ?", (fingerprint,)).fetchone()
        return dict(row) if row else None


# --- Tickets ---

def create_ticket(ticket_id, fingerprint):
    now = time.time()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO tickets (id, fingerprint, timestamp) VALUES (?, ?, ?)",
            (ticket_id, fingerprint, now)
        )
        conn.commit()


def set_ticket_response(ticket_id, response):
    with get_db() as conn:
        conn.execute("UPDATE tickets SET response = ? WHERE id = ?", (response, ticket_id))
        conn.commit()


def update_ticket_partial(ticket_id, partial_content):
    with get_db() as conn:
        conn.execute("UPDATE tickets SET partial = ? WHERE id = ?", (partial_content, ticket_id))
        conn.commit()


def get_ticket_partial(ticket_id):
    with get_db() as conn:
        row = conn.execute("SELECT partial FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        return row['partial'] if row else None


def get_ticket_response(ticket_id):
    with get_db() as conn:
        row = conn.execute("SELECT response FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        return row['response'] if row else None


def cleanup_stale_tickets(max_age_seconds=300):
    now = time.time()
    with get_db() as conn:
        conn.execute("DELETE FROM tickets WHERE (? - timestamp) > ?", (now, max_age_seconds))
        conn.commit()


# --- Rate Limits ---

def check_rate_limit(ip, max_requests=20, window_seconds=60):
    now = time.time()
    with get_db() as conn:
        row = conn.execute("SELECT count, window_start FROM rate_limits WHERE ip = ?", (ip,)).fetchone()
        if not row:
            conn.execute("INSERT INTO rate_limits (ip, count, window_start) VALUES (?, 1, ?)", (ip, now))
            conn.commit()
            return True, max_requests - 1, window_seconds

        count = row['count']
        window_start = row['window_start']

        if now - window_start >= window_seconds:
            conn.execute("UPDATE rate_limits SET count = 1, window_start = ? WHERE ip = ?", (now, ip))
            conn.commit()
            return True, max_requests - 1, window_seconds

        if count >= max_requests:
            reset_in = max(int(window_seconds - (now - window_start)), 0)
            return False, 0, reset_in

        conn.execute("UPDATE rate_limits SET count = count + 1 WHERE ip = ?", (ip,))
        conn.commit()
        return True, max_requests - count - 1, window_seconds


def cleanup_stale_rate_limits(window_seconds=60):
    now = time.time()
    with get_db() as conn:
        conn.execute("DELETE FROM rate_limits WHERE (? - window_start) > ?", (now, window_seconds * 2))
        conn.commit()


# --- Findings ---

def get_finding_shown(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT shown FROM findings WHERE fingerprint = ?", (fingerprint,)).fetchone()
        if row and row['shown']:
            return json.loads(row['shown'])
        return None


def set_finding_shown(fingerprint, shown_list):
    with get_db() as conn:
        conn.execute(
            """INSERT INTO findings (fingerprint, shown) VALUES (?, ?)
               ON CONFLICT(fingerprint) DO UPDATE SET shown=excluded.shown""",
            (fingerprint, json.dumps(shown_list))
        )
        conn.commit()


def reset_findings(fingerprint):
    with get_db() as conn:
        conn.execute("DELETE FROM findings WHERE fingerprint = ?", (fingerprint,))
        conn.commit()


# --- Interviews ---

def get_pending_interview(fingerprint):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM pending_interviews WHERE fingerprint = ?", (fingerprint,)).fetchone()
        if row:
            d = dict(row)
            d['qna'] = json.loads(d['qna'])
            return d
        return None


def append_interview_qna(fingerprint, name, question, answer):
    with get_db() as conn:
        row = conn.execute("SELECT qna, started_at FROM pending_interviews WHERE fingerprint = ?", (fingerprint,)).fetchone()
        qna_list = []
        started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if row:
            qna_list = json.loads(row['qna'])
            started_at = row['started_at']
        qna_list.append({"q": question, "a": answer})
        conn.execute(
            """INSERT INTO pending_interviews (fingerprint, name, qna, started_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(fingerprint) DO UPDATE SET
               qna=excluded.qna, name=excluded.name""",
            (fingerprint, name, json.dumps(qna_list), started_at)
        )
        conn.commit()


def delete_pending_interview(fingerprint):
    with get_db() as conn:
        conn.execute("DELETE FROM pending_interviews WHERE fingerprint = ?", (fingerprint,))
        conn.commit()


init_db()
