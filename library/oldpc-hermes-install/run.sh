#!/usr/bin/env bash
# 로컬탐 2026-10-08: 구PC(goosolar) 헤르메스 1단계 설치 스크립트. LLM을 거치지 않는다. 구PC에서 실행(ssh goosolar 'bash -s' < 이 파일).
# 근거: 신PC 설치본 README의 리눅스 공식 설치(https://hermes-agent.nousresearch.com/install.sh)와 scripts/install.sh의 옵션 도움말.
# 원칙: ~/.hermes-ops 에만 설치(기존 ~/hermes-agent 와 telegram_agent.py 는 건드리지 않음), sudo 요구 시 멈춤, 크론·서비스 등록 없음.
set -u
HH="$HOME/.hermes-ops"; INST=/tmp/hermes_install.sh
echo "== 0. 사전 상태"; free -m | sed -n 2p; df -h ~ | tail -1
echo "== 1. 설치기 내려받기(파이프 실행 금지, 파일로 받아 확인)"
curl -fsSL -m 60 -o "$INST" https://hermes-agent.nousresearch.com/install.sh || { echo "FAIL download rc=$?"; exit 10; }
sha256sum "$INST" | cut -c1-16; wc -l "$INST"
if grep -nE '^\s*sudo |apt(-get)? install' "$INST" | head -5 | grep -q .; then echo "NOTE: 설치기에 sudo/apt 호출이 있음(실행 중 필요 시 멈춤):"; grep -nE '^\s*sudo |apt(-get)? install' "$INST" | head -5 | cut -c1-140; fi
echo "== 2. 설치(--hermes-home $HH, 대화형 설정·브라우저·컴퓨터 사용 제외)"
timeout 900 bash "$INST" --hermes-home "$HH" --skip-setup --skip-browser --skip-computer-use < /dev/null 2>&1 | tail -25
echo "install rc=${PIPESTATUS[0]}"
echo "== 3. 확인"
export HERMES_HOME="$HH"; export PATH="$HOME/.local/bin:$HH/bin:$PATH"
command -v hermes || echo "hermes 경로 못 찾음"
hermes --version 2>&1 | head -3
echo "== 4. 사후 상태"; free -m | sed -n 2p; df -h ~ | tail -1; ls -d "$HH" "$HH/hermes-agent" 2>&1 | head -3
pgrep -af telegram_agent.py | head -1 | cut -c1-80 || true
echo "SCRIPT-END"
