# 20261007-tam-two-checks - 수신 확인

## 메타
- 수신 시각: 2026-10-07T01:57:05
- 레인: pending-long

## 의뢰(받은 그대로)

# 정기 점검 2건 실행 (N164 정기 누락 감시, N105 다이얼로그 합성 점검) (탐 -> 헤르메스)

받는 이: 헤르메스
보낸 이: 탐 (2026-10-07, 사장님 지시 "헤르메스와 클라우드에 줄 수 있는 건 최대한 다")
성격: 읽기 전용 측정. 탐이 같은 명령을 먼저 돌려 동작을 확인했다.

손대지 말 것: 저장소 파일 수정·삭제 금지, 키·토큰 값 출력 금지. 결과 파일 외에는 아무것도 쓰지 않는다. 결과 폴더 C:/work/_ops/n173/hermes 가 없으면 만든다.

실행할 명령 (한 줄):
```
mkdir -p C:/work/_ops/n173/hermes && cd C:/work/hansunghee7.github.io && PYTHONIOENCODING=utf-8 python scripts/ops/check_gcp_usage_schedule.py > C:/work/_ops/n173/hermes/checks_1007.txt; echo "exit=$?" >> C:/work/_ops/n173/hermes/checks_1007.txt; PYTHONIOENCODING=utf-8 python scripts/ops/check_dialog_daily.py >> C:/work/_ops/n173/hermes/checks_1007.txt; echo "exit=$?" >> C:/work/_ops/n173/hermes/checks_1007.txt
```

성공 기준: 결과 파일 C:/work/_ops/n173/hermes/checks_1007.txt 이 생기고, 파일에 '정기 실행 성공 N건'과 'OK'가 있고 exit=0이 두 번 나온다 (exit=1이면 실패가 아니라 그대로 보고).

실패 시: 같은 명령을 최대 3회 재시도하고, 그래도 안 되면 오류 마지막 5줄을 C:/work/_ops/n173/hermes/error_two-checks.txt 에 적고 멈춘다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 탐 우편함에 '완료·파일 위치' 한 줄로 회신한다.
