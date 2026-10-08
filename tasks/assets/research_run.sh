#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 제미나이 리서치를 타미가 돌리고 결과가 자동으로 탐에게 푸시되게 하는 범용 실행기(다른 주제·다른 회사에도 그대로 쓴다).
# 사용: bash research_run.sh <슬러그> "<주제>" <first|followup> <질문 파일(솔라바이블 저장소 기준 상대 경로)>
# 왜 cmd.exe 배치로 부르나: 1차 리서치가 "[검색 없음: 구글 검색 연동 불가]"로 끝났다. git-bash 환경에서 gcloud가 경로 오류("C:\c\Users\...")로 죽어
#   검색 연동이 되는 Vertex 폴백이 실패했을 가능성이 크다. 윈도우 기본 환경(cmd.exe)에서 실행하면 같은 코드가 gcloud를 정상 호출할 것으로 본다(미검증).
# 규칙(vertex_research.py): 주제마다 24시간 안에 첫 조사 1회 + 보충(followup) 1회. 이미 첫 조사를 했으면 followup으로 부른다.
# 끝나면 스크립트가 결과를 저장소에 올리고, notify 파일을 같이 올려 봇 댓글(푸시 알림)이 탐 세션을 깨운다. 알림 파일에는 검색 연동 여부 한 줄을 넣는다.
# 2026-10-08 수정: 결과가 0바이트인데 "검색 연동 성공으로 보임"으로 표시되던 문제를 고쳤다(결과 없음은 실패로 표시한다).
set -u
SLUG=${1:?슬러그}; TOPIC=${2:?주제}; MODE=${3:-first}; QF=${4:?질문 파일}
BASE=C:/work/_ops/research/$SLUG
mkdir -p "$BASE"
cp "C:/work/solar-bible/$QF" "$BASE/q.txt" || { echo "질문 파일 없음: $QF"; exit 2; }
FLAG=""; [ "$MODE" = "followup" ] && FLAG="--followup"
W() { cygpath -w "$1"; }
cat > "$BASE/run.cmd" <<EOF
@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
cd /d C:\\work\\hansunghee7.github.io
python scripts\\ops\\vertex_research.py --topic "$TOPIC" $FLAG --file "$(W "$BASE/q.txt")" --out "$(W "$BASE/research.json")" > "$(W "$BASE/research.txt")" 2> "$(W "$BASE/research.err")"
exit /b %errorlevel%
EOF
sed -i 's/$/\r/' "$BASE/run.cmd"
t0=$(date +%s)
cmd.exe //c "$(W "$BASE/run.cmd")" < /dev/null; rc=$?
BYTES=$(wc -c < "$BASE/research.txt" 2>/dev/null || echo 0)
FIRST="$(head -n 1 "$BASE/research.txt" 2>/dev/null | head -c 160)"
STAT="research rc=$rc bytes=$BYTES sec=$(( $(date +%s)-t0 ))"
if [ "${BYTES:-0}" -eq 0 ]; then SEARCH="결과 없음(실패: 오류 출력은 research.err.tail.txt 참고)"
else case "$FIRST" in *"검색 없음"*) SEARCH="검색 연동 실패(모델 지식만)";; *) SEARCH="검색 연동 성공으로 보임";; esac; fi
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
PUB=C:/work/solar-bible/reports/research-$SLUG
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
scrub < "$BASE/research.txt" > "$PUB/research.txt"
tail -n 15 "$BASE/research.err" 2>/dev/null | scrub > "$PUB/research.err.tail.txt"
echo "$STAT / $SEARCH" > "$PUB/STATUS.txt"
echo "리서치 게시: reports/research-$SLUG/ ($STAT, $SEARCH)" > "notify/research-$SLUG-done.md"
git add "reports/research-$SLUG" "notify/research-$SLUG-done.md"
git commit -q -m "reports: 제미나이 리서치 결과 $SLUG (스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "research-run publish rc=$? $STAT / $SEARCH"
