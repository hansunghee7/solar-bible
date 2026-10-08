#!/usr/bin/env bash
# 탐 2026-10-08: 신PC의 solar-bible 클론(C:/work/solar-bible)이 리베이스 도중에 멈춰 폴러가 pull·push에 실패하던 문제를 한 번에 진단하고 복구한다.
# LLM 호출 없이 이 스크립트 한 번이면 끝난다(크레딧 절약). 안전 규칙: 리베이스 취소는 원래 브랜치 끝으로 되돌리므로 커밋이 사라지지 않는다.
# 로컬 변경(커밋 안 된 것)은 autostash로 보관하고, 충돌이 나면 멈추고 사람에게 보고한다. 비밀값·이메일은 출력하지 않는다.
set -u
R=C:/work/solar-bible
cd "$R" || { echo "클론 없음"; exit 2; }
echo "== 복구 전 상태"; git status -sb | head -5
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "리베이스 진행 중 -> 취소(원래 브랜치로 복귀)"; git rebase --abort || { echo "취소 실패: 사람 확인 필요"; exit 3; }
else echo "리베이스 진행 중 아님"; fi
git checkout -q main 2>&1 | tail -2
git fetch -q origin main
ahead=$(git rev-list --count origin/main..main 2>/dev/null || echo ?)
echo "origin/main보다 앞선 로컬 커밋: $ahead"
git pull --rebase --autostash --quiet 2>&1 | tail -3; rc=$?
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then echo "pull 중 충돌: 취소하고 사람 확인 필요"; git rebase --abort; exit 4; fi
mkdir -p C:/work/_ops/pushalert C:/work/_ops/research C:/work/_ops/dex/topicwork
echo "== 복구 후 상태"; git status -sb | head -3
mkdir -p notify
echo "신PC 폴러 클론 복구 실행(앞선 로컬 커밋 $ahead개, pull rc=$rc). 상세는 실행 출력 참고." > notify/repair-poller-clone-done.md
git add notify/repair-poller-clone-done.md && git commit -q -m "notify: 신PC 폴러 클론 복구 결과" && { git push origin main 2>&1 | tail -1 || true; }
echo "repair done"
