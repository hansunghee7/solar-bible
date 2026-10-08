#!/usr/bin/env python3
"""교신 대화방 새 댓글 확인기(LLM 호출 전에 돌리는 사전 확인). 새 댓글이 없으면 NONE만 출력하고 끝나서 토큰을 거의 쓰지 않는다.

사용: python chatroom_check.py <소유자/저장소> <PR번호> <내이름> [상태파일]
  - 내 이름이 지명된 댓글(`[누구→내이름 ...]` 또는 `→전체`)과 사람 댓글 중 `중지`로 시작하는 것만 가져온다.
  - 이미 본 댓글 번호는 상태파일에 기록해 다시 보여주지 않는다. 봇이 쓴 `[중계]` 댓글은 건너뛴다.
  - 출력: 새 댓글이 있으면 한 줄에 하나씩 `번호<TAB>작성자<TAB>시각<TAB>본문 앞 300자`, 없으면 NONE.
  - 오류는 숨기지 않고 표준 오류에 출력하고 종료 코드 2로 끝난다(호출부는 이를 '멈춤'으로 처리한다).
필요: GitHub CLI(gh)가 로그인돼 있고 그 저장소를 읽을 수 있어야 한다. 파이썬 표준 라이브러리만 쓴다.
"""
import json, os, re, subprocess, sys


def fetch(repo, pr):
    r = subprocess.run(["gh", "api", f"repos/{repo}/issues/{pr}/comments", "--paginate"],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode != 0:
        raise RuntimeError("gh api 실패: " + r.stderr.strip()[:200])
    txt, i, out = r.stdout.strip(), 0, []
    dec = json.JSONDecoder()
    while i < len(txt):  # --paginate는 페이지마다 JSON 배열을 이어 붙여 출력한다
        arr, j = dec.raw_decode(txt, i)
        out += arr
        i = j
        while i < len(txt) and txt[i].isspace():
            i += 1
    return out


def pick(comments, me, last_id):
    out = []
    for c in comments:
        if c["id"] <= last_id:
            continue
        body = c["body"].strip()
        if c["user"]["login"].endswith("[bot]") or body.startswith("[중계]"):
            continue
        head = body.split("]", 1)[0] if body.startswith("[") else ""
        to_me = ("→" + me) in head or "→전체" in head
        stop = body.startswith("중지") or (head and body.split("]", 1)[1].strip().startswith("중지"))
        if to_me or stop:
            out.append(c)
    return out


def main():
    if len(sys.argv) < 4:
        sys.exit("사용: chatroom_check.py <소유자/저장소> <PR번호> <내이름> [상태파일]")
    repo, pr, me = sys.argv[1:4]
    state = sys.argv[4] if len(sys.argv) > 4 else os.path.expanduser(f"~/.chatroom_{pr}_{me}.state")
    try:
        last = int(open(state).read().strip())
    except Exception:
        last = 0
    try:
        comments = fetch(repo, pr)
    except Exception as e:
        print("확인 실패:", e, file=sys.stderr)
        sys.exit(2)
    new = pick(comments, me, last)
    if comments:
        open(state, "w").write(str(max(c["id"] for c in comments)))  # 못 본 것까지 앞으로 감지하지 않도록 최신 번호까지 기록
    if not new:
        print("NONE")
        return
    for c in new:
        print(f'{c["id"]}\t{c["user"]["login"]}\t{c["created_at"]}\t{c["body"][:300].replace(chr(10), " ")}')


if __name__ == "__main__":
    main()
