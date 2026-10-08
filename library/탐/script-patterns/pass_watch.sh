#!/usr/bin/env bash
# 금고 일반 구역에 Anthropic 키가 envput 가능해질 때까지 1분 간격으로 시도한다(최대 3시간). 값은 보지도 출력하지도 않는다.
LOG=C:/work/_ops/pass_watch.log
for i in $(seq 1 180); do
  out=$(cd C:/work/saegim-pass-dev/host && PYTHONUTF8=1 python pass.py --from 탐 --why "Claude API 크레딧 운용 래퍼용 키 주입(사장님 10/9 허용)" --to hermes envput "trello.com - NEXT STEP" ANTHROPIC_API_KEY_OPS 2>&1 | sed 's/"value"[^,}]*//' | tr -d '\n' | cut -c1-200)
  if echo "$out" | grep -q '"ok": true'; then
    echo "$(date -u +%FT%TZ) envput OK" >> $LOG
    cd C:/work/hansunghee7.github.io && PYTHONUTF8=1 python scripts/ops/tg_boss.py text "[탐 컨펌] 금고가 Anthropic 키를 헤르메스 환경 파일에 넣었습니다(ANTHROPIC_API_KEY_OPS). 다음은 0.01달러 시험입니다." --persona 탐 >> $LOG 2>&1
    echo "PASS-WATCH DONE"; exit 0
  fi
  echo "$(date -u +%FT%TZ) try $i: $(echo "$out" | cut -c1-120)" >> $LOG
  sleep 60
done
echo "$(date -u +%FT%TZ) timeout" >> $LOG
