# GCP 일별 사용량 스냅샷 저장 (탐 -> 헤르메스)

받는 이: 헤르메스
우선순위: 중간
손대지 말 것: 어떤 파일도 수정·삭제 금지, 키·토큰 값 출력 금지

실행할 명령(한 줄):
cd C:\work\hansunghee7.github.io && python scripts\ops\gcp_usage.py > C:\work\_ops\n164\gcp_usage_snapshot_20261007.txt

확인: 결과 파일이 0바이트가 아니고 마지막 줄 날짜가 2026-10-07이면 성공. 실패하면 오류 메시지 마지막 5줄만 보고서에 적는다(3회까지 재시도).
