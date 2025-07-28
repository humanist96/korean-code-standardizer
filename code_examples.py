"""
Code Examples Module
Provides various code examples for testing the variable name standardization system
"""

from typing import Dict, List, Tuple
import random


class CodeExamples:
    """Manages code examples for testing"""
    
    def __init__(self):
        self.basic_examples = self._initialize_basic_examples()
        self.issue_based_examples = self._initialize_issue_based_examples()
        self.patterns = self._initialize_patterns()
    
    def _initialize_basic_examples(self) -> Dict[str, Dict]:
        """Initialize basic example codes"""
        return {
            "인증 시스템": {
                "description": "사용자 인증 및 세션 관리 코드",
                "code": """def auth_usr(usr_id, pwd):
    # 사용자 인증 처리
    usr_info = get_usr_from_db(usr_id)
    err_msg = ""
    res = None
    
    if usr_info and check_pwd(pwd, usr_info):
        res = create_session(usr_id)
        usr_cnt = update_login_cnt(usr_id)
        로그인시간 = datetime.now()
    else:
        err_msg = "인증 실패"
    
    return res, err_msg, 로그인시간""",
                "issues": [
                    ("usr → user", "약어 사용", "high"),
                    ("pwd → password", "약어 사용", "high"),
                    ("res → result", "약어 사용", "medium"),
                    ("err_msg → error_message", "약어 사용", "medium"),
                    ("cnt → count", "약어 사용", "medium"),
                    ("로그인시간 → login_time", "한글 변수명", "high")
                ],
                "total_issues": 6
            },
            
            "데이터 처리": {
                "description": "데이터 변환 및 처리 로직",
                "code": """class DataProc:
    def __init__(self):
        self.db_conn = None
        self.데이터목록 = []
        self.cfg = load_config()
    
    def proc_데이터(self, 입력데이터):
        res_lst = []
        err_cnt = 0
        
        for itm in 입력데이터:
            try:
                proc_itm = self.transform_itm(itm)
                res_lst.append(proc_itm)
            except Exception as e:
                err_cnt += 1
                
        return res_lst, err_cnt""",
                "issues": [
                    ("DataProc → DataProcessor", "약어 사용", "medium"),
                    ("db_conn → database_connection", "약어 사용", "medium"),
                    ("cfg → configuration", "약어 사용", "high"),
                    ("proc → process", "약어 사용", "high"),
                    ("res_lst → result_list", "약어 사용", "medium"),
                    ("err_cnt → error_count", "약어 사용", "medium"),
                    ("itm → item", "약어 사용", "high"),
                    ("데이터목록 → data_list", "한글 변수명", "high"),
                    ("입력데이터 → input_data", "한글 변수명", "high")
                ],
                "total_issues": 9
            },
            
            "클래스 정의": {
                "description": "사용자 관리 클래스",
                "code": """class UserMgr:
    def __init__(self):
        self.usr_lst = []
        self.활성사용자수 = 0
        self.max_usr = 1000
    
    def add_usr(self, usr_nm, 이메일, 전화번호):
        usr_obj = {
            'nm': usr_nm,
            'email': 이메일,
            'tel': 전화번호,
            'created_dt': datetime.now(),
            'is_act': True
        }
        
        if len(self.usr_lst) < self.max_usr:
            self.usr_lst.append(usr_obj)
            if usr_obj['is_act']:
                self.활성사용자수 += 1
            return True
        return False""",
                "issues": [
                    ("UserMgr → UserManager", "약어 사용", "medium"),
                    ("usr_lst → user_list", "약어 사용", "high"),
                    ("usr_nm → user_name", "약어 사용", "high"),
                    ("usr_obj → user_object", "약어 사용", "medium"),
                    ("nm → name", "약어 사용", "high"),
                    ("tel → telephone", "약어 사용", "medium"),
                    ("dt → datetime", "약어 사용", "medium"),
                    ("is_act → is_active", "약어 사용", "high"),
                    ("활성사용자수 → active_user_count", "한글 변수명", "high"),
                    ("이메일 → email", "한글 변수명", "high"),
                    ("전화번호 → phone_number", "한글 변수명", "high")
                ],
                "total_issues": 11
            },
            
            "API 엔드포인트": {
                "description": "REST API 핸들러",
                "code": """def handle_req(req_obj):
    resp = {
        'stat': 'ok',
        'msg': '',
        'data': None
    }
    
    try:
        usr_id = req_obj.get('usr_id')
        cmd = req_obj.get('cmd')
        
        if cmd == 'get_usr_info':
            usr_data = fetch_usr_data(usr_id)
            resp['data'] = usr_data
        elif cmd == 'upd_usr':
            upd_res = update_usr(usr_id, req_obj.get('data'))
            resp['data'] = {'upd_cnt': upd_res}
        else:
            resp['stat'] = 'err'
            resp['msg'] = 'Invalid command'
            
    except Exception as e:
        resp['stat'] = 'err'
        resp['msg'] = str(e)
        
    return resp""",
                "issues": [
                    ("req_obj → request_object", "약어 사용", "medium"),
                    ("resp → response", "약어 사용", "high"),
                    ("stat → status", "약어 사용", "high"),
                    ("msg → message", "약어 사용", "high"),
                    ("usr_id → user_id", "약어 사용", "high"),
                    ("cmd → command", "약어 사용", "high"),
                    ("usr_data → user_data", "약어 사용", "medium"),
                    ("upd_usr → update_user", "약어 사용", "high"),
                    ("upd_res → update_result", "약어 사용", "medium"),
                    ("upd_cnt → update_count", "약어 사용", "medium"),
                    ("err → error", "약어 사용", "high")
                ],
                "total_issues": 11
            },
            
            "파일 처리": {
                "description": "파일 읽기 및 처리",
                "code": """def proc_file(파일경로):
    결과목록 = []
    err_lst = []
    
    try:
        with open(파일경로, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for idx, ln in enumerate(lines):
            try:
                proc_ln = process_line(ln.strip())
                if proc_ln:
                    결과목록.append(proc_ln)
            except Exception as e:
                err_lst.append({
                    'ln_num': idx + 1,
                    'err_msg': str(e),
                    'ln_content': ln
                })
                
        return 결과목록, err_lst
        
    except FileNotFoundError:
        return None, [{'err_msg': '파일을 찾을 수 없습니다'}]""",
                "issues": [
                    ("proc_file → process_file", "약어 사용", "high"),
                    ("err_lst → error_list", "약어 사용", "medium"),
                    ("idx → index", "약어 사용", "medium"),
                    ("ln → line", "약어 사용", "high"),
                    ("proc_ln → processed_line", "약어 사용", "medium"),
                    ("ln_num → line_number", "약어 사용", "medium"),
                    ("err_msg → error_message", "약어 사용", "medium"),
                    ("ln_content → line_content", "약어 사용", "medium"),
                    ("파일경로 → file_path", "한글 변수명", "high"),
                    ("결과목록 → result_list", "한글 변수명", "high")
                ],
                "total_issues": 10
            }
        }
    
    def _initialize_issue_based_examples(self) -> Dict[str, Dict]:
        """Initialize examples organized by issue type"""
        return {
            "약어 사용 문제": {
                "description": "의미 없는 약어와 축약형 변수명",
                "code": """def calc_ttl(usr_lst):
    ttl = 0
    cnt = 0
    
    for usr in usr_lst:
        amt = usr.get('amt', 0)
        if amt > 0:
            ttl += amt
            cnt += 1
    
    avg = ttl / cnt if cnt > 0 else 0
    return ttl, cnt, avg""",
                "expected_changes": [
                    "calc_ttl → calculate_total",
                    "usr_lst → user_list",
                    "ttl → total",
                    "cnt → count",
                    "usr → user",
                    "amt → amount",
                    "avg → average"
                ],
                "issues_count": 7
            },
            
            "한글 변수명 문제": {
                "description": "한글로 작성된 변수명과 한영 혼용",
                "code": """class 상품관리:
    def __init__(self):
        self.상품목록 = []
        self.재고수량 = {}
        
    def add_상품(self, 상품명, 가격, 수량):
        상품정보 = {
            'name': 상품명,
            'price': 가격,
            'qty': 수량,
            '등록일': datetime.now()
        }
        self.상품목록.append(상품정보)
        self.재고수량[상품명] = 수량""",
                "expected_changes": [
                    "상품관리 → ProductManager",
                    "상품목록 → product_list",
                    "재고수량 → inventory_quantity",
                    "상품명 → product_name",
                    "가격 → price",
                    "수량 → quantity",
                    "상품정보 → product_info",
                    "등록일 → registration_date"
                ],
                "issues_count": 8
            },
            
            "명명 규칙 일관성 문제": {
                "description": "서로 다른 명명 규칙이 혼재된 코드",
                "code": """class dataProcessor:
    def __init__(self):
        self.MaxSize = 1000
        self.current_size = 0
        self.DataList = []
        
    def AddData(self, newData):
        if self.current_size < self.MaxSize:
            self.DataList.append(newData)
            self.current_size += 1
            return True
        return False
    
    def get_data_by_index(self, idx):
        if 0 <= idx < self.current_size:
            return self.DataList[idx]
        return None""",
                "expected_changes": [
                    "dataProcessor → DataProcessor (또는 data_processor)",
                    "MaxSize → max_size",
                    "DataList → data_list",
                    "AddData → add_data",
                    "newData → new_data",
                    "일관된 명명 규칙 적용 필요"
                ],
                "issues_count": 5
            }
        }
    
    def _initialize_patterns(self) -> Dict[str, Dict]:
        """Initialize code generation patterns"""
        return {
            "authentication": {
                "name": "인증 시스템",
                "description": "로그인 및 인증 관련 코드",
                "template": """def auth_{type}(usr_id, pwd, 토큰=None):
    usr_info = get_usr_info(usr_id)
    res = {{
        'stat': 'fail',
        'msg': '',
        'usr_data': None
    }}
    
    if validate_{type}(usr_info, pwd, 토큰):
        res['stat'] = 'ok'
        res['usr_data'] = usr_info
        로그인횟수 = increment_cnt(usr_id)
    else:
        res['msg'] = '인증 실패'
    
    return res"""
            },
            
            "data_processing": {
                "name": "데이터 처리",
                "description": "데이터 변환 및 가공",
                "template": """def proc_data_{type}(입력데이터):
    결과 = []
    err_cnt = 0
    
    for idx, itm in enumerate(입력데이터):
        try:
            proc_itm = transform_{type}(itm)
            if validate_itm(proc_itm):
                결과.append(proc_itm)
        except Exception as e:
            err_cnt += 1
            
    return 결과, err_cnt"""
            },
            
            "database": {
                "name": "데이터베이스 쿼리",
                "description": "DB 조회 및 업데이트",
                "template": """def exec_qry(qry_type, 파라미터):
    conn = get_db_conn()
    res_lst = []
    
    try:
        cur = conn.cursor()
        
        if qry_type == 'sel':
            cur.execute("SELECT * FROM usr WHERE stat = ?", [파라미터])
            res_lst = cur.fetchall()
        elif qry_type == 'upd':
            upd_cnt = cur.execute("UPDATE usr SET stat = ?", [파라미터])
            conn.commit()
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
        
    return res_lst"""
            },
            
            "api_handler": {
                "name": "API 핸들러",
                "description": "REST API 요청 처리",
                "template": """@app.route('/api/{endpoint}')
def handle_{endpoint}_req():
    req_data = request.get_json()
    resp = {{
        'stat': 'ok',
        'msg': '',
        'res_data': None
    }}
    
    try:
        usr_id = req_data.get('usr_id')
        cmd = req_data.get('cmd')
        
        if validate_req(usr_id, cmd):
            res = process_{endpoint}(req_data)
            resp['res_data'] = res
        else:
            resp['stat'] = 'err'
            resp['msg'] = '잘못된 요청'
            
    except Exception as e:
        resp['stat'] = 'err'
        resp['msg'] = str(e)
        
    return jsonify(resp)"""
            },
            
            "file_handler": {
                "name": "파일 처리",
                "description": "파일 읽기/쓰기 작업",
                "template": """def proc_file_{type}(파일명):
    결과목록 = []
    err_lst = []
    ln_cnt = 0
    
    try:
        with open(파일명, 'r', encoding='utf-8') as f:
            for ln_num, ln in enumerate(f):
                try:
                    proc_ln = parse_{type}_line(ln.strip())
                    결과목록.append(proc_ln)
                    ln_cnt += 1
                except Exception as e:
                    err_lst.append({{
                        'ln': ln_num + 1,
                        'err': str(e)
                    }})
                    
    except FileNotFoundError:
        err_lst.append({{'err': '파일 없음'}})
        
    return 결과목록, err_lst, ln_cnt"""
            },
            
            "calculator": {
                "name": "계산 로직",
                "description": "수치 계산 및 통계",
                "template": """def calc_{metric}(데이터목록):
    ttl = 0
    cnt = 0
    min_val = float('inf')
    max_val = float('-inf')
    
    for itm in 데이터목록:
        val = itm.get('val', 0)
        if val > 0:
            ttl += val
            cnt += 1
            min_val = min(min_val, val)
            max_val = max(max_val, val)
    
    avg = ttl / cnt if cnt > 0 else 0
    
    return {{
        'ttl': ttl,
        'cnt': cnt,
        'avg': avg,
        'min': min_val if cnt > 0 else 0,
        'max': max_val if cnt > 0 else 0
    }}"""
            }
        }
    
    def get_basic_example(self, name: str) -> Dict:
        """Get a specific basic example"""
        return self.basic_examples.get(name)
    
    def get_all_basic_examples(self) -> Dict[str, Dict]:
        """Get all basic examples"""
        return self.basic_examples
    
    def get_issue_based_example(self, issue_type: str) -> Dict:
        """Get an example for a specific issue type"""
        return self.issue_based_examples.get(issue_type)
    
    def get_all_issue_based_examples(self) -> Dict[str, Dict]:
        """Get all issue-based examples"""
        return self.issue_based_examples
    
    def generate_random_code(self, pattern: str = None, complexity: str = "medium") -> Tuple[str, str, str]:
        """Generate random code based on pattern and complexity"""
        if pattern is None:
            pattern = random.choice(list(self.patterns.keys()))
        
        if pattern not in self.patterns:
            pattern = "authentication"
        
        template = self.patterns[pattern]["template"]
        
        # Customize based on complexity
        if complexity == "simple":
            # Simple version with fewer issues
            code = template.format(
                type="basic",
                endpoint="users",
                metric="sum"
            ).split('\n')[:10]  # Shorter code
            code = '\n'.join(code)
        elif complexity == "complex":
            # Complex version with more issues
            code = template.format(
                type="advanced",
                endpoint="transactions",
                metric="statistics"
            )
            # Add more complexity
            additional = """
    # 추가 복잡도
    캐시데이터 = get_cache_data(usr_id)
    if 캐시데이터:
        ttl_time = calculate_ttl(캐시데이터)
        if ttl_time > 0:
            return 캐시데이터
    
    # 추가 검증
    for idx, itm in enumerate(데이터목록):
        검증결과 = validate_complex(itm)
        if not 검증결과:
            err_cnt += 1"""
            code = code.replace("return", additional + "\n    return", 1)
        else:
            # Medium complexity
            code = template.format(
                type="standard",
                endpoint="data",
                metric="average"
            )
        
        pattern_info = self.patterns[pattern]
        description = f"{pattern_info['name']} - {pattern_info['description']} (복잡도: {complexity})"
        
        return code, pattern, description
    
    def get_pattern_names(self) -> List[str]:
        """Get list of available pattern names"""
        return [(key, info["name"]) for key, info in self.patterns.items()]