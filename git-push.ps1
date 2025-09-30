# Git 자동 푸시 스크립트
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "   Git Push 자동화 스크립트" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# 1단계: Git Status 확인
Write-Host "[1단계] 변경사항 확인 중..." -ForegroundColor Yellow
Write-Host ""
git status
Write-Host ""

$continue = Read-Host "변경사항을 Stage에 추가하시겠습니까? (y/n)"
if ($continue -ne "y") {
    Write-Host "작업을 취소했습니다." -ForegroundColor Red
    exit
}

# 2단계: Git Add
Write-Host ""
Write-Host "[2단계] 모든 변경사항을 Stage에 추가 중..." -ForegroundColor Yellow
git add .
Write-Host "✓ 완료!" -ForegroundColor Green
Write-Host ""

# Stage된 파일 확인
Write-Host "Stage된 파일 목록:" -ForegroundColor Cyan
git status --short
Write-Host ""

$continue = Read-Host "커밋을 진행하시겠습니까? (y/n)"
if ($continue -ne "y") {
    Write-Host "작업을 취소했습니다." -ForegroundColor Red
    exit
}

# 3단계: Git Commit
Write-Host ""
Write-Host "[3단계] 커밋 메시지 입력" -ForegroundColor Yellow
$commitMessage = Read-Host "커밋 메시지를 입력하세요"

if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    Write-Host "커밋 메시지가 비어있습니다. 작업을 취소합니다." -ForegroundColor Red
    exit
}

git commit -m "$commitMessage"
Write-Host "✓ 커밋 완료!" -ForegroundColor Green
Write-Host ""

# 4단계: Git Push
Write-Host "[4단계] GitHub에 푸시 준비 완료" -ForegroundColor Yellow
Write-Host ""
Write-Host "마지막 커밋 정보:" -ForegroundColor Cyan
git log --oneline -1
Write-Host ""

$continue = Read-Host "GitHub에 푸시하시겠습니까? (y/n)"
if ($continue -ne "y") {
    Write-Host "푸시를 취소했습니다. 커밋은 로컬에 저장되었습니다." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "푸시 중..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "   ✓ 성공적으로 푸시했습니다!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "   ✗ 푸시 실패" -ForegroundColor Red
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "오류를 확인하고 다시 시도하세요." -ForegroundColor Yellow
}

Write-Host ""
