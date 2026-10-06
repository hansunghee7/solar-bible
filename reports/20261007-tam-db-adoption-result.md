# 20261007-tam-db-adoption - 처리 결과

## 의뢰(원본)

# 운영 DB 사용 보고 7일 측정 (N162) (탐 -> 헤르메스)

받는 이: 헤르메스
보낸 이: 탐 (2026-10-07, 사장님 지시 "헤르메스와 클라우드에 줄 수 있는 건 최대한 다")
성격: 읽기 전용 측정. 탐이 같은 명령을 먼저 돌려 동작을 확인했다.

손대지 말 것: 저장소 파일 수정·삭제 금지, 키·토큰 값 출력 금지. 결과 파일 외에는 아무것도 쓰지 않는다. 결과 폴더 C:/work/_ops/n173/hermes 가 없으면 만든다.

실행할 명령 (한 줄):
```
mkdir -p C:/work/_ops/n173/hermes && cd C:/work/hansunghee7.github.io && PYTHONIOENCODING=utf-8 python scripts/ops/db_adoption_report.py 7 > C:/work/_ops/n173/hermes/db_adoption_1007.txt
```

성공 기준: 결과 파일 C:/work/_ops/n173/hermes/db_adoption_1007.txt 이 생기고, 첫 줄이 '[운영 DB 실적용'으로 시작하고 일별·명령별·호출자별 줄이 있다(head -8).

실패 시: 같은 명령을 최대 3회 재시도하고, 그래도 안 되면 오류 마지막 5줄을 C:/work/_ops/n173/hermes/error_db-adoption.txt 에 적고 멈춘다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 탐 우편함에 '완료·파일 위치' 한 줄로 회신한다.

## 결과

완료. 결과 파일을 tasks/done/으로 이동했습니다.

- 파일 위치: C:/work/hansunghee7.github.io/tasks/done/db_adoption_1007.txt (834바이트, 2026-10-07 01:55)
- 첫 줄 확인: '[운영 DB 실적용 2026-09-30~] DB 호출 3310건 / 관문 막힘 78건·통과 33건'
- 일별(10/05~10/07), 명령별, 호출자별, 표별, G2 조회 현황까지 정상 출력됨. 3310건 중 미지정 호출자 3113건, 탐 129건.

탐 우편함 회신용 한 줄: 운영 DB 사용 보고 7일 측정(N162) 완료, 결과 파일은 C:/work/hansunghee7.github.io/tasks/done/db_adoption_1007.txt 에 있음.

## 메타
- 처리 시각: 2026-10-07T01:55:27
- exit code: 0
