#!/usr/bin/env bash
# 탐 2026-10-08: 신PC 폴러 교차 감시(읽기 전용). 구PC에서 5분마다 돌린다.
# tasks/pending/ 의 의뢰 파일이 THRESH초(기본 600) 넘게 남아 있으면 알림 파일을 올려 탐 세션에 푸시(봇 댓글)한다. 작업 파일은 건드리지 않는다.
#  - 접수 폴더(received/done)에 없음  -> "미수신"  : 폴러가 못 잡았다
#  - 접수 폴더에 있음                 -> "원본 잔류": 처리됐는데 pending에 남아 반복 실행 위험
# 사용: bash pending_watchdog.sh <솔라바이블 클론 경로> [임계초]   (DRY=1 이면 알림 파일을 올리지 않고 출력만)
set -u
REPO=${1:?저장소 경로}; THRESH=${2:-600}
cd "$REPO" || exit 2
STATE="${WATCH_STATE:-$HOME/.pending_watch_state}"; touch "$STATE"
git pull --rebase --autostash --quiet 2>/dev/null || { echo "pull 실패"; exit 3; }
now=$(date +%s); new=0
for f in tasks/pending/*.md; do
  [ -e "$f" ] || continue
  n=$(basename "$f")
  born=$(git log --diff-filter=A --format=%ct -- "$f" | tail -1); [ -n "$born" ] || continue
  age=$(( now - born )); [ "$age" -ge "$THRESH" ] || continue
  if [ -e "tasks/received/$n" ] || [ -e "tasks/done/$n" ]; then kind="원본 잔류(처리됐는데 pending에 남음, 반복 실행 위험)"; tag=residual
  else kind="미수신(폴러가 아직 못 잡음)"; tag=stall; fi
  key="$tag:$n"; grep -qxF "$key" "$STATE" && continue
  echo "ALERT $key age=${age}s"
  if [ "${DRY:-0}" != "1" ]; then
    mkdir -p notify
    echo "폴러 감시(구PC): $n — $kind, 경과 $((age/60))분. 신PC 폴러 상태를 확인해야 한다." > "notify/watch-$tag-${n%.md}.md"
    git add "notify/watch-$tag-${n%.md}.md"; new=1
  fi
  echo "$key" >> "$STATE"
done
if [ "$new" = 1 ]; then
  git commit -q -m "notify: 폴러 감시 알림 (pending 정체)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
fi
echo "watchdog done rc=$? alerts_new=$new"
