# 구PC(goosolar) Claude Code CLI+Bun+텔레그램 플러그인 설치 (탐 -> 헤르메스)

## TASK
구PC(goosolar, Ubuntu, Tailscale로 SSH 접속 가능: `ssh goosolar`)에 Claude Code 터미널 CLI를
텔레그램 채널 상시 서비스로 띄울 준비를 해줘. 지금은 Node/Bun/claude CLI가 전혀 없고 파이썬
헤르메스 크론만 돌고 있음을 확인함.

1. `ssh goosolar "curl -fsSL https://claude.ai/install.sh | bash"` 로 CLI 네이티브 설치(Node/npm 불필요).
2. `ssh goosolar "curl -fsSL https://bun.sh/install | bash"` 로 Bun 설치(텔레그램 플러그인 실행에 필요).
3. `ssh goosolar "cd ~/goosolar-tam 2>/dev/null || mkdir -p ~/goosolar-tam && cd ~/goosolar-tam && claude --version"` 로
   설치 확인 겸 워크스페이스로 쓸 디렉터리 준비(없으면 만들기).
4. 그 디렉터리에서 `claude` 를 1회 실행해 텔레그램 플러그인(`plugin:telegram@claude-plugins-official`)을 설치.
5. `/login`은 브라우저가 필요함 - 화면 없는 서버라 나오는 로그인 URL을 그대로(값 편집 없이) 결과에 남겨줘,
   사장님이 다른 기기 브라우저로 열어 완료할 것임. 로그인 전까지는 여기서 멈추고 결과 보고.

**하지 마세요**: 봇 토큰 값을 직접 다루거나 `.env`에 쓰는 것(비밀값 직접 전달 금지 원칙, 별도 세션이 처리함).

## 보고 형식
각 단계 실행 출력 원문과 종료 코드, `claude --version` 결과, 확보한 로그인 URL을 STATUS 앞에 적어줘.
STATUS: DONE 또는 실패 사유
