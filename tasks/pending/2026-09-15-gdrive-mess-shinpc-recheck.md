## 발주: 탐 → 신솔라 (재조사 — 지난 조사가 "미설치"로 잘못 판정함)

status: QUEUED

받는 이: 신솔라

## 배경

`tasks/done/2026-09-15-gdrive-hermes-file-mess-survey-retry.md`에서
"구글 드라이브 동기화 프로그램이 이 PC(신PC)에 미설치"라고 판정했으나,
**사장님이 방금 신PC 화면에서 구글 드라이브 앱이 실제로 열려 "동기화
중..." 상태인 걸 직접 확인했다(스크린샷 있음).** 지난 조사 방법이
뭔가를 놓쳤다. 이번엔 더 확실한 방법으로 다시 확인한다. **이 작업은
조사만 한다. 파일을 옮기거나 지우지 않는다.**

## 조사 항목 (전부 읽기 전용, 이번엔 아래 방법을 반드시 다 써라)

1. **프로세스로 확인**: `tasklist | findstr /i "GoogleDriveFS"` (구글
   드라이브 for desktop의 실제 프로세스명). 없으면 `tasklist`
   전체에서 "google"이 포함된 프로세스를 전부 찾아라(`findstr /i
   google`).
2. **설치 경로로 확인**: 아래 경로들이 실제로 있는지 하나씩 확인해라
   (지난 조사가 어떤 경로를 봤는지 안 적혀 있어서, 이번엔 전부 직접
   존재 여부를 찍어라):
   - `C:\Program Files\Google\Drive File Stream\`
   - `%LOCALAPPDATA%\Google\DriveFS\`
   - `%APPDATA%\Google\Drive`
3. **설치 프로그램 목록으로 확인**: PowerShell
   `Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Where-Object {$_.DisplayName -like "*Google Drive*"}`
   (32/64비트 레지스트리 둘 다, 필요하면 Wow6432Node 경로도).
4. **동기화 대상 폴더 실제 확인**: 위에서 설치가 확인되면, 그 동기화
   대상 폴더(보통 `G:` 드라이브 가상 드라이브이거나
   `~/Google Drive`) 경로를 찾아 실제로 어떤 폴더가 동기화되고 있는지
   나열한다.
5. **Hermes 폴더와 겹침 확인**: 4번에서 찾은 동기화 폴더와 Hermes
   작업 폴더(`~/.hermes`, `%LOCALAPPDATA%\hermes`, 저장소 클론 위치
   등)가 겹치는 곳이 있는지 확인한다.
6. **구체적 증상 확인**: 동기화 충돌 파일명 패턴("(1)", "충돌 사본"
   등), 같은 파일이 여러 위치에 중복돼 있는지 확인한다.
7. **원인 추정**: 확인된 사실만으로 가장 그럴듯한 설명을 적는다.

## 완료 기준

1~7번을 전부 실행하고 실제 출력(존재/부재, 프로세스 있음/없음 등)을
이 파일에 그대로 적은 뒤에만 `tasks/done/
2026-09-15-gdrive-mess-shinpc-recheck.md`로 옮기고 git add·commit·
push한다. **"미설치로 보인다"처럼 근거 없이 단정하지 마라** — 1~3번
중 최소 하나로 실제 존재를 확인하거나, 셋 다 확실히 없다는 걸
보여준 뒤에만 결론을 낸다.
