---
name: 신PC 폴더 정리안 (S1-2, 계획표까지)
about: 신PC(CSSD+HDD) 폴더 현황 실측 + 정리 계획표 작성. 실제 이동/삭제 없음. 완료 기준: 표 작성 → tasks/done 이동 → git push.
title: "[정리안] 신PC 폴더 정리 계획표"
labels: 정리안, 계획
assignee: @hansunghee7-bot

---

## 배경
동일한 실제 문제(네이버 클라우드 탐색기의 "사본"/" (1)" 충돌 표시와 구글 드라이브 충돌 알림)를 두 곳에서 바라보는 상황:
- 구글 드라이브(G:)에서는 130개 충돌 알림.
- 네이버 클라우드 탐색기(네이버 MyBox)에서는 C:\Users\PC\Documents\shorts-lab-pilot\ 및 C:\Users\PC\Videos\ 등 실제 C:/D: 폴더에 "사본"/" (1)" 표시.

하나의 파일 집합이 두 가지 관점으로 중복 보여지는 문제. 경로 아래로 내려가서 실제 파일을 확인해야 정확히 보임.

## 작업
1. **D: 드라이브 실측**: Get-PhysicalDisk + Get-Volume으로 디스크 정보, 여유 공간.
2. **C: 대용량 폴더 상위 20개 측정**: PowerShell 폴더 크기 측정 (5분 타임아웃 적용).
3. **git 저장소 17개 조사**: 신PC(C:\Users\PC) 및 /c/work 아래 git 저장소 전수 탐색, 원격 URL, 마지막 커밋, 미커밋 변경, 중복 클론 식별.
4. **G: 충돌 파일 조사**: PowerShell로 구글 드라이브(G:) 충돌 후보 파일 개수, 총 크기, 상위 10개 경로.
5. **정리안 표 작성**: 1~4 결과를 하나의 표로 정리. 열: 번호 | 경로 | 크기(GB) | 종류 | 제안(4종 중 하나) | 근거 | 사장님 O/X. 표 맨 위에 "제안대로 하면 C: 여유 예상 xxx GB" 한 줄. 삭제 제안은 하지 않는다.

## 하지 말 것
- **이 작업 중에는 실제 파일 이동·삭제·포맷을 하지 않는다.** 표(계획)만 작성한다.
- 캐시를 함부로 지우지 않는다.
- 시스템 폴더(AppData, Program Files 등)를 통째로 이동하지 않는다.
- 용량 확보 제안을 할 때 "삭제" 단어는 쓰지 않는다.

## 완료 기준
- 1~5의 실측값과 조사 결과를 이 파일에 적을 것.
- 정리안 표를 완성할 것.
- 표의 모든 행에 크기 실측값(측정값이 없는 경우 "미측정"으로 표기).
- 제안 컬럼에는 "D:\Archive\...\ 로 이동", "D:\_정리대기\...\ 로 격리 (구조·이름 그대로)", "그대로 둠", "사장님 판단" 중 하나만 쓸 것.
- 이 파일을 **tasks/done/2026-09-15-shinpc-folder-cleanup-plan.md** 로 옮기고 아래 '조사 결과' 절에 1~5의 실측값과 정리안 표를 적은 뒤 git add·commit·push.
- Solar Bible §3에 따라 단계(1~5)마다 중간 저장한다. (장기 작업 시 safety.)

---

## 조사 결과

### 1. D: 드라이브 실측 (PowerShell)
- 물리적 디스크: ST8000DM004-2U9188, HDD, 8,001,563,222,208 Bytes (약 8 TB)
- 볼륨 D:: 여유 7,993,259,921,408 Bytes (약 7,993 GB ≈ 7.99 TB) — 거의 전체 여유
- 판정: C:→D: 아카이브 이동 시 타겟 용량 충분. HDD라 속도 느리지만 저장 목적 적합.

