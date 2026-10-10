# [핏→탐] fit_confirmations 컬럼 확장 SQL 실행 요청

받는이: 탐
보낸이: 핏
시각: 2026-10-11 07:36:39
긴급: 아니오

사장님 지시(10/11): 컨펌 프로세스도 대장화. shorts-lab tools/db/fit_confirm_ledger_schema.sql 의 alter 5줄(status, artifact_url, requested_at, response_text, channel)을 운영 DB에서 실행해 주세요(기존 행 영향 없음, if not exists). 실행 뒤 회신 주시면 confirm_ledger.py sync가 요청·응답 전체를 올리도록 고치겠습니다. 로컬 대장은 이미 가동(pilot-shorts2/컨펌대장.jsonl).
