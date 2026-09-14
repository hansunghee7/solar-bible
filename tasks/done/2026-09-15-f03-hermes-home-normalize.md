## 발주: 탐 → 신솔라

status: QUEUED

받는 이: 신솔라 (구솔라 몫으로 넘길지는 신솔라가 내부에서 판단)

## 배경

헤르메스 과제 백로그 우선순위(사장님 확정, hansunghee7.github.io
`docs/진행상황.md` 2026-09-14 8차 인수인계의 "완료/우선순위 정리판"
순서 7번, 원래 ID F0-3)를 오늘부터 순서대로 발주한다. 이 항목이 1번인
이유: Gateway와 CLI가 서로 다른 설정 경로를 보고 있으면 이후 모든
진단·작업이 꼬인다. 기반부터 정리한다.

## 작업

`%LOCALAPPDATA%\hermes`와 `~/.hermes` 두 경로 중 Gateway와 CLI가 실제로
어느 쪽 config/.env를 읽는지 확인한다. 두 경로에 서로 다른 설정이 있다면
어느 쪽이 실제로 적용되는지부터 실측으로 밝힌다(추측 금지, 솔라바이블
§10). 확인되면 둘 중 하나를 canonical 경로로 확정하고, 다른 쪽을
참조/심볼릭 링크하거나 정리해 설정이 하나로 합쳐지게 만든다.

## 완료 기준

Gateway와 CLI가 동일한 config/.env를 쓰는 것을 실제로 확인한다(예: 값을
한쪽에서 바꿔 다른 쪽에서 반영되는지 테스트). 결과를 이 파일을
`tasks/done/2026-09-15-f03-hermes-home-normalize.md`로 옮긴 안에 적고
git add·commit·push까지 한다. 솔라바이블 §3에 따라 중간에 멈추면 그때까지
한 것만이라도 저장한다.
---
2026-09-14T22:50:04Z
처리 결과: 아래

## 조사 결과

### 환경
- HERMES_HOME 환경변수: C:\Users\PC\AppData\Local\hermes (설정됨)
- hermes CLI 경로: /c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes
- HOME: /c/Users/PC
- ~ = /c/Users/PC

### 두 경로 실측
1. ~/.hermes = /c/Users/PC/.hermes
   - config.yaml 있음 (플랫폼 설정: telegram enabled, token 마스킹, allowed_users)
   - .env 있음 (TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS, OLLAMA_KEEP_ALIVE)
   - TEST_MARKER_LOCAL_HERMES.txt 존재함 (실행 에이전트가 생성한 테스트 마커)

2. %LOCALAPPDATA%\hermes = /c/Users/PC/AppData/Local/hermes
   - HERMES_HOME 환경변수가 이 경로로 설정됨
   - config.yaml 있음 (모델, database, runtime, gateway, display, llm, api_server, bot_peers, platforms 등 전체 설정 — ~/.hermes보다 훨씬 방대함)
   - .env 있음 (큰 파일, 용량 비교 필요 — 접근 승인 문제로 내용 전체 확인 못함)
   - auth.json, channel_directory.json, gateway.lock, cron/, cache/, backups/, skills_prompt_snapshot 등 큰 상태 디렉터리 다수 존재
   - 다수의 .env.backup, config.yaml.backup 있음

### 판정
- HERMES_HOME 환경변수가 C:\Users\PC\AppData\Local\hermes (%LOCALAPPDATA%\hermes)로 설정되어 있음.
- hermes doctor에서 state.db, cron/executions.db 등의 경로가 HERMES_HOME 기반임.
- 두 경로 모두 실제 파일이 존재하고 서로 다른 설정을 담고 있음:
  - ~/.hermes: telegram 플랫폼 설정 + telegram 토큰/허용사용자 등 메시징 관련 env가 중심
  - %LOCALAPPDATA%\hermes: 모델/환경/gateway/display 등 전체 config + 큰 상태 데이터(auth.json, 세션, cron DB 등)
- 어느 쪽이 실제로 적용되는지는 HERMES_HOME 환경변수가 %LOCALAPPDATA%\hermes로 설정되어 있으므로, 대부분의 헤르메스 런타임은 이 경로를 canonical home으로 사용할 가능성이 높음.
- 단, config.yaml은 두 곳 모두에 존재하고 내용이 다르므로, 실제 적용되는 config.yaml이 어느 쪽인지 실측 확인이 필요했음. 그러나 hermes CLI가 이 환경에서 config.yaml을 실제로 읽는 경로를 안전하게 확인하기 위한 테스트(예: 한쪽 config에 테스트 키 삽입 후 hermes config get으로 확인)는 "위험 명령"으로 차단되어 실행하지 못함.

### 한계
- %LOCALAPPDATA%\hermes/.env 내용 전체 확인 불가 (접근 승인 필요 — 비밀값 포함)
- 두 config.yaml이 실제로 런타임에 어느 쪽에서 로드되는지 실측 테스트 불가 (쓰기 승인 차단)
- 텔레그램 토큰/허용사용자 등 민감값이 양쪽 .env에 중복 존재할 가능성 있음

### 결론
- HERMES_HOME이 %LOCALAPPDATA%\hermes로 설정되어 있고, 헤르메스 doctor 및 상태파일이 이 경로를 기준으로 동작하므로 **canonical home은 %LOCALAPPDATA%\hermes**로 판단됨.
- ~/.hermes는 과거 설정/백업 또는 별도 소스로부터 생성된 것으로 보이며, 실제 런타임과의 정합성은 미확인 상태.
- 완전 마무리를 위해: (1) %LOCALAPPDATA%\hermes/.env와 ~/.hermes/.env의 실제 내용 비교(승인 후), (2) 한쪽 config.yaml에 고유 테스트 키(예: test_canonical_marker: "2026-09-15-f03")를 넣고 hermes config get으로 어느 쪽이 읽히는지 확인, (3) 결과를 바탕으로 canonical 결정 후 나머지 경로 정리(심볼릭 링크 혹은 병합)가 필요.
