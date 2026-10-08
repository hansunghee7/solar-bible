#!/usr/bin/env bash
# 탐(클라우드) 2026-10-08: 덱스 자문을 다시 받는다. 진단3에서 "작업 폴더로 이동한 뒤 -C 없이 실행"이 되는 것으로 확인됐다(rc=0, 답 파일 생성).
# ask_dex.sh(경로 수정은 병합됐지만 로컬 PC가 최신을 받았는지 모름)를 거치지 않고 codex를 직접 부른다. 읽기 전용 샌드박스, 카드는 표준입력으로 넘긴다.
# 카드 card_dex.md는 이미 비밀 의심 단어를 치환한 정제본이다.
# 2026-10-08 수정: 재실행에서 codex가 1초 만에 "input is not valid UTF-8 (invalid byte at offset 12621)"로 실패했다.
#   카드를 만들 때 바이트 수로 잘라 한글 한 글자가 중간에 끊겼기 때문으로 보인다. 호출 전에 잘못된 바이트를 버린 사본(card_dex.utf8.md)을 만들어 넘긴다.
set -u
OUT=C:/work/_ops/pushalert
W="C:/work/_ops/dex/topicwork"
scrub() { sed -E 's/(api[_-]?key|token|password|secret)[^ ]*/[민감어 줄임]/Ig; s/sk-[A-Za-z0-9_-]+/[키 줄임]/g'; }
[ -f "$OUT/card_dex.md" ] || { echo "dex3 카드 없음" >> "$OUT/DONE.txt"; echo "dex3 publish rc=2"; exit 2; }
python -X utf8 -c "import sys; d=open(sys.argv[1],'rb').read(); open(sys.argv[2],'wb').write(d.decode('utf-8','ignore').encode('utf-8'))" "$OUT/card_dex.md" "$OUT/card_dex.utf8.md" || { echo "dex4 카드 정리 실패" >> "$OUT/DONE.txt"; }
rm -f "$OUT/dex.md"
t0=$(date +%s); rc=0
( cd "$W" && timeout 600 codex exec --sandbox read-only -o "$OUT/dex.md" - < "$OUT/card_dex.utf8.md" > "$OUT/dex.md.log" 2>&1 ) || rc=$?
echo "dex4 rc=$rc bytes=$(wc -c < "$OUT/dex.md" 2>/dev/null || echo 0) sec=$(( $(date +%s)-t0 )) $(date '+%F %T')" >> "$OUT/DONE.txt"
PUB=C:/work/solar-bible/reports/20261008-pushalert-out
cd C:/work/solar-bible || exit 3
git pull --rebase --autostash --quiet 2>/dev/null
mkdir -p "$PUB" notify
cp "$OUT/DONE.txt" "$PUB/DONE.txt"
[ -s "$OUT/dex.md" ] && scrub < "$OUT/dex.md" > "$PUB/dex.md"
tail -n 20 "$OUT/dex.md.log" 2>/dev/null | scrub > "$PUB/dex.md.log.tail.txt"
echo "덱스 자문 재실행 게시: reports/20261008-pushalert-out/ ($(tail -n 1 "$OUT/DONE.txt" | head -c 200))" > notify/20261008-pushalert-dex4-done.md
git add reports/20261008-pushalert-out notify/20261008-pushalert-dex4-done.md
git commit -q -m "reports: 덱스 자문 재실행 결과(스크립트가 직접 게시)" && { git push origin main 2>&1 || { git pull --rebase --autostash --quiet; git push origin main 2>&1; }; }
echo "dex4 publish rc=$?"
