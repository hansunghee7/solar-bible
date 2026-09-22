# Studio 수집 파일럿 결과 보고서

## TASK
- **지시서**: `C:\work\solar-bible\tasks\hold\2026-09-21-studio-collect-pilot.md`
- **목적**: 어사이드(Aside) 브라우저 즐겨찾기의 YouTube Studio 화면을 새로고침해 최신 수치를 읽기 전용으로 수집 가능한지 실측
- **실행 시각**: 2026-09-21 23:30(예약) — 크론 작업으로 자동 실행
- **시행 횟수**: 1회(실패 시 1회 재시도 허용, 지시서 §39)

## EXECUTION
| 단계 | 시도 내용 | 결과 |
|------|-----------|------|
| 1 | `computer_use.list_apps`로 Aside 실행 확인 | Aside(PID 31988) 실행 중 확인됨 |
| 2 | `computer_use.capture(app="Aside", mode="som")`로 화면 캡처 시도 | "no on-screen window matched" — 창이 화면에 없음(최소화/숨김 추정) |
| 3 | `computer_use.focus_app(app="Aside", raise_window=true)`로 창 앞으로 가져오기 시도 | **차단됨**: "BLOCKED: computer_use `focus_app` requires approval but cron jobs run without a user present to approve it. Find an alternative approach that avoids driving the desktop." |
| 4 | 대체 수단 탐색 | 크론 환경에서 승인 불가 → 데스크톱 조작 도구 사용 불가 |

**소요 시간**: 약 2분 (도구 확인~차단 확인)

## OBSERVATION
- **화면 조작 도구 가용성**: `computer_use` 툴은 설치돼 있으나, `focus_app` 등 포커스/입력 액션은 크론 작업에서 **승인 필요로 차단**됨(config.yaml의 `approvals.cron_mode: approve` 미설정).
- **Aside 브라우저 상태**: 백그라운드 실행 중이나 화면상 윈도우가 노출되지 않음. 수동 포커싱 없이는 캡처·클릭·스크롤·새로고침(F5) 모두 불가능.
- **browser_exec 도구**: 웹 자동화용이며, Aside 데스크톱 앱 내부의 임베디드 웹뷰 제어에는 부적합(지시서 대상은 Aside 네이티브 창).
- **지시서 §17 조건 충족**: "화면 조작 도구(computer_use 또는 browser)가 이 실행에 없다" → **"도구 없음"으로 보고하고 중단**함.

## VERIFICATION
화면 수집 자체가 수행되지 않아 대조 불가.  
기존 `C:\work\hansunghee7.github.io\assets\data\youtube-insight.json`(2026-09-21 스냅샷) 최신 값만 기록:

| 항목 | API 값(2026-09-21) | 비고 |
|------|-------------------|------|
| 채널명 | 신기한 아파트사전 | handle: @sinkihanapt |
| 구독자 수 | 28 | |
| 총 조회수 | 16,823 | |
| 비디오 수 | 10 | |
| 상위 5개 영상(조회수 순) | 1. 주민 차는 들어가는데, 택배차는 못 들어갑니다 — 5,134<br>2. 아파트 옥상 물탱크가 전부 사라진 이유 — 4,481<br>3. 아파트 경사로를 만들었더니 주민들이 반대를 했습니다 — 1,554<br>4. 우리 집 창문을 열었는데 옆집 냄새가 들어오는 이유 — 1,622<br>5. 아파트 계단실에 바람을 넣는 놀라운 이유 — 1,304 | 2026-09-21 기준 누적 조회수 |

> 대조 가능 항목 0개 / 필요 절반 미만 → **검증 불충분**(지시서 §28)

## EVIDENCE
- **수집한 화면 수치**: 없음(도구 차단으로 화면 진입 실패)
- **절대 수치 저장 파일**: `C:\work\_ops\pilot\studio-values-2026-09-21.txt` — 화면 값 없음 표기
- **로그**: `computer_use` 차단 메시지 전문 위 EXECUTION 표에 기재

## FAILURE-RECOVERY
| 실패 원인 | 복구 시도 | 결과 |
|-----------|-----------|------|
| 크론에서 `focus_app` 승인 불가 | config.yaml에 `approvals.cron_mode: approve` 설정 필요 | 현재 세션 내 수정 불가(보호 파일, 사용자 승인 필요) |
| Aside 창 최소화/숨김 | 수동 포커싱 필요 | 크론 무인 환경에서 불가 |
| 재시도 1회 | 동일 환경에서 재시도해도 동일 차단 발생 | 재시도 생략(원인 동일) |

**판단**: 환경 설정 변경(`approvals.cron_mode: approve`) 및 Aside 창 상시 표시 상태가 선행돼야 재시도 의미 있음. 탐(CTO) 판단 대기.

## STATUS
**막힘(도구 없음)** — 화면 조작 도구(`computer_use` 포커스/입력 액션)가 크론 무인 환경에서 승인 차단으로 사용 불가. 지시서 §17·§20 준수해 즉시 중단, 재시도 없음.

---

**보고서 경로**: `C:\work\solar-bible\reports\2026-09-21-studio-collect-pilot.md`  
**절대 수치 보관**: `C:\work\_ops\pilot\studio-values-2026-09-21.txt`  
**참조 원문**: `C:\work\solar-bible\tasks\hold\2026-09-21-studio-collect-pilot.md`  
**대조용 API 스냅샷**: `C:\work\hansunghee7.github.io\assets\data\youtube-insight.json` (updated_at: 2026-09-20T22:40:31.645568Z)