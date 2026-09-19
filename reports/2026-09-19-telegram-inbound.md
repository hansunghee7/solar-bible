# 텔레그램 수신 방향 조사 (읽기 전용)

**조사 일시**: 2026-09-19  
**조사 범위**: (1) `C:/Users/PC/AppData/Local/hermes/hermes-agent/website/docs/user-guide/messaging/webhooks.md`, (2) `C:/Users/PC/AppData/Local/hermes/hermes-agent/skills/autonomous-ai-agents/hermes-agent/references/configuration.md`, (3) https://hermes-agent.nousresearch.com/docs/user-guide/messaging  
**목적**: 사장님이 텔레그램으로 보낸 글을 헤르메스가 받았을 때 그 내용을 우편함 파일(`mailbox/<받는이>/`)로 넘기는 방법이 있는지 조사 ( 만들기는 조사만)

---

## 조사 결과: 없음

세 근거 문서 어디에도 **인바운드 텔레그램 메시지가 도착했을 때 이를 로컬 우편함 파일(`mailbox/<받는이>/`)로 자동 기록하는 기능이나 설정 방법은 명시되어 있지 않다.**

### 근거 1: webhooks.md
- 웹훅 기능은 **외부 서비스(GitHub, GitLab 등)에서 헤르메스로 이벤트를 보내는** outbound/inbound 혼합 경로다.
- 텔레그램은 이 문서에서 **응답 배달(deliver) 대상**으로만 등장하며, 텔레그램으로부터 받은 메시지를 우편함 파일로 기록하는 경로는 없다.
- `deliver: telegram`은 에이전트 처리 결과를 텔레그램으로 보내는 설정이지, 텔레그램 수신 내용을 파일로 쓰는 설정이 아니다.

### 근거 2: configuration.md
- 구성 항목 중 텔레그램 수신 내용을 우편함 파일로 넘기는 설정은 존재하지 않는다.
- `platforms.telegram` 관련 설정도 이 파일에는 구체적 수신 처리 로직이 없으며, 도구셋·음성(TTS/STT) 설정 위주일 뿐 메시지→파일 라우팅은 언급되지 않는다.

### 근거 3: 공식 messaging 문서 (online)
- 메시징 게이트웨이 문서는 텔레그램을 포함한 각 플랫폼의 **수신→세션 처리→응답 발송** 흐름을 설명한다.
- 텔레그램 메시지는 게이트웨이 세션으로 들어와 AI 에이전트 처리 대상이 되지만, 그 내용을 자동으로 `mailbox/<받는이>/` 같은 로컬 파일 구조로 기록하는 기능·훅·설정 방법은 문서상 확인되지 않는다.
- 텔레그램 발송(`hermes send --to telegram` 등)은 언급되나, 수신 방향의 파일 기록은 없다.

---

## 판단

- **현재 문서 근거로 확인되는 방법: 없음.**
- 텔레그램 수신 내용을 우편함 파일로 남기려면, 현재 문서만으로는 표준 기능이라고 말할 수 없다.
- 가능한 방향(실제 존재 여부는 별도 확인 필요): 게이트웨이 훅(hook)·스크립트 플러그인·커스텀 이벤트 처리 등으로 구현할 여지는 있으나, 이 조사 범위(지정 3개 문서)에서는 그 방법이 명시적으로 확인되지 않았다.
- 위험: 이런 자동화 경로를 만들면 텔레그램 수신→파일 기록 사이의 지연·인허가·토큰 노출·파일 경합 같은 운영 리스크가 생길 수 있으므로, 도입 여부는 탐과 사장님이 별도 판단한다.

---

## 검증

- [x] webhooks.md 전체 검토 완료 — inbound 텔레그램→우편함 파일 경로 없음
- [x] configuration.md 전체 검토 완료 — 해당 설정 없음
- [x] 공식 messaging 문서 검토 완료 — 해당 기능 명시 없음
- [x] 토큰·키·IP 미포함 확인

**보고서 경로**: `C:/work/solar-bible/reports/2026-09-19-telegram-inbound.md`
