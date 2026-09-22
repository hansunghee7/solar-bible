#!/usr/bin/env python3
"""evidence_snapshot.py — 보고서 작성 세션의 실제 도구 실행 기록에서 증거를 추출한다.

이전 버전은 collected_urls/failed_or_unreadable_urls를 스크립트에 직접 타이핑한
자기신고 값이었다(백로그 30, 사장님 반려). 이 버전은 그 값을 전부 지우고,
헤르메스 세션 저장소(SQLite, `hermes sessions export`)에서 그 보고서를 만든
세션의 실제 tool_calls/tool 응답을 읽어 URL 목록과 성공/실패를 재구성한다.

사용법:
    python evidence_snapshot.py --session-id <ID> --report <REPORT_PATH>

세션 id를 모르면 먼저 찾는다:
    hermes sessions export --format jsonl --after <YYYY-MM-DD> --before <YYYY-MM-DD> \
        --min-tool-calls 1 - | grep <보고서 안의 고유 URL 일부>
"""
import argparse
import json
import os
import subprocess
import sys
import datetime

# 실제로 URL을 여러 건 인자로 받아 웹 콘텐츠를 가져오는 도구 이름들.
# 새 도구가 추가되면 여기에 더한다 — 하드코딩된 URL 목록 대신 도구 이름만 하드코딩한다.
FETCH_TOOL_NAMES = {"web_extract", "web_fetch", "fetch", "browser_fetch"}


def export_session(session_id: str) -> dict:
    """hermes SQLite 세션 저장소에서 해당 세션 하나를 jsonl로 export해 파싱한다."""
    proc = subprocess.run(
        ["hermes", "sessions", "export", "--format", "jsonl",
         "--session-id", session_id, "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"hermes sessions export 실패(exit {proc.returncode}): {proc.stderr[:500]}")
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    if not lines:
        raise RuntimeError(f"세션 {session_id}을(를) 찾지 못함(export 결과 0줄)")
    return json.loads(lines[0])


def extract_tool_result_json(raw_content: str):
    """<untrusted_tool_result ...> 래퍼가 섞인 tool 응답 문자열에서 JSON 본문만 뽑는다."""
    idx = raw_content.find("{")
    if idx == -1:
        return None
    try:
        # raw_decode: 뒤에 </untrusted_tool_result> 같은 꼬리가 붙어 있어도
        # 앞쪽 JSON 객체 하나만 파싱하고 나머지는 무시한다.
        obj, _ = json.JSONDecoder().raw_decode(raw_content[idx:])
        return obj
    except json.JSONDecodeError:
        return None


def collect_evidence(session: dict) -> dict:
    messages = session.get("messages") or []
    by_call_id = {}
    for m in messages:
        if m.get("role") == "tool" and m.get("tool_call_id"):
            by_call_id[m["tool_call_id"]] = m

    collected = []
    failed = []
    fetch_call_count = 0

    for m in messages:
        if m.get("role") != "assistant" or not m.get("tool_calls"):
            continue
        for tc in m["tool_calls"]:
            fn = (tc or {}).get("function") or {}
            name = fn.get("name")
            if name not in FETCH_TOOL_NAMES:
                continue
            fetch_call_count += 1
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            requested_urls = args.get("urls") or ([args["url"]] if args.get("url") else [])

            call_id = tc.get("id") or tc.get("call_id")
            tool_msg = by_call_id.get(call_id)
            result = extract_tool_result_json(tool_msg["content"]) if tool_msg else None

            result_by_url = {}
            if result and isinstance(result.get("results"), list):
                for r in result["results"]:
                    result_by_url[r.get("url")] = r

            for u in requested_urls:
                r = result_by_url.get(u)
                if r is None:
                    # 도구가 실패해서 응답 자체가 없거나 파싱이 안 된 경우
                    failed.append({"url": u, "reason": "응답 파싱 실패 또는 결과 없음"})
                elif r.get("error"):
                    failed.append({"url": u, "reason": r["error"]})
                else:
                    collected.append(u)

    return {
        "fetch_tool_call_count": fetch_call_count,
        "collected_urls": sorted(set(collected)),
        "failed_or_unreadable_urls": failed,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session-id", required=True, help="hermes sessions export가 인식하는 세션 id")
    ap.add_argument("--report", required=True, help="이 증거가 뒷받침하는 보고서 파일 경로")
    args = ap.parse_args()

    session = export_session(args.session_id)
    evidence = collect_evidence(session)

    snapshot = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session_id": args.session_id,
        "session_started_at": session.get("started_at"),
        "session_tool_call_count_total": session.get("tool_call_count"),
        "report_path": args.report,
        "report_exists": os.path.exists(args.report),
        "report_size_bytes": os.path.getsize(args.report) if os.path.exists(args.report) else None,
        **evidence,
    }
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
