#!/usr/bin/env bash
# 탐 2026-10-08: 소통 전용 레인 상태 한눈에(읽기 전용, 구PC에서). 값·토큰은 출력하지 않는다.
echo "--- crontab(감시)"; crontab -l 2>/dev/null | grep pending_watchdog || echo "(없음)"
echo "--- 감시 로그 마지막 3줄"; tail -n 3 "$HOME/.pending_watchdog.log" 2>/dev/null || echo "(없음)"
echo "--- 텔레그램 접수 서비스"; systemctl --user is-active telegram-inbox.service 2>/dev/null || echo "(설치 안 됨 또는 중지)"
echo "--- 접수 로그 마지막 3줄"; tail -n 3 "$HOME/.telegram_inbox.log" 2>/dev/null || echo "(없음)"
echo "--- date"; date -u +%FT%TZ
