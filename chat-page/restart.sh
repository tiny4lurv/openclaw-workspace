#!/bin/bash
pkill -f "relay.py" 2>/dev/null
sleep 1
cd /root/.openclaw/workspace/chat-page
python3 relay.py 8081 &
sleep 2
curl -s http://localhost:8081/health
