#!/bin/bash
cd /root/.openclaw/workspace/chat-page
python3 relay.py 8081 >> relay.log 2>&1 &
echo $! > relay.pid
sleep 3
curl -s http://204.168.204.198:8081/health
