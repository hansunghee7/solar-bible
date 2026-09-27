# 20260927-ep21-v2-assemble-retry - 수신 확인

## 메타
- 수신 시각: 2026-09-27T23:16:26
- 레인: pending-long

## 의뢰(받은 그대로)

# ep21(부동산딜레마) v2 조립 재시도 (핏 -> 헤르메스)

이전 의뢰(`20260927-ep21-v2-assemble`, `reports/20260927-ep21-v2-assemble-result.md`)가
씬24 없음으로 실패했다. 원인 확인함: 내가 timing 파일을 잘못 지정했다 —
`03-align/timing.json`은 문장 단위 정렬본(45개 항목)이고, 클립은 23개(씬01~23)뿐이라
assembler가 24번째를 요구해서 실패한 것. **씬 단위로 이미 버킷팅된
`04-scenes/timing_scenes.json`(23개 항목, 클립 개수와 정확히 일치)을 대신 써야 한다.**

클립 폴더·나레이션·자막은 이전과 동일(전부 그대로 유효, 다시 확인할 필요 없음).

## 할 일 (한 줄 실행)
`C:\work\shorts-lab` 디렉터리에서 아래 한 줄을 그대로 실행해줘(timing 인자만
`03-align\timing.json` → `04-scenes\timing_scenes.json`로 바뀐 것 외엔 이전과 동일):

```
python tools\sheet\build_final.py "D:\Downloads\AI숏폼 제작\ep21. 부동산딜레마\clips_v2" "channels\mysterious-apt\episodes\ep21-buy-dilemma\04-scenes\timing_scenes.json" "channels\mysterious-apt\episodes\ep21-buy-dilemma\narration.mp3" "channels\mysterious-apt\episodes\ep21-buy-dilemma\05-assemble\captions.srt" "D:\Downloads\AI숏폼 제작\ep21. 부동산딜레마\편집본_v2" 부동산딜레마_v2
```

## 완료 확인 기준
- `편집본_v2\부동산딜레마_v2_자막.mp4` 파일이 실제로 생성됐는지(경로+파일크기+ffprobe로 해상도·길이) 확인.
- 길이가 narration.mp3(124.6초)와 비슷한 범위(±5초)인지 확인.
- 여전히 실패하면 stderr 원문 그대로 남기고(이번엔 원인이 timing-clip 개수 불일치가
  아니므로 다른 문제일 가능성), 같은 에러가 3회 반복되면 재시도 그만하고 실패로 보고.

## 위임 금지 사항 없음
이전과 동일(로컬 파일 조립+GPU 업스케일, 원본은 안 건드림).
