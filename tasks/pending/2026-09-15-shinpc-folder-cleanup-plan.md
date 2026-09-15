## 조사 결과

### 1. D: 드라이브 실측 (PowerShell)

- `Get-PhysicalDisk` 결과:
  - Disk 2: Samsung SSD 990 PRO 1TB, 크기 931.51 GB, 미디어 유형 SSD → C: 드라이브 (사용 885 GB / 여유 113 GB 확인됨)
  - Disk 1: Samsung SSD 980 848 GB, 크기 788.44 GB, 미디어 유형 SSD → D: 드라이브 (사용 8 GB / 여유 780 GB)
  - **판정: D:는 HDD가 아닌 Samsung SSD 980 848GB. 여유 약 780 GB.**

- `Get-Volume` 결과 메모: C: NTFS 931GB (여유 113GB), D: NTFS 788.44GB (여유 780.08GB), 복구 파티션(450MB, 449.99MB 여유), 시스템 예약(260MB).

### 2. C: 대용량 폴더 상위 20개 (미측정 항목 포함)

#### A. `C:\Users\PC\AppData\Local` (os.walk, 20개만)
| 경로 | 크기(GB) |
|---|---|
| Docker\wsl\disk | 12.35 |
| CapCut\Apps\9.3.0.3970 | 0.89 |
| CapCut\Apps\9.4.0.4015 | 0.88 |
| CrashDumps | 0.39 |
| Adobe\Acrobat\AVWebview2\...\Cache_Data | 0.33 |
| CapCut\User Data\CEF\Cache\...\Cache_Data | 0.31 |
| Figma\app-126.7.10 | 0.28 |
| CapCut\Videos | 0.28 |
| Figma\app-126.8.16 | 0.27 |
| Discord\app-1.0.9257 | 0.27 |
| CapCut\Apps\...\cef | 0.26 ×2 |
| CapCut\User Data\Cache\ressdk_db\... | 0.17 |
| Adobe\AVWebview2\Code Cache\js | 0.14 |
| electron\Cache\... | 0.13 |
| Discord\packages | 0.13 |
| Adobe\...\CacheStorage\... | 0.13 |
| CapCut\User Data\Cache\ressdk_db\... | 0.11 |
| CapCut\User Data\Cache\image | 0.10 |
| Adobe\DC\BHCache\Files | 0.10 |

- 미측정: AppData/Local 전체 측정은 1단계 서브 폴더 각각이 0.1GB 이하로 분산되어 있어 누락이 있을 수 있으나(5분 초과로 타임아웃났던 부분), 상위 20개는 위 표에 정리. 가장 큰 것은 Docker\wsl\disk 12.35GB.

#### B. `C:\Users\PC\Downloads` (Python os.walk)
| 경로 | 크기(GB) |
|---|---|
| 히스토리 | 19.13 |
| 히스토리\hansunghee7.github.io-main\...\images | 0.38 ×2 |
| hansunghee7.github.io-main\...\images | 0.38 |
| 히스토리\...\images(중복 경로) | 0.37 |
| 히스토리\drive-download-20260216T074921Z-1-001 | 0.14 |

- Downloads 전체(파일 12,627개): 21.3 GB. 대부분 `히스토리` 아래 설치파일 아카이브.

#### C. `C:\c\c\Users\PC\_tmp_repo`
- 경로 없음(C:\c\c\Users\PC\_tmp_repo가 현재 존재하지 않음). 이전 조사에서 1.11GB로 측정되었던 위치이나 현재 실측 불가. **미측정(경로 소실).**

#### D. `C:\Users\PC\shorts-lab`
- 경로 없음(C:\Users\PC\shorts-lab가 현재 존재하지 않음). **미측정(경로 소실).**

#### E. `C:\Users\PC\ComfyUI`
- AppData/Local 상위 20에 들지 않았고, ComfyUI 단독 상위 20 측정에서도 0.03GB 미만으로 미미. 별도 정밀 측정 보류(정리안에서 "그대로 둠" 후보).

#### F. `C:\Users\PC\OneDrive`
- 경로 없음(현재 이 경로 존재하지 않음). OneDrive 동기화 대상 확인 불가. **미측정.**

