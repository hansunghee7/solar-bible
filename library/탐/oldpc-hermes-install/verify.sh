#!/usr/bin/env bash
# 검증 스크립트(LLM 없음, 읽기 전용): 구PC 헤르메스 설치가 살아 있는지 확인한다. 마지막 줄 VERIFY PASS/FAIL.
out=$(ssh -o ConnectTimeout=15 -o BatchMode=yes goosolar 'export HERMES_HOME=~/.hermes-ops PATH=$HOME/.local/bin:$PATH; hermes --version | head -1; test -d $HERMES_HOME/hermes-agent && echo DIR_OK; pgrep -fc telegram_agent.py' 2>&1)
echo "$out"
echo "$out" | grep -q "Hermes Agent v" && echo "$out" | grep -q DIR_OK && echo "$out" | tail -1 | grep -qE '^[1-9]' && echo "VERIFY PASS" || echo "VERIFY FAIL"
