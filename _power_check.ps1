$scheme = powercfg /getactivescheme
Write-Output $scheme
Write-Output "---"
# GUID로 계획 이름 확인
$guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
try {
    $name = (powercfg /setactive $guid 2>&1)
    Write-Output "GUID $guid 이름 조회 시도 완료"
} catch {
    Write-Output "GUID 조회 실패: $_"
}
