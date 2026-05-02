# Dusk Chat Widget — Project Overview

## Goal

Embed a floating chat widget on navahc.com so visitors can talk to **Ask Dusk** — the Nava Healthcare Recruitment AI assistant — directly on any page of the site.

Visitors should be able to:
- Click pre-written buttons to learn about Nava's services
- Ask free-text questions and get answers
- Get context-aware responses based on the page they're on (future)

---

## Current Status

**Working:**
- Floating chat button (FAB) + chat panel, served at `https://askdusk.tinymanyonga.online/`
- Backend relay (`relay.py`) running and responding correctly to curl requests
- Widget JS served from same origin

**Broken:**
- Clicking any button or sending a message shows: "Sorry, I'm having trouble connecting."
- This happens in the browser only — the same `/message` endpoint returns correct responses in curl
- The fetch from the browser is failing for an unknown reason

---

## Potential Blockers / Problems

1. **Cloudflare Free Plan** — The Cloudflare Tunnel is on a free plan. Cloudflare may be blocking or stripping JSON API requests that originate from browser JavaScript (as opposed to browser navigations).
2. **CORS** — Even though the relay adds `Access-Control-Allow-Origin` headers, Cloudflare may be removing them before the response reaches the browser.
3. **SSL mixed content** — If navahc.com is HTTP only, a widget served over HTTPS would be blocked by the browser's mixed content policy.
4. **Cloudflare Workers** — The tunnel runs as a Cloudflare named tunnel (service: `cloudflared-tunnel`). There may be a Cloudflare config issue specific to how the tunnel handles proxied API calls vs page loads.
5. **Preflight requests** — The `POST /message` endpoint requires `Content-Type: application/json`. Browser preflight OPTIONS requests may not be handled correctly.

---

## Future Ideas

1. **Page-aware responses** — Widget reads the URL and page content (via DOM), sends context to Dusk. Enables questions like "what is this article about?" and "give me a tl;dr of this page."
2. **Standalone Chrome extension** — Same widget packaged as a browser extension that works on any site.
3. **Notification badge** — Pulse indicator when Dusk has a new response while the panel is closed.
