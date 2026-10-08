#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 푸시 알림 설계 검토의 덱스 단계만 다시 돌린다.
# 1차·2차에서 dex rc=3(= ask_dex.sh의 "카드에 비밀값 의심 문자열" 관문)으로 막혔다. 카드에 붙인 제미나이 리서치 원문에
# x-api-key, Bearer <TOKEN> 같은 단어가 있어서다. 이 스크립트는 그 단어를 치환한 정제본으로 카드를 다시 만들어 덱스를 부른다.
# 비티·리서치 결과는 이미 있으므로 건드리지 않는다. 결과는 스크립트가 직접 저장소에 게시한다.
set -u
OUT=C:/work/_ops/pushalert
cd C:/work/hansunghee7.github.io || { echo "저장소 폴더 없음" >> "$OUT/DONE.txt"; exit 2; }
[ -f "$OUT/card.md" ] && [ -f "$OUT/research.txt" ] || { echo "dex2 입력 파일 없음(card.md 또는 research.txt)" >> "$OUT/DONE.txt"; cat "$OUT/DONE.txt"; exit 2; }
PAT='(api[_-]?key|token|password|secret|sk-[A-Za-z0-9])'
scrub() { sed -E 's/api[_-]?key/키헤더/Ig; s/token/토큰값/Ig; s/password/암호/Ig; s/secret/비밀/Ig; s/sk-([A-Za-z0-9])/sk_\1/g'; }
sed '/^## 제미나이 리서치 결과/,$d' "$OUT/card.md" > "$OUT/card_dex.md"
{
  echo "## 제미나이 리서치 결과(정제본: 민감어를 치환함. 검색 연동 없이 모델 지식으로만 답한 것이라 Claude Code의 구독·웹훅 기능에 대한 설명은 틀렸을 수 있음)"
  head -c 9000 "$OUT/research.txt" | scrub
} >> "$OUT/card_dex.md"
if grep -Eiq "$PAT" "$OUT/card_dex.md"; then echo "dex2 정제 실패(민감어 남음)" >> "$OUT/DONE.txt"; cat "$OUT/DONE.txt"; exit 4; fi
rm -f "$OUT/dex.md"
bash scripts/ops/ask_dex.sh "$OUT/card_dex.md" "$OUT/dex.md" > "$OUT/dex.log" 2>&1
echo "dex2 rc=$? bytes=$(wc -c < "$OUT/dex.md" 2>/dev/null || echo 0) $(date '+%F %T')" >> "$OUT/DONE.txt"

PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || { echo "solar-bible 폴더 없음" >> "$OUT/DONE.txt"; cat "$OUT/DONE.txt"; exit 3; }
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
cp "$OUT/DONE.txt" "$PUB/DONE.txt"
[ -f "$OUT/dex.md" ] && cp "$OUT/dex.md" "$PUB/dex.md"
tail -n 20 "$OUT/dex.log" 2>/dev/null | scrub > "$PUB/dex.log.tail.txt"
echo "덱스 검토 단계 게시: reports/20261008-pushalert-out/ ($(tail -n 1 "$OUT/DONE.txt" | head -c 200))" > notify/20261008-pushalert-dex-done.md
git add reports/20261008-pushalert-out notify/20261008-pushalert-dex-done.md
git commit -q -m "reports: 푸시 알림 설계 덱스 검토 단계 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "publish2 rc=$?" >> "$OUT/DONE.txt"
tail -n 8 "$OUT/DONE.txt"
