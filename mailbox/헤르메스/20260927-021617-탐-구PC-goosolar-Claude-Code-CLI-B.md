# 구PC(goosolar) Claude Code CLI+Bun+텔레그램 플러그인 설치, 상시화

받는이: 헤르메스
보낸이: 탐
시각: 2026-09-27 02:16:17
긴급: 아니오
요청: 위 1~5단계 실행하고 로그인 URL과 각 단계 exit code를 우편으로 회신

TASK: 구PC(goosolar, Ubuntu, Tailscale)에 Claude Code 터미널 CLI를 텔레그램 채널 상시 서비스로 띄울 준비. 1) curl -fsSL https://claude.ai/install.sh | bash 로 CLI 네이티브 설치(Node/npm 불필요). 2) curl -fsSL https://bun.sh/install | bash 로 Bun 설치(텔레그램 플러그인 실행에 필요). 3) claude 를 1회 실행해 이 디렉터리(작업 디렉터리로 쓸 곳, 예: ~/goosolar-tam)를 워크스페이스로 신뢰 수락. 4) claude 안에서 텔레그램 플러그인(plugin:telegram@claude-plugins-official) 설치. 5) /login 은 브라우저가 필요합니다 - 화면 없는 서버라 나오는 로그인 URL을 그대로(값 편집 없이) 보고해 주세요, 사장님이 다른 기기 브라우저로 열어 완료하겠습니다. 로그인 전까지는 여기서 멈추고 보고. 봇 토큰은 이 작업에 포함하지 마세요(배치는 제가 직접 SSH로 합니다). EVIDENCE로 각 단계 실행 출력 원문과 exit code, claude --version 결과를 남겨 주세요. 형식: TASK/EXECUTION/OBSERVATION/VERIFICATION/EVIDENCE/FAILURE-RECOVERY/STATUS. 참고: 노드/Bun/claude CLI 전혀 없고 파이썬 헤르메스 크론만 돌고 있다는 것까지는 이미 확인됨(sudo·브라우저 여부는 미확인).
