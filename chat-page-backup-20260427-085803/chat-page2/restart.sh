#!/bin/bash
cd /root/.openclaw/workspace/chat-page
pkill -f "relay.py" 2>/dev/null
sleep 2
nohup python3 relay.py 8081 > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:8081/health
echo ""
pgrep -fa "relay.py" | grep -v grep