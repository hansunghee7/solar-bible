#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 덱스 호출이 rc=0인데 답 파일이 없는 원인 진단(읽기 전용). 결과는 스크립트가 직접 저장소에 게시한다.
# 읽기만 한다: dex.log 전체, codex 버전, 로그인 상태 한 줄, 호출 기록 중 덱스 줄. 키·토큰 값은 치환한다.
set -u
OUT=C:/work/_ops/pushalert
D=$OUT/dex-diag.txt
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
{
  echo "## 진단 시각 $(date '+%F %T')"
  echo "## dex.log 전체(최대 80줄)"; head -n 80 "$OUT/dex.log" 2>&1
  echo "## card_dex.md 크기와 앞 5줄"; wc -c "$OUT/card_dex.md" 2>&1; head -n 5 "$OUT/card_dex.md" 2>&1
  echo "## codex 버전"; codex --version 2>&1 | head -n 2
  echo "## codex 로그인 상태(한 줄)"; codex login status 2>&1 | head -n 2
  echo "## 작업 폴더"; ls -la "${DEX_WORKDIR:-/c/work/_ops/dex/topicwork}" 2>&1 | head -n 12
  echo "## 호출 기록 중 덱스 최근 5줄"; grep -i "dex" /c/work/_ops/agent_calls.csv 2>/dev/null | tail -n 5
} 2>&1 | scrub > "$D"
PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
cp "$D" "$PUB/dex-diag.txt"
echo "덱스 진단 게시: reports/20261008-pushalert-out/dex-diag.txt" > notify/20261008-pushalert-dexdiag-done.md
git add reports/20261008-pushalert-out/dex-diag.txt notify/20261008-pushalert-dexdiag-done.md
git commit -q -m "reports: 덱스 단계 진단 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "diag publish rc=$?"
