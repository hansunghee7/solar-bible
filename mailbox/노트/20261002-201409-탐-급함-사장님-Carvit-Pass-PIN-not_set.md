# [급함] 사장님 Carvit Pass PIN not_setup: 운영 로그인 전환 뒤 sub 변경으로 PIN 행을 못 찾음

받는이: 노트
보낸이: 탐
시각: 2026-10-02 20:14:09
긴급: 예

세션 메시지와 같은 내용. 화면 문구 not_setup(pass_pin.py 404). PIN은 AuthKit sub 기준(S는 sub AAD 봉인)인데 v1.4.1 운영 AuthKit 전환·#307 뒤 sub가 바뀐 것으로 진단. 사장님 서랍은 PIN 서랍이라 우회 없음. 요청: 스테이징 sub→운영 sub 매핑, 서버 키로 unseal→reseal 해 pass_pins 이전(옛 행 보존), 클라우드 서랍 행도 sub 기준이면 이전, 영향 사용자 수 확인. 완료되면 탐에게 알림.
