#!/usr/bin/env python3
# mailbox_courier_new.py - mailbox_courier.py 재작업 시험본 (dry-run 포함)
# 원본: mailbox_courier.py.broken_0919_hermes (헤르메스 스크립트 디렉토리)
# 수정: timedelta import 추가, should_send_to_boss_today 호출 수정,
#       사장님/긴급 알림 문구 사장님 확정 초안 반영, --dry-run 옵션,
#       boss 요약 21:00 시간 조건, 상한 초과 시 전체 미송출 요약,
#       상태 파일 구 형식 자동 변환, 중복 발송 방지.
# 운영 파일(mailbox_courier.py)은 시험 종료까지 건드리지 않음.

import argparse
import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime, date, time as dt_time, timedelta

# UTF-8 출력 강제
sys.stdout.reconfigure(encoding='utf-8')

# 설정
DEFAULT_MAILBOX_DIR = Path(r"C:\work\solar-bible\mailbox")
STATE_FILE = Path(r"C:\Users\PC\AppData\Local\hermes\mailbox_courier_state.json")
SOLAR_BIBLE_ROOT = Path(r"C:\work\solar-bible")
ENV_FILE = Path(r"C:\Users\PC\AppData\Local\hermes\.env")

# 하루 상한
DAILY_LIMIT = 20
EVENING_SUMMARY_TIME = dt_time(21, 0)  # 한국 시간 21:00

# 사장님 확정 알림 문구 형식 (2026-09-19 밤)
# 알림형 (요청: 없음): "📬 탐 : 사장님, 알려드려요. <제목>."
# 확인 부탁형 (요청: 있음): "📬 탐 : 사장님, 확인 부탁드려요. <제목>. <요청 문장 그대로>"
# 보내는 이는 이름 앞에 "이름 : " 형태로 붙인다.
# 다른 에이전트 앞 긴급 알림도 같은 형식(받는이만 바꿈).
# 이모지는 맨 앞 📬 하나만 허용. 제목 끝 마침표 중복 정리.


def load_env():
    """환경변수 파일에서 TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS 읽기"""
    env_vars = {}
    try:
        with ENV_FILE.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"\'')
                    env_vars[key.strip()] = value
    except OSError:
        pass
    return env_vars


def norm_key(x):
    return str(x).replace('\\\\', '/').replace('\\', '/')


def load_state():
    """상태 파일 로드 (발송 이력 + 날짜별 카운트).
    새 형식: {notified_files: [...], daily_counts: {YYYY-MM-DD: N}}
    구 형식(목록): [...] → 집합 변환.
    구 형식(사전): {path: true} → 키 집합 변환.
    """
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open('r', encoding='utf-8') as f:
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
            return {
                'notified_files': set(),
                'daily_counts': {}
            }
        except (json.JSONDecodeError, OSError):
            return {'notified_files': set(), 'daily_counts': {}}
    return {'notified_files': set(), 'daily_counts': {}}


