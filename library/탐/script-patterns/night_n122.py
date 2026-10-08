# -*- coding: utf-8 -*-
# 야간 일감 2(N122): Carvit Pass 보안 모델 문서 초안(공개 테크리포트 후보). 입력은 사장님이 10/9에 허용한 비공개 설계 문서만(키 값·고객 정보·가격은 없음).
# 공개 전 비티 검토를 거치므로 초안 단계에서 포트, 파일 경로, 토큰 위치, 세부 우회 방법을 쓰지 말라고 지시하고, 결과에 그런 패턴이 있는지 스크립트가 센다.
import json, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTD = Path("C:/work/_ops/api_night"); OUTD.mkdir(parents=True, exist_ok=True)
SRC = [
    Path("C:/work/simplifier-cxo-db/reports/pass/Pass_저장구조_결정_1003.md"),
    Path("C:/work/saegim-pass/docs/PIN_서버_요청서.md"),
    Path("C:/work/saegim-pass/docs/에이전트_통로_설계.md"),
    Path("C:/work/saegim-pass/docs/동기화_설계_공통로그인.md"),
]
parts, used = [], []
for p in SRC:
    if p.exists():
        parts.append("### 자료: " + p.name + "\n" + p.read_text(encoding="utf-8", errors="replace")[:14000]); used.append(p.name)
mat = "\n\n".join(parts)
prompt = ("너는 보안 설계 문서 작성자다. 아래 [자료]만 근거로, 비전문가인 대표와 외부 개발자가 읽는 'Carvit Pass 보안 모델' 테크리포트 초안을 한국어로 써라. "
          "구성: 1) 무엇을 지키려는가(보호 범위) 2) 열쇠 계층(일반 키와 보안 상위 키의 차이) 3) 위협 모델(누가 무엇을 노리고 어떻게 막는가, 한계 포함) 4) 승인 흐름 5) 아직 설계에만 있고 구현이 확인되지 않은 것 6) 알려진 한계. "
          "규칙: 자료에 없는 사실은 쓰지 말고 '자료에 없음'이라 써라. 중요한 주장마다 자료에서 한 구절을 큰따옴표로 글자 그대로 인용하라. "
          "공개 문서라서 포트 번호, 파일·폴더 경로, 토큰·키가 저장되는 위치, 세부 우회 방법, 내부 주소는 쓰지 말라. 키 값은 당연히 쓰지 말라.\n\n[자료]\n" + mat)
(HERE / "n122_p.txt").write_text(prompt, encoding="utf-8")
r = subprocess.run([sys.executable, "C:/work/hansunghee7.github.io/scripts/ops/api_run.py", "--who", "탐", "--model", "claude-sonnet-5-5", "--prompt-file", str(HERE / "n122_p.txt"),
                    "--max-tokens", "14000", "--out", str(OUTD / "N122_security_model_draft_1009.md"), "--daily-usd", "5"], capture_output=True, text=True, encoding="utf-8", timeout=300)
print("rc", r.returncode, r.stderr[-160:], flush=True)
draft = (OUTD / "N122_security_model_draft_1009.md").read_text(encoding="utf-8") if (OUTD / "N122_security_model_draft_1009.md").exists() else ""
quotes = re.findall(r"\"([^\"\n]{12,200})\"", draft)
ok_q = sum(1 for q in quotes if q in mat)
danger = {
    "포트 번호": len(re.findall(r"(?:포트|port)\s*:?\s*\d{3,5}|:\d{4,5}\b", draft, re.I)),
    "윈도우 경로": len(re.findall(r"[A-Za-z]:[\\/]", draft)),
    "환경 파일": len(re.findall(r"\.env\b", draft)),
    "레지스트리": len(re.findall(r"HKCU|HKLM", draft)),
    "키 모양 문자열": len(re.findall(r"sk-[A-Za-z0-9_-]{16,}|eyJ[A-Za-z0-9_-]{20,}", draft)),
}
rep = {"자료": used, "초안 글자수": len(draft), "인용 수": len(quotes), "원문 일치 인용": ok_q, "공개 위험 패턴": danger}
(OUTD / "N122_check_1009.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
summary = "야간 일감 2(N122 보안 모델 초안): 자료 %d건, 초안 %d자, 인용 %d개 중 원문 일치 %d개, 공개 위험 패턴 %s. 파일: C:/work/_ops/api_night/N122_security_model_draft_1009.md (비티 검토와 사장님 컨펌 전 공개 금지)" % (len(used), len(draft), len(quotes), ok_q, danger)
print(summary, flush=True)
try:
    subprocess.run([sys.executable, "C:/work/hansunghee7.github.io/scripts/ops/tg_boss.py", "text", "[탐 컨펌] " + summary, "--persona", "탐"], capture_output=True, timeout=60)
except Exception:
    pass
print("NIGHT2 DONE")
