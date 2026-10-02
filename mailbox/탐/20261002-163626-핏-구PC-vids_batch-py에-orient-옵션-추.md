# 구PC vids_batch.py에 --orient 옵션 추가(롱폼 가로, 핏 10/2)

받는이: 탐
보낸이: 핏
시각: 2026-10-02 16:36:26
긴급: 아니오

사장님 롱폼 1호 대본 OK로 가로 생성이 필요해 구PC ~/workshop/vids_batch.py를 고쳤습니다(백업 vids_batch.py.bak1002b). --orient portrait|landscape(기본 portrait, 기존 동작 그대로): 첫 화면 '세로 동영상 만들기' 대신 '가로 동영상 만들기'(구PC 9226에서 버튼 이름 실측), 설정 판정 단어도 세로/가로로. factory_runner.py는 job.json orient=landscape면 Vids에 --orient, Flow에 --ratio 16:9 전달(shorts-lab 4d96e7d, 구PC 반영, 백업 factory_runner.py.bak1002c). 저장소 원본(scripts/ops/goosolar/workshop/vids_batch.py) 동기화는 탐이 해 주세요. 차이는 구PC에서 diff vids_batch.py.bak1002b vids_batch.py.
