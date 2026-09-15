## 발주: 탐 → 구솔라

status: DONE
받는 이: 구솔라 — **이 발주부터 먼저 처리해라(오늘 큐 중 최우선).**

## 배경

구PC(구솔라)를 두는 목적은 "사장님이 외부에서 신PC를 깨우거나 간단한 조사를 하는 것"이다(solar-bible.md §14, 2026-09-15 재정의). 그 외부 통로는 텔레그램이다. 그런데 사장님이 실제로 텔레그램으로 말을 걸어도 응답이 없다고 확인했다. 자체조사(`tasks/done/2026-09-15-gusolar-self-survey.md`)에서 config.yaml엔 `platforms.telegram.enabled: true`로 나왔지만, 그건 설정값을 본 것이지 실제로 게이트웨이가 떠서 텔레그램과 통신하고 있는지 확인한 게 아니었다. 이게 안 고쳐지면 구PC의 존재 이유 자체가 없다 — 최우선으로 고친다.

## 조사·조치 항목

1. **텔레그램 게이트웨이 프로세스가 실제로 떠 있는지 확인**한다(프로세스 목록, `hermes` 관련 명령이 있으면 그걸로, 없으면 tasklist 등으로).
2. 떠 있다면 **로그를 확인**해 연결 실패 원인을 찾는다(인증 오류, 네트워크 타임아웃, 봇 토큰 문제 등). 로그 위치를 모르면 config.yaml 근처나 hermes 관련 폴더에서 찾는다.
3. 안 떠 있다면 **직접 시작해보고** 어떤 에러가 나는지 그대로 기록한다.
4. **네트워크 도달성 확인**: 이 PC에서 `api.telegram.org`로 나가는 연결이 되는지 확인한다(방화벽·프록시가 막고 있을 가능성).
5. 원인을 찾았으면 **고쳐본다**(게이트웨이 재시작, 설정 수정 등 — 되돌리기 쉬운 조치는 승인 없이 진행해도 된다. 예: 서비스 재시작, config.yaml의 명백한 오타 수정).
6. **실제로 검증한다**: 고쳤다고 적기 전에, 사장님이 텔레그램으로 메시지를 보내면 실제로 응답이 오는지까지 확인해야 완료다(DONE=VERIFIED — "설정이 맞아 보인다"는 증거가 아니다). 이 검증은 사장님이 직접 텔레그램에서 메시지를 보내주셔야 확인되니, 조치까지 마친 뒤 이 파일에 "사장님, 지금 텔레그램으로 [정확히 어떤 메시지]를 보내 확인해주세요"라고 구체적으로 요청하는 문장을 남긴다.

## 완료 기준

1~5번 결과를 이 파일에 적는다. 6번(실제 텔레그램 응답 확인)은 사장님 확인이 필요하니, 조치 결과 + 사장님께 요청할 정확한 문장을 적은 뒤 `tasks/done/2026-09-15-gusolar-telegram-fix-최우선.md`로 옮기고 git add·commit·push한다. 원인을 못 찾았어도 중간에 멈추면 그때까지 확인한 것만이라도 적어서 옮긴다(솔라바이블 §3).

## 조사 결과

