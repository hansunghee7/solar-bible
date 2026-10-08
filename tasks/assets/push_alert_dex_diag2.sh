#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 진단 1에서 읽은 dex.log는 ask_dex.sh 자신의 출력이었다. codex 자체 로그는 $OUT.log, 즉 dex.md.log다. 그것만 읽어 게시한다(읽기 전용).
set -u
OUT=C:/work/_ops/pushalert
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
{
  echo "## 진단2 시각 $(date '+%F %T')"
  echo "## 파일 존재와 크기"; ls -la "$OUT" 2>&1 | grep -i -E "dex|card" | head -n 12
  echo "## dex.md.log 앞 40줄"; head -n 40 "$OUT/dex.md.log" 2>&1
  echo "## dex.md.log 끝 25줄"; tail -n 25 "$OUT/dex.md.log" 2>&1
  echo "## ask_dex.sh 38~44줄(호출 부분)"; sed -n 36,44p C:/work/hansunghee7.github.io/scripts/ops/ask_dex.sh 2>&1
} 2>&1 | scrub > "$OUT/dex-diag2.txt"
PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
cp "$OUT/dex-diag2.txt" "$PUB/dex-diag2.txt"
echo "덱스 진단2 게시: reports/20261008-pushalert-out/dex-diag2.txt" > notify/20261008-pushalert-dexdiag2-done.md
git add reports/20261008-pushalert-out/dex-diag2.txt notify/20261008-pushalert-dexdiag2-done.md
git commit -q -m "reports: 덱스 진단2 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "diag2 publish rc=$?"
