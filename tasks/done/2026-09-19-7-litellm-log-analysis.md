# LiteLLM Proxy 로그 분석 보고서

**대상 파일:** `C:\Users\PC\AppData\Local\hermes\litellm-proxy\proxy.log`
**분석일:** 2026-09-19
**총 로그 줄 수:** 3001줄

---

## 1) 'Started server process' 재시작 목록

| 재시작 횟수 | 줄 번호 | PID | 직전 로그 시각 | 비고 |
|:---:|:---:|:---:|:---:|:---|
| 1 | 1 | [42836] | N/A (첫 시작) | 최초 기동 |
| 2 | 195 | [22500] | 00:13:28 | prisma ModuleNotFoundError 500 오류 직후 |
| 3 | 410 | [38436] | 00:51:04 | prisma ModuleNotFoundError 500 오류 직후 |
| 4 | 464 | [3976] | 00:51:04 | 정상 응답 구간 후 재시작, 종료 흔적 없음 |
| 5 | 874 | [20304] | 13:03:23 | prisma 오류 + UTF-8/BOM 파싱 오류 혼재 구간 |
| 6 | 1586 | [11208] | 13:14:22 | prisma 오류 구간 |
| 7 | 1756 | [32020] | 13:21:08 | Gemini RateLimit(429) 발생 직후 |
| 8 | 1796 | [24304] | 18:03:47 | 'No api key passed in' 오류 구간 |
| 9 | 1887 | [20508] | 18:21:50 | UTF-8 디코딩 오류 + 'No api key' 혼재 구간 |
| 10 | 1990 | [5876] | 22:01:08 | **^C (Ctrl+C) 수동 중단** — 로그에 `^C` 원문 확인 |
| 11 | 2064 | [30464] | 08:18:11 | 'No connected db' 오류 대량 발생 구간 |
| 12 | 2076 | [22976] | 08:18:11 | 직전 재시작(11회차) 직후 매우 짧은 간격 재시작 |
| 13 | 2516 | [25156] | 15:46:25 | 'No connected db' 오류 지속 구간 |
| 14 | 2633 | [16436] | 20:42:28 | 'No connected db' 오류 대량 발생 구간 |
| 15 | 2933 | [22616] | 23:46:14 | 'No connected db' 오류 대량 발생 구간 |

**총계:** 15회 재시작 (최초 1회 + 재시작 14회)

---

## 2) 401 Unauthorized 응답 목록

| 줄 번호 | 시각 | 메서드 | 경로 | 클라이언트 | 비고 |
|:---:|:---:|:---:|:---|:---|:---|
| 1624 | 13:15:52 | GET | /health | 127.0.0.1:56838 | health 체크 401 |
| 1632 | 13:18:02 | GET | /v1/models | 127.0.0.1:50115 | 모델 목록 조회 401 |
| 1794 | 18:03:47 | GET | /health | 127.0.0.1:52958 | health 체크 401 |
| 1834 | 18:13:32 | GET | /health | 127.0.0.1:58192 | health 체크 401 |
| 1872 | 18:21:50 | GET | /health | 127.0.0.1:65049 | health 체크 401 |
| 2583 | 15:58:42 | GET | /models | 127.0.0.1:56171 | 모델 목록 조회 401 |
| 2677 | 23:15:33 | GET | /health | 127.0.0.1:60174 | health 체크 401 |
| 2987 | 08:13:00 | GET | /v1/models | 127.0.0.1:61626 | 모델 목록 조회 401 |
| 2994 | 08:13:00 | GET | /models | 127.0.0.1:61627 | 모델 목록 조회 401 |
| 3001 | 08:25:50 | POST | /v1/chat/completions | 127.0.0.1:59499 | **★ 채팅 완료 API 401 ★** |

**총계:** 10건

### 시간대별 401 횟수

| 시간대 | 횟수 | 내역 |
|:---|:---:|:---|
| 08시대 (08:00~08:59) | 3건 | GET /v1/models, GET /models, **POST /v1/chat/completions** |
| 13시대 (13:00~13:59) | 2건 | GET /health, GET /v1/models |
| 15시대 (15:00~15:59) | 1건 | GET /models |
| 18시대 (18:00~18:59) | 3건 | GET /health ×3 |
| 23시대 (23:00~23:59) | 1건 | GET /health |

### ★ POST /v1/chat/completions 401 강조

