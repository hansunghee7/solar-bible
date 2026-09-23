# P1 완료: caller_tenant_id 컬럼 PR #101, auto-merge, SQL 수동실행 필요

받는이: 지투
보낸이: 노트
시각: 2026-09-23 22:42:02
긴급: 아니오

P1 끝났습니다. PR: https://github.com/hansunghee7/simplifier-saegim/pull/101 (auto-merge 켜둠)

- store.py의 record_view/get_section/lookup/cite에 caller_tenant_id 인자 추가(기존 tenant_id=스코프는 그대로, 문서 공유 동작 안 바뀜)
- mcp_server.py의 lookup/get_section/cite 도구가 _current_tenant_id()를 caller_tenant_id로 전달
- supabase/011_caller_tenant_id.sql: guide_views/guide_citations에 nullable 컬럼+인덱스
- 테스트 5개 추가, 전체 185개 통과(기존 실패 1건은 이 변경과 무관, main에도 있음)

사람 손 필요: SQL 마이그레이션은 파일만 커밋했고 실제 실행은 Supabase 대시보드에서 직접 해야 합니다(이 저장소 기존 마이그레이션 전부 이 방식). PR 머지 후 지투나 사장님이 실행해주셔야 caller_tenant_id가 실제로 쌓입니다.

(SendMessage로도 같은 내용 보냈습니다)
