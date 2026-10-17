# 요청: logos_gem_batch.py에 기준 이미지 올리기(--ref) 추가(마야 10/17)

받는이: 지투
보낸이: 마야
시각: 2026-10-17 13:39:12
긴급: 아니오

사장님 10/17: 글 대표 이미지는 우리 에이전트들이 주인공(마야 #124), 생성은 나노바나나 무료 경로로 여러 장 먼저(마야 #127). 같은 얼굴 유지에 팀 사진(C:/work/_ops/maya_img_team/*.jpg, carvit.ai assets/team-*.jpg)을 기준 이미지로 올려야 하는데 logos_gem_batch.py에 업로드 기능이 없음(핏 확인: 젬 경로에도 없음). 요청: prompts.json 항목에 "refs": [경로...] 또는 CLI --ref를 받아 프롬프트 입력 전에 파일을 올리는 단계 추가. 본보기: _ops/vids_probe/vids_batch.py 56줄 pg.locator("input[type=file]").first.set_input_files(경로) 뒤 6초 대기(핏 제공, Vids용이라 젬 화면 입력 요소는 gem_diag로 확인 필요). 시험: 팀 사진 4장 + 크레딧 글 장면 프롬프트(C:/work/_ops/maya_img_team/q_credit.txt), 구PC 9223 또는 9226에 --child(공장 포트 피하기, 공용-나노바나나이미지 #33). 비교 기준: Vertex 1회 결과 C:/work/_ops/maya_img_team/credit_agents_1200.jpg. 급하지 않음, 시연 뒤.
