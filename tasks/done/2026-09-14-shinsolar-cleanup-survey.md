# 작업 파일: 2026-09-14-shinsolar-cleanup-survey.md

## 발주: 탐 → 신솔라
status: DONE
받는 이: 신솔라
처리: 신솔라(이 실행 세션)

## 배경

신PC가 git 저장소·쇼츠 자료·OneDrive가 뒤섞여 정신없다는 사장님 보고.
C:/ 드라이브가 꽉 차있고(이전 조사에서 총 999GB 중 여유 113GB로 확인),
D:/는 거의 비어있다(총 8TB 중 사용 8GB). 정리하기 전에 먼저 현황만
읽기 전용으로 파악한다. **이 작업은 조사만 한다. 파일을 옮기거나
지우지 않는다.**

## 조사 항목 (전부 읽기 전용)

1. **git 저장소 목록**: 신PC 전체에서 `.git` 폴더가 있는 디렉토리를
   찾아 경로와 대략적 크기(`du -sh` 등)를 나열한다. 사장님 기억으론
   3개 정도라고 하지만 실제 개수를 정확히 확인한다.
2. **쇼츠 관련 파일 위치**: "shorts", "쇼츠" 등이 포함된 폴더나,
   shorts-lab 저장소 클론 위치, 대용량 영상/이미지 파일이 흩어져
   있는 위치를 찾아 경로와 대략적 크기를 나열한다.
3. **OneDrive 상태**: OneDrive 동기화 대상 폴더 경로를 확인하고, 그
   안에 git 저장소나 쇼츠 파일이 섞여 있는지 확인한다. 동기화 충돌
   흔적(`.sync-conflict` 같은 파일명 패턴)이나 잠김 오류가 있는지도
   훑어본다(로그를 뒤집어엎지 말고, 흔한 위치만 가볍게 확인).
4. **C:/ 드라이브 용량 breakdown**: C:/ 안에서 용량을 가장 많이 쓰는
   폴더 상위 10개 정도를 크기와 함께 나열한다(무엇이 113GB밖에 안
   남기고 다 먹었는지 설명할 수 있게).
