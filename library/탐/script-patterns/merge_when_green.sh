#!/usr/bin/env bash
# 체크가 등록될 때까지 기다린 뒤(최대 4분), 전부 통과일 때만 병합한다. 실패하면 병합하지 않는다.
N=$1; L=C:/work/_ops/pr${N}_merge.log
for i in $(seq 1 24); do o=$(gh pr checks $N 2>&1); echo "$o" | grep -qi "no checks" || break; sleep 10; done
gh pr checks $N --watch --interval 20 >> $L 2>&1; rc=$?; echo "checks rc=$rc" >> $L
if [ $rc -eq 0 ]; then gh pr merge $N --squash --delete-branch >> $L 2>&1; echo "merge rc=$?" >> $L; fi
echo "MERGE-DONE pr=$N" >> $L
