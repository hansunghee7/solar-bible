# 20261008-tam-exp1-state-maker - 수신 확인

## 메타
- 수신 시각: 2026-10-08T20:48:36
- 레인: pending

## 의뢰(받은 그대로)

# 실험 E1 만드는 쪽: 구PC 헤르메스 읽기 전용 점검 (STATE.md 단계 기록) (로컬 탐 -> 타미)

받는이: 타미
보낸이: 로컬 탐 (2026-10-08, 사장님 지시: 헤르메스 고수 운용법 가설 ① STATE.md 단계 기록 + ② 만드는 세션과 검증 세션 분리를 타미에게 실험)
성격: 읽기 전용 점검이다. 설치·삭제·등록 금지. 아래 4단계를 순서대로 하고, **한 단계가 끝날 때마다 즉시** `reports/exp1-state.md` 맨 아래에 한 줄을 덧붙인다(형식 고정): `STEP <번호> DONE <UTC 시각> <한 줄 결과>`. 이미 같은 번호의 DONE 줄이 있으면 그 단계는 다시 하지 말고 다음 단계로 간다(반복 실행에도 안전하게).
실패한 단계는 `STEP <번호> FAIL <UTC 시각> <명령 출력 한 줄>` 을 쓰고 멈춘다(설명을 길게 쓰지 않는다).

단계 (구PC에서 ssh로 실행, 환경 `export HERMES_HOME=~/.hermes-ops PATH=$HOME/.local/bin:$PATH`):
1. `hermes --version | head -1`
2. `ls $HERMES_HOME | wc -l`
3. `free -m | sed -n 2p | awk '{print $7}'` (가용 MB)
4. `pgrep -fc telegram_agent.py`

끝나면: 결과 문서에는 STATE 파일 마지막 4줄만 붙이고 다른 설명은 쓰지 않는다. 이 파일을 tasks/done/으로 옮긴다. 검증은 다른 세션이 아니라 스크립트(`tasks/assets/tami_exp_check.sh`)가 따로 한다. 너는 검증하지 않는다.
