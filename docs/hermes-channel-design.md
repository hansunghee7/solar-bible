# 헤르메스 통신 채널 설계: SSH 직결 / GitOps 이중 채널

기록: 탐, 2026-09-15 (3차 인수인계 후속, 로컬 세션 실측)

## 배경

기존 채널(GitOps 폴링: 신솔라 크론 3분, 클로드 쪽 25분 send_later)은 항상
비동기다. 짧은 작업(수 초~수십 초 응답)까지 폴링 주기를 기다리는 건
낭비라서, 로컬 클로드 코드 세션이 있을 때는 SSH로 직접 동기 호출하는
경로를 추가한다. 클라우드 세션은 egress 차단으로 이 경로를 못 쓴다
(신PC 진행상황.md 3차 절 참고) — 그 경우는 그대로 GitOps만 쓴다.

## 채널 분기 기준

| 상황 | 채널 |
|---|---|
| 로컬 클로드 코드 + 응답을 몇 초~몇 분 안에 받아야 함(10분 이내) | SSH 직결 |
| 클라우드 세션(egress 차단) | GitOps만 (SSH 불가) |
| 긴 작업(10분 초과, 배치성) | GitOps (tasks/incoming → completed/failed) |
| 헤르메스↔헤르메스(A2A) | 지금 아님 — 구PC 파킹 상태, 상대 없음 |

## SSH 직결 사전 조건 (신PC 기준 실측 완료)

- **Tailscale**: 신PC(`desktop-2udnsls`, 100.67.79.19)·다른 기기
  (`desktop-202ap4o`, 100.83.83.53) 둘 다 이미 tailnet에 있음. 새로 설치
  불필요 — 오늘 확인 시점에 이미 Running.
- **OpenSSH Server(sshd)**: 기본 `Add-WindowsCapability OpenSSH.Server`
  경로가 이 신PC에서 COMException으로 막혀 있었다(2026-09-12
  `hermes-node-bridge/tasks/completed/SHINPC_SSH_TEST_RESULT.md`). 추정
  원인: `wuauserv`(Windows Update 서비스) Stopped/Manual — Capability
  설치가 내부적으로 Windows Update 소스를 써서 막혔을 가능성. **우회:**
  ```powershell
  winget install --id Microsoft.OpenSSH.Preview -e --accept-source-agreements --accept-package-agreements
  Start-Service sshd
  Set-Service -Name sshd -StartupType Automatic
  New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
  ```
  winget 경로는 Windows Update에 의존하지 않아 위 차단을 피한다.
- **관리자 계정 키 등록**: 로그인 계정이 Administrators 그룹이면 일반
  `~/.ssh/authorized_keys`는 sshd_config의 `Match Group administrators`
  규칙에 의해 **무시**된다. 반드시
  `C:\ProgramData\ssh\administrators_authorized_keys`에 공개키를 넣고,
  Administrators+SYSTEM만 접근 가능하도록 ACL을 좁혀야 한다:
  ```powershell
  Copy-Item "C:\Users\<user>\.ssh\id_ed25519.pub" "C:\ProgramData\ssh\administrators_authorized_keys" -Force
  icacls.exe "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r
  icacls.exe "C:\ProgramData\ssh\administrators_authorized_keys" /grant "Administrators:F" /grant "SYSTEM:F"
  ```

## 호출 방법 (실측 완료, DONE=VERIFIED)

```bash
ssh pc@100.67.79.19 'hermes chat -q "echo hello"'
```

- 2026-09-15 신PC 자기 자신(loopback, 같은 PC의 Tailscale IP)으로 실측:
  비밀번호 없이 키 인증 성공, 원격 헤르메스가 정상 응답
  (Session 20260915_223433_b9ec51).
- 같은 PC에서 호출할 때는 SSH 없이 `hermes chat -q "..."` 직접 호출.

### ⚠️ 명령경로 함정: 원격 셸은 Windows cmd.exe, 홑따옴표(')는 인자 구분 안 됨

로컬(bash)에서 흔히 쓰는 `ssh host "hermes chat -q 'echo hello'"` 형태는
**실패한다** — Windows OpenSSH가 원격 명령을 넘기는 기본 셸이 cmd.exe라
홑따옴표를 그대로 문자로 취급해 `unrecognized arguments: hello'` 에러가
난다(2026-09-15 실제로 겪음). 올바른 형태:

```bash
ssh host 'hermes chat -q "echo hello"'
```

즉 **로컬 쪽은 홑따옴표로 전체를 감싸고, 원격에 전달될 인자는 큰따옴표로
감싼다.** 따옴표를 반대로 쓰면 원격 cmd.exe 파싱이 깨진다.

## 아직 검증 안 된 것

- 위 실측은 신PC → 신PC 자기 자신(loopback)이다. 신PC 외 **다른 물리
  기기(노트북 등, 100.83.83.53)에서 실제로 접속하는 것**은 그 기기가
  검증 시점에 offline이라 아직 못 했다. 온라인일 때 동일 명령으로
  재검증 필요.
- 반대 방향(구PC → 신PC, 신PC → 구PC 중 구PC가 호출하는 방향)은 구PC가
  파킹 상태라 범위 밖. `hermes-node-bridge/tasks/incoming/
  GU_SOLAR_CHECK_SSH_STATUS.md`에 별도로 확인 요청이 올라가 있음.

## 폴링 대체안 (판단 진행 중, 확정 아님)

클로드 쪽 25분 폴링은 SSH 직결로 대체하는 대신, 헤르메스가
`tasks/done/` 커밋 후 solar-bible PR에 댓글 → 그 PR을
`subscribe_pr_activity`로 구독한 세션이 몇 초 안에 깨어나는 방식도 검토
중(진행상황.md 3차 절 참고). 이건 SSH 직결과 별개로, 클라우드 세션처럼
SSH를 못 쓰는 경우에도 적용 가능한 대안이라 우선순위 작업으로 남겨둔다.
