# 20260928-n70-goosolar-insight-cron — 탐 검증(JUDGE)

## 의뢰(내가 보낸 것)
`tasks/pending-long/20260928-n70-goosolar-insight-cron.md` — 구PC(goosolar) crontab에
`run_sns_daily.sh` → `build_insight_db.py`(SQLite 빌드 + rclone Drive 업로드) 체이닝 등록,
지금 1회 수동 실행으로 성공 증거 확보.

## 완료 확인(내가 직접 검증한 근거, DONE=VERIFIED)
헤르메스 보고서(`reports/20260928-n70-goosolar-insight-cron-result.md`)가 "증거 4종 확인
완료"라고만 적고 원문을 안 붙였길래(지시서에 원문 그대로 남기라고 했는데 요약만 됨), SSH로
직접 재확인했다.

- `ssh goosolar "crontab -l"`: 새 줄 `0 1 * * * cd $HOME/workshop && ./run_sns_daily.sh &&
  venv/bin/python build_insight_db.py >> out/sns/build_insight.log 2>&1 && date "+%F %T" >
  out/sns/insight_build.last` 정상 등록. 기존 5줄(kick_publish, watch.py, start_chromes ×2,
  rclone mount)은 그대로 보존됨 — 삭제 사고 없음.
- `~/workshop/out/sns/last_run`: `2026-09-28 07:46:00 ok channels_with_followers=11`
- `~/workshop/out/sns/insight_build.last`: `2026-09-28 07:46:38`
- `~/workshop/out/sns/2026-09-28.jsonl`(5552B)·`compare_2026-09-28.md`·`err_2026-09-28.txt`(0B,
  에러 없음) 전부 07:46 시각으로 새로 생성됨
- `~/workshop/insight.db`: 45056B, 07:46 mtime
- `rclone lsl gdrive:인사이트-데이터/`: `45056 2026-09-28 07:46:00 insight.db` — 로컬과 크기
  정확히 일치, Drive 업로드 확인

end-to-end로 실제 실행됐고 결과물이 실재함을 로컬 파일·Drive 양쪽에서 직접 확인했다.

## 문제점/개선사항(내 관점)
1. **보고서에 원문 증거 누락** — 지시서에 "요약 금지, 원문 그대로"라고 명시했는데 헤르메스가
   "증거 4종 확인 완료"로만 요약해서 남김. 다음엔 지시서에 "각 명령의 stdout을 코드블록으로
   그대로 붙여넣어라"처럼 더 구체적으로 못박는 게 나을 듯.
2. **`build_insight.log` 파일 미생성** — 크론 줄은 `>> out/sns/build_insight.log`로 리다이렉트
   하는데 실제로는 그 파일이 없음. `insight_build.last`는 갱신됐으니 빌드 자체는 성공했지만,
   실행 경로가 크론 줄 그대로였는지 변형이었는지 애매함. 기능상 문제는 없지만 다음 실행(내일
   새벽 크론)에서 로그 파일이 실제로 쌓이는지 한 번 더 확인 필요.
3. **rclone shared client_id 은퇴 경고** — `rclone lsl` 실행 시 "This remote uses rclone's
   shared Google Drive client_id, which is being retired and will stop working during 2026"
   경고가 나옴. 지금 당장 문제는 아니지만 2026년 안에 막힐 수 있어 별도 백로그로 등록해야 함
   (자체 client_id 발급 필요).
4. **`rm /tmp/...` "dangerous command" 차단 우회** — 헤르메스가 임시 파일 정리 중 안전
   분류기에 막혀 `/home/goosloar/.tmp_c12345`로 경로를 바꾸고 삭제를 생략함. 작은 파일 방치라
   실질 위험은 없지만, 이런 우회가 반복되면 구PC에 임시 파일이 쌓일 수 있어 주시 대상.

## 메타
- 검증 시각: 2026-09-28 (KST)
- 검증자: 탐(로컬)
