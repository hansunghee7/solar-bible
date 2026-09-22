import os
import sys

base = r"C:\work\solar-bible"
p = os.path.join(base, "tasks", "pending")

print("dir:", p)
print("exists:", os.path.isdir(p))
names = os.listdir(p)
print("entry count:", len(names))

for fn in names:
    fp = os.path.join(p, fn)
    sz = os.path.getsize(fp)
    abspath = os.path.abspath(fp)
    print()
    print("FILE:", repr(fn))
    print("  size:", sz)
    print("  abspath:", abspath)
    if sz > 0:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            print("  content preview:")
            print(content[:1500])
        except Exception as e:
            print("  READ ERROR:", repr(e))
    else:
        print("  (empty file)")
