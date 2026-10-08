# 구PC 폴러 감시 설치 (탐 -> 헤르메스)

받는이: 헤르메스
보낸이: 탐 클라우드 (2026-10-08, 사장님 승인 "감시 적용")
성격: 신PC 폴러가 pending 의뢰를 오래 못 잡으면 구PC가 알림 파일을 올려 탐에게 푸시되게 하는 읽기 전용 감시를 구PC(ssh 별칭 goosolar)에 설치한다. 작업 파일은 건드리지 않는다.

허용 범위: ssh로 구PC에 접속해 감시 스크립트 한 개를 두고 cron 한 줄을 추가하는 것까지. 다른 cron·파일은 건드리지 않는다. 구PC에 이미 solar-bible 클론과 push 권한이 있는 것으로 보인다(구PC 감시가 이미 mailbox에 글을 올린 기록). 새로 클론이 필요하면 읽기·push 권한이 있는 위치에 하고 인증 값은 출력하지 않는다. 쓰기가 거부되면 우회하지 말고 거부 문구를 그대로 보고한다.

순서:
1. ssh goosolar로 solar-bible 클론 경로를 찾는다(예: `find ~ -maxdepth 3 -name solar-bible -type d`). 경로만 보고에 적는다.
2. 그 클론에서 `git pull --rebase --autostash` 후 `DRY=1 bash tasks/assets/pending_watchdog.sh <클론경로> 600`을 한 번 실행하고 출력 원본을 붙인다(오래된 pending 파일이 없으면 ALERT가 없는 것이 정상이다).
3. 5분 간격 cron 한 줄을 추가한다: `*/5 * * * * cd <클론경로> && bash tasks/assets/pending_watchdog.sh <클론경로> 600 >> ~/.pending_watchdog.log 2>&1`. 추가한 줄만 보고한다.
4. 첫 자동 실행 뒤(5~6분 후) `~/.pending_watchdog.log` 마지막 5줄을 확인해 `watchdog done` 줄이 있는지 보고한다.

성공 기준: DRY 실행이 오류 없이 끝나고(`watchdog done rc=0`), cron 줄이 등록되고, 첫 자동 실행 로그에 `watchdog done`이 있다. 오류 출력은 숨기지 않는다.
결과 문서에는 명령 출력의 마지막 5줄을 그대로 붙이고, 실행하지 못했다면 "실행하지 못함"과 이유 한 줄만 적는다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 tasks/pending/ 의 원본은 삭제한다. 탐 우편함에 한 줄 회신한다.
