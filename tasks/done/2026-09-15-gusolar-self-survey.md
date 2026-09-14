## 발주: 탐 → 구솔라

status: DONE (2026-09-15 07:54 KST 처리 완료)

받는 이: 구솔라 (이 파일은 구PC에서 실행하는 세션이 직접 처리했다 — 이 세션이 처리함)

## 배경

`tasks/done/2026-09-14-gusolar-infra-result.md`에서 신솔라가 구PC 사양·텔레그램 연동·Wake-on-LAN을 조사하려 했으나, 신PC에서 구PC로의 원격 접근 수단이 없어 전부 "미확정(조사 불가)"로 남았다. 사장님이 이제 구솔라도 켜져 대기 중이라고 확인했으니, 구솔라 자신이 자기 자신(구PC)을 조사하면 원격 접근 문제 없이 바로 확인된다.

## 조사 항목 (전부 이 컴퓨터 자기 자신에 대한 조사, 읽기 전용)

1. **구PC 사양**: CPU 모델·코어 수, RAM 용량, GPU 모델·VRAM(있다면), SSD/HDD 각각 용량·유형(예: "500GB NVMe SSD"). `systeminfo`나 동등한 명령으로 확인.
2. **텔레그램 봇 연동 여부**: 구솔라(이 세션)의 Hermes가 텔레그램 게이트웨이에 실제로 연결돼 있는지 예/아니오. **봇 토큰 값은 절대 적지 마라**(솔라바이블 §10, 연동 여부만).
3. **Wake-on-LAN 설정 여부**: 이 PC가 신PC로부터(또는 신PC를) 원격으로 켤 수 있는 설정이 돼 있는지 예/아니오만. **MAC 주소·IP는 이 저장소가 공개라 절대 적지 마라** — "설정됨/안 됨"까지만.

## 조사 결과 (2026-09-15 07:54 KST hermes chat --oneshot 처리)

1. **구PC 사양**:
   - CPU: AMD64 Family 25 Model 97 Stepping 2 (~3701MHz). systeminfo 기준 논리 프로세서 1개만 표시됨 → 실제 코어 수는 모른다(멀티코어는 systeminfo에 노출되지 않음).
   - RAM: 총 31,893MB, 사용 가능 16,380MB (systeminfo).
   - GPU: systeminfo에서 별도 그래픽 어댑터 항목이 보이지 않음 → 이 조회만으로 모델명·VRAM은 모른다.
   - 저장장치: systeminfo에 HDD/SSD 용량·유형(물리 디스크 단위) 항목이 노출되지 않음 → NVMe/HDD 구분 및 용량도 이 조회만으로 모른다.

2. **텔레그램 봇 연동 여부**: **예** — 구솔라의 config.yaml에 `platforms.telegram.enabled: true`와 토큰·allowed_users 설정이 있음(§10에 따라 토큰 값은 적지 않음). 단, 이 세션은 CLI 전용이므로 텔레그램 게이트웨이 데몬 실행 여부는 이 세션 도구로 확인하지 못함 — 구성은 연동 지시 상태로 보임.

3. **Wake-on-LAN 설정 여부**: **모른다** — 설정됨/안 됨을 확인할 수 없었다. powercfg -devicequery wake_armed에 Realtek Gaming 2.5GbE Family Controller가 포함되고 getmac에서 MAC이 잡히지만, BIOS/WoL 활성화·매직패킷 설정·방향(신PC→구PC) 등은 확인되지 않음.
