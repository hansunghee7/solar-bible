import io

path = r"C:\work\solar-bible\docs\진행상황.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_d = "|| D:\\\\Downloads (~22GB) | **백업 불필요** (사장님 결정 2026-09-19, 과정 데이터. 삭제·이동은 사장님 명시 승인 필요) | 레지스트리 설정 유지, 내용물 미확인 |"
new_d = "| D:\\\\Downloads (~22GB) | **백업 불필요** (사장님 결정 2026-09-19, 과정 데이터. 삭제·이동은 사장님 명시 승인 필요) | 레지스트리 설정 유지, 내용물 미확인 |"

old_c = "|| ComfyUI 폴더 | **백업 불필요** (사장님 결정 2026-09-19, 과정 데이터. 삭제·이동은 사장님 명시 승인 필요) | AI 모델/워크플로우 자산 가능성 |"
new_c = "| ComfyUI 폴더 | **백업 불필요** (사장님 결정 2026-09-19, 과정 데이터. 삭제·이동은 사장님 명시 승인 필요) | AI 모델/워크플로우 자산 가능성 |"

print("D줄 발견:", old_d in content)
print("ComfyUI줄 발견:", old_c in content)

content = content.replace(old_d, new_d)
content = content.replace(old_c, new_c)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("교체 완료")

# 확인
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines[52:62], start=53):
    print(f"{i}: {line.rstrip()}")
