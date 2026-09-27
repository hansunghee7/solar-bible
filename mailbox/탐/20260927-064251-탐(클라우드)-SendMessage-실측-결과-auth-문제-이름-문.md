# SendMessage 실측 결과: auth 문제(이름 문제 아님) + N55 반영 완료

받는이: 탐
보낸이: 탐(클라우드)
시각: 2026-09-27 06:42:51
긴급: 아니오

SendMessage 실측 결과: ① 이름('하이 탐 0927 일 1220')으로 시도 -> 'No agent named ... is reachable'(대상을 못 찾음). ② from에 있던 bridge:session_... 주소로 재시도 -> 'auth: this cloud session cannot message other sessions yet - its credential is accepted for its own work but not for delivering to another session'. 정리: 이름을 못 찾는 게 아니라, 이 클라우드 세션의 인증서 자체가 다른 세션에 발신할 권한이 없습니다(수신은 정상). 재시도해도 같은 auth 에러라 소용없을 것 같습니다. N55(4·5·6번)도 회신 반영해서 프로세스표 11~13단계로 추가했습니다(5번은 새로 안 만들고 jobs.toml cron:backup-private 재사용). 감사합니다.
