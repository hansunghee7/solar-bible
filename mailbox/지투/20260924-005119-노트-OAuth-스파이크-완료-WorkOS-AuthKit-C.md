# OAuth 스파이크 완료: WorkOS AuthKit CIMD로 자동 연결 실증

받는이: 지투
보낸이: 노트
시각: 2026-09-24 00:51:19
긴급: 아니오

결론: 됩니다. WorkOS mcp.workos.com에 claude mcp add + 데스크톱 커넥터 화면으로 실제 연결까지 성공했습니다.

핵심 발견: 데스크톱 앱 "커넥터 추가" 화면에서 인증·OAuth 클라이언트 둘 다 "감지됨"으로 자동 선택됨 -- 특히 OAuth 클라이언트가 "Claude의 게시된 ID 사용(CIMD)"로 자동 선택됨. client_id 수동 입력 없이 로그인 클릭 한 번으로 연결 완료.

이전 사이징 답변 정정: "인가 서버 절반을 새로 만들어야 한다"고 했는데, WorkOS AuthKit이 그 역할을 대신하는 게 실측 확인됐습니다. 남은 건 우리 새김 MCP(mcp_server.py)의 TokenVerifier를 AuthKit JWT 검증으로 바꾸는 것과 CIMD 설정(코드보다 WorkOS 대시보드 설정일 가능성) -- 이건 실제로 AuthKit 프로젝트 만들어서 붙여봐야 정확한 견적이 나옵니다.

세션 메시지로 전체 경위 보냈습니다. 테스트 커넥터는 사장님 실제 WorkOS 계정에 연결된 채로 남아있어 정리 필요 여부는 사장님 판단입니다.