### 3. git 저장소 17개 (경로·크기·원격·마지막 커밋·미커밋)

| 저장소 경로 | 크기(GB) | 원격 | 마지막 커밋 | 미커밋 |
|---|---|---|---|---|
| C:\work\hansunghee7.github.io | 0.0043 (약 4.5MB 추정) | origin https://github.com/hansunghee7/hansunghee7.github.io.git | 2026-09-15 14:26:23 +0900 094c7631 | 2줄 |
| C:\work\shorts-lab | 측정 불가(아래) | origin https://github.com/hansunghee7/shorts-lab.git | 2026-09-15 17:08:41 +0900 fca8f17 | 0줄 |
| C:\work\simplifier-agent | 측정 불가(아래) | origin https://github.com/hansunghee7/simplifier-agent.git | 2026-09-03 11:44:35 +0900 b2072cd | 0줄 |
| C:\work\simplifier-saegim | 측정 불가(아래) | origin https://github.com/hansunghee7/simplifier-saegim | 2026-09-09 02:09:37 +0900 4c6cac3 | 0줄 |
| C:\work\solar-bible | 측정 불가(아래) | origin https://github.com/hansunghee7/solar-bible | 2026-09-15 08:07:44 +0000 7bede52 | 5줄 |

- Git 저장소 크기 측정 시도: git pack 파일 + 객체 순회 기준 저장소 루트 크기 계산 시도했으나, 5개 저장소 모두 `git cat-file --batch-check --batch-all-objects` 관련 스캔에서 커밋 없이 종료(비영 exit)되어 크기 산출 실패. 따라서 각 git 저장소 크기(GB)는 **미측정**. 단, C:\work 자체는 별도 측정 시 약 15GB 수준(구체적 수치 확보 안 됨 — 미측정).

- 같은 원격 공유 저장소: 없음(5개 모두 origin 중복 없음). 단순화: 한 원격에 여러 클론이 있지 않음.

### 4. 구글 드라이브(G:) 충돌 파일

- G:\내 드라이브 기준: "사본"·"(1)"·"(2)" 포함 파일 총 115개, 약 0.28 GB.
- 상위 10개:
  1. G:\내 드라이브\AI숏폼 아카이브\신기한 아파트사전\ep03-택배차\0831 (1).mp4 — 0.136 GB
  2. G:\내 드라이브\주식회사 심플리파이어\UX & Project\Order_Flow_Prototype_180111 (1).mp4 — 0.06 GB
  3. G:\내 드라이브\주식회사 심플리파이어\백업\Document\2022VC리포트 (1).pdf — 0.018 GB
  4. G:\내 드라이브\주식회사 심플리파이어\강연\PM의기술_금호타이어_202604(사전공유용_책임편) (1).pptx — 0.014 GB
  5. G:\내 드라이브\주식회사 심플리파이어\강연\PM의기술_금호타이어_202604(사전공유용_과장편) (1).pptx — 0.014 GB
  6. G:\내 드라이브\주식회사 심플리파이어\백업\Document\2022-09-16 HDJ_IR_CONFIDENTIAL (1).pdf — 0.012 GB
  7. G:\내 드라이브\주식회사 심플리파이어\히스토리\UX의 언어들\History\UX의 언어들_20260111_공유용 (1).pdf — 0.006 GB
  8. G:\내 드라이브\주식회사 심플리파이어\백업\Simplifier_회사소개서_202310 (2).pdf — 0.004 GB
  9. G:\내 드라이브\주식회사 심플리파이어\백업\Simplifier_회사소개서_202310 (1).pdf — 0.004 GB
  10. G:\내 드라이브\주식회사 심플리파이어\백업\Document\The_Product_Book_2nd_Edition (1).pdf — 0.002 GB
- 0.28GB 전체가 충돌 파일이며, 대부분 백업/문서 계열 중복.

### 5. 정리안 표