def save_state(state):
    """상태 파일 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open('w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run_git_pull():
    """git pull --ff-only 실행 (실패해도 계속)"""
    try:
        result = subprocess.run(
            ['git', 'pull', '--ff-only'],
            cwd=SOLAR_BIBLE_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
    except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
        pass


def extract_metadata_and_body(filepath):
    """파일에서 메타데이터와 본문 추출. 받는이, 보낸이, 제목, 본문 첫 줄, 요청 반환.
    받는이 판정은 '받는이:' 헤더 우선, 없으면 첫 # 제목줄 앞의 맥락으로 추정."""
    try:
        with filepath.open('r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError:
        return None, None, None, None, None

    recipient = None
    sender = None
    subject = None
    body_start = 0
    saw_meta = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('받는이:'):
            recipient = stripped[4:].strip()
        elif stripped.startswith('보낸이:'):
            sender = stripped[4:].strip()
        elif stripped.startswith('제목:'):
            subject = stripped[3:].strip()
        elif stripped.startswith('# ') and subject is None:
            subject = stripped[2:].strip()
        elif stripped.startswith('긴급:'):
            saw_meta = True
        elif saw_meta and stripped == '':
            body_start = i + 1
            break
        elif stripped == '---':
            body_start = i + 1
            break

    ask = ''
    for ln in lines[:body_start]:
        if ln.strip().startswith('요청:'):
            ask = ln.strip()[3:].strip()

    body_lines = [ln for ln in lines[body_start:] if ln.strip()]
    body_first = body_lines[0].strip() if body_lines else ''

    # 받는이가 명시되지 않았으면 파일 경로에서 추정 (폴더명)
    if not recipient:
        try:
            rel = filepath.relative_to(DEFAULT_MAILBOX_DIR)
            parts = rel.parts
            if len(parts) >= 2:
                recipient = parts[0]  # 첫 폴더명 = 받는이
        except ValueError:
            pass

    return recipient, sender, subject, body_first, ask


def has_urgent_flag(filepath):
    """본문에 '긴급: 예' 줄이 있는지 확인"""
    try:
        with filepath.open('r', encoding='utf-8') as f:
            for line in f:
                if line.strip() == '긴급: 예':
                    return True
    except OSError:
        pass
    return False


def shorten(text, limit):
    """단어(공백)나 문장부호 경계에서 자르고 줄임표를 붙인다."""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ('. ', '! ', '? ', ', ', ' '):
        i = cut.rfind(sep)
        if i >= limit // 2:
            cut = cut[:i + (0 if sep == ' ' else 1)]
            break
    return cut.rstrip(' ,.') + '…'


def clean_subject(subject):
    """제목 끝의 마침표 중복 정리. 이미 끝이 '.'이면 하나 남김."""
    if subject and subject.endswith('.'):
        return subject.rstrip('.') + '.'
    return subject


def build_message_for_boss(sender, subject, ask=''):
    """사장님 앞 한 줄 메시지 (사장님 확정 초안).

    알림형 (요청: 헤더 없음):
        "📬 탐 : 사장님, 알려드려요. <제목>."
    확인 부탁형 (요청: 헤더 있음):
        "📬 탐 : 사장님, 확인 부탁드려요. <제목>. <요청 문장 그대로>"

    보내는 이는 "이름 : " 형태로 제목 앞에 붙인다.
    이모지는 맨 앞 📬 하나만. 제목 끝 마침표는 clean_subject로 정리.
    """
    subject_clean = clean_subject(subject)
    if ask:
        # 확인 부탁형
        text = f"📬 {sender} : 사장님, 확인 부탁드려요. {subject_clean}. {ask}"
    else:
        # 알림형
        text = f"📬 {sender} : 사장님, 알려드려요. {subject_clean}."
    return text


def build_message_others(sender, recipient, subject, body_first, ask=''):
    """다른 에이전트/전체 앞 긴급 알림 한 줄 메시지 (사장님 확정 형식).

    형식: "📬 <보낸이> : <받는이>, 알려드려요. <제목>."
    요청 있으면: "📬 <보낸이> : <받는이>, 확인 부탁드려요. <제목>. <요청>"
    이모지 맨 앞 하나만. 제목 끝 마침표 정리.
    주의: 사장님이 보는 알림이 아니면 텔레그램으로 보내지 않는다는 기존 규칙 유지.
    이 함수는 메시지만 조립하며, 실제 발송 여부는 호출 측이 결정한다.
    """
    subject_clean = clean_subject(subject)
    if ask:
        text = f"📬 {sender} : {recipient}, 확인 부탁드려요. {subject_clean}. {ask}"
    else:
        text = f"📬 {sender} : {recipient}, 알려드려요. {subject_clean}."
    return text


def send_telegram(token, chat_id, text):
    """Telegram Bot API sendMessage 직접 호출"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.json()
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def get_today_str():
    """한국 시간 기준 오늘 날짜 문자열 YYYY-MM-DD.
    이 PC의 시계는 이미 KST로 설정되어 있으므로 datetime.now()를 그대로 사용.
    UTC 기준 시계에서 KST를 구하는 상황이면 timedelta를 쓸 수 있으나,
    현재 환경에서는 불필요. (timedelta import는 향후 대비 유지)
    """
    now_kst = datetime.now()  # PC 시계 이미 KST
    return now_kst.strftime('%Y-%m-%d')


def is_evening_now():
    """현재 한국 시간이 21:00 이상인지 확인."""
    now_kst = datetime.now()
    return now_kst.time() >= EVENING_SUMMARY_TIME


def should_send_to_boss_today(state):
    """사장님 앞 오늘 이미 요약 발송했는지 확인.
    boss_key 인자 제거: 항상 오늘 날짜 기준 키로 판정.
    """
    today = get_today_str()
    counts = state.get('daily_counts', {})
    key = f"boss_summarized_{today.replace('-', '')}"
    return key not in counts


def mark_boss_summarized(state):
    """오늘 사장님 앞 요약 발송 기록."""
    today = get_today_str()
    key = f"boss_summarized_{today.replace('-', '')}"
    counts = state.get('daily_counts', {})
    counts[key] = True
    state['daily_counts'] = counts


def count_today_sent(state):
    """오늘 텔레그램 발송 건수."""
    today = get_today_str()
    counts = state.get('daily_counts', {})
    return counts.get(today, 0)


def inc_today_count(state):
    """오늘 발송 건수 증가."""
    today = get_today_str()
    counts = state.get('daily_counts', {})
    counts[today] = counts.get(today, 0) + 1
    state['daily_counts'] = counts


def can_send_today(state):
    """오늘 하루 상한 도달 여부."""
    return count_today_sent(state) < DAILY_LIMIT


def build_boss_summary_message(total_unread):
    """사장님 앞 쌓인 우편 요약 (21:00 발송용).
    형식: "📬 사장님 앞 우편 N건 쌓임"
    """
    return f"📬 사장님 앞 우편 {total_unread}건 쌓임"


def build_overflow_summary_message(total_unread):
    """하루 20건 초과로 발송 못한 우편 전체 요약 (21:00 발송용).
    형식: "📬 오늘 쌓인 우편 N건"
    """
    return f"📬 오늘 쌓인 우편 {total_unread}건"


def main():
    parser = argparse.ArgumentParser(description='mailbox_courier 시험본')
    parser.add_argument('--dry-run', action='store_true',
                        help='텔레그램 실제 발송 없이 출력만. 상태 파일도 쓰지 않음.')
    parser.add_argument('--mailbox-dir', type=str, default=None,
                        help='메일함 디렉토리 override (환경변수 MAILBOX_DIR 대체)')
    parser.add_argument('--state-file', type=str, default=None,
                        help='상태 파일 경로 override')
    args = parser.parse_args()

    dry_run = args.dry_run
    if dry_run:
        print("[DRY-RUN] 실제 발송·상태 기록 없음. 아래 출력만 확인.")

    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN', '')
    allowed_users = env.get('TELEGRAM_ALLOWED_USERS', '')

    if not token or not allowed_users:
        print("[WARN] TELEGRAM_BOT_TOKEN 또는 TELEGRAM_ALLOWED_USERS 없음. 발송 건너뜀.")
        # dry-run에서는 실제 발송을 하지 않으므로 토큰 없어도 시나리오별 출력 진행.
        if not dry_run:
            print("[INFO] 토큰 없음 → 실제 발송 건너뜀. dry-run이 아니면 여기서 종료.")
            return 0

    chat_id = allowed_users.split(',')[0].strip()

    mailbox_dir_env = os.environ.get('MAILBOX_DIR') or args.mailbox_dir
    if mailbox_dir_env:
        mailbox_dir = Path(mailbox_dir_env)
        use_default = False
    else:
        mailbox_dir = DEFAULT_MAILBOX_DIR
        use_default = True

    if use_default:
        run_git_pull()

    # 상태 파일 override (global 선언은 참조보다 먼저)
    global STATE_FILE
    if args.state_file:
        STATE_FILE = Path(args.state_file)
    # else: 이미 기본 STATE_FILE 유지

    state = load_state()
    notified_files = set(state.get('notified_files', []))
    if not isinstance(notified_files, set):
        notified_files = set(notified_files)

    # 카운터 초기화 (상태 파일에 오늘 카운트가 없으면 0으로 시작)
    today_str = get_today_str()
    if today_str not in state.get('daily_counts', {}):
        state['daily_counts'][today_str] = 0

    new_notifications = []
    boss_unread_files = []   # 사장님 앞 안 읽은 우편 (개별 발송하지 않고 수집)
    overflow_files = []      # 하루 상한 초과로 오늘 못 보낸 우편 (21:00 요약 대상)

    current_time = datetime.now()
    now_kst_time = current_time.time()

    for md_file in mailbox_dir.rglob('*.md'):
        try:
            rel_path = norm_key(md_file.relative_to(mailbox_dir))
        except ValueError:
            rel_path = norm_key(md_file)

        if rel_path in notified_files:
            continue

        recipient, sender, subject, body_first, ask = extract_metadata_and_body(md_file)
        if not all([recipient, sender, subject]):
            continue

        # 받는이 분류
        is_boss = (recipient == '사장님')
        is_everyone = (recipient == '전체')

        if is_boss:
            # 사장님 앞: 긴급 여부 무관하게 수집 (개별 발송 안 함)
            boss_unread_files.append((rel_path, sender, subject, ask))
            continue

        # 전체 또는 다른 에이전트: 긴급 플래그 있는 것만
        if not has_urgent_flag(md_file):
            continue

        # 하루 상한 체크
        if not can_send_today(state):
            # 상한 초과 → 오늘 못 보냄. 21:00 요약에 포함되도록 기록만.
            overflow_files.append((rel_path, sender, recipient, subject, ask, body_first))
            if dry_run:
                print(f"[DRY-RUN] 상한 초과로 발송 보류: {rel_path}")
            continue

        # 전체 또는 다른 에이전트 앞 긴급: 메시지는 같은 형식으로 구성하지만
        # 사장님이 보는 알림이 아니면 텔레그램 발송 금지 (기존 규칙).
        # dry-run에서는 메시지 본문만 출력하고 발송·카운터 증가 모두 Skip.
        message = build_message_others(sender, recipient, subject, body_first, ask)
        if dry_run:
            print(f"[DRY-RUN] 발송 안 함 (수신자 비 사장님, 텔레그램 미발송 규칙): {rel_path}")
            print(f"  → 구성 메시지(참고):\\n{message}")
        else:
            print(f"[INFO] 발송 Skip (수신자 비 사장님): {rel_path}")

    # === 사장님 앞 처리 ===
    if boss_unread_files:
        total_boss = len(boss_unread_files)

        if is_evening_now():
            # 21:00 이후: 요약 1건 발송
            if dry_run:
                print(f"\n[DRY-RUN] 21:00 이후 → 사장님 앞 요약 발송 예정:")
                print(f"  요약 메시지: {build_boss_summary_message(total_boss)}")
                print(f"  포함 파일 ({total_boss}건):")
                for p, s, sub, a in boss_unread_files:
                    print(f"    - {p} (보낸이: {s}, 제목: {sub})")
            else:
                if can_send_today(state):
                    summary = build_boss_summary_message(total_boss)
                    result = send_telegram(token, chat_id, summary)
                    if result.get('ok'):
                        new_notifications.append(f"_boss_summary_{today_str}")
                        mark_boss_summarized(state)
                        inc_today_count(state)
                        print(f"[INFO] 사장님 앞 요약 발송 완료: {total_boss}건")
                    else:
                        print(f"[ERROR] 사장님 앞 요약 발송 실패: {result}")
                else:
                    # 상한 도달 시에도 요약은 보내야 함 (사장님 앞 특별 처리)
                    summary = build_boss_summary_message(total_boss)
                    result = send_telegram(token, chat_id, summary)
                    if result.get('ok'):
                        new_notifications.append(f"_boss_summary_{today_str}")
                        mark_boss_summarized(state)
                        # 카운터는 올리지 않음 (상한 카운트 이미 찼으므로)
                        print(f"[INFO] 사장님 앞 요약 발송 완료 (상한 도달 상태): {total_boss}건")
                    else:
                        print(f"[ERROR] 사장님 앞 요약 발송 실패: {result}")
        else:
            # 21:00 이전: 발송하지 않고 기록만. 다음 21:00 크론에서 발송.
            if dry_run:
                print(f"\n[DRY-RUN] 21:00 이전 → 사장님 앞 {total_boss}건 수집 완료. "
                      f"발송 보류 (21:00 크론에서 요약 발송 예정).")
                print(f"  포함 파일:")
                for p, s, sub, a in boss_unread_files:
                    print(f"    - {p} (보낸이: {s}, 제목: {sub})")
            else:
                print(f"[INFO] 사장님 앞 {total_boss}건 수집 완료. 21:00까지 발송 보류.")

    # === 하루 상한 초과분 처리 (21:00 요약) ===
    if overflow_files:
        total_overflow = len(overflow_files)
        if is_evening_now():
            if dry_run:
                print(f"\n[DRY-RUN] 21:00 이후 → 상한 초과분 요약 발송 예정:")
                print(f"  요약 메시지: {build_overflow_summary_message(total_overflow)}")
                print(f"  포함 파일 ({total_overflow}건):")
                for p, s, r, sub, a, bf in overflow_files:
                    print(f"    - {p} (보낸이: {s}, 받는이: {r}, 제목: {sub})")
            else:
                # 상한 이미 찼지만 21:00 요약은 발송 (미달분 합산)
                summary = build_overflow_summary_message(total_overflow)
                result = send_telegram(token, chat_id, summary)
                if result.get('ok'):
                    new_notifications.append(f"_overflow_summary_{today_str}")
                    # 카운터 올리지 않음 (이미 상한)
                    print(f"[INFO] 상한 초과분 요약 발송 완료: {total_overflow}건")
                else:
                    print(f"[ERROR] 상한 초과분 요약 발송 실패: {result}")
        else:
            if dry_run:
                print(f"\n[DRY-RUN] 21:00 이전 → 상한 초과분 {total_overflow}건 수집 완료. "
                      f"발송 보류 (21:00 크론에서 요약 발송 예정).")
            else:
                print(f"[INFO] 상한 초과분 {total_overflow}건 수집. 21:00까지 발송 보류.")

    # === 상태 저장 (dry-run에서는 하지 않음) ===
    if not dry_run:
        if new_notifications:
            notified_files.update(new_notifications)
            state['notified_files'] = list(notified_files)
            save_state(state)
            print(f"[INFO] 상태 저장 완료: {len(new_notifications)}건 신규 알림.")
    else:
        print(f"\n[DRY-RUN] 상태 파일 저장 안 함 (dry-run). "
              f"신규 알림 {len(new_notifications)}건 (모의).")

    # dry-run 요약
    if dry_run:
        print(f"\n[DRY-RUN] === 처리 완료 요약 ===")
        print(f"  사장님 앞 수집: {len(boss_unread_files)}건")
        print(f"  상한 초과 수집: {len(overflow_files)}건")
        print(f"  오늘 발송 건수(모의): {count_today_sent(state)}")
        if boss_unread_files:
            now_hour = datetime.now().hour
            if now_hour >= 21:
                print(f"  → 21:00 이후: 사장님 요약 '{build_boss_summary_message(len(boss_unread_files))}' 발송 예정")
            else:
                print(f"  → 21:00 이전: 사장님 요약 보류 (다음 크론까지)")
        if overflow_files:
            now_hour = datetime.now().hour
            if now_hour >= 21:
                print(f"  → 21:00 이후: overflow 요약 '{build_overflow_summary_message(len(overflow_files))}' 발송 예정")
            else:
                print(f"  → 21:00 이전: overflow 요약 보류 (다음 크론까지)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
