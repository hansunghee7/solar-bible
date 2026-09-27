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

**고친 상태(2026-09-27 적용·검증 완료)**: 파일 락으로 두 레인이 겹치지 않게 했다.
`pending_poller.py`의 `main()` 맨 앞에서 `.poller.lock` 파일을 확인해, 20분 안에
만들어진 락이 있으면 이번 회차는 조용히 건너뛰고(다른 레인이 쓰는 중), 없으면 락을
만들고 `finally`에서 지운다(`acquire_repo_lock`/`release_repo_lock`). 사장님 승인 뒤
탐이 직접 적용, 격리된 테스트 저장소로 정상 동작(락 생성·해제, 빈 pending 정상 종료)
확인. 같은 김에 `git add -A`가 이 체크아웃에 남아있던 다른 세션의 무관한 편집까지
같이 커밋해버리던 문제도 고쳤다(처리한 파일 두 경로만 정확히 `git add`).

**부수 발견 - "완료"가 진짜 완료가 아니었던 문제, 해결됨(2026-09-27, 사장님 지시)**:
`process_one()`이 `hermes chat`의 실제 응답 텍스트를 어디에도 저장하지 않았다(로그
길이만 기록). 그래서 `tasks/done/` 파일도, 우편 알림 본문도 실제 결과를 안 담아
**폴러가 "완료"로 기록해도 실제 작업이 성공했는지는 agent.log를 직접 봐야 알 수
있었다**(구PC 설치 지시서는 두 번 다 poller 기준 "완료"였지만 실제로는 `curl|bash`가
무인 모드 안전 차단에 걸려 아무것도 설치되지 않았음, SSH로 직접 확인해서야 발견).

**적용한 설계**: 사장님 지시대로 **의뢰와 결과를 한 파일에 안 섞고 분리**한다.
- `tasks/done/<이름>.md` - 그대로 "무엇을 의뢰했는지"만(원본 지시서, 변경 없음).
- `reports/<이름>-result.md`(새로 신설) - `## 의뢰(원본)` + `## 결과`(hermes chat 응답
  원문 그대로, 지시서가 "문제점·STATUS를 적어달라"고 요청했으면 그 내용이 여기 그대로
  들어온다) + `## 메타`(처리 시각, exit code). 이 파일도 done 커밋에 같이 넣어 push된다.
- 우편 알림 본문도 "실제 결과·문제점은 `reports/<이름>-result.md`에 있음"으로 갱신.
- 격리된 테스트 저장소(가짜 hermes/mailbox 명령)로 전체 흐름(의뢰 → 처리 → done 이동 →
  report 생성 → 커밋에 두 파일만 정확히 포함 → 알림) 1회 실측, 정상 동작 확인.

**헤르메스 쪽 관점도 매번 받는다(2026-09-27, 사장님 지시)**: `process_one()`이 실제
모델에 넘기는 프롬프트에 지시서 원문 뒤로 고정 문구(`FEEDBACK_SUFFIX`)를 덧붙인다 -
"이 지시서 형식(산문/스크립트, 단계 수 등)이 실행하기 쉬웠는지 어려웠는지, 어려웠으면
정확히 어느 부분이 그랬는지(모호한 지시, 막힌 도구 호출, 무인 모드 승인 필요 등)를
`## 실행 피드백` 아래 2~5줄로 적어달라"는 요청. `tasks/done/` 원본 지시서에는 이 문구가
안 남고(원본 그대로), `reports/<이름>-result.md`의 `## 결과`에는 모델의 실제 답변과
함께 이 피드백 절이 자연히 포함된다. 격리 테스트로 프롬프트에 문구가 실제로 실려가는 것
확인(`MARKER_FOUND=True`). **목적**: 의뢰 형식 자체가 헤르메스에게 실행하기 어려웠던
사례(예: 오늘의 산문형 vs 스크립트형 차이, curl\|bash 무인 승인 벽)를 매 건마다 모아,
나중에 `reports/*-result.md`를 훑어보면 "헤르메스가 어떤 식의 의뢰를 못 견디는지"
패턴을 축적할 수 있게 한다.

## 문서 4종 분리: 수신 확인 + 클로드 쪽 완료 판정 추가 (2026-09-27, 사장님 지시)

