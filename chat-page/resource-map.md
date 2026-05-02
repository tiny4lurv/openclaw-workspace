# Nava Chat Page — Resource Map

All resources available to Ask Dusk sessions. Check cascade in order.

## QR-Notebook (`/root/.openclaw/workspace/memory/qr-notebook.md`)
**Purpose:** Fast answers, concise responses, first lookup.
**Use:** Questions that need a quick, direct answer — service descriptions, pricing structure, policy questions.
**Cascade:** If not found here → Nava-Notebook.

---

## Nava-Notebook (`/root/.openclaw/workspace/memory/nava-notebook.md`)
**Purpose:** Strategic frameworks, thematic synthesis, deeper context.
**Use:** When QR-Notebook doesn't have enough depth. Questions about strategy, market positioning, recruitment philosophy.
**Cascade:** If not found here → Blog-Notebook.

---

## Blog-Notebook (`/root/.openclaw/workspace/memory/blog-notebook/`)
**Purpose:** Per-article chronological notes, source tracing.
**Use:** When you need to verify what a specific article said or trace an argument back to its source.
**Cascade:** If not found here → RAG corpus.

---

## RAG Corpus (`/root/.openclaw/workspace/nava-for-dusk/rag/clean_txt/`)
**Purpose:** Raw article text for deep queries.
**Use:** When you need the full context of a claim or want to verify exact wording. This is the cleaned blog article corpus.
**Cascade:** If not found here → SoT RAG corpus.

---

## SoT RAG Corpus (`/root/.openclaw/workspace/rag/sot-clean/`)
**Purpose:** Research documents, methodology verification, primary sources.
**Use:** When a question involves calculations, financial claims, compliance details, or requires verifying the methodology behind a number. Also for in-depth research on staffing models, visa pathways, turnover costs.
**Cascade:** Last resort. If not found here, say "I don't know" and suggest contacting Nava directly.

---

## Calculations Notebook (`/root/.openclaw/workspace/memory/numbers-notebook.md`)
**Purpose:** Numbers, figures, ROI calculations — all audited financial claims.
**Use:** Any question involving money figures, cost savings, annual estimates, percentage changes, staffing budgets.
**Note:** This is the audited version. If a number appears in other resources and doesn't match this notebook, flag the discrepancy.
**Cascade:** Available as a check — not part of the main cascade, but always check this for number-related questions.

---

## Articles Library (`/root/.openclaw/workspace/chat-page/articles.md`)
**Purpose:** URL lookup for article recommendations.
**Use:** When recommending a next step article — read this file to get the correct URL. Never hardcode article URLs.
**Format:** One URL per line, labeled by article topic.

---

## Cascade Summary

```
QR-Notebook
    ↓ (not found)
Nava-Notebook
    ↓ (not found)
Blog-Notebook
    ↓ (not found)
RAG corpus
    ↓ (not found)
SoT RAG corpus
    ↓ (not found)
→ Say "I don't know"
```

**For number/calculation questions:** Check Calculations Notebook first, then follow cascade above.