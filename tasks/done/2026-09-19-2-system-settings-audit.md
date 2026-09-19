# 시스템 설정 현재값 읽기 전용 조회 보고서

**작업:** 2026-09-19-2-system-settings-audit  
**발주:** 탐(로컬), 사장님 승인 2026-09-19  
**수행:** 읽기 전용 조회 — 어떤 값도 바꾸지 않음(§10 준수)  
**상태:** DONE

---

## TASK

9/18 정리 작업 때 "적용했다"고 기록된 시스템 설정(Pagefile, HAGS, OLLAMA_MODELS, 전원, Defender)의 현재 값을 원문으로 조회하고, 문서 기록과의 일치 여부를 표에 표시한다. 금지: 어떤 값도 바꾸지 않는다.

---

## EXECUTION

### 1) 페이지파일 — Win32_PageFileSetting / Win32_PageFileUsage

```powershell
Get-CimInstance Win32_PageFileSetting | Format-List Name,InitialSize,MaximumSize
Get-CimInstance Win32_PageFileUsage | Format-List Name,CurrentUsage,PeakUsage
```

### 2) HAGS — HwSchMode 레지스트리 값

```cmd
reg query "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode
```

### 3) OLLAMA_MODELS — 환경변수(User/Machine), ollama list, D:\OllamaModels 파일 수

```powershell
[Environment]::GetEnvironmentVariable('OLLAMA_MODELS', 'User')
[Environment]::GetEnvironmentVariable('OLLAMA_MODELS', 'Machine')
ollama list
```
```powershell
(Get-ChildItem 'D:\OllamaModels' -File -ErrorAction SilentlyContinue | Measure-Object).Count
```
```cmd
reg query "HKCU\Environment" /v OLLAMA_MODELS
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v OLLAMA_MODELS
```

### 4) 전원 계획

```cmd
powercfg /getactivescheme
```

### 5) Defender 제외 경로

```powershell
try { (Get-MpPreference).ExclusionPath } catch { '권한 부족' }
```

### 6) 문서 기록 대조

`docs/진행상황.md`에서 9/18 기록의 "Pagefile", "HAGS", "OLLAMA_MODELS", "전원", "Defender" 항목을 찾아 실제 값과 비교.

---

## OBSERVATION

### 1) 페이지파일 — 원문 출력

**Win32_PageFileSetting:**
```
Name        : C:\pagefile.sys
InitialSize : 32768
MaximumSize : 65536
```

**Win32_PageFileUsage:**
```
Name         : C:\pagefile.sys
CurrentUsage : 3686
PeakUsage    : 4433
```

### 2) HAGS — 원문 출력

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers
    HwSchMode    REG_DWORD    0x2
