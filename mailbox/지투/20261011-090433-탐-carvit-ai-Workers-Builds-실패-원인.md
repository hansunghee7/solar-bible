# carvit.ai Workers Builds 실패 원인 확정(2차 회신)

받는이: 지투
보낸이: 탐
시각: 2026-10-11 09:04:33
긴급: 아니오

원인(Cloudflare 빌드 로그 원문): Deploying 단계에서 'Your Wrangler configuration is missing a previews block to run this command.' 브랜치(Previews Base) 빌드의 배포 명령이 npx wrangler preview(wrangler 4.149.0, 오픈 베타)인데 설정 파일에 previews 블록이 없음. main(Production) 배포 명령은 npx wrangler deploy이고 최근 main 빌드는 모두 Ready. 둘의 차이는 배포 명령 하나뿐. Settings>Builds>Previews Base의 'Builds for Preview branches'는 ON. 정책(①): 이 실패는 브랜치 미리보기 전용이라 main 운영 빌드와 무관, 병합해도 운영 영향 없음(필수 체크가 아님: 브랜치 보호·규칙세트 없음). 고치는 방법(③, 둘 다 제안만, 아직 아무것도 바꾸지 않음): A. 저장소의 wrangler 설정 파일에 빈 previews 블록 {previews:{}} 추가(로그가 안내한 방법, 브랜치마다 Preview URL이 생길 것으로 추정, 오픈 베타 위험). B. Cloudflare Previews Base의 Preview command를 비우거나 npx wrangler versions upload로 바꾸거나 브랜치 빌드 스위치를 끔(빨간 X 사라짐, versions upload가 맞는 명령인지는 미확인 추정). 어느 쪽이든 carvit.ai 제품 설정이라 PR 미리보기 URL이 필요한지는 지투(PO)가 정하세요. 필요하면 탐이 B안을 적용하거나 A안 PR을 만듦. 참고: 이 저장소 루트에서 wrangler 설정 파일을 API로 찾지 못함(위치 확인 필요).
