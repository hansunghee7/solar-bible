#!/usr/bin/env bash
# 탐 2026-10-08: 구PC의 "소통 전용 레인" 설치기(여러 번 실행해도 안전). 타미 줄과 분리돼 구PC에서 상시 도는 스크립트 묶음이다. LLM을 거치지 않는다.
# 구성: (1) 폴러 감시 cron(pending_watchdog.sh) 보장 (2) 텔레그램 답장 접수 서비스(telegram_inbox.py) — 환경 파일과 클론이 있을 때만 설치
# 사용(구PC에서): bash comm_lane_install.sh <solar-bible 클론 경로> [cxo-db 클론 경로]
# 비밀값은 출력하지 않는다. 환경 파일 ~/.config/comm-lane/env 에 TG_BOT_TOKEN, TG_ALLOWED_CHAT_ID 가 있어야 텔레그램 서비스가 설치된다(사람이 만든다).
set -u
PUB=${1:?solar-bible 클론 경로}; PRIV=${2:-$HOME/simplifier-cxo-db}
ENVF="$HOME/.config/comm-lane/env"
echo "== 1. 폴러 감시 cron"
LINE="*/5 * * * * cd $PUB && bash tasks/assets/pending_watchdog.sh $PUB 600 >> \$HOME/.pending_watchdog.log 2>&1"
if crontab -l 2>/dev/null | grep -q pending_watchdog; then echo "이미 등록됨"; else (crontab -l 2>/dev/null; echo "$LINE") | crontab - && echo "등록함"; fi
echo "== 2. 텔레그램 답장 접수"
if [ ! -f "$ENVF" ]; then echo "건너뜀: 환경 파일 없음($ENVF). 봇 확인 후 사람이 TG_BOT_TOKEN, TG_ALLOWED_CHAT_ID를 넣어야 한다"
elif ! grep -q '^TG_BOT_TOKEN=' "$ENVF" || ! grep -q '^TG_ALLOWED_CHAT_ID=' "$ENVF"; then echo "건너뜀: 환경 파일에 필요한 항목이 없음(값은 출력하지 않는다)"
elif [ ! -d "$PRIV/.git" ]; then echo "건너뜀: 비공개 저장소 클론이 없음($PRIV)"
else
  mkdir -p "$HOME/.config/systemd/user"
  cat > "$HOME/.config/systemd/user/telegram-inbox.service" <<EOF
[Unit]
Description=사장님 텔레그램 답장 접수(소통 전용 레인)
[Service]
EnvironmentFile=$ENVF
Environment=PUBLIC_REPO=$PUB
Environment=PRIVATE_REPO=$PRIV
ExecStart=/usr/bin/python3 $PUB/tasks/assets/telegram_inbox.py
Restart=always
RestartSec=10
StandardOutput=append:%h/.telegram_inbox.log
StandardError=append:%h/.telegram_inbox.log
[Install]
WantedBy=default.target
EOF
  systemctl --user daemon-reload && systemctl --user enable --now telegram-inbox.service && echo "서비스 설치·시작함" || echo "서비스 설치 실패: 사람 확인 필요"
  echo "참고: 구PC가 재부팅된 뒤에도 로그인 없이 돌려면 loginctl enable-linger \$USER 가 필요할 수 있다(관리자 확인)"
fi