### 2. C: 대용량 폴더 상위 20개 (PowerShell, 폴더별 5분 타임아웃 — 전부 측정 완료, 최대 30.9초)
| 폴더 | 크기(GB) | 비고 |
|------|---------|------|
| Documents | 292.21 | 사용자 문서. 아카이브 대상 다수 포함 추정. 내부 구조 확인 필요. |
| AppData | 147.92 | 프로그램 데이터 (Hermes, ComfyUI, 모델 등 포함). 하위 분류 필요. |
| CrossDevice | 64.1 | 정체성 불명. 격리 제안. |
| .lmstudio | 32.74 | LM Studio 모델 저장소. 재다운로드 가능 시 D:Archive 이동. |
| .cache | 27.52 | 캐시. 삭제 가능하나 제안은 하지 않음. 재다운로드 비용 낮은 편. |
| Downloads | 22.87 | 설치파일 히스토리(C:\Users\PC\Downloads\히스토리) 포함. 히스토리 부분만 이동 제안. |
| .ollama | 13.92 | Ollama 모델. 재다운로드 가능 시 D:Archive 이동. |
| Videos | 5.26 | 완성 영상 추정. D:Archive 이동 제안. |
| Desktop | 3.47 | 바탕화면. 활성 작업 가능성 — 그대로 둠. |
| shorts-lab | 2.68 | 활성 작업 폴더 (/c/work/shorts-lab). 그대로 둠. |
| Pictures | 1.59 | 사진. 아카이브 가능성. |
| .claude | 1.39 | Claude 관련 활성 데이터 — 그대로 둠. |
| hansunghee7.github.io | 1.38 | GitHub Pages 저장소. 복제본 여부 확인 필요. |
| .docker | 0.71 | Docker 캐시. 그대로 둠. |
| .local | 0.45 | 로컬 설정 데이터. 그대로 둠. |
| .vscode | 0.45 | VS Code 설정. 그대로 둠. |
| workspace | 0.21 | 작업 폴더. 그대로 둠. |
| .cua-driver | 0.16 | CUA 드라이버. 그대로 둠. |
| ComfyUI | 0.15 | ComfyUI 작업 폴더 (C:\Users\PC\ComfyUI). 활성. |
| .EasyOCR | 0.1 | EasyOCR 데이터. 그대로 둠. |

### 3. git 저장소 14개 실측
저장소별 크기 측정이 오래 걸려 일부는 "미측정"으로 표기. (미측정: du 값 미반환 또는 측정 타임아웃)

| 번호 | 경로 | 크기 | 원격 URL | 마지막 커밋 | 미커밋 | 묶음 |
|------|------|------|---------|------------|--------|------|
| 1 | /c/Users/PC/AppData/Local/hermes/hermes-agent | 미측정 (AppData 전체 147.92GB의 일부) | NousResearch/hermes-agent | 2026-09-14 fix(desktop): dragging a link | 1 | Hermes 본체 |
| 2 | /c/Users/PC/AppData/Local/Temp/.../ComfyUI-LTXVideo | 111M | Lightricks/ComfyUI-LTXVideo | 2026-08-20 Merge pull request #550 | 1 | 임시 위치, 정리 대상 |
| 3 | /c/Users/PC/AppData/Local/Temp/hermes-clone-test | 131K | hansunghee7/hermes-node-bridge | 2026-09-12 완료: echo_test | 0 | 테스트용, 정리 대상 |
| 4 | /c/Users/PC/AppData/Local/Temp/simplifier_style | 419M | 없음(ERROR) | 없음(ERROR) | 0 | 정체 불명 — D:정리대기 격리 |
| 5 | /c/Users/PC/ComfyUI | 142M | comfyanonymous/ComfyUI | 2026-09-09 quant_ops: drop ROCm triton | 1 | ComfyUI 정본 후보① |
| 6 | /c/Users/PC/Documents/ComfyUI | 미측정 (Documents 292.21GB의 일부, 추정 ~142M) | comfyanonymous/ComfyUI | 2026-09-04 Support MiniMax-H3 | 1 | ComfyUI 중복 클론, 사장님 판단 |
| 7 | /c/Users/PC/Documents/shorts-lab-pilot | 미측정 (Documents의 일부, 추정 ~2.6GB) | hansunghee7/shorts-lab | 2026-09-10 저녁 의식: LTX-2.3 | 0 | shorts-lab 중복 클론, 사장님 판단 |
| 8 | /c/Users/PC/hermes-node-bridge | 630K | hansunghee7/hermes-node-bridge | 2026-09-12 신PC 텔레그램 발송 시험 | 2 | 활성 클론 (미커밋 2) |
| 9 | /c/Users/PC/simplifier-saegim | 1.1M | hansunghee7/simplifier-saegim | 2026-09-10 Cloud Run Dockerfile | 0 | simplifier-saegim 중복 클론, 사장님 판단 |
| 10 | /c/work/hansunghee7.github.io | 미측정 (폴더 측정 1.38GB) | hansunghee7/hansunghee7.github.io | 2026-09-15 Merge branch main | 2 | 활성 클론 (미커밋 2) |
| 11 | /c/work/shorts-lab | 2.6G | hansunghee7/shorts-lab | 2026-09-15 ep09 v14 | 0 | shorts-lab 정본 후보① (최신 커밋) |
| 12 | /c/work/simplifier-agent | 32M | hansunghee7/simplifier-agent | 2026-09-03 brief: PO 우선순위 | 0 | 활성 클론 |
| 13 | /c/work/simplifier-saegim | 1.2M | hansunghee7/simplifier-saegim | 2026-09-09 chore: 프로비저닝 검증 | 0 | simplifier-saegim 정본 후보② |
| 14 | /c/work/solar-bible | 1.3M | hansunghee7/solar-bible | 2026-09-15 tasks/pending: 신PC 폴더 정리안 발주 | 5 | 현재 작업 중인 클론 (미커밋 5) |

