# YouTube Studio 수집 파일럿 2차 시도 보고서

**실행 시각**: 2026-09-21 23:30(예약) / 실제 실행: 2026-09-21 23:32 KST
**시도 구분**: 2차 (유인, 화면이 이미 떠 있는 상태)
**STATUS**: 화면이 Studio가 아님 (BLOCKED: NOT_STUDIO)

---

## TASK
어사이드(Aside) 브라우저에 이미 떠 있는 YouTube Studio 화면을 새로고침 없이 **읽기 전용 캡처**로 수집해, 화면 수치와 `assets/data/youtube-insight.json` 최신 스냅샷을 대조한다. 승인 도구가 없으므로 클릭·키입력·스크롤·새로고침은 일체 금지.

---

## EXECUTION
| 단계 | 동작 | 결과 |
|------|------|------|
| 1 | 화면 캡처 (`computer_use` action=capture, mode=som) | **Aside.exe** 창 캡처 성공 (1456×782) |
| 2 | 화면 내용 판독 | **Remember 웹사이트**(`connect.rememberapp.co.kr`)가 메인 영역에 표시됨 |
| 3 | 좌측 즐겨찾기 확인 | "(2) 신기한 아파트사전 - YouTube"(요소 #19) 존재, YouTube Studio 책갈피 없음 |
| 4 | 탭 목록 확인 | 열려 있는 탭: 위키백과, 지메일, Google Gemini, 빙마크 — Studio 탭 없음 |
| 5 | 조작 시도 여부 | **시도하지 않음** (승인 필요 조작 금지, 화면이 Studio 아님) |

---

## OBSERVATION
- **표시된 화면**: Remember 전문가 네트워킹 사이트 (프로필 카드, 피드, 추천 토픽)
- **YouTube Studio 접근 경로**: 즐겨찾기 #19 "(2) 신기한 아파트사전 - YouTube" → 채널 페이지 → Studio 링크 클릭 필요하나 **승인 없어 클릭 불가**
- **새로고침 여부**: 수행 안 함 (F5 키 입력 금지)
- **수집된 Studio 수치**: **0개** (Studio 화면이 아니므로)

> ⚠️ 이 수치는 **새로고침을 못 한 지금 화면 상태** 기준이며, Studio 화면이 아니므로 **최신 여부 판단 불가**.

---

## VERIFICATION
`C:\work\hansunghee7.github.io\assets\data\youtube-insight.json` (최신 갱신: 2026-09-20T22:40:31Z) 기준 최신 값(2026-09-21):

| 항목 | API 값 (youtube-insight.json) | 화면 값 | 일치 여부 |
|------|------------------------------|---------|-----------|
| 구독자 수 | 28 | 수집 불가 (Studio 아님) | 대조 불가 |
| 총 조회수 | 16,823 | 수집 불가 | 대조 불가 |
| 상위 콘텐츠 1: "아파트 옥상 물탱크..." | 4,481 | 수집 불가 | 대조 불가 |
| 상위 콘텐츠 2: "주민 차는 들어가는데..." | 5,134 | 수집 불가 | 대조 불가 |
| 상위 콘텐츠 3: "지하주차장 천장에..." | 984 | 수집 불가 | 대조 불가 |
| 상위 콘텐츠 4: "아파트 계단실에..." | 1,304 | 수집 불가 | 대조 불가 |
| 상위 콘텐츠 5: "아파트 복도에..." | 370 | 수집 불가 | 대조 불가 |

- **대조 가능 항목 수**: 0 / 7 (0%)
- **일치 항목 수**: 0
- **판정**: **검증 불충분** (대조 가능 항목이 절반 미만)

---

## FAILURE-RECOVERY
| 항목 | 내용 |
|------|------|
| 차단 사유 | 화면이 YouTube Studio가 아님 (Remember 사이트 표시 중) |
| 승인 없는 우회 시도 여부 | 없음 (지시서 준수) |
| 재시도 가능성 | 승인자(사람)가 Studio 화면으로 이동시켜 둔 뒤 재실행하면 가능 |
| 차단 도구 | `computer_use`의 클릭/키입력/스크롤 액션은 승인 필요 → 자동 차단됨 |

---

## EVIDENCE
- 캡처 이미지: `C:\Users\PC\AppData\Local\hermes\cache\images\computer_use_0254136fb618464989ece80d2539bdfe.png`
- 캡처 메타: Aside.exe, 1456×782, 46개 상호작용 요소, URL 표시줄 `connect.rememberapp.co.kr`
- 기준 데이터: `C:\work\hansunghee7.github.io\assets\data\youtube-insight.json` (updated_at: 2026-09-20T22:40:31.645568Z)

---

## 측정 요약
| 지표 | 값 |
|------|-----|
| 소요 시간 | 약 2분 (캡처 1회 + 판독) |
| 사람 개입 지점 | 없음 (자동 캡처만) |
| 오류·막힘 | 화면이 Studio 아님 → 수집 중단 |
| 읽은 수치 개수 | 0개 |
| 대조 가능 항목 수 / 일치 수 | 0 / 0 |
| 새로고침 후 값 변화 | 해당 없음 (새로고침 안 함) |

---

## 참고: 1차 시도와의 비교
- **1차 (무인 크론)**: 창이 화면에 없고 승인자도 없어 `BLOCKED: NO_WINDOW_NO_APPROVER` (`reports/2026-09-21-studio-collect-pilot-attempt1-cron-blocked.md`)
- **2차 (유인)**: 창은 있으나 **Studio 화면이 아님** → `BLOCKED: NOT_STUDIO` (본 보고서)

---

## 다음 단계 제안 (탐 판정용)
1. 사람이 Aside에서 즐겨찾기 #19 "(2) 신기한 아파트사전 - YouTube" 클릭 → 채널 페이지 → "YouTube Studio" 또는 "채널 분석" 링크 클릭 → Studio 대시보드/분석 탭 도달
2. 그 상태로 3차 시도 실행 (승인 도구 없이 캡처만)
3. 또는 공식 YouTube Analytics API 연동으로 전환 검토

---
*보고서 생성: 2026-09-21 23:34 KST / 헤르메스 자동 작성*