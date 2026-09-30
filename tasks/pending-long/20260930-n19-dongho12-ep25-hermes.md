# 동호 1.2 음성 생성 ep25 헤르메스 실행 확인 (핏 -> 헤르메스)

핏이 같은 편(ep25)으로 이미 한 번 돌려 성공했다(81.8초, 16분). 이번엔 헤르메스가 같은 명령으로 돌려도 같은 증거가 나오는지 확인하는 실행이다. 청취 판정은 하지 않는다.

## 할 일 (한 줄 실행)
`C:\work\shorts-lab\pilot-shorts2` 디렉터리에서 아래 한 줄을 그대로 실행해줘. 다른 GPU 작업이 없는 상태에서 혼자 돌린다(병렬 실행 금지).

```
tts-env\Scripts\python.exe dongho12_build.py C:\work\shorts-lab\channels\mysterious-apt\episodes\ep25-modular-22f C:\work\_voice_eval\runs\ep25-modular-22f_1.2_0930_hermes
```

## 완료 확인 기준 (보이스메이킹_헤르메스_실행서.md §2-1 성공 증거)
- 마지막 줄 `완료 <mp3경로> <초>초 | 덩어리 N개, 강조 M, 재생성 K`
- `<출력폴더>\ep25-modular-22f_동호1.2.mp3` 존재, 길이 약 66~123초(기대 94.3초의 ±30%)
- `report.json`이 있고 덩어리 수가 N과 같음
- 로그에 `Traceback` 없음
- 시작·종료 시각과 걸린 분, 실행 중 `nvidia-smi` 1회 점유 기록을 결과에 남길 것

## 실패 시
같은 명령 최대 3회. `CUDA out of memory`면 다른 GPU 작업이 끝난 뒤 재시도. 3회 실패면 로그 마지막 40줄을 붙여 보고.

## 위임 금지 사항 없음
로컬 파일 생성만, 원본은 안 건드림.
