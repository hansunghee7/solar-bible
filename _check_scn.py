from datetime import datetime, time as dt_time
from pathlib import Path
import sys, os

sys.path.insert(0, '/c/work/solar-bible')
import mailbox_courier_new as mc

# 시간 패치: 21:00 이후로
fake = datetime(2026, 9, 20, 21, 5, 0)
mc.datetime = type(mc.datetime)('FakeDateTime', (datetime,), {'now': classmethod(lambda cls: fake)})()
mc.is_evening_now = lambda: fake.time() >= mc.EVENING_SUMMARY_TIME

d = Path('/c/work/solar-bible/mailbox/_scenario_tmp')
for f in sorted(d.glob('*.md')):
    r,s,sub,bf,ask = mc.extract_metadata_and_body(f)
    urg = mc.has_urgent_flag(f)
    print(f'{f.name}: recipient={r}, sender={s}, subject={sub}, ask={ask!r}, urgent={urg}')
