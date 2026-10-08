#!/usr/bin/env bash
# 로컬탐 2026-10-09 실험 E1b: 타미(LLM)에게 4개 명령을 풀어 주면 즉흥으로 딴 곳을 탐색해 실패했다(E1, 10/8).
# 그래서 "한 줄 명령"으로 바꾸고, 단계 기록(STATE)을 LLM이 아니라 이 스크립트가 직접 쓴다. LLM은 이 스크립트를 호출만 한다.
# 읽기 전용 점검(설치·삭제·등록 없음). 결과 파일: reports/exp1-state.md, 마지막 줄 "exp1 done rc=<코드>".
set -u
R=C:/work/solar-bible; S=$R/reports/exp1-state.md; cd "$R" || exit 2
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p reports; : > "$S"
ENVX='export HERMES_HOME=~/.hermes-ops PATH=$HOME/.local/bin:$PATH;'
fail=0
step(){ n=$1; shift; out=$(ssh -o ConnectTimeout=15 -o BatchMode=yes goosolar "$ENVX $*" 2>&1 | head -1 | cut -c1-120); rc=$?
  if [ -n "$out" ] && ! echo "$out" | grep -qi "ssh:\|permission denied\|could not resolve\|connection"; then echo "STEP $n DONE $(date -u +%H:%M:%S) $out" >> "$S"
  else echo "STEP $n FAIL $(date -u +%H:%M:%S) ${out:-no-output}" >> "$S"; fail=1; fi; }
step 1 "hermes --version | head -1"
step 2 "ls \$HERMES_HOME | wc -l"
step 3 "free -m | sed -n 2p | awk '{print \$7}'"
step 4 "pgrep -fc telegram_agent.py"
git add "$S" && git commit -q -m "E1b: 구PC 점검 단계 기록 (exp1_run.sh)" && { git push origin main 2>&1 | tail -1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1 | tail -1; }; }
tail -4 "$S"
echo "exp1 done rc=$fail"
exit $fail
