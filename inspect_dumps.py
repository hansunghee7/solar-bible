import glob
import json
import os

sessions_dir = r"C:\Users\PC\AppData\Local\hermes\sessions"
files = glob.glob(os.path.join(sessions_dir, "request_dump_*.json"))
print(f"Total files: {len(files)}")

for path in files[:5]:
    print("=== File:", os.path.basename(path))
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Top-level keys:", list(data.keys()))
        messages = data.get("messages", [])
        print("Messages count:", len(messages))
        tools_used = set()
        urls_found = []
        for m in messages:
            if isinstance(m, dict) and m.get("tool_calls"):
                for tc in m["tool_calls"]:
                    func = tc.get("function", {})
                    name = func.get("name")
                    tools_used.add(name)
                    args_str = func.get("arguments", "")
                    if "url" in args_str.lower():
                        try:
                            args = json.loads(args_str)
                            if "urls" in args:
                                urls_found.extend(args["urls"])
                            elif "url" in args:
                                urls_found.append(args["url"])
                        except Exception:
                            pass
        print("Tools used:", tools_used)
        print("URLs found:", urls_found[:10])
    except Exception as e:
        print("Error reading file:", e)
