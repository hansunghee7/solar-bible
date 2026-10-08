#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08 v2: 알림벨을 설치하기 전에 GCP 쪽 준비 상태를 읽기만 해서 점검한다. 아무것도 만들거나 켜지 않는다.
# v2 변경: 1차 점검에서 git-bash의 gcloud 래퍼가 "C:\c\Users\..." 경로 오류로 죽었다(경로 변환 문제, 덱스와 같은 종류). 그래서 cmd.exe를 거쳐 gcloud를 부른다.
# 결과에는 프로젝트 id가 들어가므로 공개 저장소에 올리지 않는다: 비공개 저장소 simplifier-cxo-db 이슈 425에 댓글로 남기고, 공개 저장소에는 "점검 끝남" 알림 파일만 올린다.
set -u
OUT=C:/work/_ops/hub
mkdir -p "$OUT"
R="$OUT/recon2.txt"
g() { cmd.exe //c "gcloud $*" 2>&1 | tr -d '\r'; }
{
  echo "[타미 점검2 $(date '+%F %T')] 알림벨 설치 전 GCP 점검(읽기 전용, cmd.exe 경유)"
  echo "- gcloud: $(g --version | head -n 1)"
  echo "- 로그인된 계정 수: $(g auth list --format=value\(account\) | grep -c '@')"
  echo "- 활성 계정의 도메인: $(g config get-value account | sed 's/.*@//' | tail -n 1)"
  P="$(g config get-value project | tail -n 1)"
  echo "- 현재 프로젝트: $P"
  echo "- 기본 리전 설정: functions=$(g config get-value functions/region | tail -n 1) run=$(g config get-value run/region | tail -n 1) compute=$(g config get-value compute/region | tail -n 1)"
  echo "## 프로젝트 목록(아이디, 이름)"
  g projects list --format=value\(projectId,name\) | head -n 15
  if [ -n "$P" ] && [ "$P" != "(unset)" ]; then
    echo "## 현재 프로젝트에서 켜진 관련 서비스"
    g services list --enabled --project "$P" --format=value\(config.name\) | grep -E 'run\.|cloudfunctions|cloudbuild|secretmanager|artifactregistry' || echo "(관련 서비스 없음 또는 조회 실패)"
  fi
} > "$R" 2>&1
gh issue comment 425 --repo hansunghee7/simplifier-cxo-db --body-file "$R" 2>&1 | tail -n 1
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p notify
echo "알림벨 설치 전 GCP 점검2 끝: 결과는 비공개 이슈 425 댓글에 있음" > notify/20261008-hub-recon2-done.md
git add notify/20261008-hub-recon2-done.md
git commit -q -m "notify: 알림벨 설치 전 GCP 점검2 끝(결과는 비공개 이슈)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "recon2 publish rc=$?"
