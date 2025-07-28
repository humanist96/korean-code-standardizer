# 🤖 AI 챗봇 사용 가이드

## 개선된 기능

### 1. 향상된 코드 감지
- 더 유연한 의도 분석
- 다양한 Python 문법 패턴 인식
- 인라인 코드 및 백틱 지원

### 2. 지원되는 코드 입력 방법

#### 방법 1: 코드 블록 사용 (권장)
```
이 코드를 분석해줘:
```python
def process_usr_data(usr_id, pwd):
    usr_obj = get_user(usr_id)
    return usr_obj
```
```

#### 방법 2: 인라인 백틱
```
`usr_cnt = len(usr_list)` 이 코드를 개선해줘
```

#### 방법 3: 직접 입력
```
변환해줘:
def calc_avg(lst):
    res = sum(lst) / len(lst)
    return res
```

### 3. 트리거 키워드
다음 키워드들이 코드 분석을 트리거합니다:
- 변환
- 분석
- 수정
- 개선
- 검토
- transform
- analyze
- fix
- improve
- review

### 4. 사용 예시

#### 예시 1: 코드 변환
```
사용자: 
```python
def get_usr_info(usr_id):
    usr_data = fetch_data(usr_id)
    err_msg = validate(usr_data)
    return usr_data, err_msg
```

챗봇: ✅ 3개의 개선사항을 발견했습니다!
- usr_id → user_id
- usr_data → user_data  
- err_msg → error_message
```

#### 예시 2: 간단한 분석
```
사용자: usr_cnt = count_users() 분석해줘

챗봇: ✅ 1개의 개선사항을 발견했습니다!
- usr_cnt → user_count (의미 없는 약어 사용)
```

#### 예시 3: 코드 없이 요청
```
사용자: 코드 개선해줘

챗봇: 코드 변환 방법:
다음과 같은 방법으로 코드를 입력해주세요:
```python
def process_usr_data(usr_id):
    return usr_id
```
```

### 5. 팁
- 코드 블록을 사용하면 가장 정확하게 인식됩니다
- 여러 줄 코드는 ``` 블록을 사용하세요
- 한 줄 코드는 그냥 입력해도 됩니다
- 코드와 함께 "변환", "분석" 등의 키워드를 사용하면 더 잘 인식됩니다

## 문제 해결

### 코드가 인식되지 않을 때
1. 코드를 ``` python 블록으로 감싸기
2. "변환해줘", "분석해줘" 등의 키워드 추가
3. 코드만 입력하지 말고 설명 추가

### 잘못된 분석 결과
1. 코드가 완전한지 확인
2. Python 문법이 올바른지 확인
3. 들여쓰기가 제대로 되어있는지 확인

## 🚀 바로 시작하기

1. AI 챗봇 페이지로 이동
2. 예제 코드 버튼 클릭 또는 직접 코드 입력
3. 변환 결과 확인
4. 필요시 추가 질문이나 수정 요청

이제 더 똑똑해진 AI 챗봇을 사용해보세요! 🎉