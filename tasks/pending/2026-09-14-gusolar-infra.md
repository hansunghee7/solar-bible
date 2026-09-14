## 발주: 탐 → 구솔라

status: QUEUED
받는 이: 구솔라

## 정정(2026-09-14, 탐): 파일 충돌 났으면 리베이스 그만두고 이걸로

`tasks/done/2026-09-14-infra-survey.md`는 신솔라가 이미 완료·push해서
원격에 올라가 있다. 같은 파일을 구솔라도 고치라고 시킨 게 탐의 설계
실수였다 - 병합 충돌이 난다. **리베이스나 충돌 해결을 더 시도하지
말고, 지금 하던 건 중단해라.**

## 작업 (새 파일에 쓴다)

`tasks/done/2026-09-14-infra-survey.md`를 건드리지 말고, 대신 **새
파일** `tasks/done/2026-09-14-gusolar-infra-result.md`를 만들어 아래
항목을 조사해서 적는다: 구PC의 CPU·RAM·GPU·SSD/HDD 용량, 텔레그램 봇
연동 여부(토큰 값은 절대 쓰지 않는다), Wake-on-LAN 설정 여부(예/아니오만,
MAC·IP는 절대 쓰지 않는다 - 이 저장소는 공개다).

## 완료 기준

`tasks/done/2026-09-14-gusolar-infra-result.md`(새 파일)에 조사 결과를
적고 git add·commit·push까지 한다. 기존 `2026-09-14-infra-survey.md`는
건드리지 않는다(충돌 위험). 솔라바이블 §3에 따라 중간에 멈추면 그때까지
한 것만이라도 저장한다.
