# Chat Page V2 — Migration Guide

This folder (`chat-page2`) contains the **Option B architecture** for the Nava public chat page. It successfully incorporates the **Cold-Start Latency fixes** requested in `BUILD-PLAN.md` and upgrades the fragile filesystem tracking mechanism to a robust **SQLite Database**, resolving the session bugs mentioned in the `README.md`.

## Key Architectural Differences

### 1. SQLite Database > JSON Files (Concurrency Fix)
**The V1 Problem:** The Flask app (`relay.py`) relied on reading and writing to multiple separate JSON files (`sessions.json`, `pending.json`, `names.json`) to track user context. Flask is heavily multithreaded. If multiple users query at once, the threads would step on each other, overwriting data and corrupting JSON files. This resulted in "stale sessions" and dead tickets.
**The V2 Solution:** All state is now tracked exclusively in a single, robust SQLite database file (`chat.db`). SQLite natively provides transaction locking, preventing concurrency faults entirely. 
* *All json files are obsolete in V2. The `db.py` module manages all storage.*

### 2. Pre-Canned UX Decision Tree (Cold Start Mitigation)
V2 implements the user states defined in `BUILD-PLAN.md`:
* **State 1 (`idle`)**: A new user clicks a prompt button. The frontend UI immediately (zero network delay) serves the appropriate canned response explaining Nava's services and asks for their name. Simultaneously, the backend quietly spawns an OpenClaw agent instance.
* **State 2 (`waiting_for_name`)**: The user provides their name. `relay.py` intercepts this packet, saves the name to the Database, retrieves what context the user initially clicked on, and provides both the `first_context` + `name` into the now-warm session thread. 
* **State 3 (`active`)**: The user drops into the active loop. All subsequent inputs simply stream to OpenClaw.

### 3. Native TTL Ticket Garbage Collection
V1 required periodic manual server hard-reboots to purge `pending.json`. V2 integrates a stale ticket cleanup mechanism natively when tracking tickets. Tickets lacking a response for over 5 minutes are silently deleted, ensuring no polling loops can freeze the process.

## Assistant Integration Guide

If you are replacing the production server:
1. Ensure the assets (like `nava-logo.png` and `prompt_lists.py`) have been copied.
2. To boot the V2 relay, run `python chat-page2/relay.py <PORT>`. The SQLite `chat.db` will initialize magically upon first run.
3. Keep track of interviews: they will now save to `chat-page2/interviews`.

## Recommended Future Improvements 
While V2 is extremely solid compared to V1, there is still room to optimize:
* **WebSockets via Flask-SocketIO:** The `GET /response?ticket=X` HTTP polling burns through connection limits significantly. While manageable statically right now, if user traffic scales up quickly, migrating to Server-Sent Expressions (SSE) or full WebSockets will eliminate the heavy HTTP handshaking overhead completely.
