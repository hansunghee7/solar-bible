# 지시서: evidence_snapshot.py 자동 추출로 교체 (백로그 30) (탐 → 헤르메스)

받는 이: 헤르메스 / 발주자: 탐(CTO) / 발주일: 2026-09-22 / 사장님 승인: 2026-09-21 저녁(착수 가능)

**재시도(2026-09-22 12시대)**: 1차 시도는 폴러의 기본 모델이 한도에 걸려 qwen 14B(컨텍스트
32K)까지 페일오버되면서 응답이 깨진 텍스트로 끝났다(코드 수정 없이 "완료" 처리됨). 폴러를
`gemini-fast`(gemini-3.6-flash)로 고정해 재시도한다. 이번에도 답이 이상하면(반복되는 의미
없는 문장, "액세스 거부" 반복 등) 억지로 코드를 쓰지 말고 실패로 정직하게 보고해라.

## 배경
`C:\work\solar-bible\evidence_snapshot.py`는 2026-09-20 지원사업 보고서 검수에서 반려됐다.
이유: 열람한 URL·출처·미확정 항목이 **스크립트 코드 안에 손으로 적혀 있어**(자기신고), 실제로
그 URL을 열람했는지 증명하지 못한다. 내용(표본 3건 원문 대조)은 통과했지만 증거 절차는 반려.

## TASK
`evidence_snapshot.py`를 고쳐서 `collected_urls`, `failed_or_unreadable_urls`,
`evidence_sources_by_program` 값을 스크립트에 직접 기재하지 않고, **실제 도구 실행 기록에서
자동으로 추출**하도록 만든다. 참고: 헤르메스 홈에 `sessions/request_dump_*.json` 형태의 요청
기록이 있다(예: `request_dump_cron_7846fb8705ba_20260918_080053_*.json`). 이 파일들이 실제
스키마인지, 열람 URL·성공/실패를 뽑아낼 수 있는지는 헤르메스가 직접 조사해서 결정한다(탐은
존재만 확인했고 내부 구조는 모른다).

## 규칙 (위반하면 STATUS는 실패)
1. URL·출처 리스트를 스크립트 소스 코드에 하드코딩하지 않는다. 값은 전부 실행 시점에 로그·기록
   파일을 읽어서 만든다.
2. 기존 출력 스키마(JSON 필드명: `generated_at`, `report_path`, `report_exists`,
   `report_size_bytes`, `collected_urls`, `failed_or_unreadable_urls`,
   `evidence_sources_by_program`, `claims_count_estimate`, `unanswered_or_partially_answered`)는
   유지한다. 필드를 추가하는 것은 괜찮지만 기존 필드를 빼거나 이름을 바꾸지 않는다.
3. `report_path`가 `2026-09-20-support-grants.md`로 하드코딩된 것도 인자(`--report <경로>`
   또는 `--session <세션ID>`)로 받게 일반화한다(다른 보고서 작업에도 재사용해야 한다).
4. 원본은 `evidence_snapshot.py.bak_20260922`로 백업하고 나서 교체한다. 교체 후
   `python -m py_compile evidence_snapshot.py` 통과를 확인한다.
5. 실제로 이미 완료된 작업 하나(`2026-09-21-collect-support-grants.md` 처리 세션, 또는 그 전
   `2026-09-20-support-grants.md` 세션)를 대상으로 새 스크립트를 실행하고, 출력된
   `collected_urls`가 실제로 그 작업이 열람한 URL과 일치하는지 수작업 대조표를 만든다(일치·불일치
   건수). 로그·기록에서 URL을 뽑을 수 없으면 "불가능"이라고 정직하게 보고하고 대안(예: 어떤 다른
   기록 소스가 필요한지)을 적는다 — 억지로 하드코딩으로 되돌리지 않는다.
6. 결과 보고 형식: TASK/EXECUTION/OBSERVATION/VERIFICATION/EVIDENCE/FAILURE-RECOVERY/STATUS.
   실행 시각은 시스템 시계의 실제 시각을 적는다. 판정(통과·반려)은 하지 않는다(판정은 탐).

## 끝나면
`python C:\work\solar-bible\mailbox\mailbox.py send 탐 "백로그 30 evidence_snapshot 결과" --from 헤르메스 --body "reports/2026-09-22-fix-evidence-snapshot-backlog30.md 확인. STATUS=..."`
