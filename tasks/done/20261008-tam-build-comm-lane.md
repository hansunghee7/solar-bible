# 소통 전용 레인 구PC 설치 (탐 -> 헤르메스)

받는이: 헤르메스
보낸이: 탐 클라우드 (2026-10-08, 사장님 지시: 소통 전용 레인을 스크립트로 두고 타미가 설치)
성격: 타미 줄과 분리된 소통용 스크립트 묶음(폴러 감시 cron과 텔레그램 답장 접수 서비스)을 구PC에 설치한다. 스크립트는 탐이 써 두었고 타미는 실행만 한다(LLM 판단 없음). 텔레그램 부분은 사람이 만드는 환경 파일이 없으면 건너뛰고 "건너뜀" 문구를 출력하는 것이 정상이다.

허용 범위: ssh로 구PC에서 아래 두 스크립트를 실행한다. crontab과 `~/.config/systemd/user/`에만 쓴다. 다른 파일·cron은 건드리지 않는다. 키·토큰 값 출력 금지. 쓰기가 거부되면 우회하지 말고 거부 문구를 그대로 보고한다. 명령은 한 번만 실행한다.

실행할 명령:
```
ssh goosolar 'cd /home/goosloar/solar-bible && git pull --rebase --autostash --quiet && bash tasks/assets/comm_lane_install.sh /home/goosloar/solar-bible && bash tasks/assets/comm_lane_status.sh'
```

성공 기준: 출력에 `== 1.`, `== 2.` 구역과 `--- date`가 모두 있다. 텔레그램의 "건너뜀"은 실패가 아니라 결과다.
결과 문서 본문에는 **명령 출력 원문만** 코드 블록으로 붙이고 다른 문장을 쓰지 않는다(요약·해석·계획 금지). 실행하지 못했다면 "실행하지 못함"과 이유 한 줄만 쓴다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 tasks/pending/ 의 원본은 삭제한다.
