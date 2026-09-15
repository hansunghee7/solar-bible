## 발주: 탐 → 신솔라

status: QUEUED

받는 이: 신솔라

## 배경

1차 발주(`tasks/done/2026-09-15-shinpc-folder-cleanup-plan.md`, C: 여유 예상 119GB)의 실측 위에
사장님이 2026-09-15 정리 규칙을 확정했다. 폴더별로 판단하지 않고 규칙
세 개로 간다.

1. **코드는 `C:\work\<저장소>` 하나씩만.** 같은 원격의 중복 클론은 정본 하나만
   남기고 나머지는 `D:\_정리대기\`로 격리(삭제 아님). 정본 판단 기준: `C:\work`
   아래 것이 정본. 단, 다른 클론에 push 안 된 커밋(`git log origin/HEAD..HEAD`)
   이나 미커밋 변경(`git status --porcelain`)이 있으면 "사장님 판단"으로 남긴다.
2. **C:에는 있어야 하는 것만.** OS, 프로그램, 매일 쓰는 모델(.ollama), 활성 코드.
   나머지는 전부 D:. 특히 shorts-lab 영상 산출물은 D:.
3. **구글 드라이브에는 설계·더빙 자료와 에피소드당 최종 mp4 1개만.** 씬 이미지·
   클립 같은 중간 산출물은 드라이브에 올리지 않는다(D:에만).

목표 구조:
```
C:\work\<저장소>                     코드 (git 클론, 저장소당 하나)
C:\Users\PC\.ollama                  매일 쓰는 로컬 모델 (그대로)
D:\work\shorts-lab\channels          쇼츠 에피소드 데이터 (C:\work\shorts-lab\channels 는 정션)
D:\models\comfyui                    ComfyUI 모델 (원래 위치는 정션 또는 extra_model_paths.yaml)
D:\Archive\<원래 상위폴더명>\         완성본·설치파일 히스토리·옛 결과물
D:\_정리대기\<원래 경로 그대로>\      격리 (사장님이 나중에 검토)
```

## 작업

이번 발주도 **실행 전 계획서까지**다. 다만 1차와 달리 표가 아니라 "실행할
명령 목록"을 낸다. 사장님이 목록에 O를 주면 다음 발주에서 그대로 실행한다.

1. **ComfyUI 정본 확정(최우선).** 1차에서 `C:\Users\PC\ComfyUI`가 142MB로 나왔다.
   모델이 없다는 뜻이다. ComfyUI Desktop 앱은 기본 설치 위치가 `Documents\ComfyUI`
   이고 모델을 그 안에 둔다. 확인할 것: ① `Documents\ComfyUI\models`, `output`,
   `input`, `custom_nodes` 각 크기(GB). ② ComfyUI Desktop 설치 여부(설치된 앱
   목록, `%APPDATA%\ComfyUI\extra_models_config.yaml` 또는 `config.json`의
   `basePath`). ③ `C:\Users\PC\ComfyUI`는 git 클론인지, 어느 쪽을 최근에
   실행했는지(`output` 최신 파일 날짜, 프로세스 실행 경로). 이걸로 "Documents 쪽이
   활성, C:\Users\PC 쪽이 옛 클론"인지 반대인지 확정한다. 확정 전엔 두 곳 다
   격리 후보에 넣지 않는다.
2. **중복 클론 판정표.** 1차 표의 같은 원격 클론 쌍(ComfyUI, shorts-lab,
   simplifier-saegim)과 Temp 아래 클론 3개(ComfyUI-LTXVideo, hermes-clone-test,
   simplifier_style)마다: 경로 / 마지막 커밋 날짜 / push 안 된 커밋 수
   (`git log @{u}..HEAD --oneline | wc -l`, 업스트림 없으면 "없음") / 미커밋 변경
   줄 수 / `.gitignore`된 대용량 폴더 크기(GB) / 판정(정본 · 격리 · 사장님 판단).
   1차 판정에 대한 탐 의견: shorts-lab은 `C:\work` 쪽이 정본(9/15 커밋, ep09 v14),
   `Documents\shorts-lab-pilot`은 미커밋 0이면 격리. simplifier-saegim은 둘 다
   미커밋 0이니 `C:\work` 쪽 정본, 나머지 격리. Temp 아래 3개는 미커밋·미push 없으면
   격리. 이 의견과 실측이 어긋나면 실측을 따른다.
3. **Documents·AppData 한 단계 펼치기.** 두 폴더의 직속 하위 폴더를 크기 순으로
   전부 나열하고(1GB 미만은 "기타 nGB"로 묶음) 각각 규칙 2로 C: 잔류 / D: 이동 /
   격리 중 하나를 붙인다. `CrossDevice`는 Windows "휴대폰과 연결" 캐시이므로
   격리 후보로 표시하고 그 기능이 켜져 있는지 설정값을 적는다.
4. **모델 폴더 경로 설정 조사.** ComfyUI(`extra_model_paths.yaml` 유무), LM Studio,
   Ollama 각각 모델 경로를 바꾸는 공식 설정 방법을 실제 설정 파일·환경변수 기준으로
   적는다(추측 금지). 1차 표 4·5번의 "모델을 D:\Archive로 이동" 제안은 채택하지
   않는다: 파일만 옮기면 프로그램이 못 찾고, 4090이 매일 쓰는 Ollama 모델은 HDD로
   가면 로딩이 느려진다. `.ollama`는 C: 잔류 확정(조사만). LM Studio는 최근 사용
   일자(실행 파일·로그 mtime)를 보고 "안 쓰면 D:\models\lmstudio + 설정 변경" 제안.
   ComfyUI 모델은 1번 결과에 따라 `D:\models\comfyui` + `extra_model_paths.yaml`
   등록으로 제안.
5. **탐색기 왼쪽 정리 조사(읽기 전용).**
   - 빠른 액세스 고정 항목 전부와 실제 경로:
     `(New-Object -ComObject shell.application).Namespace('shell:::{679f85cb-0220-4080-b29b-5540cc05aab6}').Items() | Select Name, Path`
   - 알려진 폴더 실제 경로(문서·바탕화면·사진·다운로드·동영상):
     `Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'`
     OneDrive 경로가 남아 있으면 기본 경로(`%USERPROFILE%\<폴더>`)로 복구 제안.
   - 사장님 확정 고정 목록(정리 후 이걸로 교체, 기존 전부 제거):
     `C:\work`, `D:\work\shorts-lab\channels`, `D:\Archive`, `D:\_정리대기`,
     G: 설계·더빙 동기화 폴더, 다운로드.
