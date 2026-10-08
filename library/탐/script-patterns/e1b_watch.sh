#!/usr/bin/env bash
# E1b 감시: 타미가 reports/exp1-state.md 를 남기면(STEP 4줄) 검증 스크립트를 돌려 텔레그램(탐)으로 보낸다. 최대 3시간.
R=C:/work/solar-bible; LOG=C:/work/_ops/e1b_watch.log
for i in $(seq 1 60); do
  git -C $R pull --rebase --autostash -q 2>/dev/null
  S=$R/reports/exp1-state.md
  if [ -f "$S" ] && [ "$(grep -c '^STEP [1-4] \(DONE\|FAIL\)' $S)" -ge 4 ]; then
    out=$(E1_TASK=20261009-tam-exp1b-script-runner.md PYTHONUTF8=1 bash $R/tasks/assets/tami_exp_check.sh $R 2>&1 | tail -2)
    echo "$(date -u +%FT%TZ) $out" >> $LOG
    cd C:/work/hansunghee7.github.io && PYTHONUTF8=1 python scripts/ops/tg_boss.py text "[탐 컨펌] 실험 E1b(한 줄 명령 + 스크립트 단계 기록) 검증 결과: $out" --persona 탐 >> $LOG 2>&1
    echo "E1b watch done"; exit 0
  fi
  sleep 180
done
echo "$(date -u +%FT%TZ) E1b watch timeout(3h, 타미 결과 없음)" >> $LOG
cd C:/work/hansunghee7.github.io && PYTHONUTF8=1 python scripts/ops/tg_boss.py text "[탐 컨펌] 실험 E1b: 3시간 안에 타미 결과가 오지 않았습니다(폴러 확인 필요)." --persona 탐 >> $LOG 2>&1
