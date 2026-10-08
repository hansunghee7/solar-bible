#!/usr/bin/env bash
# 탐 2026-10-08: 비티가 주간 한도(429)로 막혔을 때 Vertex 제미나이(GCP 크레딧)로 검증을 받는 범용 실행기. 결과는 스크립트가 직접 저장소에 올리고 알림 파일을 같이 올린다.
# 사용: bash vertex_verify_run.sh <슬러그> <질문 파일(solar-bible 기준 상대 경로)>
# 규칙: 질문 파일에는 고객 정보·비밀값·가격·전략·실명을 넣지 않는다(ask_vertex.py 규칙). 하루·누적 비용 상한은 ask_vertex.py가 코드로 강제한다(종료 코드 3 = 상한 초과).
# cmd.exe 배치로 부른다(git-bash에서 gcloud 경로가 깨지는 문제를 피한다). 질문 파일은 호출 전에 UTF-8로 정리한다(잘린 한글 바이트 사고 재발 방지).
set -u
SLUG=${1:?슬러그}; QF=${2:?질문 파일}
BASE=C:/work/_ops/vertex/$SLUG; mkdir -p "$BASE"
t0=$(date +%s)
python -X utf8 -c "import sys; d=open(sys.argv[1],'rb').read(); open(sys.argv[2],'wb').write(d.decode('utf-8','ignore').encode('utf-8'))" "C:/work/solar-bible/$QF" "$BASE/q.txt" || { echo "질문 파일 없음 또는 정리 실패: $QF"; exit 2; }
W() { cygpath -w "$1"; }
cat > "$BASE/run.cmd" <<EOF
@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
cd /d C:\\work\\hansunghee7.github.io
python scripts\\ops\\ask_vertex.py "$(W "$BASE/q.txt")" "$(W "$BASE/out.md")" --who 탐 > "$(W "$BASE/run.log")" 2>&1
exit /b %errorlevel%
EOF
sed -i 's/$/\r/' "$BASE/run.cmd"
cmd.exe //c "$(W "$BASE/run.cmd")" < /dev/null; rc=$?
STAT="vertex rc=$rc bytes=$(wc -c < "$BASE/out.md" 2>/dev/null || echo 0) sec=$(( $(date +%s)-t0 ))"
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g; s/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/[이메일 줄임]/g'; }
PUB=C:/work/solar-bible/reports/vertex-$SLUG
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
[ -s "$BASE/out.md" ] && scrub < "$BASE/out.md" > "$PUB/out.md"
tail -n 15 "$BASE/run.log" 2>/dev/null | scrub > "$PUB/run.log.tail.txt"
echo "$STAT" > "$PUB/STATUS.txt"
echo "Vertex 검증 게시: reports/vertex-$SLUG/ ($STAT)" > "notify/vertex-$SLUG-done.md"
git add "reports/vertex-$SLUG" "notify/vertex-$SLUG-done.md"
git commit -q -m "reports: Vertex 검증 결과 $SLUG (스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "vertex-verify publish rc=$? $STAT"