6. **구글 드라이브 동기화 실측.** Drive for desktop이 지금 로컬의 어느 폴더를
   "내 컴퓨터" 동기화(미러)하고 있는지, G:가 스트리밍인지 미러인지, shorts-lab
   미디어가 드라이브로 올라가는 경로가 있는지 확인. 규칙 3에 맞게 "동기화 유지 /
   해제" 제안.
7. **실행 명령 목록 작성.** 위 1~6과 1차 표의 안전 항목(Downloads\히스토리, Videos,
   CrossDevice 격리, Temp 클론 3개 격리)을 합쳐 실제 실행할 순서대로 번호를 붙인
   목록. 항목마다: 명령(예: `robocopy /MOVE`, `mklink /J`) / 대상 크기 / 되돌리는
   방법 / 사장님 O·X 칸. 원칙: 이동은 `robocopy /E /MOVE /LOG`, 정션은 이동 완료
   확인 후 생성, 삭제 명령은 목록에 넣지 않는다.

하지 말 것: 파일 이동·삭제·정션 생성·설정 변경·레지스트리 변경 일체(이번엔
조사와 목록만). 비밀값 출력 금지. 공개 저장소이므로 IP·MAC 기재 금지.

## 완료 기준

이 파일을 `tasks/done/`으로 옮기고 "조사 결과" 절에 1~7을 적은 뒤 commit·push.
7번 목록이 있어야 완료다. 단계마다 중간 저장(솔라바이블 §3).

---
## 조사 결과

(신솔라가 채운다)
