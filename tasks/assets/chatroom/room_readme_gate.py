#!/usr/bin/env python3
"""교신방 '사람용 첫 화면' 관문(N174). 방 링크를 외부 사람에게 주기 직전, 또는 방을 만든 직후에 돌린다.
기본 브랜치 README에 아래 4가지가 없으면 종료 코드 1로 멈춘다(규약 7절, CLAUDE#4e7b).

사용: python room_readme_gate.py <소유자/저장소> [--branch 작업브랜치] [--file README 로컬파일]
  ① 제목에 '하실 일'  ② 에이전트에게 붙여 넣을 문장(인용 블록 '>')  ③ '중지' 안내  ④ 비용 한 줄('비용')
  --branch를 주면 그 브랜치 README가 기본 브랜치와 같은지도 본다(어느 쪽으로 들어가도 같게).
  --file은 저장소 대신 로컬 파일을 검사한다(시험용).
  --pr <번호>를 주면 README 대신 그 PR 본문만 같은 4항목으로 검사한다(주소가 PR 링크일 때, 받는 사람이 여는 화면 기준).
출력은 UTF-8, 통과는 PASS 한 줄, 실패는 FAIL과 빠진 항목. 파이썬 표준 라이브러리와 gh만 쓴다. 엔진: 스크립트.
"""
import argparse, base64, json, re, subprocess, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def gh_readme(repo, ref=None):
    cmd = ["gh", "api", f"repos/{repo}/readme"] + ([f"-f", f"ref={ref}"] if ref else [])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode != 0:
        raise RuntimeError("README를 못 읽음: " + r.stderr.strip()[:200])
    return base64.b64decode(json.loads(r.stdout)["content"]).decode("utf-8")


def gh_pr_body(repo, num):
    cmd = ["gh", "pr", "view", str(num), "--repo", repo, "--json", "body", "-q", ".body"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode != 0:
        raise RuntimeError("PR 본문을 못 읽음: " + r.stderr.strip()[:200])
    return r.stdout


def check(text):
    miss = []
    if not re.search(r"^#{1,3}[^\n]*하실 일", text, re.M):
        miss.append("① 제목에 '하실 일'이 없음")
    if not re.search(r"^\s*>\s*\S", text, re.M):
        miss.append("② 에이전트에게 붙여 넣을 문장(인용 블록 '>')이 없음")
    if "중지" not in text:
        miss.append("③ '중지' 안내가 없음")
    if not re.search(r"비용[^\n]*", text):
        miss.append("④ 비용 한 줄이 없음")
    return miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--branch")
    ap.add_argument("--file")
    ap.add_argument("--pr", type=int)
    a = ap.parse_args()
    try:
        if a.file:
            base = open(a.file, encoding="utf-8").read()
        elif a.pr:
            base = gh_pr_body(a.repo, a.pr)
        else:
            base = gh_readme(a.repo)
        other = gh_readme(a.repo, a.branch) if a.branch and not a.file and not a.pr else None
    except Exception as e:
        print("확인 실패:", e, file=sys.stderr)
        sys.exit(2)
    miss = check(base)
    if other is not None and other.strip() != base.strip():
        miss.append(f"기본 브랜치와 '{a.branch}' 브랜치 README가 다름")
    if miss:
        print("FAIL 사람용 첫 화면 관문: 링크를 주지 말고 README부터 고치세요")
        for m in miss:
            print(" -", m)
        sys.exit(1)
    print("PASS 사람용 첫 화면 관문: 4항목 모두 있음" + (f" (PR #{a.pr} 본문)" if a.pr and not a.file else "") + ("" if other is None else f", {a.branch}와 동일"))


if __name__ == "__main__":
    main()
