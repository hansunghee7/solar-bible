#!/usr/bin/env bash
# 탐 2026-10-08: 제미나이 웹 접속·로그인 유지 확인을 신PC와 구PC에서 돌리고, 결과를 스크립트가 직접 저장소에 올린다(올라간 notify 파일이 탐을 깨운다).
# 읽기 전용: 프롬프트 입력 없음, 이메일은 마스킹, 스크린샷은 올리지 않는다(로컬에만 남김).
set -u
OUT=C:/work/_ops/research/geminiweb; mkdir -p "$OUT"
cp C:/work/solar-bible/tasks/assets/gemini_web_check.py "$OUT/gemini_web_check.py"
cd "$OUT" || exit 2
W() { cygpath -w "$1"; }
cat > run_new.cmd <<EOT
@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
cd /d $(W "$OUT")
python gemini_web_check.py 신PC > new.txt 2>&1
EOT
sed -i 's/$/\r/' run_new.cmd
timeout 300 cmd.exe //c "$(W "$OUT/run_new.cmd")" < /dev/null; echo "신PC rc=$?" > rc.txt
timeout 300 ssh -o BatchMode=yes -o ConnectTimeout=15 goosolar '~/workshop/venv/bin/python - 구PC' < gemini_web_check.py > old.txt 2>&1; echo "구PC rc=$?" >> rc.txt
scrub() { sed -E 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/[이메일 줄임]/g; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
PUB=C:/work/solar-bible/reports/research-geminiweb
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
{ cat "$OUT/rc.txt"; echo "--- 신PC"; cat "$OUT/new.txt"; echo "--- 구PC"; cat "$OUT/old.txt"; } | scrub | head -c 6000 > "$PUB/result.txt"
echo "제미나이 웹 확인 게시: reports/research-geminiweb/result.txt ($(grep -c '^PORT' "$PUB/result.txt") 포트 줄)" > notify/research-geminiweb-done.md
git add reports/research-geminiweb notify/research-geminiweb-done.md
git commit -q -m "reports: 제미나이 웹 접속 확인 결과 (스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "gemini-web publish rc=$?"
