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

## 조사 결과 (신솔라 재조사, 2026-09-15)

1. 프로세스 확인:
- `tasklist | findstr /i "GoogleDriveFS"` 실행 → GoogleDriveFS.exe PID 43812, 33140 두 개 확인됨
- `tasklist | findstr /i "google"`(전체 google 프로세스)도 동일 프로세스들 확인됨

   실제 프로세스 출력:
   IMAGE NAME    PID
   GoogleDriveFS.exe    43812
   GoogleDriveFS.exe    33140

2. 설치 경로 확인:
- `C:\Program Files\Google\Drive File Stream\` 존재 (실행 파일 다수, 엔진 버전 130.0.2.0 등)
- `%LOCALAPPDATA%\Google\DriveFS\` 존재 (103303067954153637359 폴더, logs, db 등)
- `%APPDATA%\Google\Drive\` 없음

3. 설치 프로그램 목록(레지스트리):
- HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\{6BBAE539-2232-434A-A4E5-9A33560C6283}\DisplayName = "Google Drive" 존재함을 reg query로 확인
- WOW6432Node 쪽은 없음 (32비트 설치 아님, 64비트 기준)

4. 동기화 대상 폴더:
- G:\ 드라이브 존재, 라벨 "Google Drive"
- G:\ 아래: 바탕 화면(한국어 로컬라이즈명), 문서, 네트워크 등 디렉터리 구조 + 실제 파일 다수
- G:\ 바탕 화면 등에 git repo(brunch_scraper 등), 영상, 이미지, PDF, 구글 문서 파일(gdoc/gss/gslides) 등이 동기화되어 있음

5. Hermes 폴더 겹침:
- Hermes 루트 = C:\Users\PC\AppData\Local\hermes 존재 (ls 확인: config.yaml, SOUL.md, gateway.pid, state.db 등)
- G:\ 재귀 검색 결과 "hermes", ".env", "AppData", "Users/PC" 폴더명은 G:\에 없음 → 겹치지 않음
- 단 G:\ 내부에 캐시 클립 폴더 등이 C_\Users\layte 경로명으로 저장돼 있으나 이건 구글 클립 캐시 내부 표기로 실제 윈도우 폴더 겹침이 아님

6. 구체적 증상:
- G:\에서 "X의 사본" 접미사 파일 다수 발견:
   - "The_LinkedIn_Swipe_File_by_Justin_Welsh의 사본.gdoc"
   - "The_LinkedIn_Operating_System_Resources_1_.xlsx의 사본.xlsx"
   - "MARU ...의 사본.gslides"
   - "PO Academy의 사본.gdoc"
   - "??MomentumHR    Thinksflow Dashboard의 사본.gsheet"
   - 기타 다수
- ".docx.docx" 이중 확장 파일도 하나 있음
- "(1)", "(2)", "(3)" 등 숫자 괄호 패턴 파일 다수 존재. 일부는 구글 문서 충돌 사본으로 보이고 일부는 원본의 날짜/버전 표기(UX패턴(0615) 등)
- 구글 문서(gdoc/gss/gslides) 파일이 G:\에 다수 존재함 → 구글 드라이브 for desktop이 구글 워크스페이스 문서를 로컬에 프리뷰/충돌 관리용으로 생성

7. 원인 추정:
신PC에서 구글 드라이브 for desktop이 실제로 설치·실행·동기화 중(G:\ 가상 드라이브, GoogleDriveFS.exe 프로세스 2개, HKLM 레지스트리 등록 모두 존재)이고, 구글 문서(Sheets/Slides/Documents 등)를 구글 드라이브에 올리거나 편집하는 과정에서 서버 측 충돌 사본 및 로컬 "(N)" 접미사 파일이 G:\ 동기화 폴더에 쌓이고 있음. Hermes 폴더(C:\Users\PC\AppData\Local\hermes)와는 겹치는 경로가 없으므로 이 현상은 Hermes 작업과 무관.

== 추가 확인 사항 (2026-09-15 신솔라 재조사 보완) ==
- G: 드라이브 루트에는 google 관련 폴더가 "내 드라이브/Google Meet" 하나뿐이며, drive 폴더로는 캐시 클립 OneDrive 경로(C_\Users\layte)만 존재. G: 아래에 직접적인 google-drive 또는 drive-file-stream 폴더는 없음(동기화가 G: 가상 드라이브로 통합돼 있기 때문).
- G: 아래 hermes, AppData, Users/PC 경로 없음 → Hermes 작업 폴더(C:\Users\PC\AppData\Local\hermes 등)와 G: 드라이브의 겹침은 없음.
- G:\의 파일 중 일부 파일은 C:\Users\layte 경로를 내부 표기로 갖고 있으나, 이는 구글 클립 캐시 내부 구조일 뿐 실제 윈도우 사용자 폴더(C:\Users\PC)와 겹치는 경로가 아님.
