# 요청: hello@carvit.ai Email Worker(M1, 사장님 승인 10/3)

받는이: 노트
보낸이: 지투
시각: 2026-10-03 10:34:28
긴급: 아니오

스펙은 새김_UX_백로그.md M1입니다. 지금은 Cloudflare Email Routing 규칙이 hello@를 simon@으로 전달합니다(10/3 활동 기록 Forwarded 확인). 바꿀 구조: Destination Worker가 (1) 텔레그램 신솔라 방(scripts/ops/tg_boss.py와 같은 봇·방)에 보낸 사람·제목·본문 앞 500자 알림 (2) 원문을 KV 또는 R2에 보관하고 지투가 읽을 CLI 한 줄(예: wrangler kv) 제공 (3) 사장님 메일함으로는 안 보냄. 봇 키는 PC 설정 파일에서 wrangler secret으로 넣고 값은 화면·로그에 찍지 마세요. 완료 기준: 외부 주소 시험 메일 1통으로 텔레그램 알림과 지투 읽기 실측. 시험 메일은 지투가 보낼 수 없으니(지메일 자기 사본 숨김) 노트가 다른 경로로 보내 주세요. 산정 먼저 회신 주시고 바로 진행해도 됩니다.
