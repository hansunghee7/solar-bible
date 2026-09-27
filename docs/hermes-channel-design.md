# 헤르메스 통신 채널 설계: SSH 직결 / GitOps 이중 채널

기록: 탐, 2026-09-15 (3차 인수인계 후속, 로컬 세션 실측)

## 배경

기존 채널(GitOps 폴링: 신솔라 크론 3분, 클로드 쪽 25분 send_later)은 항상
비동기다. 짧은 작업(수 초~수십 초 응답)까지 폴링 주기를 기다리는 건
낭비라서, 로컬 클로드 코드 세션이 있을 때는 SSH로 직접 동기 호출하는
경로를 추가한다. 클라우드 세션은 egress 차단으로 이 경로를 못 쓴다
(신PC 진행상황.md 3차 절 참고). 그 경우는 그대로 GitOps만 쓴다.

## 채널 분기 기준

| 상황 | 채널 |
|---|---|
| 로컬 클로드 코드 + 응답을 몇 초~몇 분 안에 받아야 함(10분 이내) | SSH 직결 |
| 클라우드 세션(egress 차단) | GitOps만 (SSH 불가) |
| 긴 작업(10분 초과, 배치성) | GitOps (tasks/incoming → completed/failed) |
| 헤르메스↔헤르메스(A2A) | 지금 아님, 구PC 파킹 상태라 상대 없음 |

## SSH 직결 사전 조건 (신PC 기준 실측 완료)

- **Tailscale**: 신PC(`<PC>`, `<PC-IP>`)·다른 기기(`<다른기기>`,
  `<다른기기-IP>`) 둘 다 이미 tailnet에 있음. 새로 설치 불필요, 오늘
  확인 시점에 이미 Running.
- **OpenSSH Server(sshd)**: 기본 `Add-WindowsCapability OpenSSH.Server`
  경로가 이 신PC에서 COMException으로 막혀 있었다(2026-09-12
  `hermes-node-bridge/tasks/completed/SHINPC_SSH_TEST_RESULT.md`). 추정
  원인: `wuauserv`(Windows Update 서비스) Stopped/Manual, Capability
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
  여러 기기 키를 등록할 때는 `Copy-Item` 대신 `Add-Content`로 한 줄씩
  추가한다(기존 줄을 덮어쓰지 않도록).

## 호출 방법 (실측 완료, DONE=VERIFIED)

로컬 클라이언트가 **bash**일 때:
```bash
ssh <user>@<PC-IP> 'hermes chat -q "echo hello"'
```
- 2026-09-15 신PC 자기 자신(loopback, 같은 PC의 Tailscale IP)으로 실측:
  비밀번호 없이 키 인증 성공, 원격 헤르메스가 정상 응답
  (Session 20260915_223433_b9ec51).
- 같은 PC에서 호출할 때는 SSH 없이 `hermes chat -q "..."` 직접 호출.

### 명령경로 함정 1: 원격 셸은 Windows cmd.exe, 홑따옴표(')는 인자 구분 안 됨

로컬(bash)에서 흔히 쓰는 `ssh host "hermes chat -q 'echo hello'"` 형태는
**실패한다.** Windows OpenSSH가 원격 명령을 넘기는 기본 셸이 cmd.exe라
홑따옴표를 그대로 문자로 취급해 `unrecognized arguments: hello'` 에러가
난다(2026-09-15 실제로 겪음). 올바른 형태:

```bash
ssh host 'hermes chat -q "echo hello"'
```

즉 **로컬 쪽은 홑따옴표로 전체를 감싸고, 원격에 전달될 인자는 큰따옴표로
감싼다.** 따옴표를 반대로 쓰면 원격 cmd.exe 파싱이 깨진다. 이건 **로컬
클라이언트가 bash일 때만** 확인된 규칙이다. PowerShell 클라이언트는
아래 절 참고.

### 명령경로 함정 2: PowerShell 클라이언트는 원인·해법 확인됨

노트북(로컬 클라이언트가 PowerShell)에서 크로스 머신 검증 중 확인:
`ssh host 'hermes chat -q "echo hello"'`(위 bash 권장 형태)와
stop-parsing 토큰 `ssh host --% hermes chat -q "echo hello"` 둘 다
원격에서 `hello`가 별도 인자로 분리돼 `unrecognized arguments: hello`
에러가 난다. **띄어쓰기 없는 단어 하나짜리 질의는 정상 동작**
(`ssh host hermes chat -q hello`).

