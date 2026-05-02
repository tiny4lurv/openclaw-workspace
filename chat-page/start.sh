#!/bin/bash
cd /root/.openclaw/workspace/chat-page
pkill -f "relay.py" 2>/dev/null
sleep 2
nohup python3 relay.py 8081 >> relay.log 2>&1 &
sleep 3
curl -s http://localhost:8081/health