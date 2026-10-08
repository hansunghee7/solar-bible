#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 덱스가 "지정된 경로를 찾을 수 없습니다(os error 3)"로 끝나는 원인을 가린다. 사장님 가설: 주간 사용 한도일 수도 있음.
# 읽기 전용 짧은 질문 1개를 경로 방식 3가지로 던져 보고, 어느 쪽이 되는지와 한도 문구가 있는지를 본다(덱스 호출 3회, 작업 폴더는 읽기만).
set -u
OUT=C:/work/_ops/pushalert
mkdir -p "$OUT"
D="$OUT/dex-diag3.txt"
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
W_WIN="C:/work/_ops/dex/topicwork"
W_POSIX="/c/work/_ops/dex/topicwork"
PROMPT="이 작업 폴더의 파일 이름을 하나만 말하고 끝이라고 답하라. 아무것도 수정하지 마라."
t() { local name=$1; shift; ( "$@" ) > "$OUT/t_$name.out" 2>&1 < /dev/null; echo "## 시험 $name rc=$?"; head -n 12 "$OUT/t_$name.out"; }
{
  echo "## 진단3 시각 $(date '+%F %T')"
  echo "## codex 버전"; codex --version 2>&1 | head -n 2
  echo "## codex 설정의 sandbox·windows 줄"; grep -n -i -E "sandbox|windows" ~/.codex/config.toml 2>&1 | head -n 6
  t A_windows_path codex exec -C "$W_WIN" --sandbox read-only -o "$OUT/t_A.md" "$PROMPT"
  t B_posix_path codex exec -C "$W_POSIX" --sandbox read-only -o "$OUT/t_B.md" "$PROMPT"
  t C_cd_only bash -c "cd '$W_WIN' && codex exec --sandbox read-only -o '$OUT/t_C.md' '$PROMPT'"
  echo "## 답 파일 크기"; ls -la "$OUT"/t_?.md 2>&1 | head -n 5
  echo "## 한도 관련 문구 검색(시험 출력 전체)"; grep -i -E "usage limit|rate limit|quota|429|한도|weekly|exceeded" "$OUT"/t_*.out 2>&1 | head -n 8
} 2>&1 | scrub > "$D"
PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
cp "$D" "$PUB/dex-diag3.txt"
echo "덱스 진단3 게시: reports/20261008-pushalert-out/dex-diag3.txt" > notify/20261008-pushalert-dexdiag3-done.md
git add reports/20261008-pushalert-out/dex-diag3.txt notify/20261008-pushalert-dexdiag3-done.md
git commit -q -m "reports: 덱스 진단3 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "diag3 publish rc=$?"