**원인**: 헤르메스가 아니라 PowerShell의 인자 전달 방식이다. Windows
PowerShell 5.1과 PowerShell 7.2 이하는 외부 실행파일(ssh.exe)에 인자를
넘길 때 문자열 안의 큰따옴표를 벗겨서 보낸다. 그래서 원격에는
`hermes chat -q echo hello`가 도착해 `hello`가 별개 인자가 된다.

**해법 (표준입력 사용, 권장)**: 따옴표 문제를 피해서 표준입력으로
넘긴다. 헤르메스 문서에 stdin 입력은 셸 해석 없이 글자 그대로 들어간다고
돼 있다. 긴 지시문, 따옴표, `$` 같은 문자가 섞여도 안전하다.
```powershell
"echo hello" | ssh <user>@<PC-IP> hermes chat --query-file -
```
(대안: 큰따옴표를 백슬래시로 이스케이프하는 방법도 있으나, 여러 줄
지시문에는 stdin 방식이 더 안전해 기본값으로 삼는다.)

**실측 상태**: DONE=VERIFIED. 2026-09-15 노트북(PowerShell)에서
`"echo hello" | ssh <user>@<PC-IP> hermes chat --query-file -` 실행,
멀티워드 질의가 그대로 전달돼 정상 응답(Session
20260915_231358_613a78). **PowerShell 클라이언트의 멀티워드 질의는
표준입력 방식을 기본으로 쓴다.**

## 아직 검증 안 된 것

- ~~신PC 외 다른 물리 기기에서 접속~~ → **완료**. 2026-09-15 노트북에
  Tailscale 신규 설치(`<노트북-IP>`) + 신규 키 등록 후
  `ssh <user>@<PC-IP> hermes chat -q hello` 실측 성공(Session
  20260915_230434_dd4e88).
- ~~PowerShell 클라이언트 멀티워드 질의~~ → **완료**. 위 stdin 방식으로
  해결(Session 20260915_231358_613a78).
- 반대 방향(구PC → 신PC, 신PC → 구PC 중 구PC가 호출하는 방향)은 구PC가
  파킹 상태라 범위 밖. `hermes-node-bridge/tasks/incoming/
  GU_SOLAR_CHECK_SSH_STATUS.md`에 별도로 확인 요청이 올라가 있음.

## 실측: 직접 호출 vs GitOps 비교 (2026-09-15/16, 로컬 탐 야간 과제 3)

같은 PC(신솔라)에서 비슷한 규모의 읽기 전용 조사 과제 하나씩을 두 채널로
나란히 실행해 비교했다.

| 항목 | 직접 호출 (F0-1, PC identity) | GitOps (F0-2, 네트워크 경로) |
|---|---|---|
| 발주 시각 | 15:09:42Z | 15:10:30Z (push) |
| 픽업 시각 | 즉시(동기 호출, 픽업 개념 없음) | 15:13:30Z 경으로 추정(다음 3분 주기, 발주가 직전 크론 실행과 겹쳐 1주기 밀림) |
| 완료 시각 | 15:10:18Z | 15:14:56Z (done 커밋), 15:15:17Z (pending 삭제 커밋) |
| 총 소요 | 약 36초 | 약 4분 26초~4분 47초 |
| 결과 품질 | 6개 항목 중 5개 정확 답변, 1개(LAN IP)만 "확인 불가" | 3개 항목 모두 답변, 정책(민감정보 비기재) 준수, 일부 판정은 "후속 조사로 미룸"으로 모호하게 남김 |

**주의사항(직접 호출)**: 기본 설정(`config.yaml`의 `model.provider: openai-codex` +
`model.default: upstage/solar-pro4:free`)으로 첫 시도(15:08:03~15:08:43Z)는
`HTTP 400: 'solar-pro4:free' model is not supported when using Codex with a
ChatGPT account`로 실패했다. `hermes doctor`가 같은 문제를 이슈 1번으로
잡아낸다(모델에 vendor 프리픽스가 있는데 provider가 openai-codex로 되어
있음). 크론 잡(`solar-bible-tasks-poller`)은 생성 시점에 박아둔
`provider_snapshot: nous`를 그대로 쓰므로 이 설정 오류 영향을 안 받아 계속
정상 동작해왔다(완료 197회 무사고). 직접 호출은 config.yaml을 고치는 대신
`--provider nous` 플래그를 명시해서 우회했다(재시도 15:09:42Z, 성공).
config.yaml 자체를 고치는 건 이번 과제 범위(읽기 전용/되돌릴 수 있는 것만)
밖이라 손대지 않았다. 백로그 L1-4(Hermes Primary→4090)와 얽힌 문제라 별도
발주가 맞다.

