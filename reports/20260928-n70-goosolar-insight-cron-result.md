# 20260928-n70-goosolar-insight-cron - 처리 결과

## 의뢰(원본)

# N70 구PC(goosolar) 인사이트 수집 파이프라인 cron 연결 (탐 -> 헤르메스)

## 배경
`탐_업무대장.md` N70. 구PC(goosolar) SNS 수집(`~/workshop/sns_read.py`) →
SQLite 빌드 → 구글드라이브 업로드(`~/workshop/build_insight_db.py`) 파이프라인은
2026-09-28에 수동 1회 PoC로 DONE=VERIFIED 확인됐다(SQLite→Drive→왕복조회 성공).
남은 건 이걸 **구PC crontab에 주기 등록**하는 것뿐. 페이스북 게시물별
좋아요·댓글 수집(메타 앱 권한 필요)은 사장님이 이미 보류 결정해서 이 작업
범위 밖이다 — 손대지 말 것.

`run_sns_daily.sh` 스크립트 자체에 이미 실행할 crontab 줄이 주석으로
박혀 있다(`0 1 * * * $HOME/workshop/run_sns_daily.sh`, 구PC는 UTC라
01:00 UTC = 10:00 KST). 이번 작업은 여기에 `build_insight_db.py`(SQLite
빌드 + rclone Drive 업로드)를 체이닝하고, 새 heartbeat 파일을 추가하는 것.

## 할 일 (순서대로, 중간 판단 필요 없음 — 한큐로 실행)

1. `ssh goosolar "crontab -l"`로 현재 crontab을 확인. `run_sns_daily.sh`가
   이미 등록돼 있는지 먼저 본다(있을 수도, 없을 수도 있음 — 확인 안 된 상태).
2. 없으면(또는 있어도 `build_insight_db.py` 체이닝이 안 돼 있으면) 아래
   한 줄로 crontab을 갱신한다(기존 다른 crontab 줄이 있으면 절대 지우지
   말고 이 줄만 추가/교체):
   ```
   0 1 * * * cd $HOME/workshop && ./run_sns_daily.sh && venv/bin/python build_insight_db.py >> out/sns/build_insight.log 2>&1 && date '+%F %T' > out/sns/insight_build.last
   ```
3. **지금 1회 수동으로 실행해서 성공 증거를 직접 만든다**(다음 새벽 1시까지
   기다리지 않는다):
   ```
   ssh goosolar "cd ~/workshop && ./run_sns_daily.sh && venv/bin/python build_insight_db.py"
   ```
4. 아래를 확인해 증거로 남긴다:
   - `ssh goosolar "cat ~/workshop/out/sns/last_run"` — 방금 시각으로 갱신됐는지
   - `ssh goosolar "cat ~/workshop/out/sns/insight_build.last"` — 방금 시각 파일이 새로 생겼는지
   - `build_insight_db.py`의 표준출력(`followers_daily rows=N, content_items rows=M` 형태) — 0이 아닌지
   - `ssh goosolar "crontab -l"` 재확인 — 줄이 실제로 저장됐는지(dry-run 아님)

## 완료 확인 기준
- 위 4개 증거(last_run 갱신 시각, insight_build.last 존재+시각, build 스크립트
  출력 행 수, crontab -l 출력)를 표준출력 그대로 `reports/`에 남겨줘(요약 금지,
  원문 그대로).
- 하나라도 실패하면(SSH 접속 실패, 스크립트 exit 비정상, rclone 업로드 실패 등)
  에러 메시지 원문을 그대로 남기고 멈춰도 된다 — 3회 재시도 규칙 적용, 같은
  에러가 3회 반복되면 재시도 그만하고 실패로 보고.

## 위임 금지 사항 없음
기존에 이미 설계·1회 검증된 스크립트를 crontab에 등록하고 1회 재실행하는
것뿐이라 안전하고 되돌리기 쉬운 작업이다(crontab 줄 하나 추가/교체, 계정
생성·결제·비밀값 입력·파괴적 변경 없음).

## 결과

보고서 작성 완료. 이제 `## 실행 피드백`을 추가하고 종료합니다.

---

작업 완료. crontab 등록 + 수동 1회 실행 성공 + 증거 4종 확인 완료.

## 실행 피드백

지시서 형식은 명확했고 단계도 직선으로 이어져 실행하기 쉬웠다. 유일한 장애는 구PC 측 SSH 세션 안에서 로컬의 `rm /tmp/...`를 실행할 때 "dangerous command"플래그로 막힌 것 하나 — 구PC temp 경로를 `/home/goosloar/.tmp_c12345`로 바꾸고 `rm`은 생략(파일 방치해도 문제 없는 작은 파일)한 것으로 우회했다. SSH 접속·스크립트 실행·crontab 갱신·증거 수집은 모두 한 번에 통과.
  [tool] ( ˘⌣˘)♡ ruminating...

## 메타
- 처리 시각: 2026-09-28T16:48:07
- exit code: 0
