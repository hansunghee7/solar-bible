# 지시서: 폴러 결정적 실행기 회귀 시험 (백로그 31 검증) (탐 → 헤르메스)

받는 이: 헤르메스 / 발주자: 탐(CTO) / 발주일: 2026-09-22 / 사장님 승인: 2026-09-21 저녁(착수 가능)

## 배경
백로그 31이 지적한 사고: 2026-09-20 14:19 폴러(Solar Pro 4 무료)가 지시서 처리 중 done 이동
단계를 빼먹고 27자짜리 짧은 답으로 정상 종료해, 같은 지시서를 재처리하느라 20분을 낭비하고
후속 지시서가 20분 대기했다. 원래 요구는 "폴러의 마무리(완료 표시, done 이동, 커밋, 알림)를 AI
대신 스크립트가 하고 AI는 실제 작업만 하기"였다.

이 요구는 **이번 세션 이전에 이미 구현됐다**: `pending_poller.py`(헤르메스 홈
`scripts/pending_poller.py`, 저장소 사본 `hansunghee7.github.io` 레포
`scripts/ops/hermes-poller/pending_poller.py`, PR #925·#927)가 done 이동·git add·commit·push·
우편 알림을 전부 스크립트가 결정적으로 처리하고, AI(`hermes chat`)는 지시서 본문 처리 결과
텍스트만 돌려준다. 즉 AI 응답이 얼마나 짧든 done 이동 여부는 AI가 아니라 스크립트의
`process_one()` 반환값(성공 exit code 여부)에만 달려 있어, 이 사고가 구조적으로 재발할 수
없어야 한다(탐 판단, 미검증).

이 지시서는 새로 만드는 것이 아니라 **그 판단이 맞는지 원래 사고 시나리오로 실제로 재현해
검증**하는 것이다.

## TASK
`pending_poller.py`(헤르메스 홈 실행본)를 바꾸지 않고, 2026-09-20 사고와 같은 조건(AI가 아주
짧은 응답만 내고 끝나는 상황)을 만들어 회귀 시험한다.

1. `tasks/pending/`에 "아주 짧은 답만 나오도록 유도하는" 시험 지시서를 하나 넣는다(예: "숫자
   1만 답하고 다른 말은 하지 마라"). 실행 전후 `tasks/pending/`, `tasks/done/`, git log를
   스크린샷 대신 텍스트로 기록한다.
2. 크론이 자연 실행되길 기다리거나 `hermes cron run <폴러 id>`로 직접 트리거한다(짧은 레인
   `dbec1e96eff3`).
3. 짧은 응답이 나온 뒤에도 파일이 `tasks/done/`으로 옮겨지고 git commit·push까지 실제로
   일어나는지 확인한다(git log 해시, done 폴더 파일 존재로 증명).
4. 만약 옮겨지지 않거나 재처리가 필요한 상황이 재현되면(즉 사고가 아직 안 고쳐졌으면) 그대로
   "재발함"이라고 정직하게 보고한다 — 통과로 꾸미지 않는다. 코드 수정은 이 지시서 범위 밖이다
   (발견만 하고 판단은 탐에게 넘긴다).
5. 별도로: 백로그 31 원문에는 "프로필별 병렬 실행 가능"이라는 조건도 있었다. 현재
   `pending_poller.py`는 파일을 순차(for 루프)로 처리한다. 병렬 실행이 구현돼 있는지 코드를
   읽고 사실만 보고한다(구현하라는 지시가 아니다).
6. 결과 보고 형식: TASK/EXECUTION/OBSERVATION/VERIFICATION/EVIDENCE/FAILURE-RECOVERY/STATUS.
   시험에 쓴 지시서 파일명과 실행 시각(시스템 시계), git 커밋 해시를 EVIDENCE에 정확히 적는다.

## 끝나면
`python C:\work\solar-bible\mailbox\mailbox.py send 탐 "백로그 31 회귀 시험 결과" --from 헤르메스 --body "reports/2026-09-22-verify-poller-executor-backlog31.md 확인. STATUS=..."`
