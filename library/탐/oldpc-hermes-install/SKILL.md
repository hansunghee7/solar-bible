---
name: oldpc-hermes-install
description: 구PC(goosolar, Linux)에 헤르메스를 별도 프로필 ~/.hermes-ops 로 설치한다. 기존 ~/hermes-agent는 건드리지 않는다.
---
# 구PC 헤르메스 설치 (검증된 닫힌 절차)
- 실행: `ssh goosolar 'bash -s' < run.sh` (약 4분, sudo 불필요, 크론·서비스 등록 없음)
- 검증: `bash verify.sh` → 마지막 줄 `VERIFY PASS`
- 증거: evidence.md (2026-10-08 실행 출력, v0.21.5)
- 주의: 설치기에 sudo 호출 줄이 있으나 이번 실행에서는 요구되지 않았다. 요구되면 멈추고 보고한다.
- 정본: 이 폴더. 프로세스표 공정 카드에는 이 폴더 경로만 적는다(복사 금지).
