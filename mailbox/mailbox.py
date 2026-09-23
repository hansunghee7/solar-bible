#!/usr/bin/env python3
"""우편함: 에이전트끼리 정보를 주고받는 도구 (2026-09-19 도입)

원칙: 메시지 1개 = 파일 1개. 사장님이 복사해서 붙이지 않고, 폴링으로 기다리지 않는다.
  보내기 : python mailbox.py send <받는이> "<제목>" [--from 탐] [--urgent]   (본문은 표준입력 또는 --body)
  개수   : python mailbox.py list                     (안 읽은 메시지가 있을 때만 출력, 세션 시작 훅용)
  읽기   : python mailbox.py read <내 이름>             (내 우편 + 전체 공지를 읽고 읽음 표시)
받는이: 전체, 탐, 마야, 시안, 노트, 핏, 페이브, 헤르메스, 사장님, 지투
이 저장소는 공개다. 비밀값(키, 토큰), 개인정보, 호스트명, IP를 쓰지 않는다.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SEEN = Path.home() / ".claude" / "mailbox_seen.json"
PERSONAS = ["전체", "탐", "마야", "시안", "노트", "핏", "페이브", "헤르메스", "사장님", "지투"]


def git(*args, timeout=30):
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
    )


def sync():
    try:
        git("pull", "--ff-only", "--quiet", timeout=15)
    except Exception:
        pass


def load_seen():
    try:
        return json.loads(SEEN.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_seen(d):
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def files_of(persona):
    d = ROOT / persona
    return sorted(p for p in d.glob("*.md")) if d.is_dir() else []


def unread_for(reader, seen):
    """reader의 안 읽은 메시지: 내 우편 + 전체 공지"""
    mine = set(seen.get(reader, []))
    out = []
    for box in (reader, "전체"):
        for p in files_of(box):
            key = f"{box}/{p.name}"
            if key not in mine:
                out.append((key, p))
    return out


LAST_LIST = Path.home() / ".claude" / "mailbox_last_list.txt"


def cmd_list(args):
    sync()
    seen = load_seen()
    parts = []
    for name in PERSONAS[1:]:
        n = len(unread_for(name, seen))
        if n:
            parts.append(f"{name} {n}건")
    summary = ", ".join(parts)
    if getattr(args, "changed", False):
        # 프롬프트마다 실행되는 훅용: 지난번에 보여 준 내용과 달라졌을 때만 출력한다.
        try:
            last = LAST_LIST.read_text(encoding="utf-8")
        except Exception:
            last = ""
        if summary == last:
            return
        LAST_LIST.parent.mkdir(parents=True, exist_ok=True)
        LAST_LIST.write_text(summary, encoding="utf-8")
    if parts:
        print("📬 우편함 안 읽은 메시지: " + summary)
        print(f"   읽기: python \"{ROOT / 'mailbox.py'}\" read <내 이름>")


def recent_for(reader, hours):
    """최근 N시간 안에 온 메시지 전부(읽음 여부와 상관없이). 파일명 앞의 날짜-시각으로 판단한다."""
    limit = time.time() - hours * 3600
    out = []
    for box in (reader, "전체"):
        for p in files_of(box):
            m = re.match(r"(\d{8})-(\d{6})-", p.name)
            if not m:
                continue
            try:
                ts = time.mktime(time.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S"))
            except ValueError:
                continue
            if ts >= limit:
                out.append((f"{box}/{p.name}", p))
    return sorted(out, key=lambda kv: kv[1].name)


def cmd_read(args):
    sync()
    seen = load_seen()
    if args.recent is not None:
        # 새 세션용: 다른 세션이 이미 읽음 처리했더라도 최근 메시지를 다시 보여 준다(읽음 표시는 바꾸지 않는다).
        for key, p in recent_for(args.name, args.recent):
            print("=" * 60)
            print(f"[{key}]")
            print(p.read_text(encoding="utf-8").strip())
        return
    items = unread_for(args.name, seen)
    if not items:
        return
    keys = set(seen.get(args.name, []))
    for key, p in items:
        print("=" * 60)
        print(f"[{key}]")
        print(p.read_text(encoding="utf-8").strip())
        keys.add(key)
    seen[args.name] = sorted(keys)
    save_seen(seen)


def slug(s):
    s = re.sub(r"[^\w]+", "-", s, flags=re.UNICODE).strip("-")
    return s[:30] or "메시지"


def cmd_send(args):
    if args.to not in PERSONAS:
        print(f"받는이는 {', '.join(PERSONAS)} 중 하나여야 합니다.")
        sys.exit(2)
    if args.body is not None:
        body = args.body
    else:
        # 윈도우 표준입력은 기본이 cp949라서 UTF-8 본문이 깨진다. 바이트로 읽어 직접 디코딩한다.
        body = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    now = time.localtime()
    ts = time.strftime("%Y%m%d-%H%M%S", now)
    name = f"{ts}-{args.sender}-{slug(args.title)}.md"
    d = ROOT / args.to
    d.mkdir(parents=True, exist_ok=True)
    f = d / name
    header = (
        f"# {args.title}\n\n받는이: {args.to}\n보낸이: {args.sender}\n"
        f"시각: {time.strftime('%Y-%m-%d %H:%M:%S', now)}\n긴급: {'예' if args.urgent else '아니오'}\n"
        + (f"요청: {args.ask.strip()}\n" if args.ask else "")
        + "\n"
    )
    f.write_text(header + body.strip() + "\n", encoding="utf-8")
    rel = str(f.relative_to(REPO)).replace("\\", "/")
    git("add", "--", rel)
    r = git("commit", "-m", f"mail: {args.sender}에서 {args.to}로 메시지 전달", "--", rel)
    if r.returncode != 0:
        print("커밋 실패:", (r.stdout + r.stderr).strip()[:300])
        sys.exit(1)
    for _ in range(2):
        git("pull", "--rebase", "--autostash", "--quiet", timeout=30)
        p = git("push", "origin", "main", timeout=40)
        if p.returncode == 0:
            print(f"발송 완료: {rel}")
            return
    print("푸시 실패(로컬에는 저장됨):", (p.stdout + p.stderr).strip()[:300])
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="에이전트 우편함")
    sub = ap.add_subparsers(dest="cmd", required=True)
    lp = sub.add_parser("list")
    lp.add_argument("--changed", action="store_true", help="지난번과 달라졌을 때만 출력(프롬프트 훅용)")
    lp.set_defaults(fn=cmd_list)
    r = sub.add_parser("read")
    r.add_argument("name")
    r.add_argument("--recent", nargs="?", const=24.0, type=float, default=None,
                   help="최근 N시간(기본 24) 메시지를 읽음 여부와 상관없이 표시. 새 세션의 아침 의식용")
    r.set_defaults(fn=cmd_read)
    s = sub.add_parser("send")
    s.add_argument("to")
    s.add_argument("title")
    s.add_argument("--from", dest="sender", default="탐")
    s.add_argument("--body", default=None)
    s.add_argument("--urgent", action="store_true")
    s.add_argument("--ask", default=None, help="받는 사람이 할 일 한 줄 (긴급 알림의 👉 줄에 그대로 쓰임)")
    s.set_defaults(fn=cmd_send)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