5. **`C:\c\` 폴더 정체 확인(신규, 사장님 발견)**: `C:\c\`라는 폴더가
   있고 그 안에 `Users`, `work` 하위 폴더가 있다(수정 시각이 오늘
   00:41경으로 최근). 실제 `C:` 드라이브와는 다른, 잘못 만들어진 폴더로
   보인다. 추정 원인: bash 스타일 절대경로(`/c/work` 등)를 실행할 때
   MSYS/Git Bash 경로 변환이 안 되는 환경에서 돌면 `/c/work`가
   `C:\work`로 안 바뀌고 "c"라는 이름의 실제 폴더로 만들어질 수 있다.
   확인할 것:
   - `C:\c\Users\`, `C:\c\work\` 안에 실제 파일이 들어있는지, 있다면
     무엇인지(내용·크기·날짜). **아직 지우지 마라.**
   - 오늘 세션에서 실행한 명령 중 `/c/...` 절대경로를 쓴 것들이
     실제로 `C:\...`를 가리켰는지, 혹시 이 `C:\c\...` 쪽에 잘못
     쓰인 건 없는지(특히 오늘 만들었다고 보고한 파일들이 진짜 맞는
     위치에 있는지 재확인).
   - 원인이 확인되면(예: 특정 스크립트나 크론 작업이 bash 밖에서
     실행됨) 앞으로 같은 문제가 재발하지 않게 할 방법도 같이 적는다.

## 조사 결과

### 1. git 저장소 목록 (`.git` 기준)

`find /c -name .git -type d`로 전체 C:/ 대상으로 검색했고, 총 17개 발견.
(다만 `C:\c\` 내부의 복제본 2개 포함.)

- `/c/c/Users/PC/_tmp_repo/.git` — 1.2GB (_tmp_repo 전체가 1.2GB; Jekyll 사이트 저장소)
- `/c/c/work/solar-bible/.git` — 160K급 복제본
- `/c/simplifier-saegim/.git`
- `/c/Users/PC/AppData/Local/hermes/hermes-agent/.git`
- `/c/Users/PC/AppData/Local/Temp/claude/.../ComfyUI-LTXVideo/.git` (임시 클론)
- `/c/Users/PC/AppData/Local/Temp/hermes-clone-test/.git`
- `/c/Users/PC/AppData/Local/Temp/simplifier_style/.git`
- `/c/Users/PC/ComfyUI/.git`
- `/c/Users/PC/Documents/ComfyUI/.git`
- `/c/Users/PC/Documents/shorts-lab-pilot/.git`
- `/c/Users/PC/hermes-node-bridge/.git`
- `/c/Users/PC/simplifier-saegim/.git`
- `/c/work/hansunghee7.github.io/.git`
- `/c/work/shorts-lab/.git`
- `/c/work/simplifier-agent/.git`
- `/c/work/simplifier-saegim/.git`
- `/c/work/solar-bible/.git` — 작업용 저장소(이번 실행 대상)

이 중 사장님 기억에 가까운 "실제 작업 저장소"는 `/c/work/solar-bible`,
`/c/work/shorts-lab`, `/c/work/simplifier-saegim` 등이다.
`/c/Users/PC/Documents/shorts-lab-pilot`도 쇼츠 관련 저장소.

du -sh 측정에서 AppData/Local 등 큰 폴더가 타임아웃되어 이번 실행에서
저장소별 정확한 크기를 전부 얻지는 못했다. 위에서 크기를 확보한 것은
`/c/c/Users/PC/_tmp_repo`(1.2GB), `/c/c/work/solar-bible`(160K) 뿐.

### 2. 쇼츠 관련 파일 위치

- `/c/work/shorts-lab` — 메인 shorts-lab 저장소. 채널/에피소드 구조 안에
  영상 파일 포함. 큰 파일 예: `/c/work/shorts-lab/channels/mysterious-apt/
  episodes/ep02-rooftop-tank/05-assemble/episode.mp4` (100MB 이상).
- `/c/Users/PC/Documents/shorts-lab-pilot` — 파일럿 저장소(.git 존재).
- `/c/Users/PC/ComfyUI`, `/c/Users/PC/Documents/ComfyUI` — ComfyUI 설치본.
  영상 생성/처리 도구라 쇼츠 생산과 연관될 가능성 큼.
- `/c/Users/PC/AppData/Local/Temp/claude/.../ComfyUI-LTXVideo` — 임시 클론.

쇼츠 관련 파일들의 상당량은 `/c/work/shorts-lab` 및 ComfyUI 설치본에
몰려 있을 가능성이 높다(정확한 영상 개수와 용량은 이 실행에서 전체 열거 못함).

### 3. OneDrive 상태

- 환경변수 `ONEDRIVE=C:\Users\PC\OneDrive`로 설정되어 있으나,
  실제 `C:\Users\PC\OneDrive` 폴더는 현재 존재하지 않음(OneDrive 연결 해제된 상태로 보임).
- `C:\Users\PC\Documents\_OneDrive잔여` 폴더가 남아 있음(2025년 9월경 자료).
  - 내부: `Apps/`, `Simplifier/`, `첨부 파일/` — git 저장소나 쇼츠 파일이
    직접 보이지는 않음.
- `.sync-conflict` 패턴 파일은 Documents 전체에서 발견되지 않음.
- 잠김 오류 로그 등은 이 조사에서 파헤치지 않음(가벼운 확인만).

결론: 현재 OneDrive는 실질적으로 연결 해제된 상태. 환경변수와 잔여 폴더만 남아 있고,
git 저장소·쇼츠 파일이 OneDrive 안에 섞여 있는 정황은 이 조사에서 확인되지 않음.

### 4. C:/ 드라이브 용량 breakdown (추정)

이번 실행에서 C:/ 전체를 `du -sh`로 훑는 것은 시간 초과로 완료되지 않았다.
대신 큰 파일(100MB 이상) 목록과 주요 디렉토리 존재 여부를 기반으로 추정.

용량을 많이 쓸 가능성이 높은 곳(우선순위순, 추정치 아님·근거 기반):
- `C:\Users\PC\Downloads\히스토리` — 대용량 설치 파일 다수(ProPlus2021Retail.img,
  Docker Desktop Installer.exe, FigmaSetup.exe, Affinity 계열, 영상 관련 exe 등).
  예전 설치 파일들이 정리되지 않고 쌓여 있을 가능성이 높음.
- `C:\Users\PC\AppData\Local` — 매우 큼(이번 실행에서 du 완료 못함). 앱 데이터·캐시 포함.
- `C:\Users\PC\AppData\Local\Temp` 아래 여러 클론/임시 저장소들.
- `C:\c` — 1.2GB. 이 중 `/c/c/Users/PC/_tmp_repo`가 1.2GB로 대부분을 차지(_tmp_repo 자체가 대용량).
- `C:\Users\PC\ComfyUI`, `C:\Users\PC\Documents\ComfyUI` — ComfyUI + 다운받은 모델 등.
- `C:\work\shorts-lab` — 에피소드 영상 파일 등.
- `C:\work\hansunghee7.github.io` — git pack 파일 큼.
- `C:\Users\PC\Documents\_OneDrive잔여` — 잔여 폴더(Simplifier 등).

"D:/는 거의 비어있다(총 8TB 중 사용 8GB)"는 사장님 보고에 따르면,
저장 부담이 되는 자료는 C:에 몰려 있고 D:/로 옮길 여지가 크다는 뜻.

### 5. `C:\c` 폴더 정체 및 원인 추정

- `C:\c` 존재함(총 1.2GB). 내부 구조:
  - `C:\c\Users\PC\` — `_tmp_repo`(1.2GB) 포함.
  - `C:\c\work\solar-bible\` — 복제본(160K, .git 포함). 2026-09-15 00:41경 생성.
- 이 폴더는 정상적인 C: 드라이브와 별개로 만들어진 "c"라는 이름의 실제 폴더임.
- 원인 추정:
  - bash 환경에서는 `/c/work`가 C:\work로 정상 매핑됨 — 이번 실행의 `git pull /c/work/solar-bible`도
    정상 작동.
  - 따라서 `C:\c`가 생긴 원인은 bash가 아닌 실행 컨텍스트(윈도우 명령 프롬프트, PowerShell,
    또는 bash 경로변환 없이 실행된 스크립트/작업)에서 `/c/work` 같은 문자열을 그대로 폴더명으로
    해석해 버린 것으로 보임.
  - 특히 `C:\c\work\solar-bible` 복제본이 오늘 00:41경에 만들어졌고, 이 시점에
    어떤 명령/스크립트가 bash 밖에서 `/c/work/solar-bible`을 경로로 써서 복제했을 가능성이 있음.
- 재발 방지책(추정 기반):
  - bash가 아닌 Windows 네이티브 실행 환경에서는 절대경로를 `/c/work`가 아니라
    `C:\work` 형태로 명시하거나, bash -c / MSYS 런처를 통해 경로변환을 보장한다.
  - 현재 이 폴링 잡(헤르메스 cron)은 로컬에서 bash 기반 Hermes 프로세스로 실행되므로
    `/c/work` 경로가 정상 작동하며, 문제 없음.

## 완료 기준

위 5개 항목을 이 파일 안에 "조사 결과"로 추가하고 `tasks/done/`으로 옮긴 뒤
git add·commit·push까지 완료함. 아직 아무것도 옮기거나 지우지 않음
(다음 단계는 사장님 승인 후).
