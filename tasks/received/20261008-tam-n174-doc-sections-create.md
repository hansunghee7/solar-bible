# 20261008-tam-n174-doc-sections-create - 수신 확인

## 메타
- 수신 시각: 2026-10-08T18:38:28
- 레인: pending

## 의뢰(받은 그대로)

# N174 1단계: 수파베이스 doc_sections 표 생성과 적재 (로컬 탐 -> 타미)

받는이: 타미
보낸이: 로컬 탐 (2026-10-08, 사장님 지시: 브라우저 조작은 타미가 하고 수행 후 스크립트로 검증)
성격: 새 표 하나를 만든다(CREATE만, 삭제·변경 없음). 소넷 서브에이전트와 클로드 크레딧은 쓰지 않는다.

순서:
1. `python C:/work/hansunghee7.github.io/scripts/ops/browser_lease.py status` 가 "임대 없음"이면 타미 이름으로 진행(점유 중이면 진행하지 말고 그 사실만 보고).
2. 수파베이스 운영 프로젝트의 SQL Editor를 열고 `C:/work/_ops/n174/s1/doc_sections.sql` 내용을 실행한다. 운영 SQL 요령은 탐 기억 reference_supabase-prod-sql-editor 를 따른다. 키 값은 화면·로그에 출력하지 않는다.
3. 스크립트 검증(필수, 눈으로 확인 금지): `python C:/work/_ops/n174/s1/load_sections.py --dry` 가 오류 없이 끝나는지 확인하고, 이어서 `python C:/work/_ops/n174/s1/load_sections.py` 로 적재한 뒤 `python C:/work/hansunghee7.github.io/scripts/ops/opsdb.py select doc_sections --cols id --limit 1` 로 행이 있는지 확인한다.
4. 임대를 반납한다(`browser_lease.py` 의 release).

허용 범위: INSERT와 CREATE TABLE만. DROP·DELETE·ALTER 금지. 쓰기가 거부되면 우회하지 말고 거부 문구를 그대로 보고한다. 로그인 화면이 뜨면 `[사람 개입 필요: 자격증명]` 한 줄만 올리고 멈춘다.

성공 기준: 3번 두 명령의 종료 코드 0과 select 결과 1행 이상. recall@3 20문항 시험은 이번 범위가 아니다(탐 클라우드가 이어서 한다).
결과 문서에는 각 명령 출력의 마지막 5줄을 그대로 붙이고 요약을 쓰지 않는다. 실행하지 못했다면 "실행하지 못함"과 이유를 쓴다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 pending의 원본은 삭제한다. 결과는 mailbox/탐/ 에 올린다.
