#!/usr/bin/env bash
# 로컬탐 2026-10-08: 실험 E1의 "검증 세션" 역할을 하는 스크립트(LLM 없음). 만든 쪽(타미)과 분리된 눈으로 같은 명령을 다시 돌려 대조한다.
# 사용: bash tami_exp_check.sh <solar-bible 클론 경로>   출력 마지막 줄: E1 PASS 또는 E1 FAIL(사유)
set -u; R=${1:?경로}; cd "$R" && git pull --rebase --autostash -q 2>/dev/null
S=reports/exp1-state.md; N=20261008-tam-exp1-state-maker.md; fail=""
[ -f "$S" ] || { echo "E1 FAIL(상태 파일 없음)"; exit 1; }
for i in 1 2 3 4; do c=$(grep -c "^STEP $i DONE" "$S"); [ "$c" = 1 ] || fail="$fail 단계$i DONE줄=$c개;"; done
live=$(ssh -o ConnectTimeout=15 -o BatchMode=yes goosolar 'export HERMES_HOME=~/.hermes-ops PATH=$HOME/.local/bin:$PATH; hermes --version | head -1; ls $HERMES_HOME | wc -l; pgrep -fc telegram_agent.py' 2>/dev/null)
v=$(echo "$live" | sed -n 1p | cut -c1-40); grep -q "^STEP 1 DONE.*$(echo "$v" | awk '{print $4}')" "$S" || fail="$fail 버전 불일치(실측 $v);"
echo "$live" | sed -n 3p | grep -qE '^[1-9]' || fail="$fail 구PC telegram_agent 미실행;"
rec=$(git log --oneline --grep="received: $N" | wc -l); [ "$rec" -le 1 ] || fail="$fail 반복 접수 ${rec}회;"
[ ! -e "tasks/pending/$N" ] || fail="$fail pending 원본 잔류(reaper 대기);"
[ -z "$fail" ] && echo "E1 PASS" || echo "E1 FAIL($fail)"
