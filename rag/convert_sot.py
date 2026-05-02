#!/usr/bin/env python3
"""Convert SoT .docx files to clean plain text for RAG corpus."""

import os
from docx import Document

SRC_DIR = "/root/.openclaw/workspace/SoT-Collection"
OUT_DIR = "/root/.openclaw/workspace/rag/sot-clean"

os.makedirs(OUT_DIR, exist_ok=True)

files = [f for f in os.listdir(SRC_DIR) if f.endswith(".docx")]
files.sort()

converted = []
failed = []

for fname in files:
    docx_path = os.path.join(SRC_DIR, fname)
    # Build output filename: sot_Preserved_Name.txt
    base = os.path.splitext(fname)[0]
    # Strip trailing (1) style duplicates for output name
    out_name = base.replace(" ", "_").replace("&", "_").replace(",", "").replace("__", "_") + ".txt"
    out_name = "sot_" + out_name
    out_path = os.path.join(OUT_DIR, out_name)

    try:
        doc = Document(docx_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        content = "\n\n".join(paragraphs)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        word_count = len(content.split())
        converted.append((fname, out_name, word_count))
    except Exception as e:
        failed.append((fname, str(e)))

print(f"\n{'='*60}")
print(f"CONVERSION REPORT")
print(f"{'='*60}")
print(f"Total .docx files found: {len(files)}")
print(f"Successfully converted: {len(converted)}")
print(f"Failed: {len(failed)}")
total_words = sum(x[2] for x in converted)
print(f"Total word count (converted): {total_words:,}")
print()

if converted:
    print(f"{'Source File':<50} {'Output File':<55} {'Words'}")
    print("-" * 115)
    for src, out, wc in converted:
        print(f"{src:<50} {out:<55} {wc:,}")

if failed:
    print(f"\nFAILED FILES:")
    for fname, err in failed:
        print(f"  {fname}: {err}")

print(f"\nOutput directory: {OUT_DIR}")