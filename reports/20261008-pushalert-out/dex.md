## 1. 설계안의 결함·위험

- **수신 후 저장 전에 2xx를 반환하면 유실될 수 있습니다.** Tally는 10초 안에 2xx를 받지 못하면 정해진 간격으로 재시도하므로, 서명 검증 후 저장소 push나 큐 적재가 확인된 뒤 응답해야 합니다. [Tally 웹훅 재시도 안내](https://tally.so/help/webhooks)
- **응답 원문을 PR 댓글에 넣으면 폼 내용이 세션 프롬프트로 유입됩니다.** 민감정보·악성 지시문 노출 위험이 있으니, 댓글에는 제출 ID와 안전한 요약만 두고 원문은 접근을 제한해 저장하는 편이 낫습니다. (위험 분석)
- **저장소 push는 경합·덮어쓰기·토큰 권한 문제가 있습니다.** 동시 제출 시 파일 경로와 커밋 충돌을 고려하고, GitHub 토큰은 필요한 저장소와 권한만 허용해야 합니다. [GitHub 파일 API](https://docs.github.com/en/rest/repos/contents)
- **중복 방지는 원자적이어야 합니다.** “확인 후 기록” 사이에 동시 재시도가 끼면 중복 처리될 수 있고, 처리 기록을 너무 빨리 지우면 늦은 재시도도 중복됩니다. Tally가 고정된 이벤트 ID를 재시도마다 유지하는지는 확인하지 못했습니다.
- **GitHub Actions 토큰으로 만든 일반 push/댓글은 후속 워크플로를 깨우지 않을 수 있습니다.** `GITHUB_[민감어 줄임] 이벤트는 기본적으로 새 워크플로를 유발하지 않으며 `repository_dispatch` 등 예외가 있습니다. [GitHub 문서](https://docs.github.com/en/actions/concepts/security/github_[민감어 줄임]

## 2. 더 단순하거나 싼 대안

- **Tally에서 GitHub 이벤트로 직접 변환하는 기능은 확인하지 못했습니다.** Tally는 사용자 지정 헤더는 지원하지만, 본문을 GitHub API의 `event_type`/`client_payload` 형식으로 재구성하거나 GitHub API 인증을 동적으로 붙이는 기능은 문서에서 확인되지 않습니다. [Tally 웹훅](https://tally.so/help/webhooks) · [GitHub `repository_dispatch`](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- 변환기는 GCP를 이미 쓰고 있다면 **Cloud Run 함수 하나**로 서명 확인, ID 기반 중복 처리, `repository_dispatch` 호출만 하는 구성이 단순합니다. dispatch에는 `Contents: write` 권한 토큰이 필요합니다. [GitHub API 권한 요건](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- 저장소가 기록의 정본이어야 한다면, 워크플로가 알림 댓글을 남기는 구조는 합리적입니다. 다만 동작 검증 전에는 **댓글 알림을 유일한 전달 경로로 보지 말고** 제출 파일/이벤트 기록도 남기세요.

## 3. 푸시 실험 프로토콜의 허점

- 조건별 1회 관측으로는 재현성과 세션 상태별 차이를 판단하기 어렵습니다. 세 상태 각각에서 여러 차례, 시간대를 달리해 측정하고 **중앙값·최댓값·누락률**을 기록하세요.
- 제출·워크플로·댓글·세션 수신 시각을 각각 기록해야 지연 구간을 분리할 수 있습니다. 사람이 알림을 묻거나 세션이 API를 조회하면 해당 회차는 오염으로 처리하세요.
- “재전송 중복 알림 0”은 재시도 간격과 처리 기록 보존 기간을 정해야 검증 가능합니다. 서명 오류 거부는 한 번이 아니라 변형된 서명과 본문으로 반복하고, **2xx가 아닌 응답**인지 확인하세요. 생존 세션 60초 기준은 제품이 보장하는 SLA가 아니라 실험 목표로 해석해야 합니다.

## 4. 로컬 세션을 깨우는 가장 단순한 방법

Windows에서 실행되는 작은 **Pub/Sub StreamingPull 수신기**를 세션 실행과 함께 띄우고, 메시지를 받으면 로컬 세션의 지원되는 입력 경로로 알림을 전달하는 방식을 권합니다. 수신기는 재연결·ack를 맡기고, 중복이 허용되지 않는 처리는 제출 ID로 별도 멱등성을 보장해야 합니다. Pub/Sub는 낮은 지연을 위해 StreamingPull을 권하지만, 전달은 재전달될 수 있습니다. [StreamingPull 문서](https://cloud.google.com/pubsub/docs/pull) · [중복/ack 설명](https://cloud.google.com/pubsub/docs/monitoring)

## 5. 봇 댓글만 알림이 온 현상

- GitHub 웹훅의 일반 동작과 클라우드 세션의 구독 전달은 별개입니다. GitHub에는 댓글 이벤트·작성자 정보가 있지만, 이것만으로 해당 세션 호스트가 사람 작성 댓글을 필터링한다고 결론낼 수 없습니다. [GitHub 이벤트 문서](https://docs.github.com/en/webhooks/webhook-events-and-payloads#issue_comment)
- 현재 데이터는 작성자별 1건뿐이므로 **계정 필터링은 가설**입니다. Claude Code 클라우드 세션 구독의 작성자 필터 규칙이나 안정성 보장은 공개 문서에서 확인하지 못했습니다.
- 따라서 봇 계정 댓글 알림에 의존하지 말고, `repository_dispatch`/워크플로 경로의 반복 실험으로 동작을 확인하세요. 제품 업데이트에 따른 변경 위험도 문서로 확인할 수 없습니다.