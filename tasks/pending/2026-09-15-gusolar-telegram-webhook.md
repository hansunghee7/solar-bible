## 발주: 탐 → 구솔라

status: IN_PROGRESS

받는 이: 구솔라 — 이 발주부터 먼저 처리해라(최우선)

## 배경

`tasks/done/2026-09-15-gusolar-telegram-fix-최우선.md`에서 밝혀진 원인:
Hermes Agent의 텔레그램 polling 모드에 알려진 미해결 버그가 있다
("silent polling death" — getUpdates는 계속 호출되지만 받은 메시지가
핸들러로 전달 안 됨, GitHub 이슈 #102260, 재시작·업데이트·웹훅 삭제
전부 효과 없었다고 보고됨). 유일하게 시도 안 된 우회책이 **webhook
모드 전환**이다. 사장님이 이 우회책으로 진행하기로 결정했다(2026-09-15).

**목표는 "웹훅 모드가 이 버그를 실제로 피해가는지 검증"이다.** 영구
인프라를 바로 짓지 말고, 먼저 싸고 빠르게 확인한다(솔라바이블 §10
원칙과 같은 정신 — 검증 안 된 걸 자산으로 치지 않는다).

## 작업

### 1단계: 임시 공개 HTTPS 주소 만들기 (Cloudflare Quick Tunnel)

- `cloudflared`가 설치돼 있는지 확인(`cloudflared --version`). 없으면
  설치한다(공식 Cloudflare 도구, 무료, 되돌리기 쉬움 — 설치까지는
  승인 없이 진행해도 된다).
- Hermes 게이트웨이가 webhook을 받을 로컬 포트를 정한다(기본값 8443,
  `TELEGRAM_WEBHOOK_PORT`로 바꿀 수 있음 — 특별한 이유 없으면 기본값
  그대로 8443 써라).
- **Quick Tunnel 실행**(계정·도메인 없이 즉시 임시 공개 URL을 받는 방법):
  ```
  cloudflared tunnel --url http://localhost:8443
  ```
  실행하면 `https://무작위단어들.trycloudflare.com` 같은 임시 주소가
  나온다. 이 주소를 받아 적어둔다. **이 프로세스는 켜져 있는 동안만
  유효하다 — 꺼지면 주소가 사라진다. 지금은 "된다/안 된다"만 확인하는
  단계라 상시 자동 실행은 이번에 안 한다(별도 발주).**

### 2단계: Hermes를 webhook 모드로 전환

- 환경변수 설정(솔라바이블 §10 — 비밀값은 이 저장소에 절대 적지 마라,
  로컬에만 둔다):
  - `TELEGRAM_WEBHOOK_URL=https://<1단계에서 받은 주소>/telegram`
  - `TELEGRAM_WEBHOOK_SECRET=<openssl rand -hex 32 같은 걸로 새로 생성>`
    (필수 — 이게 없으면 게이트웨이가 webhook 모드로 시작을 거부한다)
- `hermes gateway restart`로 재시작.
- 게이트웨이 로그에 `[telegram] Connected to Telegram (webhook mode)`가
  찍히는지 확인한다(polling 모드가 아니라 webhook 모드로 붙었다는 뜻).

### 3단계: 실제 검증 (여기가 진짜 완료 기준)

- 재시작 완료했다는 걸 이 파일에 적은 뒤, **사장님께 텔레그램으로 정확한
  검증 문구를 보내달라고 요청**하는 문장을 남긴다(예: "웹훅 검증1").
- 그 문구가 gateway.log에 inbound로 찍히는지, 그리고 **실제로 텔레그램에
  답장이 가는지**까지 확인해야 한다. 이번엔 polling 때와 달리 "연결됨"
  로그만으로 완료 처리하지 마라 — 지난번에 그렇게 했다가 실제로는 안
  되는 걸 완료로 잘못 표시한 적이 있다(오늘 있었던 일, 재발 금지).

## 완료 기준

1~2단계 실제 조치 내용(설치 여부, 받은 tunnel 주소는 이 파일엔 적어도
되지만 웹훅 시크릿 값은 적지 마라)을 적고, 3단계 검증 요청 문장을 남긴
뒤 `tasks/done/2026-09-15-gusolar-telegram-webhook.md`로 옮기고 git
add·commit·push한다. **사장님의 실제 텔레그램 응답 확인 전까지는
"DONE=VERIFIED"라고 쓰지 마라** — "웹훅 모드 전환 완료, 검증 대기"까지만.

---

처리 중 (시작 01:09 UTC+9) — 자동 폴러 처리
처리 중 (10:17 UTC+9) — 자동 폴러 중단: 게이트웨이 webhook 전환에 필요한 `.env` 쓰기 및 `hermes gateway stop/restart`가 승인 패턴으로 스마트 거부되어 2~3단계 진행 불가. 수동 승인 필요.