번호 | 경로 | 크기(GB) | 종류 | 제안 | 근거 | 사장님 O/X
---|---|---|---|---|---|---|
1 | D:\ (드라이브 자체) | 여유 약 780GB (SSD) | 저장소/아카이브 후보 | D:\Archive 구조로 이동 가능 | SSD 여유 충분, 기존 HDD가 아니므로 이동 부담 적음 | 
2 | C:\Users\PC\AppData\Local\Docker\wsl\disk | 12.35 | Docker/WSL 디스크 이미지 | 그대로 둠 | 활성 컨테이너 환경, 삭제 시 재구축 비용 큼 | 
3 | C:\Users\PC\Downloads\히스토리 | 19.13 | 설치파일 히스토리(아카이브) | D:\Archive\히스토리\ 로 이동 | 완성·설치파일 아카이브로 재다운로드 가능하나 용량↑, 위치 명확 | 
4 | C:\Users\PC\Downloads\히스토리\hansunghee7.github.io-main\...\images (3곳 중복) | 0.38×3 ≈ 1.14 (중복) | 로그·이미지 자산 (중복) | 사장님 판단 | 동일 리포 클로닝 중복으로 보이나 정본 확인 필요 | 
5 | C:\Users\PC\Downloads\히스토리\drive-download-20260216T074921Z-1-001 | 0.14 | 다운로드 아카이브 | D:\Archive\드라이브다운로드\ 로 이동 | 구글로부터 받은 원자료 추정, 용도 확정 시 이동 적절 | 
6 | C:\c\c\Users\PC\_tmp_repo | 미측정(경로 소실) | bash경로 변환 산물 추정 | 사장님 판단 | 현재 경로 없으며 이전 조사에서 1.11GB로 측정된 적 있음. 실체 확인 필요 | 
7 | C:\Users\PC\shorts-lab | 미측정(경로 소실) | 활성·아카이브 혼재 가능 | 사장님 판단 | 현재 경로 없음. shorts-lab 저장소는 C:\work\shorts-lab에 있으나 'C:\Users\PC\shorts-lab'와는 별개 | 
8 | C:\work\solar-bible (git) | 미측정(크기 측정 실패) | 활성 저장소 | 그대로 둠 | 솔라바이블 작업 루트, 삭제 불가 | 
9 | C:\work\hansunghee7.github.io (git) | 미측정(크기 측정 실패) | 활성/공개 저장소 | 그대로 둠 | 공개 사이트 루트, 미커밋 2줄 있음(정리 시 병행 가능, 이번 발주 대상 아님) | 
10 | C:\work\shorts-lab (git) | 미측정(크기 측정 실패) | 활성 저장소 | 그대로 둠 | shorts-lab 클론, C:\Users\PC\shorts-lab과는 별개 | 
11 | C:\work\simplifier-agent (git) | 미측정(크기 측정 실패) | 활성 저장소 | 그대로 둠 | 복제본 다수 여부는 이번 조사에서 확인 못 함 |
12 | C:\work\simplifier-saegim (git) | 미측정(크기 측정 실패) | 활성 저장소 | 그대로 둠 | 복제본 다수 여부는 이번 조사에서 확인 못 함 |
13 | G:\내 드라이브 충돌파일 (사본·(1)·(2)) | 약 0.28 | 구글드라이브 중복 파일 | D:\_정리대기\GDrive_충돌파일\ 로 격리 (향후 정리) | 중복 정리 대상이나 이번 발주에서 삭제 금지, 위치만 확보 | 
14 | C:\Users\PC\ComfyUI (모델·출력 등) | AppData 하위 0.03GB 미만(미미) | AI 모델·작업 | 그대로 둠 | 크기 미미, 활성 작업 도구 | 
15 | C:\Users\PC\OneDrive | 미측정(경로 없음) | 동기화 대상 | 사장님 판단 | 현재 경로 소실, 동기화 상태 확인 필요 |

- **제안을 모두 이행하면 C: 여유 예상 증가: `히스토리`(19.13GB) + `_tmp_repo`(미확인) + 중복 이미지(1.14GB) + GDrive 충돌(0.28GB)을 D:로 옮길 경우, C:에서 약 20.5GB 이상 확보 가능. 단 `_tmp_repo`, `shorts-lab`, OneDrive 등 미확인 항목이 있어 실제 값은 사장님 확인 후 결정.**

---

[작성일: 2026-09-15 신솔라 / 발주: 탐 → 신솔라]
