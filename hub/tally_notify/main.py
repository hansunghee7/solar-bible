"""폼(Tally) 응답 알림 변환 함수 (탐 클라우드 2026-10-08, 사장님 결정: 알림벨 달기 + 기준선도 같이 달기).

하는 일: 폼에 응답이 제출되면 Tally가 이 함수를 부른다 -> 서명을 확인하고 -> 저장소에 "알림 파일"을 한 개 올린다.
 - 푸시 모드(MODE=push): notify/ 아래에 올린다. 저장소의 자동 실행(notify-inbox.yml)이 수신함 PR에 봇 댓글을 달고, 그 PR을 구독한 세션이 깨어난다.
 - 조용한 모드(MODE=silent): notify-silent/ 아래에 올린다. 자동 실행이 반응하지 않아 알림이 오지 않는다(기준선 측정용: 같은 경로, 벨만 뺀 것).
알림 파일에는 응답 내용을 쓰지 않는다(공개 저장소이고 개인정보가 들어올 수 있다). 폼 이름, 제출 id, 시각 3개(제출 T0, 함수 수신 T1, 파일 기록 T2)만 쓴다.
중복: 같은 제출 id로 다시 오면(재시도) 이미 있는 파일이라 새로 만들지 않고 200을 돌려준다.
다른 회사의 에이전트 셋업에도 같은 구조를 쓰도록 폼 종류, 저장소, 모드는 환경변수로 받는다.

환경변수: GH_TOKEN(저장소 쓰기 전용 제한 토큰, 비밀 금고에서 주입), TALLY_SIGNING_SECRET(서명 비밀, 비밀 금고에서 주입), REPO, MODE.
"""
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request

REPO = os.environ.get("REPO", "hansunghee7/solar-bible")
MODE = os.environ.get("MODE", "push")  # push | silent
BRANCH = os.environ.get("BRANCH", "main")


def _verify(raw: bytes, signature: str) -> bool:
    secret = os.environ.get("TALLY_SIGNING_SECRET", "")
    if not secret:
        return False  # 서명 비밀이 없으면 받지 않는다(가짜 알림 방지)
    candidates = [raw]
    try:  # Tally 문서 예시는 파싱한 JSON을 다시 직렬화해 서명하므로 그 형태도 허용
        candidates.append(json.dumps(json.loads(raw), separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    except Exception:
        pass
    for body in candidates:
        expected = base64.b64encode(hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()).decode("ascii")
        if hmac.compare_digest(expected, signature or ""):
            return True
    return False


def _put_file(path: str, text: str, message: str):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    body = json.dumps({
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "branch": BRANCH,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="PUT", headers={
        "Authorization": "Bearer " + os.environ["GH_TOKEN"],
        "Accept": "application/vnd.github+json",
        "User-Agent": "tally-notify-hub",
    })
    with urllib.request.urlopen(req, timeout=8) as r:
        return r.status


def handler(request):
    t1 = time.time()
    raw = request.get_data()
    if not _verify(raw, request.headers.get("Tally-Signature", "")):
        return ("서명 불일치", 401)
    try:
        event = json.loads(raw)
    except Exception:
        return ("형식 오류", 400)
    if event.get("eventType") != "FORM_RESPONSE":
        return ("무시(응답 이벤트 아님)", 200)
    data = event.get("data") or {}
    form_id = str(data.get("formId", "unknown"))
    sub_id = str(data.get("submissionId") or data.get("responseId") or event.get("eventId", "unknown"))
    t0 = data.get("createdAt") or event.get("createdAt") or ""
    folder = "notify" if MODE == "push" else "notify-silent"
    path = f"{folder}/tally-{form_id}-{sub_id}.md"
    t2 = time.time()
    text = (
        f"폼 응답 도착(모드 {MODE})\n"
        f"- 폼: {data.get('formName', '')} ({form_id})\n"
        f"- 제출 id: {sub_id}\n"
        f"- T0 제출 시각(폼 서비스): {t0}\n"
        f"- T1 함수 수신 시각: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t1))}\n"
        f"- T2 파일 기록 시각: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t2))}\n"
    )
    try:
        _put_file(path, text, f"notify: tally 응답 {sub_id[:8]} ({MODE})")
    except urllib.error.HTTPError as e:
        if e.code == 422:  # 이미 있는 파일 = 재시도 중복
            return ("중복(이미 기록됨)", 200)
        return (f"기록 실패 {e.code}", 502)  # 2xx가 아니면 Tally가 재시도한다
    return ("ok", 200)
