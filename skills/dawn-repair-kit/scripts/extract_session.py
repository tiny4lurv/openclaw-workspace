#!/usr/bin/env python3
"""Extract messages from OpenClaw JSONL session files for analysis."""

import json
import sys
from datetime import datetime

def extract_session_messages(filepath, max_messages=None):
    """Extract user and assistant messages from a JSONL session file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    messages = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            if obj.get('type') == 'message':
                role = obj['message'].get('role', '')
                if role in ('user', 'assistant'):
                    ts = obj.get('timestamp', '')
                    content = obj['message'].get('content', '')
                    
                    # Extract all text blocks
                    texts = []
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get('type') == 'text':
                                texts.append(block.get('text', ''))
                    
                    full_text = '\n'.join(texts)
                    messages.append({
                        'index': i,
                        'timestamp': ts,
                        'role': role,
                        'text': full_text
                    })
        except Exception as e:
            pass
    
    return messages

def format_messages(messages, max_length=500):
    """Format messages for readable output."""
    output = []
    for msg in messages:
        ts = msg['timestamp']
        role = msg['role'].upper()
        text = msg['text'][:max_length]
        if len(msg['text']) > max_length:
            text += '... [TRUNCATED]'
        output.append(f"[{ts}] {role}: {text}")
    return '\n'.join(output)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_session.py <session.jsonl>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    messages = extract_session_messages(filepath)
    
    print(f"=== {filepath} ===")
    print(f"Total messages: {len(messages)}")
    print()
    print(format_messages(messages))
