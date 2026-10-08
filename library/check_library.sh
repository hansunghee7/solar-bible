#!/usr/bin/env bash
# 도서관 자체 점검(LLM 없음): 각 항목 폴더에 run.sh, verify.sh, evidence.md, SKILL.md가 있는지 확인한다.
# 출처 발췌처럼 아직 미검증인 항목(README.md만 있음)은 "미검증"으로 따로 센다. 마지막 줄 LIBRARY OK/FAIL.
cd "$(dirname "$0")"; ok=0; unv=0; bad=""
for d in */*/; do
  [ -d "$d" ] || continue
  if [ -f "$d/run.sh" ] && [ -f "$d/verify.sh" ] && [ -f "$d/evidence.md" ] && [ -f "$d/SKILL.md" ]; then ok=$((ok+1))
  elif [ -f "$d/README.md" ] && [ ! -f "$d/run.sh" ]; then unv=$((unv+1)); echo "미검증: $d"
  else bad="$bad $d"; fi
done
echo "검증 항목 $ok개, 미검증 $unv개"
[ -z "$bad" ] && echo "LIBRARY OK" || echo "LIBRARY FAIL(파일 부족:$bad)"
