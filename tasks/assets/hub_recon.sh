#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 알림벨(폼 응답 변환 함수)을 설치하기 전에 GCP 쪽 준비 상태를 읽기만 해서 점검한다. 아무것도 만들거나 켜지 않는다.
# 결과에는 프로젝트 id가 들어가므로 공개 저장소에 올리지 않는다: 비공개 저장소 simplifier-cxo-db 이슈 425에 댓글로 남기고, 공개 저장소에는 "점검 끝남" 알림 파일만 올린다.
set -u
OUT=C:/work/_ops/hub
mkdir -p "$OUT"
R="$OUT/recon.txt"
{
  echo "[타미 점검 $(date '+%F %T')] 알림벨 설치 전 GCP 점검(읽기 전용)"
  echo "- gcloud: $(gcloud --version 2>&1 | head -n 1)"
  echo "- 로그인된 계정 수: $(gcloud auth list --format='value(account)' 2>/dev/null | wc -l)"
  echo "- 활성 계정의 도메인: $(gcloud config get-value account 2>/dev/null | sed 's/.*@//')"
  P="$(gcloud config get-value project 2>/dev/null)"
  echo "- 현재 프로젝트: $P"
  echo "- 기본 리전 설정: functions=$(gcloud config get-value functions/region 2>/dev/null) run=$(gcloud config get-value run/region 2>/dev/null) compute=$(gcloud config get-value compute/region 2>/dev/null)"
  echo "## 프로젝트 목록(아이디, 이름)"
  gcloud projects list --format='value(projectId,name)' 2>&1 | head -n 15
  if [ -n "$P" ]; then
    echo "## 현재 프로젝트에서 켜진 관련 서비스"
    gcloud services list --enabled --project "$P" --format='value(config.name)' 2>&1 | grep -E 'run\.|cloudfunctions|cloudbuild|secretmanager|artifactregistry' || echo "(관련 서비스 없음 또는 조회 실패)"
  fi
} > "$R" 2>&1
gh issue comment 425 --repo hansunghee7/simplifier-cxo-db --body-file "$R" 2>&1 | tail -n 1
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p notify
echo "알림벨 설치 전 GCP 점검 끝: 결과는 비공개 이슈 425 댓글에 있음" > notify/20261008-hub-recon-done.md
git add notify/20261008-hub-recon-done.md
git commit -q -m "notify: 알림벨 설치 전 GCP 점검 끝(결과는 비공개 이슈)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "recon publish rc=$?"