- **줄3001, 08:25:50** — 유일하게 채팅 완료 엔드포인트(`POST /v1/chat/completions`)에서 401 발생.
- 클라이언트는 `127.0.0.1:59499`. Authorization 헤더 누락 또는 무효.
- 나머지 9건은 모두 GET 요청(health 체크 또는 모델 목록 조회). 채팅 완료 API에 대한 401은 이 건이 유일.

---

## 3) 재시작별 직전 30줄 종료 흔적 원문 발췌

### 1회차 (줄1, PID [42836]) — 최초 기동
- 직전 30줄: 없음 (파일 첫 줄)
- 종료 흔적: **없음**

### 2회차 (줄195, PID [22500])
- 직전 30줄 범위: 줄165~194
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄175~176: `Traceback (most recent call last):` / `File "...starlette/middleware/errors.py", line 164, in __call__`
  - 줄186~188: `File "...litellm/proxy/db/exception_handler.py", line 115, in is_database_infrastructure_error` / `import prisma` / `ModuleNotFoundError: No module named 'prisma'`
  - 줄194: `ModuleNotFoundError: No module named 'prisma'`

### 3회차 (줄410, PID [38436])
- 직전 30줄 범위: 줄380~409
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄392~394: `File "...litellm/proxy/db/exception_handler.py", line 115, in is_database_infrastructure_error` / `import prisma` / `ModuleNotFoundError: No module named 'prisma'`
  - 줄408~409: 동일 패턴 반복

### 4회차 (줄464, PID [3976])
- 직전 30줄 범위: 줄434~463
- 종료 흔적: **없음**
- INFO 응답 23건 정상 처리 구간 (POST /chat/completions 200 OK 다수)
- 종료 신호 없이 재시작

