#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08 v2: 설문 도착 알림 설계 리서치(제미나이, 구글 검색 연동) -> 비티·덱스 검토를 차례로 돌린다.
# v2 변경(같은 날): 이미 끝난 단계는 건너뛴다(리서치는 주제당 24시간 1회 규칙이라 다시 돌려도 안전). 결과 파일은 LLM이 문서에 붙이게 하지 않고
# 이 스크립트가 직접 저장소(reports/20261008-pushalert-out/)에 올린다(1차 시도에서 에이전트가 결과를 붙이지 못한 사고 반영).
# 순서를 코드로 못박는다(병렬 없음). 한 단계가 실패해도 다음 단계는 계속하고 결과를 DONE.txt에 남긴다.
# 질문과 카드에는 고객 정보·비밀값·가격·전략을 넣지 않았다. 비티·덱스의 답은 가설이며 채택 판정은 탐이 한다.
set -u
OUT=C:/work/_ops/pushalert
mkdir -p "$OUT"
cd C:/work/hansunghee7.github.io || { echo "저장소 폴더 없음" > "$OUT/DONE.txt"; exit 2; }
done_ok() { [ -f "$1" ] && [ "$(wc -c < "$1")" -gt 500 ]; }   # 500바이트 넘으면 이미 끝난 단계
echo "start $(date '+%F %T')" >> "$OUT/DONE.txt"

# 1) 제미나이 리서치: 질문 5개를 한 번에(vertex_research.py 규칙: 주제당 첫 조사 1회)
cat > "$OUT/q.txt" <<'EOF'
Anthropic의 Claude Code 웹/클라우드 세션(원격 컨테이너에서 도는 코딩 에이전트)이 외부 서비스 이벤트를 폴링 없이 받는 공식 방법에는 무엇이 있나? 웹훅 수신, GitHub 이슈·PR 활동 구독, 예약 작업(루틴)의 API 발동 등의 현황과 제한(서명 인증, 토큰 요구)을 알려 줘.
Tally 폼의 웹훅(Tally-Signature 서명 헤더, 사용자 지정 HTTP 헤더, 재시도 정책)을 받아 GitHub 이슈·PR 댓글이나 repository_dispatch 이벤트로 바꿔 주는 가장 가볍고 싼 방법을 비교해 줘: GCP Cloud Run 또는 Cloud Functions, Cloudflare Workers, GitHub Actions. Tally가 보내는 JSON을 변환 없이 GitHub API에 직접 보낼 수 있는지도 알려 줘.
GitHub에서 PR 활동을 구독하는 에이전트는 같은 GitHub 계정이 단 댓글이나 GitHub App 봇이 단 댓글에도 알림을 받나? 자기 댓글 필터링 여부와 비공개 저장소 지원 여부를 알려 줘.
방화벽 안쪽 Windows PC에서 도는 로컬 세션을 외부 이벤트로 즉시 깨우는 가장 단순한 방법은? 밖으로 나가는 연결 하나로 푸시를 받는 패턴(Pub/Sub 스트리밍 풀, SSE, WebSocket, GitHub 알림 등)을 비교해 줘.
웹훅 기반 알림 파이프라인의 신뢰성 모범 사례를 알려 줘: 중복 제거(idempotency), 재시도 순서, HMAC-SHA256 서명 검증, 개인정보 최소화, 1인 규모에서 과하지 않은 수준.
EOF
if done_ok "$OUT/research.txt"; then
  echo "research skip(이미 있음) bytes=$(wc -c < "$OUT/research.txt")" >> "$OUT/DONE.txt"
else
  PYTHONIOENCODING=utf-8 python scripts/ops/vertex_research.py --topic "푸시 알림 설계 1008" --file "$OUT/q.txt" --common "각 답에 원본 출처 전체 주소를 붙이고 확인되지 않은 것은 확인 불가로 쓴다. 2026년 10월 기준 최신 정보만 쓴다." --out "$OUT/research.json" > "$OUT/research.txt" 2> "$OUT/research.err"
  echo "research rc=$? bytes=$(wc -c < "$OUT/research.txt" 2>/dev/null || echo 0)" >> "$OUT/DONE.txt"
fi

