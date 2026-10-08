# 텔레그램 탐 컨펌방에 설문 시험 링크 1건 발송 (탐 -> 헤르메스)

받는 이: 헤르메스
보낸 이: 탐 클라우드 (2026-10-08, 사장님 지시 "헤르메스(타미)를 통해서 대행 발주")
성격: 사장님 본인 텔레그램 컨펌방(탐)으로 글 1건 발송. 외부인에게 가는 게 아님. 클라우드 세션에는 텔레그램 봇 토큰이 없어 대행을 맡긴다.

손대지 말 것: 저장소 파일 수정·삭제 금지, 키·토큰 값 출력 금지. 아래 명령 한 번만 실행(같은 글을 두 번 보내지 않는다. 실패했을 때만 재시도). 결과 폴더 C:/work/_ops/tam 이 없으면 만든다.

실행할 명령 (한 줄):
```
mkdir -p C:/work/_ops/tam && cd C:/work/hansunghee7.github.io && PYTHONIOENCODING=utf-8 python scripts/ops/tg_boss.py text "[시험] 지투시그마 파일럿 사전 질문 폼입니다. 폰에서 열어 시험 제출 한 번 부탁드립니다(대표님께는 아직 안 보냈습니다): https://tally.so/r/J9NEZz" --persona 탐 > C:/work/_ops/tam/tg_send_1008.txt 2>&1; echo "exit=$?" >> C:/work/_ops/tam/tg_send_1008.txt
```

성공 기준: 결과 파일 C:/work/_ops/tam/tg_send_1008.txt 의 마지막 줄이 exit=0 이고 오류 문구(Traceback, 401, 403 등)가 없다. 파일 내용에 토큰 값이 보이면 그 줄을 지우고 보고한다.

실패 시: 보내지지 않은 것이 확실할 때만 같은 명령을 최대 3회 재시도하고, 그래도 안 되면 오류 마지막 5줄(토큰 값 제외)을 C:/work/_ops/tam/error_tg_send.txt 에 적고 멈춘다.
끝나면: 이 파일을 tasks/done/ 으로 옮기고 탐 우편함에 '완료·파일 위치 또는 실패 사유' 한 줄로 회신한다.
