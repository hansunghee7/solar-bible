# 카카오톡 사용처 인벤토리 (읽기 전용 조사)

**조사 일시**: 2026-09-19  
**조사 범위**: `C:/work/solar-bible`, `C:/work/hansunghee7.github.io`(읽기만), 헤르메스 `scripts`·`cron/jobs.json`, `C:/Users/PC/.claude/settings.json` MCP 항목  
**목적**: 사장님 알림 채널을 텔레그램으로 통일함에 따라 카카오톡 잔재 식별 및 대체 매핑

---

## 요약표

| 파일:줄 | 용도 | 텔레그램 대체 방법 |
|---------|------|-------------------|
| solar-bible/mailbox/README.md:49 | 정책 문구: "카카오톡과 카카오톡 MCP는 쓰지 않는다" 선언 | 이미 텔레그램 통일 정책 반영됨 (별도 조치 불필요) |
| solar-bible/mailbox/탐/20260919-191339-마야-정정-...md:16 | README 내 "카카오톡 나에게 보내기" 항목이 방침과 충돌함을 지적 | README에서 해당 항목 제거/수정 → 텔레그램 안내로 대체 |
| hansunghee7.github.io/docs/진행상황_아카이브/2026-09-17.md:394,402,411,426,464,490,498-499,501,505,517,519,532,534,542-543,636,647,653 | 과거 기록: 카카오톡 "나에게 보내기"/MCP(`KakaotalkChat-MemoChat`)로 양방향 알림 검증·운용 이력 | 아카이브 문서이므로 수정 불필요. 운영 참고용 보존 |
| hansunghee7.github.io/docs/에이전트_퍼포먼스_백로그.md:27 | 계획: 헬스체크 실패 시 카카오톡 "나에게 보내기"로 알림 | `hermes send --to telegram` 또는 `mailbox_courier.py` 텔레그램 경로로 대체 |
| hansunghee7.github.io/docs/지시서/2026-09-17_로컬탐_양방향릴레이_HumanRelay제거.md:200-206 | 설계안: 탐(클라우드)이 `📥` 작성 시 카카오톡 "나에게 보내기" 병행 발송 | 지시서 아카이브라 수정 불필요. 신규 구현 시 텔레그램 gateway `deliver: telegram` 사용 |
| hansunghee7.github.io/docs/진행상황_아카이브/2026-09-03.md:143,147 | 모닝 브리핑에 카카오 PlayMCP "나와의 채팅", 카카오톡 커넥터 연동 시도 기록 | 모닝 브리핑 크론(`daily_briefing`)은 이미 `deliver: local` → 텔레그램 발송은 `hermes send --to telegram`로 별도 처리 |
| hansunghee7.github.io/_layouts/default.html:34 | 공유 버튼용 percent-encoding 안내에 "카카오톡" 언급 | 정적 문구이므로 수정 불필요(기능적 연동 아님) |
| .claude/projects/*/...jsonl (여러 파일, 예: 75a96c61..., ba9cfc44...) | Claude Code 세션 내 MCP 서버 **"claude.ai 카카오톡 나챗방"** 등록 이력 (settings.json 본문엔 없음) | Claude Code용 MCP는 별도 관리. 헤르메스 알림 경로와 무관 → 조치 불필요 |
| solar-bible/reports/2026-09-15-shinpc-cleanup-investigation.md:69,165,268 | 폴더명/캐시 통계: "카카오톡 받은 파일" (파일 시스템 잔재) | 정리 완료 이력. 운영 경로 아님 |
| solar-bible/docs/진행상황.md:234,245 | 캐시 통계: `KakaoTalk_cache_approx` (과거 측정값) | 기록용. 현재 운영 경로 아님 |

---

## 조사 상세

### 1. 헤르메스 런타임 (scripts, cron/jobs.json)
- **scripts/**: 카카오톡 관련 코드 없음 (검색 결과 0건)
- **cron/jobs.json**: `relay-watcher`가 `deliver: "telegram"` 사용. 카카오톡 발송 잡 없음.

### 2. C:/Users/PC/.claude/settings.json
- MCP 서버 등록 항목 없음 (hooks만 존재).
- 단, `.claude/projects/` 하위 이력 파일들에 `"claude.ai 카카오톡 나챗방"` MCP 추가 기록이 남아 있음 → Claude Code 세션용이며 헤르메스 알림 경로와 무관.

### 3. hansunghee7.github.io (문서/아카이브 위주)
- **운영 코드 아님**: 대부분 과거 진행상황 아카이브, 지시서 초안, 블로그 콘텐츠(카카오페이 로고 등)에서 언급.
- **실질적 운영 잔재**: `에이전트_퍼포먼스_백로그.md`의 헬스체크 알림 계획(카카오톡 "나에게 보내기") 정도가 향후 구현 시 대체 필요.

---

## 조치 권고

| 우선순위 | 대상 | 조치 |
|----------|------|------|
| 높음 | `solar-bible/mailbox/README.md` | "카카오톡 나에게 보내기" 항목 제거 → 텔레그램 안내로 교체 |
| 높음 | `hansunghee7.github.io/docs/에이전트_퍼포먼스_백로그.md` | 헬스체크 알림 채널을 텔레그램으로 명시 수정 |
| 낮음 | 기타 아카이브/문서 | 기록물로 보존(수정 불필요) |

---

## 검증

- [x] `C:/work/solar-bible` 전체 검색 완료
- [x] `C:/work/hansunghee7.github.io` 전체 검색 완료 (읽기 전용)
- [x] 헤르메스 `scripts/`, `cron/jobs.json` 검색 완료
- [x] `C:/Users/PC/.claude/settings.json` 및 프로젝트 이력 확인 완료
- [x] 토큰·키·IP 미포함 확인

**보고서 경로**: `C:/work/solar-bible/reports/2026-09-19-kakao-inventory.md`