# 2) 검토 카드(비티·덱스 공용)
{
cat <<'EOF'
# 검토 요청: 클라우드 AI 에이전트 세션에 외부 이벤트(설문 제출)를 폴링 없이 알리는 설계 (탐 -> 비티·덱스)

목적: 폼 서비스(Tally)에 응답이 제출되면, 클라우드에서 도는 에이전트 세션이 사람이 묻기 전에 즉시 알게 한다. 규모는 1인 회사 + AI 에이전트들이고, GCP 무료 크레딧을 쓸 수 있다. 과한 설계는 피한다.

## 지금까지 실측한 사실
1. 폼 응답 수신은 된다(에이전트가 API 도구로 읽음). 그러나 에이전트는 물어보기 전까지 몰랐다: 제출 후 약 7~10분 뒤 사람이 물었을 때 알았다(기준선, 폴링도 푸시도 없는 구조).
2. 클라우드 세션 전용 인바운드 웹훅 주소가 있다. 서명 없이 POST하면 401이다. 서명용 비밀은 봉인돼 있어 외부 서버가 쓸 수 없다. 즉 폼 서비스나 우리 서버가 이 주소를 직접 때릴 수 없다.
3. 세션이 GitHub PR을 구독하면 PR 이벤트(댓글, CI, 리뷰, 병합)가 세션 대화에 wake 이벤트로 들어온다. 구독 생성 이벤트는 실제로 쉬는 세션을 깨웠다.
4. 실측(2026-10-08): 사람(저장소 주인) 계정이 PR에 단 댓글은 11분 안에 알림이 오지 않았다. 워크플로 봇(github-actions)이 단 댓글은 파일 push 후 약 12초에 알림이 도착했다. 표본은 각 1건. 즉 작성자가 봇이면 알림이 오고, 같은 계정 댓글은 걸러지는 것으로 보인다.
5. 폼 서비스 웹훅은 무료이며 서명(SHA256) 헤더, 사용자 지정 헤더, 실패 시 재시도(5분, 30분, 1시간, 6시간, 1일)를 지원한다. 그러나 보내는 JSON 형식은 고정이라 GitHub API에 바로 보낼 수는 없어 보인다(미확인).
6. 클라우드 세션은 다른 세션에 메시지를 보낼 권한이 없다(인증 오류). 로컬 세션은 우편함(저장소 파일)을 새 세션을 열 때만 읽는다.

## 현재 설계안
폼 웹훅 -> 변환 함수(서명 검증, 제출 id로 중복 제거) -> 저장소에 파일 push 또는 repository_dispatch -> 저장소 워크플로가 수신함 PR에 봇 댓글 -> 구독 중인 클라우드 세션이 wake. 댓글은 기록이기도 하다(저장소가 우편함 정본). 로컬 세션은 별도 경로가 필요하다(후보: Pub/Sub 스트리밍 풀을 감시 스크립트가 유지).

## 푸시 실험 프로토콜
측정값 = 제출 시각 T0에서 세션이 알림을 받은 시각 T1까지. 측정 구간에 에이전트는 조회·폴링 금지, 사람은 제출을 알리지 않음. 조건 3가지: 세션이 쉬는 중, 작업 중, 세션 종료 후(다음 시작 때 우편함에서 발견). 통과 기준: 살아 있는 세션 60초 이내, 10건 연속 누락 0, 재전송 시 중복 알림 0, 서명이 틀린 요청은 거부.

## 묻는 것 (각 항목 3줄 이내, 근거 출처 주소 포함, 확인 못 한 것은 확인 불가로)
1. 설계안의 결함이나 놓친 위험 5개 이내(보안, 신뢰성, 비용 포함).
2. 더 단순하거나 더 싼 대안이 있나? 있다면 왜 설계안보다 낫나. 특히 Tally 웹훅을 변환 함수 없이 GitHub 이벤트로 바꾸는 길이 있는가.
3. 푸시 실험 프로토콜의 허점(측정 오염, 표본 수, 통과 기준).
4. 로컬 세션을 깨우는 가장 단순한 방법 한 가지 추천.
5. 봇 계정 댓글에만 알림이 오는 현상(자기 계정 필터링)이 실제 제품 동작인지, 의존해도 되는지, 바뀔 위험.
EOF
echo
echo "## 제미나이 리서치 결과(원문 일부, 가설이며 출처 미검증)"
head -c 12000 "$OUT/research.txt" 2>/dev/null
} > "$OUT/card.md"
echo "card bytes=$(wc -c < "$OUT/card.md")" >> "$OUT/DONE.txt"

# 3) 비티 -> 4) 덱스 (차례로, 이미 끝났으면 건너뜀)
if done_ok "$OUT/bt.md"; then echo "bt skip bytes=$(wc -c < "$OUT/bt.md")" >> "$OUT/DONE.txt"; else
  bash scripts/ops/ask_bt.sh "$OUT/card.md" "$OUT/bt.md" > "$OUT/bt.log" 2>&1
  echo "bt rc=$? bytes=$(wc -c < "$OUT/bt.md" 2>/dev/null || echo 0)" >> "$OUT/DONE.txt"
fi
if done_ok "$OUT/dex.md"; then echo "dex skip bytes=$(wc -c < "$OUT/dex.md")" >> "$OUT/DONE.txt"; else
  bash scripts/ops/ask_dex.sh "$OUT/card.md" "$OUT/dex.md" > "$OUT/dex.log" 2>&1
  echo "dex rc=$? bytes=$(wc -c < "$OUT/dex.md" 2>/dev/null || echo 0)" >> "$OUT/DONE.txt"
fi
echo "finished $(date '+%F %T')" >> "$OUT/DONE.txt"

# 5) 결과를 스크립트가 직접 저장소에 게시(탐 클라우드가 읽을 수 있게). 공개 저장소라 설계 조사 내용만 올린다(고객 정보 없음).
PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || { echo "solar-bible 폴더 없음" >> "$OUT/DONE.txt"; cat "$OUT/DONE.txt"; exit 3; }
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
for f in research.txt bt.md dex.md DONE.txt; do [ -f "$OUT/$f" ] && cp "$OUT/$f" "$PUB/$f"; done
echo "푸시 알림 리서치 결과 게시: reports/20261008-pushalert-out/ ($(tr '\n' ';' < "$OUT/DONE.txt" | head -c 300))" > notify/20261008-pushalert-done.md
git add reports/20261008-pushalert-out notify/20261008-pushalert-done.md
git commit -q -m "reports: 푸시 알림 리서치와 비티·덱스 검토 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "publish rc=$?" >> "$OUT/DONE.txt"
cat "$OUT/DONE.txt"
