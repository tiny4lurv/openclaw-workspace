#!/usr/bin/env python3
"""
Nightly brief generator for Nava chat page sessions.
Reads session JSONL files, strips system prompts, outputs human-readable markdown.
Run via cron: 0 6 * * * /usr/bin/python3 /root/.openclaw/workspace/chat-page/generate_brief.py
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime, timedelta

SESSIONS_JSON = Path("/root/.openclaw/workspace/chat-page/sessions.json")
NAMES_JSON = Path("/root/.openclaw/workspace/chat-page/names.json")
OUTPUT_DIR = Path("/root/.openclaw/workspace/chat-page/briefs")
INIT_MARKER = "You are Dusk."

def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def get_sessions():
    sessions = load_json(SESSIONS_JSON)
    names = load_json(NAMES_JSON)
    for fp, entry in sessions.items():
        if isinstance(entry, dict):
            sf = entry.get("sessionFile")
        else:
            continue
        if sf and Path(sf).exists():
            mtime = Path(sf).stat().st_mtime
            yield fp, sf, names.get(fp), mtime

def extract_transcript(session_file, name=None):
    lines = Path(session_file).read_text().strip().split("\n")
    msgs = []
    for line in lines:
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
            if msg.get("type") != "message":
                continue
            role = msg["message"].get("role")
            content = msg["message"].get("content", "")
            if isinstance(content, list):
                content = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            if not content:
                continue
            # Strip INIT_MESSAGE echoes
            if INIT_MARKER in content:
                continue
            label = "**You**" if role == "user" else "**Dusk**"
            prefix = f"{label}: "
            if name and ("they" in content.lower() or "the user" in content.lower()):
                content = content.replace("the user", name).replace("they ", f"{name} ")
            msgs.append(f"{prefix}{content}")
        except Exception:
            continue
    return "\n\n".join(msgs) if msgs else "(no readable messages)"

def generate():
    yesterday = datetime.now() - timedelta(days=1)
    output_dir = OUTPUT_DIR / yesterday.strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    sessions = list(get_sessions())
    if not sessions:
        print("No sessions found.")
        return

    index_entries = []
    for fp, sf, name, mtime in sessions:
        session_id = Path(sf).stem
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        preview = extract_transcript(sf, name)
        first_line = preview.split("\n\n")[0][-80:] if preview else "(empty)"

        out_file = output_dir / f"{session_id}.brief.md"
        content = f"# Chat Session — {ts}\n"
        if name:
            content += f"**Name:** {name}\n"
        content += f"**Fingerprint:** {fp}\n\n---\n\n{preview}\n"
        out_file.write_text(content)
        index_entries.append(f"- [{ts}] {name or 'Unknown'} — {first_line}")

    idx = output_dir / "index.brief.md"
    idx.write_text(f"# Briefs — {yesterday.strftime('%Y-%m-%d')}\n\n" + "\n".join(index_entries))
    print(f"Generated {len(index_entries)} brief(s) in {output_dir}")

if __name__ == "__main__":
    generate()