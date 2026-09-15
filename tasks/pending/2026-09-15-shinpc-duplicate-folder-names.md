## 발주: 탐 → 신솔라

status: QUEUED

받는 이: 신솔라 (2차 발주 `2026-09-15-shinpc-cleanup-execute-plan.md`를 끝낸 뒤 처리)

## 배경

사장님 지시(2026-09-15): "똑같은 폴더명이 중복으로 있는 것도 조사". 지금까지
발견된 것만 해도 ComfyUI 3곳(`C:\Users\PC\ComfyUI`, `Documents\ComfyUI`,
`Temp\...\ComfyUI-LTXVideo`), shorts-lab 2곳, simplifier-saegim 2곳, 그리고
`Documents`(C:)와 `G:\다른 컴퓨터\내 노트북\문서`처럼 이름만 같은 폴더가 다른
드라이브에 나란히 있다. 사장님이 탐색기에서 같은 이름을 보고 다른 곳을 여는
것이 "작업 경로가 꼬이는" 직접 원인이다. 정리 실행 전에 전수 목록이 필요하다.

## 작업

읽기 전용. 이동·삭제 없음.

1. **범위**: `C:\Users\PC`, `C:\work`, `C:\c`, `D:\`, `G:\내 드라이브`,
   `G:\다른 컴퓨터`. 깊이는 각 루트에서 4단계까지(그 아래는 노이즈).
   제외: `.git`, `node_modules`, `__pycache__`, `venv`, `.venv`, `site-packages`,
   `$RECYCLE.BIN`, `System Volume Information`, `AppData\Local\Microsoft`,
   `AppData\Local\Packages`.
2. **집계**: 폴더의 마지막 이름(leaf)이 같은 것끼리 묶어 2개 이상인 것만.
   대소문자 무시. 한글·영어가 뜻만 같은 경우(`문서`↔`Documents`, `동영상`↔`Videos`,
   `바탕 화면`↔`Desktop`)도 같은 묶음으로 취급하되 "이름 다름" 표시.
   PowerShell 예:
   `Get-ChildItem -Path <루트> -Directory -Recurse -Depth 4 -EA SilentlyContinue | Group-Object { $_.Name.ToLower() } | Where Count -ge 2`
3. **표**: `이름 | 개수 | 경로 | 크기(GB, 1분 타임아웃, 넘으면 미측정) | 최근
   수정일 | git 저장소 여부 | 판정 후보`. 판정 후보는 넷 중 하나:
   - `같은 것의 사본` (내용이 거의 같음. 파일 수·최신 수정일로 판단)
   - `이름만 같은 다른 것` (내용이 다름. 이름을 바꿔 구분할 후보)
   - `백업 미러` (G:\다른 컴퓨터처럼 드라이브가 자동으로 만든 것)
   - `모름`
4. **우선 묶음**: shorts-lab, ComfyUI, simplifier-saegim, hansunghee7.github.io,
   solar-bible, hermes, 문서/Documents, 동영상/Videos, 다운로드/Downloads,
   OneDrive 흔적(`_OneDrive잔여` 포함). 이 묶음은 표 맨 위에 두고 경로별로
   "어느 것이 살아 있는가"(최근 30일 파일 수정 있음 / 실행 중 프로세스의 경로 /
   탐색기 고정 항목이 가리키는 곳)를 같이 적는다.
5. 표 아래에 한 줄: "이름 충돌로 사장님이 잘못 열 가능성이 큰 상위 5개"와
   각각의 해소 제안(사본 격리 / 이름 변경 / 고정 항목에서 제거). 제안만, 실행 없음.

하지 말 것: 이동·삭제·이름 변경·설정 변경. 비밀값 출력 금지. IP·MAC 기재 금지.

## 완료 기준

이 파일을 `tasks/done/2026-09-15-shinpc-duplicate-folder-names.md`로 옮기고
"조사 결과"에 표와 상위 5개를 적은 뒤 commit·push. 루트마다 중간 저장(§3).

---
## 조사 결과

(신솔라가 채운다)
