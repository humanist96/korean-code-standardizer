@echo off
echo ====================================
echo 변수명 표준화 시스템 테스트 실행
echo ====================================
echo.

echo 1. 빠른 테스트 실행
python quick_test.py
echo.
echo 테스트 완료!
echo.

echo 2. 대화형 테스트를 시작하려면 아무 키나 누르세요...
pause > nul
python run_local.py