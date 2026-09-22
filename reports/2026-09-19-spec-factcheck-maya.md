# 5개 주장 팩트체크 결과 보고서

**작성일시**: 2026-09-20  
**검증 기준**: 공식 문서 및 원 출처(Anthropic Claude Code 공식 문서, Google AI 공식 문서, Ollama/Qwen 공식 자료) 우선  
**검증 단계**: 제미나이 대조 미실행  

---

## 주장 1: Claude Code는 `claude -p(--print)` 비대화형 실행과 `--permission-mode` 옵션을 지원하며, permission-mode에 `auto` 값이 있다.

**판정**: 부분확인  
**출처 URL**: https://code.claude.com/docs/en/headless  
**원문 인용(15단어 이내)**: "`--print (-p)` flag for non-interactive usage... `--permission-mode` flag accepts values: default, acceptEdits, bypassPermissions, plan"  
**확인 일시**: 2026-09-20  

**상세 근거**:  
- 공식 문서에서 `-p` / `--print` 플래그로 비대화형(헤드리스) 실행 지원 확인  
- `--permission-mode` 옵션 존재 확인  
- 단, 허용 값은 `default`, `acceptEdits`, `bypassPermissions`, `plan` 네 가지이며 **`auto` 값은 없음**  
- 따라서 "auto 값이 있다"는 부분은 반증됨  

---

## 주장 2: Claude Code의 SessionStart 훅이 표준출력으로 낸 문자열은 컨텍스트에 주입된다.

**판정**: 확인됨  
**출처 URL**: https://code.claude.com/docs/en/hooks-guide  
**원문 인용(15단어 이내)**: "SessionStart... The hook's stdout is added to the context as a user message"  
**확인 일시**: 2026-09-20  

**상세 근거**:  
- 공식 Hooks 가이드에서 `SessionStart` 훅 설명에 "The hook's stdout is added to the context as a user message" 명시  
- 세션 시작 시(`claude` 실행, `-r`로 재개, 히스토리 클리어 시) 동작 확인  

---

## 주장 3: `claude -p`로 무인 실행할 때 `--allowedTools` 등으로 허용 도구를 제한할 수 있다.

**판정**: 확인됨  
**출처 URL**: https://code.claude.com/docs/en/headless  
**원문 인용(15단어 이내)**: "`--allowedTools`: A comma-separated list of tools the agent is allowed to use. Example: `--allowedTools \"Read,Write,Bash\"`"  
**확인 일시**: 2026-09-20  

**상세 근거**:  
- 헤드리스 모드 문서에서 `--allowedTools` 플래그로 사용 가능 도구를 콤마 구분 목록으로 제한 가능함을 명시  
- 예시: `--allowedTools "Read,Write,Bash"`  

---

## 주장 4: Gemini API 무료 등급에서 입력 컨텍스트 100만 토큰 창을 쓸 수 있고, 분당 토큰(TPM) 및 일일 요청(RPD) 한도가 있다. 현재 모델별 무료 등급 한도 수치를 찾을 것.

**판정**: 부분확인  
**출처 URL**: https://ai.google.dev/gemini-api/docs/rate-limits, https://ai.google.dev/gemini-api/docs/pricing  
**원문 인용(15단어 이내)**: "Rate limits are usually measured across three dimensions... RPD quotas reset at midnight Pacific time... Limits vary depending on the specific model... For details on those rate limits, see the AI Studio Rate Limit page"  
**확인 일시**: 2026-09-20  

**상세 근거**:  
- **컨텍스트 100만 토큰**: 가격 페이지에서 Gemini 3.5 Flash, 3.8 Flash 등 특정 모델이 1M 컨텍스트 지원 확인  
- **TPM/RPD 한도 존재**: 무료 등급(Free tier) 존재, RPM/TPM/RPD 3차원 제한 적용, RPD는 태평양 표준시 자정 리셋 확인  
- **모델별 구체적 수치**: 공식 문서에 무료 등급의 모델별 RPM/TPM/RPD 정확한 숫자는 **기재되지 않음** — "AI Studio Rate Limit 페이지 참조"로 안내  
- 따라서 모델별 현재 수치는 공식 문서에서 찾을 수 없음(근거없음)  

---

## 주장 5: RTX 4090에서 Ollama로 Qwen 14B급 모델은 초당 100토큰 이상을 낸다(양자화 조건 명시).

**판정**: 부분확인  
**출처 URL**: https://willitrunai.com/models/qwen-2.5-coder-14b  
**원문 인용(15단어 이내)**: "NVIDIA RTX 4090 24GB... Q4_K_M | 96.9 | Fits"  
**확인 일시**: 2026-09-20  

**상세 근거**:  
- willitrunai.com 벤치마크(단일 스트림 디코드, Q4_K_M 양자화)에서 RTX 4090 24GB 기준:  
  - **Qwen 2.5 Coder 14B**: **96.9 tok/s** (100 미만, 근접)  
  - Qwen3 14B(modelfit.io): Q4_K_M 약 65 tok/s, Q8_0 약 40 tok/s  
- "100토큰 이상"이라는 주장은 **Qwen 2.5 Coder 14B Q4_K_M에서 96.9로 근접하나 미달**, Qwen3 14B는 더 낮음  
- 양자화 조건: **Q4_K_M** 권장(8.5 GB VRAM), Q8_0은 15 GB로 더 느림  

---

## 요약

| 주장 | 판정 | 비고 |
|------|------|------|
| 1. Claude Code -p/--permission-mode/auto | 부분확인 | auto 값 없음(허용값: default, acceptEdits, bypassPermissions, plan) |
| 2. SessionStart 훅 stdout → 컨텍스트 주입 | 확인됨 | 공식 문서 명시 |
| 3. --allowedTools로 도구 제한 | 확인됨 | 공식 문서 명시 |
| 4. Gemini 무료 1M 컨텍스트 + TPM/RPD 수치 | 부분확인 | 1M 컨텍스트·한도 존재 확인, 모델별 구체 수치는 공식 문서에 없음(AI Studio 참조) |
| 5. RTX 4090 + Qwen 14B 100+ tok/s | 부분확인 | Qwen 2.5 Coder 14B Q4_K_M 96.9 tok/s(미달), Qwen3 14B 더 낮음 |

---

**STATUS: DONE**  
**검증 단계 미실행**: 제미나이 대조는 실행하지 않았습니다.