<!-- 답한 풀: Vertex 제미나이(GCP 크레딧) -->
### 1. 설계안의 결함 및 놓친 위험 (3줄 이내)
* **자기 이벤트 무한 루프 및 필터링 유실**: 세션이 동일 계정으로 기록/답글을 달 경우 `issue_comment` 트리거가 무한 루프를 일으키거나, 이를 막기 위한 `sender` 조건문 설정 미흡 시 이벤트가 유실될 수 있습니다.
* **비동기 200 OK 처리 미흡 시 중복 재시도**: GCP Cloud Function이 GitHub API 처리 및 댓글 작성을 마칠 때까지 기다리면 Tally 타임아웃(5~10초)으로 인해 동일 제출 건이 중복 재전송됩니다.
* **PR 댓글 누적에 따른 컨텍스트 과부하**: 단일 PR에 댓글이 계속 쌓이면 클라우드 세션 wake 시 읽어야 할 대화 기록이 급증하여 비용과 처리 지연이 증가합니다.
* **출처:** 
  * https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
  * https://tally.so/help/webhooks

---

### 2. 더 단순하거나 더 싼 대안 (3줄 이내)
* **대안**: Tally 웹훅 -> **Cloudflare Worker** -> **GCP Pub/Sub** (또는 세션 직접 호출).
* **이유**: GitHub PR/댓글이라는 불필요한 중간 매개체를 제거하여 레이턴시를 절반 이하로 줄이고, 하루 10만 건 무료 티어(Cloudflare)로 GCP 아티팩트/네트워크 과금 가능성마저 완전 차단합니다.
* **출처:**
  * https://developers.cloudflare.com/workers/platform/pricing/
  * https://cloud.google.com/pubsub/docs/overview

---

### 3. 푸시 실험 프로토콜의 허점 (3줄 이내)
* **표본 수 부족 및 네트워크 지연 미반영**: 표본 10건은 GCP 콜드 스타트나 GitHub API 일시 지연(P99 레이턴시)을 검증하기에 너무 적습니다.
* **작업 중 세션의 인터럽트 검증 누락**: 세션이 작업(Tool Call) 수행 중에 알림이 들어왔을 때, 기존 작업이 취소되는지 아니면 큐에 밀려 60초 통과 기준을 초과하는지 검증 항목이 없습니다.
* **출처:**
  * https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks

---

### 4. 로컬 세션을 깨우는 가장 단순한 방법 (3줄 이내)
* **추천**: GCP Pub/Sub **`StreamingPull`** 감시 스크립트(Python/Node.js 15줄 내외) 백그라운드 실행.
* **이유**: 방화벽 포트 개방 없이 단일 Outbound 443(gRPC) 연결로 100ms 이내 이벤트를 실시간 푸시받으며, 1인 기준 GCP 무료 티어 범위 내에서 완벽히 동작합니다.
* **출처:**
  * https://cloud.google.com/pubsub/docs/pull#streamingpull

---

### 5. 같은 계정 댓글 알림 미수신 시 대안 (3줄 이내)
* **대안**: GitHub Issue 댓글 대신 **`repository_dispatch`** 이벤트를 트리거합니다.
* **이유**: `repository_dispatch`는 토큰 생성자와 관계없이 구독 세션에 별도의 시스템 wake 이벤트를 즉시 발송하므로 댓글 알림 누락 문제를 근본적으로 회피합니다.
* **출처:**
  * https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event