#!/usr/bin/env bash
set -u
FAIL=0

step() {
  echo "=== $1 ==="
}

run_remote() {
  ssh goosolar "$1"
  code=$?
  echo "--- exit code: $code ---"
  [ "$code" -ne 0 ] && FAIL=1
  return $code
}

step "STEP 1: Claude Code CLI 설치"
run_remote 'curl -fsSL https://claude.ai/install.sh | bash'

step "STEP 2a: unzip 설치 확인(Bun 설치에 필요, 없으면 apt로 시도)"
run_remote 'command -v unzip >/dev/null 2>&1 && echo "unzip 이미 있음" || sudo apt-get install -y unzip'

step "STEP 2b: Bun 설치"
run_remote 'curl -fsSL https://bun.sh/install | bash'

step "STEP 3: 워크스페이스 준비 + 버전 확인"
# STEP 1에서 설치한 claude CLI는 ~/.local/bin에 들어가지만, 매 run_remote가
# 새 ssh 세션이라 그 PATH가 여기까지 안 이어진다(2026-09-27 1차 실행 실패
# 원인). PATH를 여기서 다시 명시한다.
run_remote 'export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH" && mkdir -p ~/goosolar-tam && cd ~/goosolar-tam && claude --version'

if [ "$FAIL" -eq 0 ]; then
  echo "=== STATUS: DONE (설치 3단계 성공, 플러그인·로그인은 후속 과제) ==="
else
  echo "=== STATUS: 일부 실패 (위 exit code 확인) ==="
fi