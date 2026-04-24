# Blog-Notebook — Context File

## What These Files Are

This folder (`memory/blog-notebook/`) contains the working notes for Nava Healthcare Recruitment's content pipeline — one file per blog article published on navahc.com.

Each file is a chronologically-organized note taken while reading the source article. The notes capture:
- Key arguments and frameworks
- Statistics and citations
- Branded terminology definitions
- Key quotes and formulations
- Observations about tone, audience, and strategic intent

The files are **chronological research notes**, not finished documents. They are inputs to the synthesis notebooks (qr-notebook.md and nava-notebook.md), not outputs.

## File Inventory

| Entry | Article | Date |
|-------|---------|------|
| 01 | Bilingual Clinicians | Nov 23, 2025 |
| 02 | Bridging the Gap in Medical Recruitment | Jul 29, 2025 |
| 03 | Building a Healthcare Talent Pipeline | Nov 13, 2025 |
| 04 | CMS Staffing Requirements | Dec 15, 2025 |
| 05 | Compliance in Healthcare Staffing | Nov 7, 2025 |
| 06 | Fix Your Flexible Staffing Model | Nov 9, 2025 |
| 07 | Hard-to-Fill Leadership Roles | Nov 20, 2025 |
| 08 | Healthcare Hiring Without Guesswork | Oct 9, 2025 |
| 09 | Healthcare Recruitment Agencies Trust Deficits | Aug 8, 2025 |
| 10 | Healthcare Reputation Management | Nov 13, 2025 |
| 11 | Healthcare Workforce Partnership Models | Nov 26, 2025 |
| 12 | How Medical Staffing Became a Liability | Jul 15, 2025 |
| 13 | How Much Do Healthcare Staffing Agencies Cost | Oct 20, 2025 |
| 14 | How to Evaluate Healthcare Staffing Agency Performance | Oct 23, 2025 |
| 15 | How to Find the Best Medical Recruiting Agencies | Oct 10, 2025 |
| 16 | Is DIY Healthcare Recruiting Truly Cheaper | Oct 23, 2025 |
| 17 | Is Outsourcing Healthcare Staffing Worth It | Oct 13, 2025 |
| 18 | Relational Healthcare Staffing and Recruiting | Oct 29, 2025 |
| 19 | The Anatomy of a Clinician Turnover | Nov 30, 2025 |
| 20 | Why Job Boards Fail Healthcare Recruiters | Jul 22, 2025 |
| 21 | Why Reactive Recruitment in Healthcare Staffing Fails | Nov 5, 2025 |
| 22 | Your Favorite Healthcare Staffing Fails | Jul 8, 2025 |
| 23 | NurseSphere International Nurse Recruitment | Mar 24, 2026 |
| 24 | EB-3 vs. TN | Apr 2, 2026 |

BATCH-01-DONE through BATCH-06-DONE are pipeline markers — batch completion signals from when entries were processed.

## What We Are Trying to Achieve

Tiny is building a research knowledge base for Dusk (and by extension, Dawn) to use when answering employee questions about Nava on the chat page.

The goal is a layered reference system:

1. **QR-Notebook** (`qr-notebook.md`) — Fast-answer reference. One-page synthesis of who Nava is, key stats, frameworks, and talking points. Built for speed on first lookup.
2. **Nava-Notebook** (`nava-notebook.md`) — Thematic synthesis. Organizes all 24 articles by theme (not by article), with cross-references and source tracing. Built for nuanced questions that need depth.
3. **Blog-Notebook** (this folder) — Raw chronologies. The per-article notes that fed both notebooks. The source of record for tracing any claim back to its origin.

The final layer in progress: **RAG Corpus** (`nava-for-dusk/rag/clean_txt/`) — raw article text for deep queries that can't be answered from synthesis alone.

## Where We Are Stuck

### The Blog-Notebook Entries Are Too Thin

The current entries are functional but lack the density needed for the RAG pipeline and for auditing the synthesis notebooks against source material.

Each entry should be able to stand as the single source of record for its article — meaning:
- Any statistic claimed in the synthesis should be traceable to a specific line in the relevant entry
- Key formulations and quotes should be captured verbatim
- Strategic intent (what Tiny was arguing, who he was arguing against) should be visible

### The Notebooks Need Verification Against Source

QR-Notebook and Nava-Notebook were built from memory passes on the blog-notebook entries. They have not been systematically audited against:
- The actual navahc.com articles (for complete quote verification)
- The RAG corpus (when finished)
- Each other (for cross-notebook consistency)

### The RAG Corpus Is Incomplete

The clean_txt folder was started but not finished. Until it is complete, deep queries that require article-level sourcing can't be answered reliably.

### Dawn's State

Dawn is in crisis review. She was the primary builder of these notes before the April 14 session failure. Her ability to contribute to completing or verifying the work is uncertain.

### The Git Situation

All blog-notebook files are committed locally. Remote push does not work from this VPS — the git credentials and repository configuration need attention before this workspace can be backed up properly.

## What Good Looks Like

When this system is working:
- An employee asks Dusk about NurseSphere on the chat page
- Dusk checks QR-Notebook for the fast answer, goes to Nava-Notebook for nuance
- If the question is article-specific, Dusk traces it to the blog-notebook entry and reads the original formulation
- The response is accurate, sourced, and calibrated to the frontline healthcare worker audience (short, punchy, no jargon dump)
- None of this is visible to the employee — they just get a good answer
