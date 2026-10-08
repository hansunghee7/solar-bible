# 탐 2026-10-08: 제미나이 웹 접속·로그인 유지 확인 (읽기 전용, 프롬프트 입력 없음).
# 열려 있는 크롬 디버그 포트(9222~9235)에 붙어 새 탭으로 gemini.google.com을 열고, 로그인 화면으로 튕기는지만 본다.
# 이메일은 앞 2글자+도메인만 출력한다(공개 저장소). 로그인 화면이면 아무것도 하지 않고 "로그인 필요"로 보고한다.
import re, sys, time, random, urllib.request
try:
    from playwright.sync_api import sync_playwright
except Exception as e:
    print("RESULT playwright 없음:", e); sys.exit(0)

def mask(m):
    return (m[:2] + "***@" + m.split("@")[1]) if m and "@" in m else "(없음)"

def ports():
    out = []
    for p in range(9222, 9236):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{p}/json/version", timeout=2).read(); out.append(p)
        except Exception:
            pass
    return out

host = sys.argv[1] if len(sys.argv) > 1 else "PC"
ps = ports()
print(f"HOST {host} 열린 디버그 포트: {ps}")
with sync_playwright() as pw:
    for p in ps:
        try:
            b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{p}")
            ctx = b.contexts[0]
            pg = ctx.new_page()
            t0 = time.time()
            pg.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(4000 + random.randint(0, 2000))
            url = pg.url
            title = pg.title()
            body = ""
            try: body = pg.inner_text("body", timeout=5000)[:4000]
            except Exception: pass
            em = ""
            try:
                lab = pg.locator('a[aria-label*="Google 계정"], a[aria-label*="Google Account"]').first.get_attribute("aria-label", timeout=4000) or ""
                m = re.search(r"[\w.+-]+@[\w.-]+", lab); em = m.group(0) if m else ""
            except Exception: pass
            login = ("accounts.google.com" in url) or ("Sign in" in body[:300] or "로그인" in body[:300])
            low = body.lower()[:1500]
            flags = [k for k in ("captcha", "unusual traffic", "비정상적인 트래픽") if k in low]
            ok_ui = bool(pg.locator('rich-textarea, [contenteditable="true"]').count())
            print(f"PORT {p} url={url[:60]} title={title[:30]} 계정={mask(em)} 입력창={ok_ui} 로그인화면={login} 차단징후={flags} 초={time.time()-t0:.1f}")
            pg.screenshot(path=f"gemini_check_{host}_{p}.png")  # 로컬에만 남김, 올리지 않음
            pg.close()  # 우리가 연 탭만 닫는다
        except Exception as e:
            print(f"PORT {p} 오류: {str(e)[:150]}")
print("RESULT 끝")
