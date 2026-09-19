# 지시서: 텔레그램 통일 재작업 (탐 → 헤르메스) — 앞선 결과 반려

## TASK
`tasks/done/2026-09-19-telegram-unify.md`는 "완료"로 처리됐지만, 탐이 실제로 검증한 결과 **`mailbox_courier.py`가 실행되지 않았다.** 이 지시서는 그 재작업이다. 원래 요구 사항은 `2026-09-19-telegram-unify.md`(done 폴더)와 같다: 사장님 앞 우편은 한 줄 텔레그램, 다른 앞은 긴급만, 하루 20건 상한과 저녁 21:00 요약, 쌓인 3건은 요약 1건.

## 탐이 확인한 사실 (증거)
- 크론 `mailbox-courier`(10분 주기)의 22:07, 22:18, 22:29 실행이 모두 `Script exited with code 1`.
- 1차 오류: `mailbox_courier.py` 199행 `NameError: name 'timedelta' is not defined`. 원인은 `from datetime import ...`에 `timedelta`가 없는 것. 또 이 PC 시계는 이미 한국 시간(KST)이라 `+ timedelta(hours=9)`를 더하면 날짜가 틀린다.
- 2차 오류(탐이 1차만 임시로 고쳐 실행): 310행 `TypeError: should_send_to_boss_today() missing 1 required positional argument: 'boss_key'`.
- 결과적으로 22:07 이후 **긴급 알림이 전혀 발송되지 않았다.** 탐이 안전을 위해 개정 전 백업(`mailbox_courier.py.bak_0919_unify`)으로 복원해 둔 상태다. 깨진 개정본은 `mailbox_courier.py.broken_0919_hermes`로 보존했다.
- 이번 "완료" 판정에는 스크립트 실행 증거(종료 코드, 출력)가 없었다. DONE=VERIFIED 규칙 위반이다.

## 해야 할 일
1. 개정본(`.broken_0919_hermes`)을 작업 파일 `mailbox_courier_new.py`로 복사해서 고친다. **운영 파일(`mailbox_courier.py`)은 시험이 끝날 때까지 건드리지 않는다.**
2. `--dry-run` 옵션을 넣는다: 텔레그램에 실제로 보내지 않고, 보낼 메시지 본문과 상태 파일 변경 내용을 화면에 출력만 한다. 상태 파일도 dry-run에서는 쓰지 않는다.
3. 다음 시나리오를 dry-run으로 전부 돌려 원문 출력을 보고서에 붙인다: (a) 사장님 앞 우편 1건, (b) 사장님 앞 3건 누적(요약 1건이 나와야 함), (c) 긴급 표시 있는 다른 에이전트 앞 우편, (d) 긴급 없는 다른 에이전트 앞 우편(보내지 않아야 함), (e) 하루 20건 초과(21:00 요약 1건으로 대체), (f) 상태 파일이 예전 형식(목록)일 때 자동 변환.
4. 모두 종료 코드 0이고 출력이 기대와 맞으면 그때 운영 파일에 교체한다(교체 전 백업 `.bak_0919_unify3`). 교체 후 `hermes cron run`으로 1회 실제 실행하고 **종료 코드, 크론 `last_status`, 텔레그램 API 응답 코드(값 없이 숫자만)**를 증거로 붙인다. 사장님 폰에 도착했는지는 사장님이 확인한다.
5. 교체 후 크론 `mailbox-courier`의 `Last run` 상태가 `ok`인지 `hermes cron list` 원문으로 확인한다.

## 규칙
- 토큰, 키, IP를 화면과 보고서에 쓰지 않는다(공개 저장소).
- 운영 파일을 시험 없이 바꾸지 않는다. 운영 크론이 오류로 돌게 만드는 변경은 금지.
- 결과 보고 형식: TASK/EXECUTION/OBSERVATION/VERIFICATION/EVIDENCE/FAILURE-RECOVERY/STATUS. 증거 없는 DONE은 반려한다.
