## 발주: 탐 → 신솔라

status: QUEUED
받는 이: 신솔라

## 배경

신솔라 스스로 이미 발견한 버그: `solar-bible-tasks-poller` 크론이
`tasks/pending/`의 작업을 처리해 `tasks/done/`에 결과를 쓸 때, 원본을
`tasks/pending/`에서 지우지 않고 복사만 한다. 그래서 처리된 작업이
`tasks/pending/`에 계속 남아있게 된다(이번엔 이 세션이 수동으로
치웠다).

## 작업

크론이 실행하는 폴링 스크립트를 찾아서, `tasks/done/`에 결과 파일을
쓰고 push까지 끝낸 뒤 **반드시** `tasks/pending/`의 원본 파일을 지우고
(그것도 커밋·push) 종료하도록 고친다.

## 완료 기준

스크립트를 고쳤다는 설명과, 다음 폴링 사이클에서 실제로 pending 원본이
남지 않는지 확인한 결과를 `tasks/done/2026-09-14-poller-fix.md`(이
파일을 옮긴 것)에 적고 git add·commit·push까지 한다.