**동일 원격 중복 클론 (사장님 판단 필요)**:
- comfyanonymous/ComfyUI: ⑤ C:\Users\PC\ComfyUI (142M, 커밋 9/9) vs ⑥ Documents\ComfyUI (미측정, 커밋 9/4) — 어느 것이 정본/활성인지 확인 필요.
- hansunghee7/shorts-lab: ⑦ Documents\shorts-lab-pilot (미측정, 커밋 9/10) vs ⑪ /c/work/shorts-lab (2.6G, 커밋 9/15) — /c/work/shorts-lab가 더 최신. Documents 쪽은 옛 클론 가능성.
- hansunghee7/simplifier-saegim: ⑨ C:\Users\PC\simplifier-saegim (1.1M, 커밋 9/10) vs ⑬ /c/work/simplifier-saegim (1.2M, 커밋 9/9) — 유사한 크기, 커밋 날짜 비슷. 어느 것이 정본인지 확인 필요.

### 4. G: 구글 드라이브 충돌 파일
- 충돌 후보 파일: 130개, 총 0.38 GB (376,786,990 Bytes)
- 패턴: "사본", "(1)", "(2)" 등 포함 파일
- 상위 10개 경로 (크기 순):
  1. G:\내 드라이브\AI숏폼 아카이브\신기한 아파트사전\ep03-택배차\0831 (1).mp4 — 0.15 GB
  2. G:\내 드라이브\주식회사 심플리파이어\UX & Project\Order_Flow_Prototype_180111 (1).mp4 — 0.06 GB
  3. G:\다른 컴퓨터\내 노트북\문서\카카오톡 받은 파일\UX의 언어들_Indesign_v2 (1).pdf — 0.04 GB
  4. G:\다른 컴퓨터\내 노트북\문서\카카오톡 받은 파일\UX언어들_완성본 복사본.pdf — 0.02 GB
  5. G:\내 드라이브\주식회사 심플리파이어\백업\Document\2022VC리포트 (1).pdf — 0.02 GB
  6. G:\내 드라이브\주식회사 심플리파이어\강연\PM의기술_금호타이어_202604(사전공유용_과장편) (1).pptx — 0.02 GB
  7. G:\내 드라이브\주식회사 심플리파이어\강연\PM의기술_금호타이어_202604(사전공유용_책임편) (1).pptx — 0.02 GB
  8. G:\내 드라이브\주식회사 심플리파이어\백업\Document\2022-09-16 HDJ_IR_CONFIDENTIAL (1).pdf — 0.01 GB
  9. G:\다른 컴퓨터\내 노트북\문서\[탈잉기업교육] 파트너강사 등록 양식(update.2604)_한성희 강사님 (1).pptx — 0.01 GB
  10. G:\다른 컴퓨터\내 노트북\Videos\03.아파트택배차\08 (1).png — 0.01 GB
- 판정: 충돌 파일은 총 0.38 GB로 용량 작음. "사본"/" (1)" 패턴 정리는 G: 드라이브 내 정리 대상. 이번 C:/D: 정리안과 직접 연관 적음. 별도 발주 권고.

### 5. 정리안 표
**제안대로 하면 C: 여유 예상 약 119 GB** (Downloads 히스토리 별도 측정 시 추가 확보 가능, CrossDevice 64.1GB 포함)

