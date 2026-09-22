import json
from pathlib import Path

def norm_key(x):
    return str(x).replace('\\\\', '/').replace('\\', '/')

def load_state_convert(state_path):
    """load_state의 변환 로직만 테스트"""
    p = Path(state_path)
    if not p.exists():
        return {'notified_files': set(), 'daily_counts': {}}
    with p.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # 새 형식: dict + 'notified_files' 키
    if isinstance(data, dict) and 'notified_files' in data:
        return data
    # 구 형식(목록): JSON 배열
    if isinstance(data, list):
        return {
            'notified_files': [norm_key(x) for x in data],
            'daily_counts': {}
        }
    # 구 형식(사전): {path: true} 형태
    if isinstance(data, dict):
        return {
            'notified_files': set(data.keys()),
            'daily_counts': {}
        }
    return {'notified_files': set(), 'daily_counts': {}}

# (f) 테스트: 구 형식(목록) 파일 변환
old_path = "_scn_f_state_old.json"
converted = load_state_convert(old_path)
print("(f) 구 형식 → 새 형식 변환 결과:")
print(json.dumps(converted, ensure_ascii=False, indent=2))
print()

# 검증: 목록이었을 때 notified_files가 문자열 리스트고 daily_counts가 빈 dict인지
assert isinstance(converted['notified_files'], list), "notified_files는 리스트여야 함"
assert isinstance(converted['daily_counts'], dict), "daily_counts는 dict여야 함"
assert len(converted['notified_files']) == 2, "목록의 2개 항목이 보존되어야 함"
print("✅ (f) 검증 통과: 구 형식(목록) → 새 형식 변환 정상")

# 구 형식(사전) 테스트도 추가
old_dict = {"C:\\work\\solar-bible\\mailbox\\old_1.md": True, "C:\\work\\solar-bible\\mailbox\\old_2.md": True}
p = Path("_scn_f_state_old_dict.json")
p.write_text(json.dumps(old_dict, ensure_ascii=False), encoding="utf-8")
converted2 = load_state_convert("_scn_f_state_old_dict.json")
print("\n(f-2) 구 형식(사전) → 새 형식 변환 결과:")
print(json.dumps({k: (list(v) if isinstance(v, set) else v) for k, v in converted2.items()}, ensure_ascii=False, indent=2))
assert isinstance(converted2['notified_files'], set), "사전 형식은 set으로 변환되어야 함"
assert len(converted2['notified_files']) == 2, "사전 키 2개가 보존되어야 함"
print("✅ (f-2) 검증 통과: 구 형식(사전) → 새 형식 변환 정상")
