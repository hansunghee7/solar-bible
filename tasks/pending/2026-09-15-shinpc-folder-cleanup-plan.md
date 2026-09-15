## 발주: 탐 → 신솔라

status: QUEUED

받는 이: 신솔라 (신PC 로컬 작업이라 구솔라에 넘기지 않는다)

## 배경

사장님이 2026-09-15 신솔라 과제 1순위를 "신PC 폴더 정리 및 최적화"로
확정했다(헤르메스 과제 정리판 S1-2 "신PC Active/Archive 분리"에 해당).
9/14~15 조사(`tasks/done/2026-09-14-shinsolar-cleanup-survey.md`,
`2026-09-15-gdrive-mess-shinpc-recheck.md`)로 이미 아는 것:

- C: 1TB SSD 사용 885GB / 여유 113GB. D: 8TB(HDD 추정) 사용 8GB.
- 큰 후보: `C:\Users\PC\Downloads\히스토리`(설치파일), `C:\c\c\Users\PC\_tmp_repo`
  (1.2GB, bash 경로 변환 오류 산물 추정), `AppData\Local`(크기 미측정, du
  타임아웃), shorts-lab `channels/*/episodes/*/episode.mp4`, ComfyUI 모델·출력,
  hermes backups, simplifier-saegim 복제본 여러 개, `_OneDrive잔여`.
- G: 구글 드라이브 동기화 중, "사본"·"(1)" 충돌 파일 다수.

이번 발주는 **정리안(계획표)까지만**이다. 이동·삭제는 하지 않는다. 사장님이
표를 보고 행마다 O/X를 준 뒤 다음 발주에서 실행한다(심플리파이어
`docs/PC_폴더_정리_브리프.md` Phase 1→2 순서, 솔라바이블 §10).

## 작업

목표 구조(정리판 S1-2): **C: = OS·AI 모델·캐시·활성 작업, D: = 아카이브
(완성 영상, 설치파일 히스토리, 옛 클론, 격리 폴더)**.

1. D: 드라이브 실측. PowerShell `Get-PhysicalDisk | Select FriendlyName,
   MediaType, Size`와 `Get-Volume`으로 D:가 HDD인지 SSD인지, 여유 용량을
   확정한다(추정 금지).
2. C: 대용량 폴더 상위 20개 측정. `du`가 타임아웃 났던 곳(`AppData\Local`)은
   PowerShell로 폴더 1단계씩 나눠 잰다(예: `Get-ChildItem -Directory |
   ForEach { [pscustomobject]@{Path=$_.FullName; GB=[math]::Round((Get-ChildItem
   $_.FullName -Recurse -File -EA SilentlyContinue | Measure-Object Length
   -Sum).Sum/1GB,1)} } | Sort GB -Desc`). 한 폴더가 5분 넘게 걸리면 건너뛰고
   "미측정"으로 적는다.
3. git 저장소 17개 각각: 경로, 크기, 원격 URL(`git remote -v`), 마지막 커밋
   날짜, 미커밋 변경 유무(`git status --porcelain` 줄 수). 같은 원격을 가진
   클론이 여러 개면 묶어서 표시한다.
4. 구글 드라이브(G:) 충돌 파일: "사본", "(1)", "(2)" 패턴 파일의 개수와
   총 용량만 센다. 목록 전체를 나열하지 않는다(상위 10개 경로만).
5. 위 결과를 **정리안 표** 하나로 만든다. 열: `번호 | 경로 | 크기(GB) |
   종류 | 제안 | 근거 | 사장님 O/X`. 제안은 아래 넷 중 하나만:
   - `D:\Archive\<원래 상위폴더명>\ 으로 이동` (완성 영상, 설치파일 히스토리처럼
     쓰임이 분명하고 되돌리기 쉬운 것)
   - `D:\_정리대기\<원래 경로 그대로>\ 로 격리` (무엇인지 애매한 것. 이름·구조
     그대로 옮기기만 한다)
   - `그대로 둠` (활성 작업, 캐시 중 삭제 시 재다운로드 비용이 큰 것)
   - `사장님 판단` (중복 클론 중 어느 것이 정본인지 등 신솔라가 못 정하는 것)
   삭제 제안은 하지 않는다. 표 맨 위에 "제안대로 하면 C: 여유 예상 xxx GB"
   한 줄을 쓴다.

하지 말 것: 파일 이동·삭제·이름 변경 일체. 저장소 안 파일 수정. 비밀값 출력
(`.env`, `auth.json` 내용은 크기만). 공개 저장소이므로 IP·MAC 기재 금지.

## 완료 기준

이 파일을 `tasks/done/2026-09-15-shinpc-folder-cleanup-plan.md`로 옮기고
아래 "조사 결과" 절에 1~5의 실측값과 정리안 표를 적은 뒤 git add·commit·push.
표의 모든 행에 크기 실측값이 있어야 한다(미측정이면 "미측정"이라고 명시).
솔라바이블 §3에 따라 단계(1~5)마다 중간 저장한다. 단계 2에서 시간이 오래
걸리면 1·3·4를 먼저 끝내고 2를 마지막에 한다.

---
## 조사 결과

(신솔라가 채운다)
