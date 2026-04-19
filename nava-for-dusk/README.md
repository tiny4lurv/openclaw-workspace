# Nava Content Archive — For Dusk

**Source:** Dawn's workspace (pre-upgrade backup)
**Date:** 2026-04-14

## What's Inside

### nava-corpus.tar.gz (26KB)
Social posts — the content corpus for Nava brand work:
- `linkedin-posts.md` — all Nava LinkedIn posts
- `x-posts.md` — all Nava X/Twitter posts
- `facebook-posts.md` — Nava Facebook posts
- `x-linkedin-paired-corpus.md` — X+LinkedIn post pairs (matched by topic)

### rag-clean-txt.tar.gz (148KB)
Blog article archive — 44 articles from navahc.com:
- All articles cleaned and formatted as plain text
- Used as RAG knowledge base for article writing
- Filenames are content hashes, not original titles
- See `docs/nava-content-system/Nava_Blog_Research_Notes.md` for article index

### nava-docs.tar.gz (3.2MB)
Nava brand documentation and training materials:
- `Nava Healthcare Content Bible.md` — brand bible
- `Nava_Content_Thinking_Framework_MASTER.md` — content framework
- `Nava_LinkedIn_X_Content_Guide.md` — platform-specific guide
- `ROLE & KNOWLEDGE BASE.md` — agent training base
- `Nava Custom GPT Initial Handoff Instructions.md` — handoff doc
- `agent-training/` — training materials
- `writing_analysis/` — Tiny's writing analysis corpus

## To Extract

```bash
cd /root/.openclaw/workspace/nava-for-dusk/
tar -xzf nava-corpus.tar.gz
tar -xzf rag-clean-txt.tar.gz
tar -xzf nava-docs.tar.gz
```

## What Dusk Can Use These For

1. **RAG queries** — the rag/clean_txt/ articles are the knowledge base for writing Nava content
2. **Brand voice training** — nava-corpus/ shows the established post style
3. **Agent knowledge** — nava-docs/ has everything needed to understand the Nava brand, product, and content rules

## Notes for Dusk

- The corpus posts were written by Tiny (with my editing help). Use them as style reference, not as definitive product claims.
- The blog articles are from navahc.com — they represent the brand's established content voice.
- Nava's positioning: healthcare staffing with a clinical-first, evidence-based approach. Not a vendor — a clinical partner.
