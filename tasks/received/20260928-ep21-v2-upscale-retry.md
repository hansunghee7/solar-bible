# 20260928-ep21-v2-upscale-retry - 수신 확인

## 메타
- 수신 시각: 2026-09-28T00:41:35
- 레인: pending-long

## 의뢰(받은 그대로)

# ep21(부동산딜레마) v2 업스케일 재시도 (핏 -> 헤르메스)

이전 시도(`20260927-ep21-v2-assemble-retry`)에서 조립(360p)은 성공했는데, 업스케일
도중 GPU VRAM이 다른 프로세스(ollama 로컬 모델, 20GB 점유)에 눌려 52분+ 지나도 안
끝나서 중단시켰다. 원인(OLLAMA_KEEP_ALIVE=-1) 확인·수정 완료, 지금 GPU는 깨끗하다
(`nvidia-smi` 기준 1.2GB만 사용 중). 360p는 재사용하고 업스케일부터 다시 돌리면 된다.

## 할 일 (한 줄 실행)
`C:\work\shorts-lab` 디렉터리에서 아래 한 줄을 그대로 실행해줘(이전과 완전히 동일한
명령, 360p가 이미 있으니 조립은 건너뛰고 업스케일부터 자동으로 이어감. 깨진 1080p
파일은 이미 지워뒀음):

```
python tools\sheet\build_final.py "D:\Downloads\AI숏폼 제작\ep21. 부동산딜레마\clips_v2" "channels\mysterious-apt\episodes\ep21-buy-dilemma\04-scenes\timing_scenes.json" "channels\mysterious-apt\episodes\ep21-buy-dilemma\narration.mp3" "channels\mysterious-apt\episodes\ep21-buy-dilemma\05-assemble\captions.srt" "D:\Downloads\AI숏폼 제작\ep21. 부동산딜레마\편집본_v2" 부동산딜레마_v2
```

## 요청(중요, 이전엔 안 받았던 것)
- **시작 시각과 종료 시각을 결과에 반드시 남겨줘**(실측 기준이 없어서 이번이 처음
  재보는 것 — 다음부턴 이 값으로 예상시간을 안내할 수 있게).
- 중간에 `nvidia-smi`로 GPU 점유율 1회 정도 확인해서 같이 남겨주면 좋음(정상적으로
  GPU를 쓰고 있는지 참고용).

## 완료 확인 기준
- `편집본_v2\부동산딜레마_v2_자막.mp4` 생성 확인(경로+파일크기+ffprobe 해상도·길이).
- 길이가 narration.mp3(124.6초)와 비슷한 범위(±5초)인지 확인.
- 시작~종료 소요시간을 분 단위로 명시.
- 실패하면 stderr 원문 그대로, 같은 에러 3회 반복 시 재시도 중단하고 실패 보고.

## 위임 금지 사항 없음
로컬 파일 조립+GPU 업스케일, 원본은 안 건드림. 이번엔 GPU도 깨끗한 상태에서 시작.