**배경**: 위 절의 "완료가 진짜 완료가 아니었던 문제"를 고치면서도, 더 근본적인
사고 유형 하나가 남아 있었다 - **의뢰 자체가 헤르메스에게 안 닿는 경우**(N42:
`mailbox.py send 헤르메스`로 보낸 의뢰가 헤르메스가 안 보는 채널이라 조용히
사라짐, 발주자는 "완료 알림이 안 온다"로만 알아채 원인 파악에 오래 걸림). 완료
문서 하나만으로는 "완료가 안 옴 = 실패했나? 안 받았나? 아직 처리 중인가?"를
구분할 수 없다. 사장님 지시: **의뢰·수신·완료를 양쪽이 각자 독립적으로 기록**해
서로 대조 가능하게 한다.

**적용한 4종 문서**:
1. `tasks/pending(-long)/<이름>.md` - 클로드의 업무의뢰 문서(원본, 그대로 `tasks/done/`으로 이동)
2. `tasks/received/<이름>.md`(신설) - **헤르메스의 업무수신 문서**. `process_one()`(최대
   20분 걸리는 `hermes chat` 호출) 실행 **전에** 즉시 작성해 별도 커밋(`received: <이름>`)으로
   push한다. 다음 폴링 주기(최대 15분) 안에 이 파일이 안 생기면 발주자는 완료를 기다리지
   않고도 "의뢰가 채널에 아예 안 닿았다"를 바로 알 수 있다. 의뢰 원문을 받은 그대로 담아,
   전송 중 내용이 깨지거나 잘렸는지도 나중에 대조 가능.
3. `reports/<이름>-result.md`(기존) - 헤르메스의 업무완료 문서(의뢰 원본+실제 응답+실행 피드백).
4. `reports/<이름>-tam-verdict.md`(신설, 클로드 쪽) - 탐이 3번을 읽고 직접 검증(JUDGE)한 뒤
   같은 저장소에 남긴다: `## 의뢰(내가 보낸 것)` + `## 완료 확인(직접 검증한 근거,
   DONE=VERIFIED)` + `## 문제점/개선사항(내 관점)`. 3·4번을 나란히 두면 "같은 일"을 양쪽이
   다르게 기억하는 지점(의뢰 유실·해석 차이·검증 누락)이 바로 드러난다. 이건 파일 규칙일
   뿐 스크립트가 강제하지 않는다 - `hermes-delegate` 스킬에 클로드 쪽 절차로 문서화.

**구현**: `pending_poller.py`에 `write_receipt()`/`commit_receipt()` 추가, `main()` 루프에서
`process_one()` 호출 전에 실행. 콘솔 코드페이지가 cp949일 때 로그의 치환 문자(U+FFFD)로
마지막 print가 `UnicodeEncodeError`로 죽던 것도 같이 발견해 고침(`sys.stdout/stderr.reconfigure`).

**검증(DONE=VERIFIED)**:
- 격리 테스트 저장소(가짜 hermes 명령) 3종 시나리오: 성공 시 `received`→`done` 순서로
  분리 커밋+둘 다 push 확인, 실패 시(`exit 2`)에도 `received` 커밋은 살아남고 `done`은
  안 생기는 것 확인, cp949 인코딩 버그 재현 후 수정 확인(수정 전 exit 1 크래시 → 수정 후 exit 0).
- **실제 운영 환경 1회 실행**: `tasks/pending-long/20260927-receipt-feature-smoke-test.md`
  발주 → `hermes cron run 938439795638`(solar-bible-long-poller) 실행 →
  `received:`/`done:`/`mail:` 커밋 3개 순서대로 origin/main에 push 확인, `reports/…-result.md`
  응답 내용 확인, 클로드 쪽 `reports/…-tam-verdict.md` 작성까지 완주.

## 폴링 대체안 (판단 진행 중, 확정 아님)

클로드 쪽 25분 폴링은 SSH 직결로 대체하는 대신, 헤르메스가
`tasks/done/` 커밋 후 solar-bible PR에 댓글을 남기고, 그 PR을
`subscribe_pr_activity`로 구독한 세션이 몇 초 안에 깨어나는 방식도 검토
중이다(진행상황.md 3차 절 참고). 이건 SSH 직결과 별개로, 클라우드
세션처럼 SSH를 못 쓰는 경우에도 적용 가능한 대안이라 우선순위 작업으로
남겨둔다.
