## 발주: 탐 → 구솔라

status: QUEUED

받는 이: 구솔라 (위 텔레그램 발주부터 먼저 처리한 뒤 이걸 한다)

## 배경

`tasks/done/2026-09-15-gusolar-performance-report.md`에서 확인한 불필요
상주 프로그램. 사장님 확인(2026-09-15): Epson 프린터·리그오브레전드
(Riot Client/Lunar Client) 둘 다 **이 PC에서 전혀 안 쓴다.** 구PC 목적은
"외부 웨이크업 트리거 + 가벼운 조사"뿐이라(solar-bible.md §14 참고),
이 목적에 안 맞는 건 적극적으로 정리해도 된다고 승인받았다.

## 작업 (자동 실행 제거 수준을 넘어 실제 제거까지 진행해도 된다)

1. **Epson 프린터**: 관련 서비스 중지, 자동 실행 항목(Run 키의
   E_YATIUQE.EXE 등) 제거, 프린터 장치 자체도 제거. 드라이버까지
   완전 삭제할지는 굳이 안 해도 됨(자동 실행·서비스·장치 제거로 충분).
2. **Riot Client / Lunar Client**: 실행 중이면 프로세스 종료, 자동 실행
   항목 제거. 프로그램 제거(언인스톨)까지 해도 된다(승인됨, 사장님이
   전혀 안 쓴다고 확인).
3. Google Drive File Stream, Edge 자동 시작은 **이번엔 건드리지 마라**
   — 구글드라이브는 별도 조사(`tasks/pending/
   2026-09-15-gdrive-hermes-file-mess-survey-retry.md`)가 진행 중이라
   그 결과 먼저 보고 판단한다.

## 완료 기준

1·2번 각각 무엇을 했는지(중지한 서비스명, 제거한 항목, 제거 방식)를
이 파일에 적고, 재부팅 없이 확인 가능한 범위에서 실제로 더는 안 뜨는지
확인한 결과까지 적은 뒤 `tasks/done/2026-09-15-gusolar-declutter.md`로
옮기고 git add·commit·push한다.