### 1. 텔레그램 게이트웨이 프로세스 확인
- `hermes gateway status`: 게이트웨이 실행 중 — "✓ Scheduled Task registered: Hermes_Gateway", "✓ Gateway process running (PID: 10316)". 즉 게이트웨이는 떠 있었다.
- `tasklist`: hermes.exe 프로세스 2개 확인(RDP-Tcp#8 세션 내). 게이트웨이 자체는 정상 가동 상태.

### 2. 로그 확인 (연결 실패 원인)
- 로그 위치: `/c/Users/Desktop/AppData/Local/hermes/logs/gateway.log`, `/c/Users/Desktop/AppData/Local/hermes/logs/gateway-stdio.log`.
- gateway.log 최근 텔레그램 관련 로그:
  - 2026-09-09 14:52:21~14:58:15: 텔레그램 연결 시도(1/8) → IPv4 IP 149.154.166.110, 149.154.167.220 모두 실패, "getaddrinfo failed"(`[Errno 11001]`), "Telegram connect timed out after 30s" → 재시도 간격 120s·240s·300s로 증가, 결국 연결 안 됨.
  - 2026-09-09 14:21:44 "Telegram polling confirmed healthy" → 14:23:29 "polling degraded (heartbeat probe)" → 14:23:49 "Disconnected from Telegram".
  - 이후 "Disconnected from Telegram"만 반복, "Connected to Telegram" 기록 없음. 즉 이 게이트웨이는 2026-09-09 이후 텔레그램 연결을 유지하지 못한 상태로 떠 있었음.
- gateway-stdio.log: "Sticky Telegram path 149.154.166.110 failed", "IPv4 Telegram API IP 149.154.166.110 failed" 반복 — IPv4 sticky path가 계속 실패.

**원인 판단:** 게이트웨이 자체는 떠 있으나, 텔레그램 API(149.154.166.110, 149.154.167.220)로의 연결이 유지되지 못함. config.yaml의 `platforms.telegram.enabled: true`는 맞지만, 연결 자체가 안 된 상태. auth.json의 봇 토큰(`8896539486:***`)은 설정돼 있고(노출하지 않음 — §10 준수), allowed_users `8609932977`도 설정돼 있음 — 인증 정보 자체는 정상으로 보임. 네트워크 도달성은 4번에서 확인.

### 3. 직접 시작 시도 (해당 없음 — 게이트웨이 이미 떠 있었음)
- 게이트웨이가 이미 떠 있었으므로 "직접 시작"은 불필요. 대신 재시작으로 연결 복구를 시도(5번 조치로 이어짐).

### 4. 네트워크 도달성 확인
- `curl -sS -m 10 https://api.telegram.org` → HTTP 302 응답, time 1.16s. 즉 이 PC에서 api.telegram.org로의 HTTP 연결은 성립함(302는 봇 토큰이 없어서 나오는 정상 응답 — "Not Found" 유사).
- `curl https://api.telegram.org/botXXXXXX:YYYYYYY/getMe` → `{"ok":false,"error_code":404,"description":"Not Found"}` — 봇 토큰 없이 호출한 결과(정상).
- DNS: `nslookup api.telegram.org` → kns.kornet.net(168.126.63.1)를 통해 `api.telegram.org` 주소 2001:67c:4e8:f004::9, 149.154.166.110 확인 — DNS 정상.
- **결론: 구PC에서 api.telegram.org로의 네트워크 도달성은 문제없음.** 연결 실패는 게이트웨이 측 연결 유지 문제(IPv4 stuck path 등)로 추정. 방화벽·방면 차단 아님.

### 5. 고쳐보기 (게이트웨이 재시작)
- 게이트웨이 재시작으로 텔레그램 연결 복구를 시도: `hermes gateway restart` 실행.
- 재시작 결과:
  - "✓ Killed 1 gateway process(es)"
  - "✓ Gateway stopped"
  - "✓ Gateway started via direct spawn (PID 7640) (PID: 11980)" — 새 게이트웨이 PID 11980으로 재가동.
- 재시작 후 로그 확인(08:49:00~08:49:15):
  - "Connecting to telegram..."
  - "Discovering Telegram API fallback IPs via DNS-over-HTTPS…" → "Auto-discovered Telegram fallback IPs: 149.154.166.110"
  - "Connecting to Telegram (attempt 1/8)…"
  - "Using sticky IPv4 Telegram API path 149.154.166.110"
  - **"Telegram polling confirmed healthy: getUpdates progressing (generation 1)"**
  - **"Connected to Telegram (polling mode)"**
  - **"✓ telegram connected"**
  - "set_my_commands OK for scope BotCommandScopeDefault (60 cmds)", "BotCommandScopeAllPrivateChats (60 cmds)", "BotCommandScopeAllGroupChats (60 cmds)"
  - "Telegram menu: 60 commands registered, 62 hidden (over 60 limit)"
- **게이트웨이 재시작으로 텔레그램 연결에 성공했다.** 로그상 명확한 연결 성공 표시 확인.

## 조치 결과 요약

- 원인: 게이트웨이가 떠 있으나 텔레그램 연결(149.154.166.110, 149.154.167.220)이 유지되지 못한 상태(config.yaml의 enabled: true는 맞았지만 연결 자체가 실패). 네트워크 도달성은 정상(구PC에서 api.telegram.org 접속 확인).
- 조치: `hermes gateway restart`로 게이트웨이 재시작 → 텔레그램 재연결 성공(log: `✓ telegram connected`, `polling confirmed healthy`). 설정 변경 없이 재시작만으로 해결.
- 추가 확인: 연결 후 봇 커맨드 등록까지 정상(`set_my_commands OK`).
- **이 조치는 되돌리기 쉬운 조치(게이트웨이 재시작)로, 승인 없이 진행 가능한 범위.**

## 6번 검증 — 아직 미완료 (사장님 확인 필요)

지금 게이트웨이는 텔레그램에 연결되어 있고 polling도 healthy 상태. **그러나 "실제로 사장님이 텔레그램으로 메시지를 보냈을 때 응답이 오는지"는 아직 확인하지 못했다.** 아래 문장으로 사장님께 확인 요청한다.

> **사장님, 지금 텔레그램(GooSolar_650_bot, ID 8896539486)으로 "구솔라 테스트"라고 보내주세요.** 게이트웨이는 방금 재시작해서 텔레그램 연결을 확인했습니다(log: `✓ telegram connected`, `polling confirmed healthy`, `set_my_commands OK`). 이 메시지에 구솔라가 응답하는지 확인되면 이 작업의 6번(실제 검증)이 완료됩니다. 응답 오면 "확인됨" 회신 주시면 그걸로 검증 완료 처리하겠습니다.

## 다음 것
* 사장님(텔레그램 확인): 위 문구로 "구솔라 테스트" 전송 → 구솔라 응답 여부 확인 → 회신.
* 구솔라(다음): 6번 확인되면 이 done 파일 그대로 유지 + 푸시. 안 되면 추가 원인 조사(이 미완료 상태를 done에 남긴 채).
