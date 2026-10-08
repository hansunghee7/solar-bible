# -*- coding: utf-8 -*-
# 야간 일감 1: 공정 카드가 가리키는 공개 문서와 카드 내용이 어긋나는 곳 찾기(소넷). 인용은 스크립트가 글자 그대로 있는지 검증한다(환각 제거).
# 입력은 공개 저장소 docs 문서와 공정 카드 문구뿐이다. 결과는 파일에만 저장하고 어디에도 자동 반영하지 않는다.
import json, os, re, subprocess, sys, time
from pathlib import Path

REPO = Path("C:/work/hansunghee7.github.io")
OUTD = Path("C:/work/_ops/api_night"); OUTD.mkdir(parents=True, exist_ok=True)
HERE = Path(__file__).resolve().parent
cards = json.load(open("C:/work/_ops/cards_export.json", encoding="utf-8"))
tracked = set(subprocess.run(["git", "-C", str(REPO), "-c", "core.quotepath=false", "ls-files", "-z"], capture_output=True, text=True, encoding="utf-8").stdout.split(chr(0)))
pat = re.compile(r"docs/[^\s,;:!?)\]`'\"]+\.md")
jobs = []
for c in cards:
    for ref in set(pat.findall((c.get("title") or "") + " " + (c.get("do") or ""))):
        if ref in tracked:
            jobs.append((c, ref))
print("대상", len(jobs), "건", flush=True)
results = []
for c, ref in jobs:
    doc = (REPO / ref).read_text(encoding="utf-8", errors="replace")[:24000]
    card_text = ("제목: " + (c.get("title") or "") + "\n내용: " + (c.get("do") or ""))[:3000]
    p = ("[카드]는 에이전트가 따르는 절차 카드이고 [문서]는 카드가 가리키는 정본 문서다. 카드의 구체적 주장(경로, 숫자, 순서, 규칙)이 문서와 어긋나는 곳만 찾아라. "
         "어긋남마다 카드에서 한 구절과 문서에서 한 구절을 글자 그대로 인용하라(바꾸지 말 것). 어긋남이 없으면 빈 목록. 판정이나 권장 조치는 쓰지 말라. "
         '오직 JSON 한 줄: {"conflicts":[{"card_quote":"...","doc_quote":"...","why":"한 줄"}]}\n\n[카드]\n' + card_text + "\n\n[문서]\n" + doc)
    (HERE / "night_p.txt").write_text(p, encoding="utf-8")
    t0 = time.time()
    r = subprocess.run([sys.executable, str(REPO / "scripts/ops/api_run.py"), "--who", "탐", "--model", "claude-sonnet-5-5", "--prompt-file", str(HERE / "night_p.txt"), "--max-tokens", "1500", "--out", str(HERE / "night_a.txt"), "--daily-usd", "5"], capture_output=True, text=True, encoding="utf-8", timeout=240)
    if r.returncode != 0:
        results.append({"card": c["id"], "doc": ref, "error": "rc=%s %s" % (r.returncode, r.stderr[-120:])})
        if r.returncode == 3:
            break
        continue
    txt = (HERE / "night_a.txt").read_text(encoding="utf-8")
    m = re.search(r"\{[\s\S]*\}", txt)
    try:
        d = json.loads(m.group(0)) if m else {"conflicts": []}
    except Exception:
        d = {"conflicts": [], "parse_fail": True}
    ver = []
    for x in d.get("conflicts", []):
        ok_card = bool(x.get("card_quote")) and x["card_quote"] in card_text
        ok_doc = bool(x.get("doc_quote")) and x["doc_quote"] in doc
        ver.append({**x, "card_quote_verbatim": ok_card, "doc_quote_verbatim": ok_doc})
    cost = re.search(r"cost=([0-9.]+)", r.stderr)
    results.append({"card": c["id"], "doc": ref, "sec": round(time.time() - t0, 1), "cost": float(cost.group(1)) if cost else 0, "conflicts": ver})
    (OUTD / "cardcheck_1009.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(r.get("cost", 0) for r in results)
verified = sum(1 for r in results for x in r.get("conflicts", []) if x["card_quote_verbatim"] and x["doc_quote_verbatim"])
claimed = sum(len(r.get("conflicts", [])) for r in results)
summary = "야간 일감 1(카드↔문서 어긋남 점검): 카드-문서 쌍 %d건, 어긋남 주장 %d건 중 인용 검증 통과 %d건, 비용 약 $%.3f. 파일: C:/work/_ops/api_night/cardcheck_1009.json" % (len(results), claimed, verified, tot)
(OUTD / "cardcheck_1009_summary.txt").write_text(summary, encoding="utf-8")
print(summary, flush=True)
try:
    subprocess.run([sys.executable, str(REPO / "scripts/ops/tg_boss.py"), "text", "[탐 컨펌] " + summary, "--persona", "탐"], capture_output=True, timeout=60)
except Exception:
    pass
print("NIGHT1 DONE")
