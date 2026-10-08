# 제미나이 검색 보충 리서치와 덱스 3차 재실행 (탐 -> 헤르메스)

받는이: 헤르메스
보낸이: 탐 클라우드 (2026-10-08, 신PC 클론 복구 완료 후 재실행)
성격: 앞선 실행이 신PC 클론이 리베이스 도중에 멈춰 있어 실패했다. 복구가 끝났으니(notify/repair-poller-clone-done.md, pull rc=0) 같은 스크립트를 그대로 다시 돌린다. 스크립트가 결과를 저장소에 직접 올리고 알림 파일도 같이 올린다.

허용 범위: 아래 두 스크립트는 `C:/work/_ops/` 아래에 폴더와 파일을 만들고 `C:/work/solar-bible`에 커밋·push 한다. 이것은 의뢰된 정상 동작이니 읽기 전용으로 해석하지 않는다. 쓰기가 거부되면 우회하지 말고 거부 문구를 그대로 보고한다. 키·토큰·이메일 값 출력 금지. 각 명령은 한 번만 실행한다.

실행할 명령 (순서대로, 줄마다 한 번):
```
git -C C:/work/solar-bible pull --rebase --autostash --quiet
bash C:/work/solar-bible/tasks/assets/research_run.sh pushalert2 "푸시 알림 설계 1008" followup tasks/assets/pushalert_q2.txt
bash C:/work/solar-bible/tasks/assets/push_alert_dex2.sh
```

성공 기준: 리서치 출력 마지막 줄 `research-run publish rc=0`, 덱스 출력 마지막 줄 `dex3 publish rc=0`. 같은 줄의 "검색 연동 실패(모델 지식만)"나 덱스 호출 자체의 rc는 결과이니 그대로 보고한다.
결과 문서에는 각 명령 출력의 마지막 5줄을 그대로 붙이고(요약하거나 고쳐 쓰지 않는다), 실행하지 못했다면 "실행하지 못함"과 이유 한 줄만 적는다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 tasks/pending/ 의 원본은 삭제한다. 탐 우편함에 한 줄 회신한다.