### 5회차 (줄874, PID [20304])
- 직전 30줄 범위: 줄844~873
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄864: `12:58:16 - LiteLLM Proxy:ERROR: http_parsing_utils.py:194 - Invalid JSON payload received: unexpected character...`
  - 줄867: `13:00:00 - LiteLLM Proxy:ERROR: http_parsing_utils.py:194 - Invalid JSON payload received: UTF-8 byte order mark (BOM) is not supported...`
  - 줄870: `13:03:23 - LiteLLM Proxy:ERROR: http_parsing_utils.py:194 - Invalid JSON payload received: UTF-8 byte order mark (BOM) is not supported...`
  - 줄886~890: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc0 in position 62...`
  - 줄912: `13:09:53 - LiteLLM Proxy:ERROR: common_request_processing.py:1474 - /chat/completions: Missing required parameter: 'messages'.`

### 6회차 (줄1586, PID [11208])
- 직전 30줄 범위: 줄1556~1585
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄1315: `INFO: 127.0.0.1:51279 - "GET /health HTTP/1.1" 500 Internal Server Error`
  - 줄1320~1321: `Exception: No api key passed in.` / traceback
  - 줄1419~1420: `import prisma` / `ModuleNotFoundError: No module named 'prisma'`

### 7회차 (줄1756, PID [32020])
- 직전 30줄 범위: 줄1726~1755
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄1662~1679: `litellm.RateLimitError: GeminiException - {"error": {"code": 429, "message": "You exceeded your current quota..."}}`
  - 줄1696: `litellm.llms.custom_httpx.http_handler.MaskedHTTPStatusError: Client error '429 Too Many Requests'...`
  - 줄1735~1752: `litellm.exceptions.RateLimitError: ... GeminiException - ... 429 ...`
  - 줄1755: `INFO: 127.0.0.1:51559 - "POST /chat/completions HTTP/1.1" 429 Too Many Requests`

### 8회차 (줄1796, PID [24304])
- 직전 30줄 범위: 줄1766~1795
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄1768: `18:03:47 - LiteLLM Proxy:ERROR: auth_exception_handler.py:159 - ... Exception occured - No api key passed in.`
  - 줄1770~1773: `Exception: No api key passed in.`

### 9회차 (줄1887, PID [20508])
- 직전 30줄 범위: 줄1857~1886
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄1837~1838: `18:19:08 - LiteLLM Proxy:ERROR: http_parsing_utils.py:212 - Unexpected error reading request body - 'utf-8' codec can't decode byte 0xc0 in position 64...`
  - 줄1848~1849: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4 in position 61...`
  - 줄1863: `18:19:08 - LiteLLM Proxy:ERROR: common_request_processing.py:1474 - /chat/completions: Missing required parameter: 'messages'.`
  - 줄1866~1871: `18:21:50 - LiteLLM Proxy:ERROR: auth_exception_handler.py:159 - ... No api key passed in.`

### 10회차 (줄1990, PID [5876]) — ★ Ctrl+C 수동 중단
- 직전 30줄 범위: 줄1960~1989
- 종료 흔적: **없음** (단, 줄1990 자체에 `^C` 원문 존재)
- **줄1990 원문:** `^CINFO:     Started server process [5876]`
- 주요 ERROR 원문:
  - 줄1960~1989: `21:57:25~22:01:08 - LiteLLM Proxy:ERROR: auth_exception_handler.py:159 - ... No connected db.` 다수 반복
- **원인:** 로그 파일 상에 `^C`가 직접 찍혀있어, 사용자가 터미널에서 Ctrl+C로 uvicorn을 수동 중단한 후 재시작한 것으로 확인됨.

### 11회차 (줄2064, PID [30464])
- 직전 30줄 범위: 줄2034~2063
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄2027~2042: `08:00:54 - LiteLLM Proxy:ERROR: ... No connected db.` 다수
  - 줄2048~2063: `08:18:10~08:18:11 - LiteLLM Proxy:ERROR: ... No connected db.` 다수

### 12회차 (줄2076, PID [22976])
- 직전 30줄 범위: 줄2046~2075
- 종료 흔적: **없음**
- **특이사항:** 11회차(줄2064) 재시작 후 불과 12줄 만에(줄2076) 또 재시작. 매우 짧은 운영 후 재시작.
- 주요 ERROR 원문:
  - 줄2048~2063: `08:18:10~08:18:11 - ... No connected db.` (11회차와 동일 구간 일부 중복)

### 13회차 (줄2516, PID [25156])
- 직전 30줄 범위: 줄2486~2515
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄2489~2494: `15:41:31~15:43:17 - LiteLLM Proxy:ERROR: ... No connected db.` 다수
  - 줄2500~2515: `15:43:17~15:46:25 - LiteLLM Proxy:ERROR: ... No connected db.` 다수

### 14회차 (줄2633, PID [16436])
- 직전 30줄 범위: 줄2603~2632
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄2608~2629: `20:42:19~20:42:28 - LiteLLM Proxy:ERROR: ... No connected db.` 다수
  - 줄2645~2669: 14회차 기동 후 `22:49:19 - ... No connected db.` 계속

### 15회차 (줄2933, PID [22616])
- 직전 30줄 범위: 줄2903~2932
- 종료 흔적: **없음**
- 주요 ERROR 원문:
  - 줄2902~2923: `23:45:15 - LiteLLM Proxy:ERROR: ... No connected db.` 다수
  - 줄2927~2932: `23:46:13~23:46:14 - LiteLLM Proxy:ERROR: ... No connected db.` 다수

---

## 4) 재시작별 '종료 흔적 있음/없음' 표 + 원인 후보

| 회차 | PID | 종료 흔적 | 원인 후보 |
|:---:|:---:|:---:|:---|
| 1 | [42836] | 없음 | 첫 기동 — 정상 시작 |
| 2 | [22500] | 없음 | [추정] `ModuleNotFoundError: No module named 'prisma'`로 인한 500 오류 연쇄 발생. uvicorn 자체의 정상 종료 신호가 아닌 외부(래퍼 스크립트/프로세스 관리자)에 의한 강제 재시작 가능성. |
| 3 | [38436] | 없음 | [추정] 2회차와 동일 패턴: prisma 미설치로 인한 `ModuleNotFoundError` 연쇄. 상위 래퍼에 의한 재시작. |
| 4 | [3976] | 없음 | [추정] 직전 구간이 정상 200 OK 응답 23건으로 종료 흔적 전혀 없음. uvicorn 로그상 종료 신호 없이 재시작 → 상위 프로세스 관리자, 스케줄러, 또는 수동 재시작 가능성. |
| 5 | [20304] | 없음 | [추정] prisma 오류 + UTF-8/BOM 파싱 오류(`UnicodeDecodeError`, `Invalid JSON payload`) 혼재. 명시적 종료 신호 없이 재시작 → 외부 재시작 가능성. |
| 6 | [11208] | 없음 | [추정] prisma ModuleNotFoundError + 'No api key passed in' 오류 지속. 종료 흔적 없음 → 외부 재시작. |
| 7 | [32020] | 없음 | [추정] Gemini RateLimit(429) 발생 직후 재시작. 429는 Gemini API 측 Quota 초과이며 프록시 자체 크래시 원인은 아님. 프록시 프로세스는 정상 응답(429 반환) 후 외부 재시작된 것으로 보임. |
| 8 | [24304] | 없음 | [추정] 'No api key passed in' 인증 오류 지속 환경. 종료 흔적 없이 재시작 → 상위 스크립트/스케줄러 재시작 가능성. |
| 9 | [20508] | 없음 | [추정] UTF-8 디코딩 오류 + 'No api key passed in' 혼재. 종료 흔적 없음 → 외부 재시작. |
| 10 | [5876] | **없음** (단, 줄1990에 `^C` 원문) | [추정] **사용자가 터미널에서 Ctrl+C(SIGINT)로 uvicorn을 수동 중단.** 로그 원문 `^CINFO: Started server process [5876]`에서 확인. 이후 수동 재시작. |
| 11 | [30464] | 없음 | [추정] 'No connected db' 오류 대량 발생 환경. 종료 흔적 없이 재시작 → 상위 스크립트/스케줄러 재시작. |
| 12 | [22976] | 없음 | [추정] 11회차 재시작 불과 12줄 만에 다시 재시작. 매우 짧은 운영 후 재시작으로, 기동 직후 크래시 또는 빠른 재시작 루프 가능성. 'No connected db' 오류 환경 지속. |
| 13 | [25156] | 없음 | [추정] 'No connected db' 오류 대량 발생. 종료 흔적 없음 → 외부 재시작. |
| 14 | [16436] | 없음 | [추정] 'No connected db' 오류 대량 발생. 종료 흔적 없음 → 외부 재시작. |
| 15 | [22616] | 없음 | [추정] 'No connected db' 오류 대량 발생. 종료 흔적 없음 → 외부 재시작. |

### 종합 원인 분석

1. **prisma 패키지 미설치 ( early restarts ):** 2·3·5·6회차에서 `ModuleNotFoundError: No module named 'prisma'`가 반복적으로 발생. litellm이 DB 예외 처리 로직에서 prisma 모듈을 import하려다 실패하여 500 오류로 이어짐. 프록시 크래시를 직접 유발한 것은 아니나, 상위 프로세스 관리자에 의한 재시작을 촉발했을 가능성.

2. **Ctrl+C 수동 중단 (10회차):** 유일하게 명확한 종료 원인이 로그 상에 남음. `^C` 원문이 줄1990에 존재.

3. **'No connected db' / 'No api key passed in' 오류 지속 (후반부):** 11회차 이후 대부분의 재시작 직전 구간에서 'No connected db' 또는 'No api key passed in' 오류가 대량 발생. 그러나 이는 요청 처리 중 발생한 인증/DB 연결 오류일 뿐, 프록시 프로세스 자체를 종료시킨 직접적 원인으로 보기는 어려움. 종료 흔적(Shutting down, SIGTERM, Traceback 등)이 전혀 발견되지 않으므로, **상위 래퍼 스크립트, 프로세스 관리자(watchdog), 또는 수동 재시작에 의한 재시동일 가능성**이 높음.

4. **짧은 재시작 간격 (12회차):** 11회차 재시작 후 12줄 만에 다시 재시작된 점은 비정상. 기동 직후 크래시 또는 빠른 재시작 루프 가능성.

5. **UTF-8/JSON 파싱 오류:** 여러 회차에서 `UnicodeDecodeError`, `Invalid JSON payload`, `BOM` 오류가 발생했으나, 이는 개별 요청 처리 실패일 뿐 프로세스 종료 원인은 아님.

---

## 민감값 처리

- 모든 `Authorization` 헤더, API 키, 토큰 값은 원본 로그에 노출되지 않아 <가림> 처리 불필요.
- 오류 메시지에 포함된 `Requester IP Address:127.0.0.1`은 로컬호스트이므로 식별 위험 없음.
-Gemini API 응답 본문(JSON)은 분석 목적에 필요한 범위만 인용하고, URL·계정 식별 가능 정보는 포함하지 않음.

---

*분석 끝.*
