# 헤르메스 카드: 백로그 정제용 업무대장 사본 (탐 -> 헤르메스)

읽기만 하는 작업이다. 파일을 고치거나 지우지 마라. 키·토큰은 쓰지 마라. 이 저장소에는 결과 내용을 올리지 마라.
1. 저장소 `C:/work/hansunghee7.github.io`에서 `python scripts/ops/session_brief.py 탐 --full-list` 출력을 `C:/work/_ops/orch/ledger_snapshot.txt`에 저장한다.
2. 같은 저장소에서 `python scripts/ops/ledger_lint.py` 출력을 `C:/work/_ops/orch/ledger_lint.txt`에 저장한다.
끝 조건: 두 파일이 있으면 끝. 보고는 "저장함, 열린 건 수" 한 줄만.
