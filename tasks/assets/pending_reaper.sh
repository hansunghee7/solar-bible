#!/usr/bin/env bash
# 로컬탐 2026-10-08 (클라우드 탐 #4 요청 1번): 처리가 끝났는데 tasks/pending/ 에 남은 원본을 스크립트가 지운다. LLM을 거치지 않는다.
# 배경: 타미(모델)가 원본 삭제를 안 해서 같은 일이 반복 실행됐다. 삭제를 모델 손에 맡기지 않고 구PC 크론이 한다.
# 대상: tasks/received/ 또는 tasks/done/ 에 같은 이름이 있고, 최초 커밋으로부터 THRESH초(기본 600) 지난 tasks/pending/*.md 만.
#   (접수·완료 기록이 없는 파일, 아직 안 지난 파일은 건드리지 않는다. 사본은 이미 done/received 에 있으므로 정보 손실 없음)
# 사용: bash pending_reaper.sh <솔라바이블 클론 경로> [임계초]   (DRY=1 이면 지우지 않고 목록만 출력)
set -u
REPO=${1:?저장소 경로}; THRESH=${2:-600}
cd "$REPO" || exit 2
git pull --rebase --autostash --quiet 2>/dev/null || { echo "pull 실패"; exit 3; }
now=$(date +%s); n_del=0
for f in tasks/pending/*.md; do
  [ -e "$f" ] || continue
  n=$(basename "$f")
  [ -e "tasks/received/$n" ] || [ -e "tasks/done/$n" ] || continue
  born=$(git log --diff-filter=A --format=%ct -- "$f" | tail -1); [ -n "$born" ] || continue
  [ $(( now - born )) -ge "$THRESH" ] || continue
  echo "REAP $n"
  if [ "${DRY:-0}" != "1" ]; then git rm -q "$f" && n_del=$((n_del+1)); fi
done
if [ "$n_del" -gt 0 ]; then
  git commit -q -m "chore: 처리 끝난 pending 원본 ${n_del}건 자동 삭제 (pending_reaper)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
fi
echo "reaper done reaped=$n_del"