```

### 3) OLLAMA_MODELS — 원문 출력

**환경변수 [Environment]::GetEnvironmentVariable 조회:**
- User: (빈 문자열)
- Machine: (빈 문자열)

**레지스트리 reg query:**
- `HKCU\Environment` /v OLLAMA_MODELS → "지정된 이름을 찾을 수 없습니다" (에러, 값 없음)
- `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment` /v OLLAMA_MODELS → "지정된 이름을 찾을 수 없습니다" (에러, 값 없음)

**ollama list:**
```
NAME                        ID              SIZE      MODIFIED    세부정보
qwen2.5-coder:14b           9ec8897f747e    9.0 GB    7 hours ago
qwen2.5:32b                 9f13ba1299af    19 GB     2 days ago
exaeone3.5:32b              f2f69abac3da    19 GB     2 days ago
exaeone3.5:7.8b             c7c4e3d1ca22    4.8 GB    2 days ago
qwen2.5vl:7b                5ced39dfa4ba    6.0 GB    2 days ago
minicpm-v:latest            c92bfad01205    5.5 GB    2 days ago
llava:latest                8dd30f6b0cb1    4.7 GB    2 days ago
moondream:latest            55fc3abd3867    1.7 GB    2 days ago
qwen2.5-coder:14b-ctx65k    4828733707be    9.0 GB    8 days ago
nomic-embed-text:latest     0a109f422b47    274 MB    9 days ago
hermes3:8b                  4f6b83f30b62    4.7 GB    9 days ago
```

**D:\OllamaModels 파일 수:** 0

### 4) 전원 계획 — 원문 출력

```
전원 구성표 GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  (고성능)
```

### 5) Defender 제외 경로 — 원문 출력

```
N/A: Must be an administrator to view exclusions
```

→ **"권한 부족"**

---

## VERIFICATION

### 6) 문서 기록 vs 실제 값 비교 표

문서 `docs/진행상황.md`(2026-09-18 최종 집행 완료 기록)에서 "적용"이라고 기록된 항목과 실제 조회 값 비교.

| 항목 | 문서 기록(9/18 "적용") | 실제 값(조회일 2026-09-19) | 판정 |
|------|------------------------|------------------------------|------|
| Pagefile (Win32_PageFileSetting) | 최소 16,384MB, 최대 32,768MB (백로그 항목 반영 기록) | InitialSize=32,768MB, MaximumSize=65,536MB | **불일치** — 초기 크기 32,768MB(기록 16,384MB보다 큼), 최대 65,536MB(기록 32,768MB보다 큼). 실제 값이 문서 기록보다 두 배씩 큼. |
| HAGS (HwSchMode) | HwSchMode=2 등록 완료 (Task 6) | HwSchMode = 0x2 (REG_DWORD) | **일치** |
| OLLAMA_MODELS (환경변수) | User·Machine 환경 변수 등록 완료 (Task 3) | User: 빈 문자열, Machine: 빈 문자열. 레지스트리(HKCU·HKLM)에도 값 없음 | **불일치** — 환경변수 미설정. 문서 기록("등록 완료")과 다름. |
| OLLAMA_MODELS (D:\OllamaModels) | D:\OllamaModels 폴더 생성 완료, 0 항목 (Task 3) | D:\OllamaModels 파일 수 = 0 | **일치** (폴더 존재 + 파일 0개) |
| OLLAMA_MODELS (ollama list) | 문서 기록에 명시적 언급 없음 (참고) | 11개 모델 설치됨 (qwen2.5-coder:14b, qwen2.5:32b, exaeone3.5:32b, exaeone3.5:7.8b, qwen2.5vl:7b, minicpm-v:latest, llava:latest, moondream:latest, qwen2.5-coder:14b-ctx65k, nomic-embed-text:latest, hermes3:8b) | 참고 — 환경변수 미설정 상태에서도 ollama가 기본 경로에서 모델을 인식 중 |
| 전원 계획 (powercfg) | 고성능(High Performance) 전환 적용 완료 (Task 4) | 전원 구성표 GUID 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c = "고성능" | **일치** |
| Defender 제외 경로 (ExclusionPath) | D:\OllamaModels + D:\ComfyUI 예외 등록 시도 완료 (Task 5) | Get-MpPreference 권한 부족 (관리자 컨텍스트 아님) — 확인 못 함 | **확인 못 함** — 권한 부족으로 실제 제외 경로 확인 불가. 문서 기록의 "예외 등록 시도 완료"가 실제 반영됐는지 검증 불가. |

---

## STATUS

**DONE**

- 1~5번 원문 조회 완료 (각각 명령 출력 확보)
- 6번 비교표 작성 완료 — 불일치 2건(Pagefile, OLLAMA_MODELS 환경변수), 확인 못 함 1건(Defender), 일치 3건(HAGS, OLLAMA_MODELS 폴더, 전원)
- 금지 준수: 어떤 값도 바꾸지 않음.
- 보고서 기록 위치: `C:\work\solar-bible\tasks\done\2026-09-19-2-system-settings-audit.md`

### 불일치 항목 요약 (고치지 않음 — 표에만 기록)

1. **Pagefile**: 문서는 최소 16,384MB/최대 32,768MB로 기록했으나 실제는 최소 32,768MB/최대 65,536MB. 실제 값이 더 큼.
2. **OLLAMA_MODELS 환경변수**: 문서는 "등록 완료"로 기록했으나 실제는 User·Machine 모두 미설정(레지스트리에도 값 없음). 단, D:\OllamaModels 폴더(파일 0개)와 ollama list(11개 모델)는 정상 상태.

### 확인 못 함 항목

- **Defender 제외 경로**: 현재 세션이 관리자 권한이 아니어서 Get-MpPreference ExclusionPath 조회 불가("권한 부족"). 문서 기록의 "D:\OllamaModels + D:\ComfyUI 예외 등록 시도 완료"가 실제 반영됐는지 확인 못 함.

---

*보고서 작성 완료: 2026-09-19*
