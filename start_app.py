"""
Startup script for Code Transformer Application
"""

import os
import sys
import subprocess


def main():
    """Start the Code Transformer application with proper checks"""
    
    print("=" * 60)
    print("코드 변수명 표준화 시스템 시작")
    print("=" * 60)
    
    # 1. Run system fixes first
    print("\n1. 시스템 검사 및 수정 중...")
    try:
        result = subprocess.run([sys.executable, "system_fixes.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("시스템 수정 중 오류 발생:")
            print(result.stderr)
            return
    except Exception as e:
        print(f"시스템 검사 실패: {e}")
        return
    
    # 2. Run validation
    print("\n2. 시스템 유효성 검사 중...")
    try:
        result = subprocess.run([sys.executable, "final_validation.py"], 
                              capture_output=True, text=True)
        if "PASSED" not in result.stdout:
            print("유효성 검사 실패:")
            print(result.stdout)
            return
    except Exception as e:
        print(f"유효성 검사 실패: {e}")
        return
    
    # 3. Start the application
    print("\n3. 애플리케이션 시작 중...")
    print("웹 브라우저에서 자동으로 열립니다...")
    print("\n종료하려면 Ctrl+C를 누르세요.")
    print("=" * 60)
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", 
                       "professional_code_transformer_ui.py"])
    except KeyboardInterrupt:
        print("\n애플리케이션이 종료되었습니다.")
    except Exception as e:
        print(f"\n애플리케이션 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    main()