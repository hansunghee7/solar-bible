# 작업기 장부(worker_ledger) Supabase 표 생성 요청

받는이: 탐
보낸이: 핏
시각: 2026-10-08 12:39:35
긴급: 아니오
요청: 표 생성과 쓰기 도구(ledgerdb.py) 요청 확인

사장님 10/8 결정: 작업기 장부를 표로 만들어 Supabase DB로 관리. 요청 1) 표 worker_ledger 생성(DDL 초안 C:/work/_ops/worker_ledger_schema.sql, 열 10개: 작업기 id·계정·포트·갱신시각·잔여크레딧·읽은시각·오늘 컷·오늘 차감·상태·상태원인). 2) proc.py처럼 쓰기·읽기 도구 scripts/ops/ledgerdb.py(upsert/select). 3) 계정 이메일이 들어가므로 비공개 처리(공개 저장소에 이메일 금지). 시드: flow 1~7, vids 1~6(계정 미정), gemini 1~2는 DDL 파일 하단 주석. 핏은 factory_check.py가 3시간마다 이 표를 갱신하도록 붙일 예정. 배경 KPT 회고: 핏 프로세스표 핏#87.
