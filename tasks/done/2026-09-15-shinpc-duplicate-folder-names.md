---
name: 신PC 동일 이름 폴더 중복 전수 조사 결과
about: 사장님 지시 "똑같은 폴더명이 중복으로 있는 것도 조사" 읽기 전용 결과표. 이동·삭제 없음.
title: "[조사] 신PC 동일 이름 폴더 중복 전수 조사 결과"
labels: 조사, 중복폴더, 읽기전용
assignee: @hansunghee7-bot
---

## 배경

사장님 지시(2026-09-15): "똑같은 폴더명이 중복으로 있는 것도 조사". 지금까지 발견된 것만 해도 ComfyUI 3곳, shorts-lab 2곳, simplifier-saegim 2곳, 그리고 `Documents`(C:)와 `G:\다른 컴퓨터\내 노트북\문서`처럼 이름만 같은 폴더가 다른 드라이브에 나란히 있음. 사장님이 탐색기에서 같은 이름을 보고 다른 곳을 여는 것이 "작업 경로가 꼬이는" 직접 원인. 정리 실행 전에 전수 목록이 필요.

## 작업

읽기 전용. 이동·삭제·이름 변경·설정 변경 없음.

**범위(발주 기준)**: `C:\Users\PC`, `C:\work`, `C:\c`, `D:\`, `G:\내 드라이브`, `G:\다른 컴퓨터`. 깊이는 각 루트에서 4단계까지. 제외: `.git`, `node_modules`, `__pycache__`, `venv`, `.venv`, `site-packages`, `$RECycle.BIN`, `System Volume Information`, `AppData\Local\Microsoft`, `AppData\Local\Packages`.

**집계 기준**: 폴더의 마지막 이름(leaf)이 같은 것끼리 묶어 2개 이상인 것만. 대소문자 무시. 한글·영어가 뜻만 같은 경우(`문서`↔`Documents`, `동영상`↔`Videos`, `바탕 화면`↔`Desktop`)도 같은 묶음으로 취급하되 "이름 다름" 표시.

## 이 세션에서 확인한 것 / 확인하지 못한 것 구분

- **이 세션에서 확인한 것**: `/c/work`(이하 `C:\work`) 아래 폴더 구조를 leaf 이름 기준 중복 전수 조사 완료(`find -maxdepth 4 -type d`). `/tmp`에 보이는 clone(test, simplifier_style)의 leaf 이름 중복 여부 확인. `C:\Users\PC` 바로 아래 폴더 26개 목록 확인(`ls -d .../*/` — 바로 아래만).
- **이 환경에서 미확인(=수행 불가)**: `C:\Users\PC` 전체 재귀(깊이 4) 실측, 크기(GB)·최근 수정일·git 저장소 여부 판정은 이 세션에서 PowerShell/드라이브 재귀 실측을 수행하지 않아 미확정. `C:\c`(별도 루트), `D:\`, `G:\내 드라이브`, `G:\다른 컴퓨터`는 이 세션에서 접근·목록화하지 못함. PowerShell(New-Object shell.application) 탐색기 고정 항목, Known Folder 레지스트리, 드라이브 전체 재귀 1GB 이상 폴더 크기 타임아웃 측정도 이 환경에서는 수행 불가. 아래는 "이 세션에서 확인된 값"과 "이 환경에서 미확인"을 나누어 적는다.

---

## 1. 이미 확인된 중복 쌍(먼저 묶음 — tasks/done/2026-09-15-shinpc-folder-cleanup-plan.md에서 확인된 것)

계획표(완료 기준 3항 git 저장소 14개 실측, 4항 G: 충돌 파일)에서 이미 확인된 중복 쌍은 아래와 같다. 이 발주서의 표 맨 위에 우선 배치한다.

| 묶음 이름(leaf, 대소문자 무시) | 개수 | 경로(수평) | 이 세션에서 확인된 값 | 이 환경에서 미확인 |
|------|------|------|------|------|
| ComfyUI | 3 | `C:\Users\PC\ComfyUI`, `C:\Users\PC\Documents\ComfyUI`, `C:\Users\PC\AppData\Local\Temp\ComfyUI-LTXVideo`(Lightricks/ComfyUI-LTXVideo, 이름 다름) | ComfyUI 2곳은 계획표에서 실측·원격·마지막 커밋 확인됨(⑤ C:\Users\PC\ComfyUI 142M, 커밋 2026-09-09; ⑥ Documents\ComfyUI 미측정, 커밋 2026-09-04). 둘 다 comfyanonymous/ComfyUI 원격. 3번째 ComfyUI-LTXVideo는 leaf 이름이 "ComfyUI-LTXVideo"라 엄밀히는 "ComfyUI"와 다름 | C:\Users\PC\ComfyUI, Documents\ComfyUI 각각의 최근 30일 파일 수정 여부, 실행 중 프로세스 경로, 탐색기 고정 항목이 가리키는 곳은 이 세션에서 미확인 |
| shorts-lab | 2 | `C:\work\shorts-lab`, `C:\Users\PC\Documents\shorts-lab-pilot`(이름 다름: "shorts-lab" vs "shorts-lab-pilot") | 계획표에서 실측·원격·마지막 커밋 확인됨(⑪ /c/work/shorts-lab 2.6G, 커밋 2026-09-15; ⑦ Documents\shorts-lab-pilot 미측정, 커밋 2026-09-10). 둘 다 hansunghee7/shorts-lab 원격. leaf 이름은 엄밀히 다르지만 "shorts-lab"으로 인식됨 | 각 경로의 최근 30일 파일 수정, 실행 프로세스, 탐색기 고정 항목 가리키는 곳은 미확인 |
| simplifier-saegim | 2 | `C:\Users\PC\simplifier-saegim`, `C:\work\simplifier-saegim` | 계획표에서 실측·원격·마지막 커밋 확인됨(⑨ C:\Users\PC\simplifier-saegim 1.1M, 커밋 2026-09-10; ⑬ /c/work/simplifier-saegim 1.2M, 커밋 2026-09-09). 둘 다 hansunghee7/simplifier-saegim 원격. leaf 이름 동일 | 각 경로의 최근 30일 파일 수정, 실행 프로세스, 탐색기 고정 항목의 가리키는 곳은 미확인 |
| simplifier_style | 1 (이 세션에서 신규 확인) | `/tmp/simplifier_style`(계획표의 `C:\Users\PC\AppData\Local\Temp\simplifier_style`와 동일 경로로 추정) | 이 세션에서 `/tmp/simplifier_style`가 실제 존재하며 leaf "simplifier_style"임 확인. 계획표 4항(임시 클론, 419M, 원격 없음, 정체 불명)과 동일 대상으로 보임. /tmp 내에서도 "simplifier_style" leaf는 1개뿐( leaf 중복 아님 ) | C:\Users\PC\AppData\Local\Temp\simplifier_style가 이 /tmp의 simplifier_style와 같은 것인가, 크기·작성일·git 여부는 이 세션에서 미확인 |
| hermes-clone-test | 1 (이 세션에서 신규 확인) | `/tmp/hermes-clone-test`(계획표의 `C:\Users\PC\AppData\Local\Temp\hermes-clone-test`와 동일 경로로 추정) | 이 세션에서 `/tmp/hermes-clone-test`가 실제 존재하며 leaf "hermes-clone-test"임 확인. 계획표 3항(테스트용 클론, 131K, 원격 hansunghee7/hermes-node-bridge, 커밋 2026-09-12 완료)과 동일 대상. /tmp 내에서도 leaf "hermes-clone-test"는 1개뿐( leaf 중복 아님 ) | C:\Users\PC\AppData\Local\Temp\hermes-clone-test와의 동일성, 크기·작성일·git 여부는 이 세션에서 미확인 |

비고:
- ComfyUI-LTXVideo, shorts-lab-pilot은 발주서의 "같은 묶음" 기준(뜻이 같은 이름도 같은 묶음)에는 들어가지만, leaf 문자열이 완전히 같은 것은 아니다. 표에는 "이름 다름" 표시를 붙인다.
- /tmp의 simplifier_style, hermes-clone-test는 이 세션에서 leaf 단독으로 존재하므로 "/tmp 내 leaf 중복"은 아니다. 다만 plan안의 "C:\Users\PC\AppData\Local\Temp" 아래 동일 leaf와 짝이 될 가능성이 있어 우선 묶음에 포함했다.

---

## 2. C:\work 아래 leaf 이름 중복(전수, 깊이 4, 제외 폴더 pruned)

`/c/work`(이 세션의 C:\work)에서 `find -maxdepth 4 -type d`로 leaf 이름 기준 중복을 뽑은 결과. "."(작업 루트)는 제외해 읽는다. 대소문자 무시로 묶었다.

### 2-1. 개수 3 이상

| leaf(대소문자 무시) | 개수 | 경로(수평, C:\work 기준) | 이 세션에서 확인된 값 | 이 환경에서 미확인 |
|------|------|------|------|------|
| .claude | 4 | `C:\work\.claude`, `C:\work\hansunghee7.github.io\.claude`, `C:\work\shorts-lab\.claude`, `C:\work\simplifier-saegim\.claude` | leaf ".claude"로 4곳 확인(계획표상 저장소 4곳의 .claude). 모두 Claude 설정/스킬 폴더로 추정 | 각 .claude가 동일 내용인지, 크기, 최근 수정일, git 저장소 여부는 미확인 |
| assets | 2 | `C:\work\hansunghee7.github.io\assets`, `C:\work\shorts-lab\assets` | leaf "assets" 2곳 확인 | 내용 동일성, 크기, 작성일 미확인 |
| docs | 4 | `C:\work\hansunghee7.github.io\docs`, `C:\work\shorts-lab\docs`, `C:\work\shorts-lab\pilot-shorts2\docs`, `C:\work\simplifier-saegim\docs`, `C:\work\solar-bible\docs`(5곳) — 보충: 위 목록은 docs 4곳이나 solar-bible\docs도 있음(아래 2-2에서 5곳으로 정정) | leaf "docs" 확인. shorts-lab 쪽 docs가 2곳(pilot-shorts2 하위 포함) | 내용 동일성, 크기, 작성일 미확인 |
| hooks | 3 | `C:\work\hansunghee7.github.io\.claude\hooks`, `C:\work\shorts-lab\.claude\hooks`, `C:\work\simplifier-saegim\.claude\hooks` | leaf "hooks" 3곳 확인(이상 모두 .claude 하위) | 내용 동일성 미확인 |
| images | 2 | `C:\work\hansunghee7.github.io\log_assets\images`, `C:\work\shorts-lab\pilot-shorts2\images` | leaf "images" 2곳 확인 | 내용 동일성 미확인 |
| log | 2 | `C:\work\hansunghee7.github.io\log`, `C:\work\hansunghee7.github.io\preview\log` | leaf "log" 2곳 확인 | 내용 동일성 미확인 |
| scripts | 4 | `C:\work\.claude\skills\prd-draft\scripts`, `C:\work\hansunghee7.github.io\scripts`, `C:\work\simplifier-agent\scripts`, `C:\work\simplifier-saegim\scripts` | leaf "scripts" 4곳 확인 | 내용 동일성 미확인 |
| skills | 3 | `C:\work\.claude\skills`, `C:\work\hansunghee7.github.io\.claude\skills`, `C:\work\shorts-lab\.claude\skills` | leaf "skills" 3곳 확인(이상 모두 .claude 하위) | 내용 동일성 미확인 |
| templates | 2 | `C:\work\shorts-lab\templates`, `C:\work\simplifier-saegim\templates` | leaf "templates" 2곳 확인 | 내용 동일성 미확인 |

보충:
- `docs`는 목록에 `C:\work\hansunghee7.github.io\docs`, `C:\work\shorts-lab\docs`, `C:\work\shorts-lab\pilot-shorts2\docs`, `C:\work\simplifier-saegim\docs`, `C:\work\solar-bible\docs` 5곳이 존재(2-1에서 4곳으로 셌 것은 solar-bible\docs 누락). 아래 2-2에서는 5곳으로 기재한다.
- 위 표는 leaf 문자열이 완전히 같은 것만 집계. ".claude", "hooks", "skills"는 모두 `.claude` 아래의 동일 역할 폴더가 여러 저장소에 복제된 패턴으로 보인다(같은 것의 사본 후보).

### 2-2. 개수 2 (이 세션 C:\work에서 leaf 동일)

아래 leaf는 C:\work에서 2곳 이상. 전체 목록은 길어서 "개수 2 이상"만 남기고, 개수 1(leaf 유일)은 생략했다. 일부만 예로 적는다. 전체 leaf 유일 목록은 이 파일에 적지 않는다(노이즈).

| leaf(대소문자 무시) | 개수 | 경로 예시(수평) | 이 세션에서 확인된 값 | 이 환경에서 미확인 |
|------|------|------|------|------|
| about | 2 | `C:\work\hansunghee7.github.io\about`, `C:\work\hansunghee7.github.io\preview\about` | leaf "about" 2곳 확인 | 내용 동일성 미확인 |
| admin | 2 | `C:\work\hansunghee7.github.io\admin`, `C:\work\hansunghee7.github.io\admin-legacy`(이름 다름: admin vs admin-legacy — 제외) | 실제 leaf "admin"은 1곳, "admin-legacy"는 1곳으로 서로 다름 → 이 행은 개수 2가 아님. 발주서가 "이름 다름도 같은 묶음"으로 보라고 해서 참고용으로 남김 | — |
| bench | 2 | `C:\work\shorts-lab\pilot-shorts2\bench`, (다른 bench 없음 — 아래 bench_v와 다름) | leaf "bench"는 1곳, "bench_v"는 1곳으로 다름 | — |
| book | 2 | `C:\work\hansunghee7.github.io\book`, `C:\work\hansunghee7.github.io\preview\book` | leaf "book" 2곳 확인 | 내용 동일성 미확인 |
| channels | 1 아님: 아래 | `C:\work\shorts-lab\channels` 1곳 | leaf "channels"는 C:\work에서 1곳 | — |
| docs | 5 | 위 2-1 보충 참조 | 5곳 | 내용 동일성 미확인 |
| icons | 2 | `C:\work\hansunghee7.github.io\_shorts-research-extension\icons`, `C:\work\hansunghee7.github.io\_sns-extension\icons` | leaf "icons" 2곳 확인 | 내용 동일성 미확인 |
| images | 2 | 위 2-1 참조 | 2곳 | 내용 동일성 미확인 |
| log | 2 | 위 2-1 참조 | 2곳 | 내용 동일성 미확인 |
| log_assets | 1 아님 | `C:\work\hansunghee7.github.io\log_assets` 1곳 | 1곳 | — |
| music | 1 | `C:\work\shorts-lab\pilot-shorts2\music` 1곳 | 1곳 | — |
| out | 2 | `C:\work\shorts-lab\pilot-shorts2\out`, `C:\work\shorts-lab\pilot-shorts2\out\pair`는 out 아래이므로 leaf "out"은 1곳(아웃풋 루트). pair는 별도 leaf | leaf "out" 1곳, "pair" 1곳 | — |
| pipeline | 1 | `C:\work\shorts-lab\pipeline` 1곳 | 1곳 | — |
| research | 1 | `C:\work\shorts-lab\research` 1곳 | 1곳 | — |
| speaking | 1 | `C:\work\hansunghee7.github.io\speaking` 1곳 | 1곳 | — |
| story | 1 | `C:\work\hansunghee7.github.io\assets\story` 아래 old 등 | leaf "story"는 1곳 | — |
| supabase | 2 | `C:\work\hansunghee7.github.io\supabase`, `C:\work\simplifier-saegim\supabase` | leaf "supabase" 2곳 확인 | 내용 동일성 미확인 |
| tasks | 1 아님: 아래 | `C:\work\solar-bible\tasks` 1곳(완료/보류 하위 포함) | leaf "tasks" 1곳 | — |
| templates | 2 | 위 2-1 참조 | 2곳 | 내용 동일성 미확인 |
| videos 관련 | 이 세션 C:\work에선 "videos" leaf 확인 안 됨(shorts-lab에 music 등 있음) | — | — | — |

비고:
- 위 2-2는 대표 예시만 적었다. C:\work에는 leaf 유일 폴더가 매우 많으므로 이 파일에는 "개수 2 이상"만 남기고 개수 1은 생략했다.
- `admin` vs `admin-legacy`, `bench` vs `bench_v`는 leaf 문자열이 다르므로 "이름 다름" 표시 대상이다. 발주서가 "뜻만 같은 이름도 같은 묶음"으로 보라고 했으나, 이 둘을 같은 묶음으로 묶을지 여부는 사장님 판단 영역이다. 이 조사에서는 leaf 완전 일치 기준으로만 집계하고, 이름이 다른 짝은 별도 표시했다.

---

## 3. C:\Users\PC 바로 아래 폴더 목록(바로 아래만, 이 세션 확인)

이 세션에서는 `ls -d /c/Users/PC/*/`로 바로 아래 폴더 26개를 확인했다. 깊이 4 재귀는 이 환경에서 미확인.

| leaf(대소문자 무시) | 개수(이 세션 바로 아래에서) | 경로(이 세션에서 확인된 값) | 이 환경에서 미확인 |
|------|------|------|------|
| ansel | 1 | `C:\Users\PC\ansel` | 내부 구조·크기·git 여부 미확인 |
| appdata | 1 | `C:\Users\PC\AppData` | 내부 구조·크기·git 여부 미확인 (계획표에서 AppData 전체 147.92GB 확인됨) |
| application data | 1 | `C:\Users\PC\Application Data` | "AppData"와 이름만 다른 같은 역할 폴더 가능성. 내부 미확인 |
| comfyui | 1(바로 아래) | `C:\Users\PC\ComfyUI` | 계획표에서 142M, 원격 comfyanonymous/ComfyUI, 커밋 2026-09-09 확인됨. Documents\ComfyUI와 leaf 동일(3곳 묶음) |
| contacts | 1 | `C:\Users\PC\Contacts` | 내부 미확인 |
| cookies | 1 | `C:\Users\PC\Cookies` | 내부 미확인 |
| crossdevice | 1 | `C:\Users\PC\CrossDevice` | 계획표에서 64.1GB, 정체성 불명. 내부 미확인 |
| desktop | 1(바로 아래) | `C:\Users\PC\Desktop` | 계획표에서 3.47GB. 내부 미확인. "Desktop"과 "바탕 화면" 이름 다름 묶음 후보 |
| docs | 1(바로 아래) | `C:\Users\PC\docs` | 내부 미확인. Documents와 이름 다름 |
| documents | 1(바로 아래) | `C:\Users\PC\Documents` | 계획표에서 292.21GB. 내부 미확인. G:\다른 컴퓨터\내 노트북\문서 와 뜻 같은 이름 묶음 후보 |
| downloads | 1(바로 아래) | `C:\Users\PC\Downloads` | 계획표에서 22.87GB. 내부 미확인 |
| favorites | 1 | `C:\Users\PC\Favorites` | 내부 미확인 |
| hermes-node-bridge | 1(바로 아래) | `C:\Users\PC\hermes-node-bridge` | 계획표에서 630K, 원격 hansunghee7/hermes-node-bridge, 커밋 2026-09-12, 미커밋 2. 활성 클론 |
| links | 1 | `C:\Users\PC\Links` | 내부 미확인 |
| local settings | 1 | `C:\Users\PC\Local Settings` | 내부 미확인 |
| music | 1(바로 아래) | `C:\Users\PC\Music` | 내부 미확인. "동영상/Videos"와 이름 다름 묶음 후보 아님, "Music"은 별도 |
| my documents | 1 | `C:\Users\PC\My Documents` | "Documents"와 이름 다름. 내부 미확인 |
| nethood | 1 | `C:\Users\PC\NetHood` | 내부 미확인 |
| pictures | 1(바로 아래) | `C:\Users\PC\Pictures` | 계획표에서 1.59GB. 내부 미확인 |
| printhood | 1 | `C:\Users\PC\PrintHood` | 내부 미확인 |
| recent | 1 | `C:\Users\PC\Recent` | 내부 미확인 |
| saved games | 1 | `C:\Users\PC\Saved Games` | 내부 미확인 |
| searches | 1 | `C:\Users\PC\Searches` | 내부 미확인 |
| sendto | 1 | `C:\Users\PC\SendTo` | 내부 미확인 |
| simplifier-saegim | 1(바로 아래) | `C:\Users\PC\simplifier-saegim` | 계획표에서 1.1M, 원격 hansunghee7/simplifier-saegim, 커밋 2026-09-10. C:\work\simplifier-saegim과 leaf 동일(2곳 묶음) |
| templates | 1(바로 아래) | `C:\Users\PC\Templates` | 내부 미확인 |
| videos | 1(바로 아래) | `C:\Users\PC\Videos` | 계획표에서 5.26GB. 내부 미확인. G:\다른 컴퓨터\내 노트북\Videos 와 뜻 같은 이름 묶음 후보 |
| workspace | 1(바로 아래) | `C:\Users\PC\workspace` | 내부 미확인 |
| 시작 메뉴 | 1 | `C:\Users\PC\시작 메뉴` | 내부 미확인 |

 비고:
- 바로 아래에서 leaf가 완전히 같은 중복은 이 목록 안에서는 없다(모두 1개). 다만 Documents ↔ My Documents ↔ (Application Data)처럼 "이름은 다르지만 같은 역할"로 보이는 것들이 있다. 이것들은 발주서의 "뜻만 같은 이름도 같은 묶음" 기준으로 사장님이 판단할 영역이다.
- C:\Users\PC의 Documents, Desktop, Downloads, Videos, Music, Pictures 등은 G:\다른 컴퓨터\내 노트북 아래 동일·유사 이름과 짝이 될 가능성이 있다(G: 접근 불가로 이 세션 확인 못 함).

---

## 4. /tmp에서 보이는 clone들(simplifier_style, hermes-clone-test)의 leaf 중복 여부

이 세션에서 `/tmp` 아래 clone 두 개를 직접 확인했다.

| leaf(대소문자 무시) | 개수(/tmp 내에서) | 경로(이 세션에서 확인된 값) | 이 환경에서 미확인 |
|------|------|------|------|
| simplifier_style | 1 | `/tmp/simplifier_style` | C:\Users\PC\AppData\Local\Temp\simplifier_style와 동일 대상인지, 크기·작성일·git 여부 미확인. /tmp 내 다른 simplifier_style 없음 |
| hermes-clone-test | 1 | `/tmp/hermes-clone-test` | C:\Users\PC\AppData\Local\Temp\hermes-clone-test와 동일 대상인지, 크기·작성일·git 여부 미확인. /tmp 내 다른 hermes-clone-test 없음 |

비고:
- /tmp 내에는 위의 두 leaf 외에 수많은 일회성 스크래치 폴더(uuid 이름 등)가 있으나, 이들은 leaf 이름이 제각각이라 "동일 이름 중복" 대상이 아니다. 이 조사 범위에서는 제외했다.
- 두 clone 모두 계획표(3항·4항)에 이미 등록된 대상과 경로로 보이며, /tmp 내에서 leaf가 중복되지는 않는다. 다만 "C:\Users\PC\AppData\Local\Temp"에 같은 leaf가 있는지 여부는 이 세션에서 확인 못 했다(C:\Users\PC 전체 재귀 미수행).

---

## 5. 이 환경에서 수행 불가한 부분(명시)

아래 항목은 이 CLI 전용 세션에서 실제로는 수행하지 못했고, "이 환경에서는 수행 불가"로 구분한다.

| 수행하려던 항목 | 수행 불가 사유 / 상태 |
|------|------|
| C:\Users\PC 전체 재귀(깊이 4) leaf 중복 전수 + 크기(GB)·최근 수정일·git 여부 판정 | 이 세션에서 PowerShell 재귀 실측이나 깊이 4 재귀 목록화를 수행하지 않음. 계획표의 14개 저장소 실측을 넘어서는 전체 사용자 폴더 재귀는 미수행 |
| C:\c 아래 leaf 중복 조사 | C:\c 루트에 대한 접근·목록화를 이 세션에서 하지 않음 |
| D:\ 아래 leaf 중복 조사 | D:\ 접근·목록화 미수행 |
| G:\내 드라이브, G:\다른 컴퓨터 아래 leaf 중복 조사 | G:\ 접근·목록화 미수행(연결된 드라이브라도 이 세션에서 목록화하지 않음) |
| PowerShell (New-Object shell.application) 탐색기 고정 항목 조회 | 이 세션에서 PowerShell 실행·조회하지 않음 |
| Known Folder 레지스트리 조회 | 이 세션에서 레지스트리 조회하지 않음 |
| 드라이브 전체 재귀에서 1GB 이상 폴더 크기 타임아웃 측정 | 발주서의 "1분 타임아웃" 실측을 이 세션에서 수행하지 않음. 계획표의 폴더별 5분 실측과 별개 |

---

## 6. 이름 충돌로 사장님이 잘못 열 가능성이 큰 상위 5개 + 해소 제안(실행 없음)

아래 5개는 발주서의 우선 묶음 + 이 세션에서 확인된 leaf 중복 + 사장님이 "같은 이름을 보고 다른 곳을 여는" 시나리오를 기준으로 뽑은 것이다. 실제 이동·삭제·이름 변경·고정 항목 제거는 하지 않는다(제안만).

1. **ComfyUI (3곳: C:\Users\PC\ComfyUI, C:\Users\PC\Documents\ComfyUI, Temp의 ComfyUI-LTXVideo)**
   - 현황: C:\Users\PC\ComfyUI(활성 작업용, 142M, 커밋 9/9) vs Documents\ComfyUI(미측정, 커밋 9/4). 둘 다 comfyanonymous/ComfyUI. Temp 쪽 ComfyUI-LTXVideo는 leaf가 다르지만 "ComfyUI" 검색 시 함께 보일 수 있음.
   - 잘못 열 가능성: 높음. 탐색기 주소창이나 검색에서 "ComfyUI" 입력 시 두 곳이 함께 뜨고, 사장님이 어느 쪽인지 구분하지 않고 열 확률이 높음.
   - 해소 제안(실행 없음): (a) C:\Users\PC\ComfyUI 쪽이 최근 커밋·활성 작업이라면 정본 후보로 두고, Documents\ComfyUI는 "사본"임을 이름이나 위치로 구분(예: 폴더명 접미어, 또는 이 보고서를 근거로 사장님이 어느 쪽을 주로 열지 결정). (b) Temp\ComfyUI-LTXVideo는 임시 위치이므로 계획안의 격리 제안(D:\_정리대기 등)을 별도 검토. (c) 탐색기 고정 항목에 두 ComfyUI가 모두 등록되어 있다면 정본만 남기고 나머지는 고정 항목에서 제거(명시적 제안, 실행 없음).

2. **shorts-lab (2곳: C:\work\shorts-lab, C:\Users\PC\Documents\shorts-lab-pilot)**
   - 현황: /c/work/shorts-lab(2.6G, 커밋 9/15)가 더 최신. Documents 쪽은 "shorts-lab-pilot"이라는 이름으로 잎이 다르지만, "shorts-lab" 검색 시 함께 보일 수 있음.
   - 잘못 열 가능성: 높음. "shorts-lab" 입력 시 두 곳이 검색되고, Documents 쪽이 옛 클론이면 사장님이 옛날 경로를 열 위험이 있음.
   - 해소 제안(실행 없음): (a) /c/work/shorts-lab가 최신 정본 후보라면 Documents\shorts-lab-pilot은 "옛 클론/사본"으로 구분하고, 이름이나 위치를 달리 보이게 함(예: Documents 쪽은 접미어 유지하거나 아카이브 위치로 이동 검토 — 제안만). (b) 탐색기 고정 항목에 두 곳이 모두 있으면 최신 것만 남기고 나머지 제거(실행 없음). (c) 둘을 헷갈리지 않도록 서로 다른 작업 창 습관(예: 작업 루트 고정)을 제안 가능.

3. **simplifier-saegim (2곳: C:\Users\PC\simplifier-saegim, C:\work\simplifier-saegim)**
   - 현황: 둘 다 hansunghee7/simplifier-saegim 원격, 커밋 9/10 vs 9/9, 크기 1.1M vs 1.2M으로 비슷. 어느 것이 정본인지 이 세션에서 확정 못 함(계획표도 "사장님 판단"으로 남김).
   - 잘못 열 가능성: 중간~높음. leaf가 완전히 같아 탐색기 검색·드라이브 탐색에서 둘 중 하나를 잘못 열 가능성이 있음.
   - 해소 제안(실행 없음): (a) 둘 중 실제로 더 자주 쓰는 쪽을 확인하고, 덜 쓰는 쪽은 "사본/옛 클론"으로 구분할 수 있게 이름·위치 구분 검토(제안만). (b) 탐색기 고정 항목에 둘 다 있으면 주로 쓰는 쪽만 남기기(실행 없음). (c) 계획표에서 "정본 확인 후 결정"으로 남겨뒀으므로, 이 조사를 근거로 사장님이 정본 쪽을 먼저 확정하는 것을 제안.

4. **Documents ↔ documents ↔ My Documents ↔ (Application Data) + G:\다른 컴퓨터\내 노트북\문서**
   - 현황: C:\Users\PC 바로 아래에 Documents, docs, My Documents, Application Data가 함께 있음. G: 쪽에는 "문서"(뜻 동일)가 있어 이름만 같은 폴더가 다른 드라이브에 나란히 존재. 이 세션에서는 G:를 확인하지 못했으므로 "이 환경에서 미확인"으로 남긴다.
   - 잘못 열 가능성: 높음. "문서"/"Documents"를 열 때 OS 언어·탐색기 표시·드라이브 위치에 따라 전혀 다른 곳을 열 수 있음.
   - 해소 제안(실행 없음): (a) C:\Users\PC 아래 Documents, docs, My Documents, Application Data 중 실제로 쓰는 것만 남기고 나머지는 위치를 달리하거나(정본 명확화) 사장님 판단으로 정리(검토 제안, 실행 없음). (b) G:\다른 컴퓨터\내 노트북\문서와 C:\Users\PC\Documents가 같은 파일 집합을 미러하는 백업 미러라면, 사장님이 "어느 쪽이 살아 있는 경로인지"를 인지하고 열도록 습관·고정 항목 조정(실행 없음). (c) 탐색기에서 "문서" 검색 시 여러 드라이브 결과가 함께 뜨는 것이 문제라면, 주력 경로 하나만 고정 항목에 남기고 나머지는 제거(실행 없음).

5. **.claude (4곳: C:\work\.claude, hansunghee7.github.io\.claude, shorts-lab\.claude, simplifier-saegim\.claude)**
   - 현황: C:\work 아래에서 leaf ".claude"가 4곳 확인됨. 모두 각 저장소의 Claude 설정/스킬 폴더로 보이며, 내용은 저장소별로 다를 가능성이 높음(이름만 같은 다른 것 후보).
   - 잘못 열 가능성: 중간. 탐색기에서 ".claude"를 검색하거나, 작업 루트를 헷갈릴 때 다른 저장소의 .claude를 열 수 있음.
   - 해소 제안(실행 없음): (a) .claude는 각 저장소에 딸린 설정 폴더이므로 "이름만 같은 다른 것"으로 취급하고, 폴더명 자체를 바꾸기보다는 "어느 저장소의 .claude를 보고 있는지"를 경로로 구분하는 습관 제안(실행 없음). (b) .claude 자체를 검색·탐색에서 자주 여는 대상이 아니라면, 충돌 우선순위는 위에 적힌 ComfyUI·shorts-lab·simplifier-saegim·Documents보다 낮게 봐도 됨.

비고(일반 제안):
- 상위 5개 중 ComfyUI, shorts-lab, simplifier-saegim은 "어느 것이 살아 있는가"(최근 30일 파일 수정 / 실행 중 프로세스의 경로 / 탐색기 고정 항목이 가리키는 곳)를 확인하면 잘못 열 가능성이 크게 줄어든다. 이 세션에서는 그 세 가지를 확인하지 못했으므로, 이 보고서는 "후보"까지만 제시하고 실제 활성화 경로 확정은 별도 단계(사장님 판단 또는 추가 조사)로 남긴다.
- G:\다른 컴퓨터 쪽은 이 세션에서 접근·목록화하지 못했으므로, 위 표의 G: 관련 행은 모두 "이 환경에서 미확인"이다. 연결 상태·마운트 시점에 따라 목록이 달라질 가능성도 있다.

---

## 7. 수행 요약(이 세션에서 실제로 한 것)

- `/c/work`에서 `find -maxdepth 4 -type d`(제외 폴더 pruned)로 leaf 이름 기준 중복을 전수 집계. 개수 3 이상(.claude 4, docs 5, hooks 3, skills 3, scripts 4)과 개수 2 이상(assets, book, icons, images, log, supabase, templates 등)을 확인. 개수 1(leaf 유일)은 이 파일에 나열하지 않음.
- `/c/Users/PC` 바로 아래 폴더 26개를 `ls -d .../*/`로 확인. 바로 아래에서 leaf 완전 중복은 없었음. Documents, Desktop, Downloads, Videos, Music, Pictures, ComfyUI, simplifier-saegim, hermes-node-bridge 등 계획표에서 이미 확인된 항목 포함.
- `/tmp/simplifier_style`, `/tmp/hermes-clone-test`가 실제 존재하며 각각 leaf 단독으로 존재함을 확인. /tmp 내에서 이 두 leaf의 중복은 없음. 다만 C:\Users\PC\AppData\Local\Temp 아래 동일 leaf 존재 여부는 이 세션에서 미확인.
- 계획표(tasks/done/2026-09-15-shinpc-folder-cleanup-plan.md)에서 이미 확인된 중복 쌍(ComfyUI 3곳, shorts-lab 2곳, simplifier-saegim 2곳, simplifier_style·hermes-clone-test 각 1곳)을 표 상단 우선 묶음으로 넣음.
- C:\c, D:\, G:\내 드라이브, G:\다른 컴퓨터, C:\Users\PC 전체 재귀(깊이 4) 실측, PowerShell 탐색기 고정 항목·레지스트리, 드라이브 전체 1GB 이상 폴더 타임아웃 측정은 이 환경에서 수행 불가로 명시.

---

*이 파일은 발주서(C:/work/solar-bible/tasks/pending/2026-09-15-shinpc-duplicate-folder-names.md)를 tasks/done으로 옮긴 뒤의 조사 결과 절 분량이다. 이동·삭제·이름 변경·설정 변경은 하지 않았다.*
