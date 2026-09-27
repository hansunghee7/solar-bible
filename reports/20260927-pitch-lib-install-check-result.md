# 20260927-pitch-lib-install-check - 처리 결과

## 의뢰(원본)

# N21 피치 라이브러리 설치·검증 (핏 -> 헤르메스)

## 배경
동호 1.2(말맛 층) 강조 표현 실험(N21)에서 볼륨 DSP만으로는 말맛이 안 산다는
결론이 났고, 다음 시도로 피치 변동폭도 같이 넓혀야 한다. tts-env에는 현재
librosa만 있고 피치 전용 라이브러리(pyworld, praat-parselmouth)가 없다.

## 할 일 (한 줄 실행)
아래 한 줄만 그대로 실행해줘. 스크립트가 pip install부터 검증까지 전부 처리한다.

```
C:\work\shorts-lab\pilot-shorts2\tts-env\Scripts\python.exe C:\work\shorts-lab\pilot-shorts2\pitch_env_check.py
```

(작업 디렉터리는 `C:\work\shorts-lab\pilot-shorts2` 로 cd 한 뒤 실행해도 되고,
스크립트 안에서 `voice_ref/dongho_1_0_anchor.wav`를 상대경로로 읽으니 cd 안 하면
경로 에러가 날 수 있다 — cd 후 실행 권장.)

## 완료 확인 기준
- 표준출력 전체를 그대로 `reports/`에 남겨줘(요약하지 말고 원문 그대로).
- pyworld/parselmouth 각각 pip install 성공/실패, 성공했다면 피치 범위(반음) 출력값,
  `pitch_env_check_output.wav` 파일이 실제로 생성됐는지(경로+파일크기)까지 확인.
- 둘 다 설치 실패하면 실패 원인(pip 에러 원문)을 그대로 남기고 멈춰도 된다(3회
  재시도 규칙 적용 — 같은 에러가 3회 반복되면 재시도 그만하고 실패로 보고).

## 위임 금지 사항 없음
pip install(로컬 venv, 되돌리기 쉬움) + 파이썬 스크립트 실행뿐이라 안전하고
되돌릴 수 있는 작업이다.

## 결과

완료.

## 결과 요약
- pyworld: pip install 성공 (0.3.5), 피치 범위 21.34 반음 (f0 71.2–244.2 Hz), 재합성 스모크테스트 통과
- praat-parselmouth: pip install 성공 (0.4.7), 피치 범위 31.94 반음 (f0 75.3–476.6 Hz)
- pitch_env_check_output.wav 생성 확인: C:\work\shorts-lab\pilot-shorts2\pitch_env_check_output.wav, 638,684 바이트
- 표준출력 원문: C:\work\shorts-lab\pilot-shorts2\reports\pitch_env_check_output.txt

## 실행 피드백
문제 없음. 지시서는 실행 명령 한 줄 + cd 권장 + 완료 확인 기준 3항이라 그대로 따라가기 쉬웠다. 실제 실행 시 bash가 백슬래시 윈도우 경로를 한 토큰으로 잘못 쪼개서 `C:workshorts-lab...` 형태의 명령 없음 오류가 한 번 났고, 정방향 슬래시(`C:/...`) 경로로 바꿔 재시도해 해결한 것 외에는 막힘 없었다.

## 메타
- 처리 시각: 2026-09-27T22:38:32
- exit code: 0
