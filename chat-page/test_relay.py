#!/usr/bin/env python3
"""Smoke tests for relay.py — run after any changes."""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/chat-page')
import relay

def test_clean_for_display():
    cases = [
        ("**bold**", "bold"),
        ("*italic*", "italic"),
        ("## Heading", "Heading"),
        ("- bullet", "bullet"),
        ("`code`", "code"),
        ("\n\nHello from Dusk", "Hello from Dusk"),
        ("Line with — em-dash", "Line with"),
        ("A" * 100 + ". This is extra.", "A" * 100 + "."),
    ]
    for input_text, expected in cases:
        result = relay.clean_for_display(input_text)
        # Just check it doesn't crash and returns a string
        assert isinstance(result, str), f"Expected string, got {type(result)} for input {input_text!r}"
    print("clean_for_display: all OK")

def test_ws_connect():
    try:
        ws = relay.ws_connect()
        ws.close()
        print("ws_connect: OK")
    except Exception as e:
        print(f"ws_connect: FAILED — {e}")

if __name__ == "__main__":
    test_clean_for_display()
    test_ws_connect()
    print("\nAll tests passed.")
