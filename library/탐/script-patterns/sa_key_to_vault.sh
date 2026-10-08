#!/usr/bin/env bash
# 서비스 계정 키를 발급해 값을 화면에 내지 않고 (1) 격리 설정에서 Vertex 호출 시험 (2) 카빗 패스 금고에 put (3) 임시 파일과 격리 설정 삭제.
set -u
P=simplifier-vertex-credit; SA=tam-vertex@$P.iam.gserviceaccount.com
T=$(mktemp -d); K="$T/k.json"; export CLOUDSDK_CONFIG="$T/cfg"; mkdir -p "$CLOUDSDK_CONFIG"
cleanup(){ [ -f "$K" ] && { dd if=/dev/zero of="$K" bs=1k count=4 2>/dev/null; rm -f "$K"; }; rm -rf "$T"; }
trap cleanup EXIT
echo "== 0. 정책 상태"; CLOUDSDK_CONFIG= gcloud resource-manager org-policies describe iam.disableServiceAccountKeyCreation --effective --project=$P 2>&1 | head -3
echo "== 1. 키 발급(값 비출력)"
CLOUDSDK_CONFIG= gcloud iam service-accounts keys create "$K" --iam-account=$SA --project=$P 2>&1 | sed 's/key \[[0-9a-f]*\]/key [id 숨김]/' | head -3
[ -s "$K" ] || { echo "FAIL 키 파일 없음"; exit 10; }
echo "(키 전파 대기 75초)"; sleep 75
echo "== 2. 격리 설정으로 서비스 계정 로그인 + Vertex 최소 호출"
gcloud auth activate-service-account --key-file="$K" --quiet 2>&1 | head -1 | cut -c1-80
TOK=$(gcloud auth print-access-token 2>/dev/null)
code=$(curl -s -m 40 -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" "https://aiplatform.googleapis.com/v1/projects/$P/locations/global/publishers/google/models/gemini-3.6-flash:generateContent" -d '{"contents":[{"role":"user","parts":[{"text":"OK라고만 답해"}]}],"generationConfig":{"maxOutputTokens":8}}'); echo "vertex http=$code"
unset TOK
[ "$code" = 200 ] || { echo "FAIL 시험 실패: 금고에 넣지 않음"; exit 11; }
echo "== 3. 금고에 put(값 비출력)"
unset CLOUDSDK_CONFIG
cd C:/work/saegim-pass/host && python pass.py --service "Google Cloud" --from 탐 put "Vertex tam-vertex 서비스 계정 키" < "$K" 2>&1 | sed 's/"value"[^,}]*//' | head -6 | cut -c1-200
echo "== 4. 정리"; cleanup; trap - EXIT; echo "임시 파일 삭제됨"
python pass.py list 2>&1 | grep -c "tam-vertex"
