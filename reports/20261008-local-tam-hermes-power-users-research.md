# 헤르메스 고수 운용법 조사 (제미나이 검색 연동, 로컬탐, 2026-10-08)
경로: 무료 키 429 → Vertex(회사 계정 simon 재인증 필요로 실패) → 개인 계정(hansunghee7)으로 Vertex 성공. 첫 호출은 검색 없이 모델 지식으로만 답해 "Hermes Agent는 존재하지 않는다"고 답함(환각, 폐기).

## 원문 대조 결과
- 확인됨(원문 열람): 크론은 비활동 타임아웃 기본 600초, `HERMES_CRON_TIMEOUT` 환경변수로 조정, 0이면 무제한 (공식 문서 hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting).
- 확인 못 함: "hermes cron doctor" 명령(해당 문서에 문구 없음). Reddit 글 본문(자동 열람 차단)이라 Maker/Checker·Happy path·Fail-closed·Idempotency·STATE.md 주장은 원문 대조 전.
- 지어낸 것으로 판단: 답변 본문에 적힌 주소 중 `1f3xxxx`, `1cxyyyy`, `1cqxxxx` 꼴과 github issue 130821·130431은 실재 근거 없음. 단, 이런 가짜 주소도 HTTP 200이 나오므로 200은 존재 증거가 아님.
- 실제 grounding 출처(최종 주소 12개): 공식 cron 문서, github issues 52968·131585, reddit r/hermesagent 글 6개(1tfrilq, 1t66lhy, 1u8fm0t, 1t29ogw, 1wluvmc, 1w0sqrs), webvise 프로필 가이드, dailydoseofds 마스터클래스, hermes-megathreads 사용 사례 문서.

## 주장 요약(원문 대조 전이면 가설)
1. 프로필 하나당 역할 하나(SOUL.md 단일 목적)로 컨텍스트 격리 (webvise 가이드, reddit 1t66lhy 근거 추정).
2. 크론 점검은 LLM 없는 스크립트로(0토큰), 무인 실행은 단계마다 STATE.md에 기록해 반복 실행에도 안전하게(멱등) — reddit 1w0sqrs 근거 추정.
3. 만드는 세션과 검증 세션 분리(Maker/Checker).
