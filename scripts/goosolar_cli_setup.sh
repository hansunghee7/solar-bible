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

step "STEP 2: Bun 설치"
run_remote 'curl -fsSL https://bun.sh/install | bash'

step "STEP 3: 워크스페이스 준비 + 버전 확인"
run_remote 'mkdir -p ~/goosolar-tam && cd ~/goosolar-tam && claude --version'

if [ "$FAIL" -eq 0 ]; then
  echo "=== STATUS: DONE (설치 3단계 성공, 플러그인·로그인은 후속 과제) ==="
else
  echo "=== STATUS: 일부 실패 (위 exit code 확인) ==="
fi