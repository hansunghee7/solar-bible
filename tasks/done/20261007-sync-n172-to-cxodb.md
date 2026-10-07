# 헤르메스 카드: N172 자료와 탐 기억 파일을 비공개 저장소로 복사 (탐 -> 헤르메스)

중요: 파일 내용을 열어 읽거나 화면에 출력하지 마라(cat, type, Get-Content, head 금지). 파일 이름·크기·개수만 다뤄라. 키·토큰·비밀번호를 다루지 마라. 복사 대상 저장소는 비공개 저장소 `C:/work/simplifier-cxo-db`뿐이다. 이 공개 저장소(solar-bible)에는 어떤 결과도 올리지 마라. main에는 push하지 마라.
1. `C:/work/simplifier-cxo-db`에서 `git fetch origin main` 후 브랜치 `sync/n172-1007`을 만든다(`git switch -c sync/n172-1007 origin/main`, 이미 있으면 `git switch`).
2. 폴더 `reports/n172_sync_1007`을 만든다.
3. 복사한다(내용은 보지 마라):
   a. `C:/work/_ops/n172/` 안의 모든 파일(하위 폴더 포함)을 `reports/n172_sync_1007/n172/`로. 크기가 1MB를 넘거나 이름에 `.env`, `key`, `token`, `secret`이 든 파일은 빼고 그 이름을 `reports/n172_sync_1007/skipped.txt`에 적는다.
   b. `C:/work/_ops/n174/`의 `r65.md`, `r35.md`, `keeper_request_v7.html`을 `reports/n172_sync_1007/n174/`로(없는 파일은 건너뛰고 skipped.txt에 적는다).
   c. `C:/work/_ops/n173/boss_needed.md`가 있으면 `reports/n172_sync_1007/n173/`로.
   d. `C:/work/_ops` 안(하위 포함)에서 이름에 `answer_check` 또는 `answer-check`가 든 로그·결과 파일을 `reports/n172_sync_1007/logs/`로.
   e. 탐의 로컬 기억 폴더: `C:/Users/PC/.claude/projects` 아래에서 `MEMORY.md`가 있는 폴더 중 가장 최근에 수정된 것. 그 폴더의 `.md` 파일 중 `reports/tam_memory/`에 같은 이름이 없거나 크기가 다른 것만 `reports/tam_memory/`로 덮어 복사하고, 새로 생긴 수와 바뀐 수를 센다.
4. 기계적 비밀 검사: 3단계에서 복사한 파일 전체에 `grep -rIlE "AIza|sk-[A-Za-z0-9]|eyJ[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY|ghp_|xox[bp]-|password[[:space:]]*[:=]|api[_-]?key[[:space:]]*[:=]"`를 실행한다. 걸린 파일은 복사본을 지우고(원본은 건드리지 마라) 이름만 `reports/n172_sync_1007/flagged.txt`에 적는다. 걸린 내용은 출력하지 마라.
5. `git add reports`, 커밋 메시지 "N172 자료 동기화 1007(타미)", `git push -u origin sync/n172-1007`.
끝 조건: push가 끝나면 끝. 보고는 한 줄: "복사 N개, 제외 N개, 비밀 검사에 걸린 N개, 기억 새 N·바뀐 N, 브랜치 sync/n172-1007".
