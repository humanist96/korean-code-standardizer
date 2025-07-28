"""
로컬 실행 및 테스트 스크립트
변수명 표준화 시스템을 바로 실행할 수 있는 간단한 인터페이스
"""

import sys
from variable_name_standardizer import CodeReviewer
from advanced_analyzer import AdvancedCodeReviewer


def main():
    print("=" * 60)
    print("변수명 표준화 검토 시스템")
    print("=" * 60)
    print("\n실행 옵션:")
    print("1. 간단한 테스트 (샘플 코드)")
    print("2. 직접 코드 입력")
    print("3. 파일에서 코드 읽기")
    print("4. 고급 분석 모드")
    print("5. 웹 인터페이스 실행")
    print("0. 종료")
    
    while True:
        choice = input("\n선택하세요 (0-5): ").strip()
        
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
            
        elif choice == "1":
            run_sample_test()
            
        elif choice == "2":
            run_interactive_test()
            
        elif choice == "3":
            run_file_test()
            
        elif choice == "4":
            run_advanced_test()
            
        elif choice == "5":
            run_web_interface()
            
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")


def run_sample_test():
    """샘플 코드로 테스트"""
    print("\n--- 샘플 코드 테스트 ---")
    
    sample_codes = [
        ("한글 변수명 혼용", """
def check_사용자_auth(usr_id, pwd):
    사용자 = get_user(usr_id)
    if 사용자 and 사용자['password'] == pwd:
        return True
    return False
"""),
        
        ("약어 사용", """
def proc_req(req_obj):
    usr = req_obj.get('usr')
    res = None
    err_msg = ""
    
    if usr:
        res = validate_usr(usr)
    else:
        err_msg = "User not found"
    
    return res, err_msg
"""),
        
        ("명명 규칙 불일치", """
def getUserInfo(user_id):
    userData = fetch_data(user_id)
    user_settings = get_settings(user_id)
    LastLogin = get_last_login(user_id)
    
    return {
        'data': userData,
        'settings': user_settings,
        'last_login': LastLogin
    }
""")
    ]
    
    reviewer = CodeReviewer()
    
    for name, code in sample_codes:
        print(f"\n[{name}]")
        print("코드:")
        print(code)
        print("\n검토 결과:")
        results = reviewer.review_code(code)
        print(reviewer.format_results(results))
        print("-" * 40)


def run_interactive_test():
    """사용자가 직접 코드 입력"""
    print("\n--- 직접 코드 입력 ---")
    print("코드를 입력하세요. (빈 줄을 두 번 입력하면 종료)")
    
    lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
        lines.append(line)
    
    code = '\n'.join(lines[:-2])  # 마지막 빈 줄 제거
    
    if code.strip():
        reviewer = CodeReviewer()
        print("\n검토 결과:")
        results = reviewer.review_code(code)
        print(reviewer.format_results(results))
    else:
        print("입력된 코드가 없습니다.")


def run_file_test():
    """파일에서 코드 읽기"""
    print("\n--- 파일에서 코드 읽기 ---")
    file_path = input("파일 경로를 입력하세요: ").strip()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        reviewer = CodeReviewer()
        print(f"\n파일: {file_path}")
        print("검토 결과:")
        results = reviewer.review_code(code)
        print(reviewer.format_results(results))
        
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        print(f"오류 발생: {e}")


def run_advanced_test():
    """고급 분석 모드"""
    print("\n--- 고급 분석 모드 ---")
    print("근거 기반 상세 분석을 수행합니다.")
    
    sample_code = """
class UserMgr:
    def __init__(self):
        self.usr_cnt = 0
        self.pwd_cache = {}
        
    def add_usr(self, usr_nm, pwd):
        usr_obj = {
            'id': self.usr_cnt + 1,
            'name': usr_nm,
            'password': pwd
        }
        self.usr_cnt += 1
        return usr_obj
"""
    
    print("\n분석할 코드:")
    print(sample_code)
    
    reviewer = AdvancedCodeReviewer()
    results = reviewer.review_with_evidence(sample_code)
    print("\n상세 분석 결과:")
    print(reviewer.format_detailed_results(results))


def run_web_interface():
    """웹 인터페이스 실행"""
    print("\n--- 웹 인터페이스 실행 ---")
    print("Streamlit 웹 인터페이스를 시작합니다...")
    print("브라우저에서 http://localhost:8501 로 접속하세요.")
    print("종료하려면 Ctrl+C를 누르세요.\n")
    
    import os
    os.system("streamlit run web_interface.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()