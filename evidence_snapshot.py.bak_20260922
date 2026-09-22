#!/usr/bin/env python3
"""evidence_snapshot.py — 보고서 작성 시점의 수집 증거 요약 출력."""
import os, sys, json, datetime

REPORT_PATH = "C:/work/solar-bible/reports/2026-09-20-support-grants.md"

def main():
    snapshot = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "report_path": REPORT_PATH,
        "report_exists": os.path.exists(REPORT_PATH),
        "report_size_bytes": os.path.getsize(REPORT_PATH) if os.path.exists(REPORT_PATH) else None,
        "collected_urls": [
            "https://www.kised.or.kr/menu.es?mid=a10205010000",
            "https://www.kised.or.kr/menu.es?mid=a10205020000",
            "https://www.kised.or.kr/menu.es?mid=a10205030000",
            "https://www.kised.or.kr/menu.es?mid=a10302000000",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000117172",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000121151",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000122108",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000120038",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000116971",
            "https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000118886",
            "https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=1064347",
            "https://www.mss.go.kr/site/ulsan/ex/bbs/View.do?cbIdx=254&bcIdx=1064546",
            "https://www.venturesquare.net/announcement/1041397",
            "https://www.nipa.kr/home/2-2/16664",
            "https://www.nipa.kr/home/2-2/16497",
            "https://www.nipa.kr/home/2-2/16474",
        ],
        "failed_or_unreadable_urls": [],
        "evidence_sources_by_program": {
            "예비창업패키지": [
                "창업진흥원 사업안내 페이지 (https://www.kised.or.kr/menu.es?mid=a10205010000) — 지원대상·사업화자금·예산·사업절차"
            ],
            "초기창업패키지": [
                "창업진흥원 사업안내 페이지 (https://www.kised.or.kr/menu.es?mid=a10205020000) — 지원대상·사업화자금·예산·규모·사업절차",
                "창업도약패키지(일반형) 공고 PDF 내 일정표 — 초기창업패키지 실제 접수일 교차 확인 (2026.01.23~02.13)"
            ],
            "창업도약패키지(일반형)": [
                "창업진흥원 사업안내 페이지 (https://www.kised.or.kr/menu.es?mid=a10205030000) — 지원대상·사업화자금·예산·규모·평가절차",
                "기업마당 공고 페이지 (https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000117172) — 딥테크 특화형 공고·지원대상·사업내용",
                "창업도약패키지(일반형) 공고 PDF (https://jb.riia.or.kr/file/download?id=b9cd3543-fd80-11f0-a9fb-334ae3222397) — 평가 지표·선정 절차·붙임3 동시수행 불가 목록·접수기간"
            ],
            "초격차 스타트업 프로젝트 DIPS": [
                "중기부 보도자료 (https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=1064347) — 선정규모·지원내용·6대 전략산업-12대 신산업",
                "중기부 울산지방청 공고 (https://www.mss.go.kr/site/ulsan/ex/bbs/View.do?cbIdx=254&bcIdx=1064546) — 접수기간·첨부파일"
            ],
            "창업성장기술개발사업(디딤돌)": [
                "기업마당 3차 공고 페이지 (https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000120038) — 공통자격·업력·매출액 요건",
                "TLO 공고 페이지 (https://tlo.korea.ac.kr/support-projects/2702) — 접수기간·규모·예산·세부과제 교차 확인"
            ],
            "글로벌기업 협업프로그램 (AroundX)": [
                "벤처스퀘어 공고 페이지 (https://www.venturesquare.net/announcement/1041397) — 접수기간·지원내용·사업화자금·협업 글로벌 기업 18개 목록·신청대상",
                "경기도잡아바 (https://job.gg.go.kr/entSprt/detail.do?seq=3188) — 모집일정 교차 확인"
            ],
            "AI 통합 바우처 (클라우드 바우처)": [
                "NIPA 공고 페이지 (https://www.nipa.kr/home/2-2/16664) — 신청자격·접수기간·자기부담 구조·지원규모·예산·문의처"
            ],
            "SaaS 개발환경 지원 (SaaS 전환지원센터)": [
                "NIPA 공고 페이지 (https://www.nipa.kr/home/2-2/16497) — 사업목적·대상·접수기간·공급기업 선정규모·신청방법",
                "Poliflo (https://poliflo.com/announcements/2645) — 수요기업 접수기간 교차 확인",
                "KOIPA 공고문 — 사업기간 교차 확인"
            ],
            "2026년 K-스타트업 AI리그": [
                "기업마당 공고 페이지 (https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000121151) — 신청대상·자격·AI 全 기술영역",
                "벤처스퀘어 공고 페이지 (https://www.venturesquare.net/announcement/1069076) — 접수기간 교차 확인"
            ],
            "창업패키지 (AI 인재 실증형)": [
                "기업마당 공고 페이지 (https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000122108) — 지원대상·지원내용·딥테크 5대 분야"
            ],
            "TIPS (팁스)": [
                "창업진흥원 사업공고 페이지 (https://www.kised.or.kr/menu.es?mid=a10302000000) — 2026년 팁스 수정공고·마감일자 2026-12-31"
            ],
            "창업중심대학": [
                "창업진흥원 사업공고 페이지 (https://www.kised.or.kr/menu.es?mid=a10302000000) — 사업 목록 확인"
            ],
        },
        "claims_count_estimate": 60,
        "unanswered_or_partially_answered": [
            "예비창업패키지 2026년 실제 접수일(공고 페이지에는 '2~3월 예정'만 기재, 실제 3.06~03.24는 공식 공고문 PDF 미열람 → 미확정)",
            "초기·예비·창업도약 패키지의 자기부담금 비율(공식 사업안내 페이지에 미기재, 중기부 블로그에서 자부담률 30%→우대 10~25% 언급되나 공식 공고문 확인 필요 → 미확정)",
            "창업도약패키지 평가 배점 비중(공고 PDF에 평가항목 목록은 있으나 배점 수치는 미기재 → 미확정)",
            "창업중심대학 2026년 실제 접수일(2월 공고 예정이라는 블로그 정보만, 공식 공고 미열람 → 미확정)",
            "초격차 DIPS '창업 10년 이내' 요건(중기부 보도자료에서 직접 확인되지 않고 제3자 재인용으로만 존재 → 미확정)",
            "디딤돌 1차·2차 실제 접수일(기업마당 페이지에 일자 미기재, PDF 미다운로드 → 미확정)",
            "창업패키지(AI 인재 실증형) 접수기간(기업마당 페이지에 일자 미기재, 공고문 PDF 미열람 → 미확정)",
            "글로벌기업 협업프로그램 자기부담금·중복수혜 제한(공고 본문에 있으나 본 추출에서 미확인 → 미확정)",
            "2027년 모든 사업 일정은 전년도 공고 패턴 기준 추정치이며, 당해연도 공식 공고 미확인 → 추정 층위",
        ],
    }
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