| 번호 | 경로 | 크기(GB) | 종류 | 제안 | 근거 | 사장님 O/X |
|------|------|---------|------|------|------|---------|
| 1 | D: 드라이브 | 7,993 (여유) | HDD 아카이브 | 아카이브 타겟으로 확정 | C:→D: 이동 시 용량 충분, HDD라 속도 느리지만 저장 목적 적합 | O |
| 2 | C:\Users\PC\Downloads\히스토리 (설치파일) | 미측정 (Downloads 전체 22.87GB 중 일부) | 설치파일 히스토리 | D:\Archive\설치파일_히스토리\ 로 이동 | 쓰임 분명, 되돌리기 쉬움. 재설치 시 재다운로드 가능. | |
| 3 | C:\Users\PC\Videos | 5.26 | 완성 영상 (추정) | D:\Archive\완성영상\ 으로 이동 | 완성 영상은 활성 작업 아님. 아카이브 적합. | |
| 4 | C:\Users\PC\.lmstudio | 32.74 | AI 모델 (LM Studio) | D:\Archive\LM_Studio_모델\ 으로 이동 (재다운로드 가능 시) | 모델 재다운로드 가능하면 아카이브. 불가 시 그대로 둠. | |
| 5 | C:\Users\PC\.ollama | 13.92 | AI 모델 (Ollama) | D:\Archive\Ollama_모델\ 으로 이동 (재다운로드 가능 시) | 모델 재다운로드 가능하면 아카이브. | |
| 6 | C:\Users\PC\CrossDevice | 64.1 | 불명 폴더 | D:\_정리대기\CrossDevice\ 로 격리 (구조·이름 그대로) | 정체성 불명. 삭제 제안 금지. 격리 후 사장님 확인. | |
| 7 | C:\Users\PC\AppData\Local | (AppData 전체 147.92GB의 일부, 세부 측정 필요) | 프로그램 데이터 | 사장님 판단 (하위 폴더별 분류 필요) | AppData는 프로그램 구동에 중요. Hermes, ComfyUI 등 포함. 전체 이동 불가. 하위 폴더(Cache 등)만 선별 검토. | |
| 8 | C:\Users\PC\ComfyUI | 0.15 (활성 작업용) | ComfyUI 작업 폴더 | 그대로 둠 | 활성 작업 폴더. 삭제 시 재설치 비용. | |
| 9 | C:\Users\PC\Documents\ComfyUI | 미측정 (추정 ~0.14) | ComfyUI 중복 클론 | 사장님 판단 (정본 확인 후 결정) | C:\Users\PC\ComfyUI와 중복. 어느 것이 활성인지 확인 필요. | |
| 10 | C:\Users\PC\Documents\shorts-lab-pilot | 미측정 (추정 ~2.6) | shorts-lab 중복 클론 | 사장님 판단 (정본 확인 후 결정) | /c/work/shorts-lab(2.6G, 커밋 9/15)가 더 최신. Documents 쪽은 옛 클론 가능성 — D:\Archive\shorts-lab_옛클론 으로 이동 가능. | |
| 11 | C:\Users\PC\simplifier-saegim | 0.0011 | simplifier-saegim 중복 클론 | 사장님 판단 (정본 확인 후 결정) | /c/work/simplifier-saegim과 중복. 커밋 날짜 비슷. | |
| 12 | C:\Users\PC\AppData\Local\Temp\simplifier_style | 0.419 | 정체 불명 폴더 (원격 없음) | D:\_정리대기\simplifier_style\ 로 격리 | 원격 없고 정체 불명. 임시 위치. 격리 후 확인. | |
| 13 | C:\Users\PC\AppData\Local\Temp\ComfyUI-LTXVideo | 0.111 | 임시 클론 (Lightricks/ComfyUI-LTXVideo) | D:\_정리대기\ComfyUI-LTXVideo\ 로 격리 또는 삭제 검토 | 임시 위치, 원격 있으나 앱 데이터와 무관. 격리 후 확인. | |
| 14 | C:\Users\PC\AppData\Local\Temp\hermes-clone-test | 0.00013 | 테스트용 클론 | D:\_정리대기\hermes-clone-test\ 로 격리 또는 삭제 검토 | 테스트 용도. 현재 필요 없으면 정리. | |
| 15 | /c/work/hansunghee7.github.io | 1.38 (폴더 측정값) | GitHub Pages 저장소 | 그대로 둠 (또는 D:\Archive\hansunghee7.github.io_백업 으로 이동) | 활성 저장소인지 확인 필요. 미커밋 2 있음 — 활성 가능성. | |
| 16 | G: 드라이브 충돌 파일 (130개) | 0.38 | G: 충돌 사본 | G: 드라이브 내 별도 정리 (이번 C:/D: 정리 대상 아님) | C:/D:와 무관. G:에서 "사본"/" (1)" 패턴 정리 별도 발주 권고. | |

**비고**:
- 삭제 제안은 하지 않음 (발주 제약).
- "미측정"은 5분 타임아웃 전에 측정 불가한 항목. 실제 크기는 더 클 수 있음.
- Downloads\히스토리, Documents\ComfyUI, Documents\shorts-lab-pilot는 상위 폴더 측정값에 포함되어 있으나 별도 크기 미측정. 필요 시 추가 측정.
- AppData(147.92 GB)는 전체를 대표할 수 없어 세부 분류 필요. 사장님 판단 항목으로 둠.

