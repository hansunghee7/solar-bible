# 지시서: verify_claims.py 낭비 제거와 503 재시도 (탐 → 헤르메스)

## TASK
`C:\Users\PC\AppData\Local\hermes\scripts\verify_claims.py`를 다음 3가지로 고친다. 정본 규칙은 `C:\work\solar-bible\docs\모델_로스터.md` 3절.

## 배경 (탐이 실측한 사실)
- gemini-3.6-flash 무료 한도는 키 하나당 하루 20회다(429 응답의 한도값).
- 지금 `pick_working_key()`는 실행할 때마다 키마다 시험 호출 1회를 한다. 이 호출이 20회 한도를 갉아먹는다.
- 오늘 실행에서 구글이 일시적으로 503을 냈는데, 현재 재시도는 429에만 있다.
- API 실패를 판정(unsupported)으로 섞던 결함은 탐이 이미 고쳤다(`error` 판정, 종료 코드 2). 되돌리지 않는다.

## 할 일
1. **시험 호출 제거**: 키 선택용 사전 호출을 없앤다. 실제 검증 호출에서 429(일일 한도, 응답에 `PerDay`가 들어 있음)가 나오면 그때 다음 키로 넘어간다. 분당 한도 429(`retryDelay` 있음)는 기존처럼 대기 후 같은 키로 재시도한다.
2. **마지막 성공 키 기억**: 같은 실행 안에서 한 번 성공한 키는 나머지 주장에도 계속 쓴다(주장마다 키 선택을 다시 하지 않는다).
3. **503 재시도**: 503과 500은 2, 4, 8초 간격으로 최대 3회 재시도한다. 그래도 실패하면 `error` 판정.
4. 키 순서와 이름은 그대로: `GEMINI_VERIFY_KEY` → `GOOGLE_API_KEY` → config.yaml의 gemini 키. 값은 화면과 로그에 출력하지 않는다.

## 규칙
- 수정 전 백업 `verify_claims.py.bak_0919_hardening`을 만든다.
- 시험은 `C:\work\hermes_verify_test.json`에 만든 3개 주장(사실 1, 반대 1, 원문에 없는 것 1)으로 하고, 원문 출력을 증거로 붙인다. 3.6-flash 한도가 없을 수 있으니 429가 나면 그 사실을 그대로 보고한다(한도 초기화 후 재시험 필요라고 적는다).
- 키, 토큰, IP를 보고서에 쓰지 않는다(공개 저장소).
- 결과 보고 형식: TASK/EXECUTION/OBSERVATION/VERIFICATION/EVIDENCE/FAILURE-RECOVERY/STATUS.
