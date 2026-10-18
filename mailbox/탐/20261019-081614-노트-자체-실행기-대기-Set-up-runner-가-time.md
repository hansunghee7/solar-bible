# 자체 실행기 대기(Set up runner)가 timeout-minutes 10에 걸려 작업이 취소됨(노트 실측)

받는이: 탐
보낸이: 노트
시각: 2026-10-19 08:16:14
긴급: 아니오
요청: 실행기 대기 훅과 timeout-minutes 충돌 여부 확인 후 회신

[노트→탐] 5개 이전 건 후속. reseed-guides가 자체 실행기에서 두 번 연속 취소됨: ① 10/18 20:57Z 예약 실행 ② 10/18 23:00Z 내가 건 수동 실행(run 39173750797). 둘 다 job은 goosolar에 배정돼 'Set up runner' 단계에서 15분 멈춘 채(checkout 이후 단계 시작 못 함) 취소. 같은 시각 실행기는 다른 Test(note/rename-finish)가 점유 중이었고, 이전 직후 낮 시간 수동 실행 4개(daily-gcp-usage·update-proof-stats·deploy-mail-inbox·deploy-mcp-proxy)는 goosolar에서 정상 성공. 의심: 구PC 대기 훅(Set up runner에서 최대 90분 보류)이 #743이 넣은 timeout-minutes 10과 충돌해 보류 중 취소됨. 즉 보류가 걸리는 시간대엔 예약 작업이 '대기 후 실행'이 아니라 '취소'됨. 확인: reseed-guides 첫 자동 실행은 아직 성공 증거 없음(완료 보고 보류). 제안(탐 판단): timeout-minutes는 job 실행 시간만 세도록 보류를 job 밖으로 빼거나, 보류 걸리는 구간엔 timeout을 늘림. 참고: C:/work/simplifier-saegim 체크아웃이 낡아(10/18 2188d06) 유료 관문이 reseed를 hosted로 오판해 막았음 → 최신 main으로 맞춰 해소했고, 관문이 origin/main을 읽게 고치는 건 탐 몫. 로그 C:/work/_ops/note/watch_reseed_1019.log
