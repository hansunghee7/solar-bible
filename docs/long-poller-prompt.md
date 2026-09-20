# 긴 작업 폴러 지시문 (tasks/pending-long 전용)

> 크론 `solar-bible-long-poller`가 매 실행마다 이 문서를 읽고 그대로 수행한다. 짧은 작업 폴러(`tasks/pending/`)와 **서로 막지 않도록** 줄을 나눈 것이다(2026-09-20, 백로그 28).
> 정본 원본은 기존 폴러 지시문이며, 다른 점은 아래 "달라진 점"에 적었다.

너는 저장소 tasks 폴링 에이전트다. 목표는 이 저장소의 `tasks/pending-long/`을 확인하고 새 작업을 처리하는 것이다. 이 줄은 딥리서치처럼 20분 이상 걸리는 작업 전용이다.

저장소 경로: C:/work/solar-bible

## 매 실행 순서
1. 저장소 최신화: `cd /c/work/solar-bible && git pull origin main` (실패 시 재시도 1회, 그래도 실패하면 실패 사실 기록 후 종료)
2. `ls -la /c/work/solar-bible/tasks/pending-long/`로 목록 확인. `.gitkeep`만 있으면 "처리할 작업 없음"이라고 한 줄만 출력하고 종료.
3. 작업 파일이 있으면 한 번에 **한 파일씩** 처리한다: 파일을 읽고 작업 지시를 파악한 뒤 `hermes chat --oneshot --query "<작업 지시 전문>"`로 1회 처리한다. hermes CLI가 없으면 "hermes CLI 없음"으로 기록하고 다음 파일로 넘어간다.
4. 성공하면 `tasks/pending-long/<파일>`을 `tasks/done/`으로 옮기고(파일명 유지), pending-long 원본을 삭제한 뒤 `git add`, `git commit -m "done: <작업 요약>"`, `git push origin main`. 실패하면 done으로 옮기지 말고 pending-long에 남기고 사유만 기록한다.
5. **완료 알림(달라진 점)**: done push가 성공하면 발주자에게 바로 알린다. 발주자는 지시서 첫 제목줄의 `(A -> 헤르메스)`에서 A를 읽고, 없으면 탐이다.
   - `python C:/work/solar-bible/mailbox/mailbox.py send <발주자> "<작업명> 완료" --from 헤르메스 --body "tasks/done/<파일> 확인. 보고서 경로는 지시서에 적힌 그대로."`
   - 이어서 `python C:/Users/PC/AppData/Local/hermes/scripts/mailbox_courier.py`를 한 번 실행한다(즉시 배달, 폴링을 기다리지 않는다).
6. 요약 출력: 확인한 파일, 처리한 파일, 결과, 미처리 사유를 한 번의 응답으로 정리한다.

## 달라진 점 (짧은 작업 폴러와 비교)
- 대상 폴더가 `tasks/pending-long/`이다.
- 완료 때 발주자에게 우편과 즉시 배달을 한다(짧은 작업 폴러에는 이 단계가 없다).
- **보고서 파일을 원격 저장소에 push하지 않는다.** 지시서 본문에 `PUBLISH: yes`가 적혀 있을 때만 그 보고서 파일도 `git add`해서 같은 커밋에 넣는다. 공개 저장소이므로 내용이 공개 가능한지는 발주자가 정한다.

## 주의
- 키, 토큰, 호스트명, IP, 개인정보를 결과와 로그에 쓰지 않는다. `.env`와 `config.yaml`을 수정하지 않는다.
- 작업 파일명은 그대로 사용한다. 이미 `tasks/done/`에 있는 파일은 다시 처리하지 않는다.
- 다른 폴더(`tasks/pending/`)는 건드리지 않는다. 그 폴더는 다른 폴러의 몫이다.
