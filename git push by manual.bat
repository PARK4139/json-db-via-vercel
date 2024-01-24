:: CONSOLE SETTING
title %~n0
color df
chcp 65001 >nul
@echo off
@rem @echo on
setlocal
for /f "delims=" %%i in ('Powershell.exe get-date -Format 'yyyy MM dd HH mm ss'') do set yyyyMMddHHmmss=%%i
cls


:: MINIMIZED WINDOW SETTING
:: if not "%minimized%"=="" goto :minimized
:: set minimized=true
:: start /min cmd /C "%~dpnx0"
:: goto :EOF
:: :minimized


:: COMMIT MENT SETTING 
:: set commit_ment=REFER TO README.md (commited at %yyyyMMddHHmmss%)
:: set commit_ment=Jquery 추가, Jquery 베이스 기능 자동닫힘팝업 추가
:: set commit_ment=Jquery 삭제, 자동닫힘팝업 기능변경
:: set commit_ment=build 에러 디버깅 완료, 커스텀 에러페이지 추가
:: set commit_ment=build 에러 발견 디버깅 전 백업
:: set commit_ment=기술 블로그 next.js 페이지 중간 백업
:: set commit_ment=기술 블로그 build 테스트 완료
:: set commit_ment=기술 블로그 next.js 페이지 중간 백업
:: set commit_ment=기술 블로그 next.js 페이지 상단이동버튼 추가/회전애니 추가/이동성 생성애니 추가/백그라운드 이미지 추가
:: set commit_ment=로고/네비게이션 애니 및 이벤트 수정
:: set commit_ment=팝업기능 수정
:: set commit_ment=배포테스트
:: set commit_ment=라우터에 의한 빌드 실패 디버깅 완료
:: set commit_ment=배포 후 운영에서 특정 이미지만 안나오는 현상 디버깅 전 백업
:: set commit_ment=배포 후 운영에서 특정 이미지만 안나오는 현상 디버깅 완료
:: set commit_ment=배포 후 운영에서 특정 이미지만 안나오는 현상 디버깅 완료
:: set commit_ment=next.js 클라이언트 사이드 환경변수 배포 설정 변경
:: set commit_ment=정적 리소스 캐싱 문제 디버깅 시도
set commit_ment=CORS 문제 처리 시도




:: GIT PUSH
git add *  
git commit -m "%commit_ment%"
git push -u origin main
git status | find "working tree clean" 



:: GET PROJECT_DIRECTORY
SET PROJECT_DIRECTORY=%cd%
for %%F in ("%CD%") do set "PROJECT_DIRECTORY_DIRNAME=%%~nxF"



:: CHECK GIT HUB PUSH DONE (Now)
explorer https://github.com/Park4139/%PROJECT_DIRECTORY_DIRNAME%



:: DEBUG SET UP
:: timeout 600