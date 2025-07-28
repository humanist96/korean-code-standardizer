"""
전문가용 변수명 표준화 시스템 실행 스크립트
Professional Variable Name Standardization System Launcher
"""

import sys
import os
import subprocess
import io

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_requirements():
    """Check if required packages are installed"""
    required = ['streamlit', 'pandas', 'plotly', 'openpyxl']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  필수 패키지가 설치되어 있지 않습니다: {', '.join(missing)}")
        print("다음 명령어로 설치해주세요:")
        print(f"pip install -r requirements.txt")
        return False
    
    return True


def main():
    print("=" * 60)
    print("🔍 전문가용 변수명 표준화 분석 시스템")
    print("Professional Variable Name Standardization System")
    print("=" * 60)
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n필수 패키지를 설치한 후 다시 실행해주세요.")
        sys.exit(1)
    
    # Check if CSV exists
    if os.path.exists("용어사전.csv"):
        print("✅ 용어사전.csv 파일이 로드됩니다.")
    else:
        print("⚠️  용어사전.csv 파일이 없습니다. 기본 용어사전을 사용합니다.")
    
    print("\n실행 옵션:")
    print("1. 전문가용 웹 인터페이스 (권장)")
    print("2. 기본 웹 인터페이스")
    print("3. 배치 처리 테스트")
    print("4. 랜덤 코드 생성 테스트")
    print("5. 빠른 콘솔 테스트")
    print("0. 종료")
    
    choice = input("\n선택하세요 (1-5, 0): ").strip()
    
    if choice == "0":
        print("프로그램을 종료합니다.")
        sys.exit(0)
    
    elif choice == "1":
        print("\n🚀 전문가용 웹 인터페이스를 시작합니다...")
        print("브라우저에서 http://localhost:8501 로 접속하세요.")
        print("종료하려면 Ctrl+C를 누르세요.\n")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "professional_web_interface.py"])
    
    elif choice == "2":
        print("\n🚀 기본 웹 인터페이스를 시작합니다...")
        print("브라우저에서 http://localhost:8501 로 접속하세요.")
        print("종료하려면 Ctrl+C를 누르세요.\n")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "web_interface.py"])
    
    elif choice == "3":
        print("\n📁 배치 처리 테스트를 실행합니다...")
        from batch_processor import BatchProcessor
        
        processor = BatchProcessor()
        results = processor.process_directory(".", "*.py", recursive=False)
        report = processor.generate_batch_report(results)
        
        print(f"\n분석 완료:")
        print(f"- 총 파일: {report['summary']['total_files']}개")
        print(f"- 발견된 이슈: {report['summary']['total_issues']}개")
        print(f"- 평균 처리 시간: {report['summary']['avg_time_per_file']:.2f}초/파일")
        
        if report['issue_types']:
            print("\n주요 이슈 유형:")
            for issue_type, count in list(report['issue_types'].items())[:5]:
                print(f"  - {issue_type}: {count}개")
    
    elif choice == "4":
        print("\n🎲 랜덤 코드 생성 테스트...")
        from code_generator import RandomCodeGenerator
        
        generator = RandomCodeGenerator()
        for i in range(3):
            print(f"\n--- 샘플 {i+1} ---")
            code, pattern, desc = generator.generate_random_code()
            print(f"패턴: {pattern}")
            print(f"설명: {desc}")
            print("\n생성된 코드:")
            print(code[:300] + "..." if len(code) > 300 else code)
    
    elif choice == "5":
        print("\n🔍 빠른 테스트 실행...")
        subprocess.run([sys.executable, "quick_test.py"])
    
    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()