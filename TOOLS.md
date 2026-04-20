# TOOLS.md - Local Notes

## GitHub
- Token stored in `~/.git-credentials`
- Repo: `https://github.com/tiny4lurv/openclaw-workspace`

## Resource Map

### Nava Healthcare (Primary Knowledge Base)

| Resource | Location | Use |
|----------|----------|-----|
| **QR-Notebook** | `memory/qr-notebook.md` | Fast answers, concise responses, first lookup |
| **Nava-Notebook** | `memory/nava-notebook.md` | Thematic synthesis, frameworks, detailed understanding |
| **Blog-Notebook** | `memory/blog-notebook/` | Per-article chronological notes, source tracing (01–24) |
| **RAG Corpus** | `nava-for-dusk/rag/clean_txt/` | Raw article text for deep queries |
| **Nava Research Bible** | `memory/nava-research.md` | Consolidated reference (older, superseded by Nava-Notebook) |

### Chat Page (Nava Employee Chat)
- `chat-page/relay.py` — Flask relay on port 8081
- `chat-page/index.html` — chat UI
- Cloudflare tunnel: `https://second-acts-tones-funk.trycloudflare.com`
- ACCESS_TOKEN: `nava-dusk-2026`

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