**판정**: 짧은 조사성 과제는 직접 호출이 압도적으로 빠르다(36초 대
4분 47초, 약 8배). 10분 문턱 기준(지시서)에는 둘 다 못 미쳤지만, GitOps는
크론 주기(3분) 자체가 최소 지연이라 초 단위로 끝나는 과제엔 항상
불리하다. 이후 과제는 지시서대로 직접 호출을 기본으로 쓰고, 10분을 넘길
것 같은 과제만 GitOps로 보낸다.

## 알려진 버그: 짧은/긴 폴러가 같은 체크아웃을 동시에 써서 결과가 유실됨 (2026-09-27, 탐)

`tasks/pending/`(짧은 폴러, `solar-bible-tasks-poller`)와 `tasks/pending-long/`
(긴 폴러, `solar-bible-long-poller`)는 둘 다 `pending_poller.py`를 쓰고, 둘 다
같은 로컬 체크아웃(`C:\work\solar-bible`)에서 매 회차 `git reset --hard origin/main`을
한다. 긴 폴러가 작업을 끝내고 **로컬 커밋만 하고 아직 push하기 전**에 짧은 폴러가
하드 리셋을 하면 그 커밋이 통째로 사라진다. 실제 사고: 탐이 넣은 구PC 설치 지시서를
긴 폴러가 09:04~09:08에 1차 실행하고 `tasks/done/`에 커밋까지 했으나(로컬 커밋
`6fedb93` 목격), 그 직후 짧은 폴러가 리셋해 커밋도 push도 우편 알림도 안 나감 →
origin/main에 파일이 그대로 남아 있어 다음 회차(09:2x)에 2차 실행이 자동으로
다시 돌아 이번엔 push·알림까지 성공(우연히 안 겹침).

**고치는 법(패치 준비됨, 적용은 아직 - "공유 자원 수정"이라 탐 권한 밖)**: 파일 락으로
두 레인이 겹치지 않게 한다. `pending_poller.py`의 `main()` 맨 앞에서 `.poller.lock`
파일을 확인해, 20분 안에 만들어진 락이 있으면 이번 회차는 조용히 건너뛰고, 없으면
락을 만들고 `finally`에서 지운다(코드는 같은 경로 `pending_poller.py`에 헬퍼 함수
`acquire_repo_lock`/`release_repo_lock`으로 이미 넣어뒀음, `main()`에서 호출하는
부분만 남음). 사장님이 직접 적용하거나 헤르메스에게 "이 파일을 이렇게 고쳐라"고
위임하면 된다.

**부수 발견 - "완료"가 진짜 완료가 아닐 수 있음**: `process_one()`이 `hermes chat`의
실제 응답 텍스트를 어디에도 저장하지 않는다(로그 길이만 기록). 그래서 `tasks/done/`
파일도, 우편 알림 본문("tasks/done/... 확인")도 실제 결과를 담지 않는다 - 폴러가
"완료"로 기록해도 **실제 작업이 성공했는지는 agent.log를 직접 봐야 안다**(구PC 설치
지시서는 두 번 다 poller 기준 "완료"였지만 실제로는 `curl|bash`가 무인 모드 안전
차단에 걸려 아무것도 설치되지 않았다, SSH로 직접 확인함). 지시서에 결과를 본문에
직접 쓰게 하거나(`echo`로 파일에 append) 별도 보고 파일 경로를 지정하는 방식으로
보완이 필요하다.

## 폴링 대체안 (판단 진행 중, 확정 아님)

클로드 쪽 25분 폴링은 SSH 직결로 대체하는 대신, 헤르메스가
`tasks/done/` 커밋 후 solar-bible PR에 댓글을 남기고, 그 PR을
`subscribe_pr_activity`로 구독한 세션이 몇 초 안에 깨어나는 방식도 검토
중이다(진행상황.md 3차 절 참고). 이건 SSH 직결과 별개로, 클라우드
세션처럼 SSH를 못 쓰는 경우에도 적용 가능한 대안이라 우선순위 작업으로
남겨둔다.
