#!/usr/bin/env python3
# mailbox_courier.py - 긴급 우편 배달 스크립트 (Telegram Bot API 직접 발송)
# 2026-09-19 개정: 사장님 알림 텔레그램 한 줄 통일, 하루 20건 상한, 쌓인 우편 요약
# 2026-09-19 재작업: --dry-run 옵션 추가, boss_key 인자 버그 수정, timedelta 제거

import os
import sys
import json
import subprocess
import requests
import argparse
from pathlib import Path
from datetime import datetime, date, time as dt_time

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
    """상태 파일 로드 (발송 이력 + 날짜별 카운트)"""
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open('r', encoding='utf-8') as f:
                data = json.load(f)
            # 새 형식: {notified_files: [...], daily_counts: {YYYY-MM-DD: N}}
            if isinstance(data, dict) and 'notified_files' in data:
                return data
            # 구 형식(집합) 호환
            if isinstance(data, list):
                return {
                    'notified_files': [norm_key(x) for x in data],
                    'daily_counts': {}
                }
            return {
                'notified_files': set(data.keys()) if isinstance(data, dict) else set(),
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

def build_message_forBoss(sender, subject, ask=''):
    """사장님 앞 한 줄 메시지.
    형식: 📬 탐→사장님: <제목>
    요청이 있으면 둘째 줄 👉 ..."""
    lines = [f"📬 {sender}→사장님: {subject}"]
    if ask:
        lines.append(f"👉 {shorten(ask, 80)}")
    return '\n'.join(lines)

def build_message_others(sender, recipient, subject, body_first, ask=''):
    """기존 긴급 우편 메시지 (3~4줄)."""
    lines = [
        f"📬 긴급 우편 | {sender}→{recipient}",
        f"제목: {subject}",
    ]
    if body_first:
        lines.append(f"요약: {shorten(body_first, 60)}")
    lines.append(f"👉 {shorten(ask, 60)}" if ask else "👉 우편함에서 내용을 확인해 주세요")
    return '\n'.join(lines)

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
    """한국 시간 기준 오늘 날짜 문자열 YYYY-MM-DD"""
    now_kst = datetime.now()  # 이 PC의 시계가 이미 한국 시간(KST)이다. +9시간을 더하면 날짜가 틀린다.
    return now_kst.strftime('%Y-%m-%d')

def should_send_to_boss_today(state):
    """사장님 앞 오늘 이미 요약 발송했는지 확인. boss_key 인자 제거."""
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

def build_boss_overflow_message(total_unread):
    """사장님 앞 쌓인 우편 요약 (저녁 발송용)."""
    return f"📬 오늘 쌓인 우편 {total_unread}건"

def process_mailbox(mailbox_dir, token, chat_id, state, dry_run=False):
    """메일함 처리 메인 로직. dry_run=True이면 실제 발송 없이 출력만."""
    notified_files = set(state.get('notified_files', []))
    if not isinstance(notified_files, set):
        notified_files = set(notified_files)

    new_notifications = []
    boss_unread_files = []

    # 우편물 파일 검색
    md_files = sorted(mailbox_dir.rglob('*.md'))
    
    for md_file in md_files:
        try:
            rel_path = norm_key(md_file.relative_to(mailbox_dir))
        except ValueError:
            rel_path = norm_key(md_file)

        if rel_path in notified_files:
            continue

        recipient, sender, subject, body_first, ask = extract_metadata_and_body(md_file)
        if not all([recipient, sender, subject]):
            continue

        is_boss = (recipient == '사장님')
        is_everyone = (recipient == '전체')

        if is_boss:
            boss_unread_files.append((rel_path, sender, subject, ask))
            continue

        if not has_urgent_flag(md_file):
            continue

        if not can_send_today(state):
            continue

        message = build_message_others(sender, recipient, subject, body_first, ask)
        
        if dry_run:
            print(f"[DRY-RUN] 발송 예정: {rel_path}")
            print(f"  받는이: {recipient}")
            print(f"  보낸이: {sender}")
            print(f"  제목: {subject}")
            print(f"  메시지:\n{message}")
            print()
            new_notifications.append(rel_path)
            inc_today_count(state)
        else:
            result = send_telegram(token, chat_id, message)
            if result.get('ok'):
                new_notifications.append(rel_path)
                inc_today_count(state)

    # 사장님 앞 쌓인 우편 처리
    if boss_unread_files:
        if should_send_to_boss_today(state):
            total = len(boss_unread_files)
            summary_msg = f"📬 사장님 앞 우편 {total}건 쌓임"
            
            if dry_run:
                print(f"[DRY-RUN] 사장님 앞 요약 발송 예정: {total}건")
                print(f"  메시지: {summary_msg}")
                print()
                mark_boss_summarized(state)
                inc_today_count(state)
                new_notifications.append(f"_boss_summary_{get_today_str()}")
            else:
                if can_send_today(state):
                    result = send_telegram(token, chat_id, summary_msg)
                    if result.get('ok'):
                        new_notifications.append(f"_boss_summary_{get_today_str()}")
                        mark_boss_summarized(state)
                        inc_today_count(state)

    # 상태 기록 (dry_run에서는 상태 파일 쓰지 않음)
    if new_notifications and not dry_run:
        notified_files.update(new_notifications)
        state['notified_files'] = list(notified_files)
        save_state(state)

    return new_notifications

def main():
    parser = argparse.ArgumentParser(description='우편 배달 스크립트')
    parser.add_argument('--dry-run', action='store_true', help='실제 발송 없이 출력만')
    parser.add_argument('--mailbox-dir', type=str, help='메일함 디렉토리 (기본: DEFAULT_MAILBOX_DIR)')
    args = parser.parse_args()

    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN', '')
    allowed_users = env.get('TELEGRAM_ALLOWED_USERS', '')

    if not token or not allowed_users:
        print("[ERROR] TELEGRAM_BOT_TOKEN 또는 TELEGRAM_ALLOWED_USERS가 설정되지 않음")
        sys.exit(1)

    chat_id = allowed_users.split(',')[0].strip()

    if args.mailbox_dir:
        mailbox_dir = Path(args.mailbox_dir)
    else:
        mailbox_dir = DEFAULT_MAILBOX_DIR

    if mailbox_dir == DEFAULT_MAILBOX_DIR:
        run_git_pull()

    state = load_state()
    
    print(f"[DRY-RUN 모드]" if args.dry_run else "[실제 발송 모드]")
    print(f"메일함: {mailbox_dir}")
    print(f"오늘 날짜: {get_today_str()}")
    print(f"오늘 발송 건수: {count_today_sent(state)}")
    print(f"일일 상한: {DAILY_LIMIT}")
    print(f"사장님 요약 발송 여부: {'이미 발송됨' if not should_send_to_boss_today(state) else '미발송'}")
    print("-" * 60)
    
    new_notifications = process_mailbox(mailbox_dir, token, chat_id, state, dry_run=args.dry_run)
    
    print("-" * 60)
    print(f"총 {len(new_notifications)}건 처리됨")
    if args.dry_run:
        print("(dry-run: 상태 파일 변경 없음)")
    
    sys.exit(0)

if __name__ == '__main__':
    main()
