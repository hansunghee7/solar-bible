import glob
import json
import os

sessions_dir = r"C:\Users\PC\AppData\Local\hermes\sessions"
files = glob.glob(os.path.join(sessions_dir, "request_dump_*.json"))

# Check a few files that might have body content with messages
for path in files[-5:]:
    print("=== File:", os.path.basename(path))
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Check the body field
        request = data.get("request", {})
        if isinstance(request, dict):
            body = request.get("body", "")
            if body:
                print("Body preview:", str(body)[:500])
            else:
                print("No body")
        print()
    except Exception as e:
        print("Error reading file:", e)
        print()