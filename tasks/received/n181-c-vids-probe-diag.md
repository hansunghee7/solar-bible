# n181-c-vids-probe-diag - 수신 확인

## 메타
- 수신 시각: 2026-10-11T10:30:28
- 레인: pending

## 의뢰(받은 그대로)

# (탐 -> 헤르메스) N181-C vids-probe 감시 fail 원인 읽기 전용 진단

실행할 명령 한 줄:
`ssh goosolar "date; ls -l --time-style=full-iso ~/workshop/logs | grep -i vids; crontab -l | grep -i vids; tail -n 15 ~/workshop/logs/vids_probe.log"`

성공 기준 한 줄: 위 출력에서 (1) vids_probe.last 의 마지막 갱신 시각 (2) 크론에 항목이 있는지 (3) 로그 마지막 오류 한 줄, 이 세 가지를 각각 한 줄로 적는다. 출력에 없으면 "출력에 없음"이라고 쓴다(추측 금지).

보고(마지막 5줄만): 성공/실패, 소요 초, 위 세 줄, 환각 여부(출력에 없는 원인을 단정하면 "환각 있음"), 막힌 곳. 배경: 감시 cron:vids-probe 는 vids_probe.last 가 180분 넘게 갱신 없으면 fail (10/11 실측 3903분).

막히면 멈추고 보고: ssh 접속 실패·타임아웃 30초·권한 거부 시 그 한 줄만 보고하고 끝낸다. 읽기 전용: 파일 수정, 크론 수정, 프로세스 재시작, 키 출력 금지. 재시도 금지.
