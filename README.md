# 🤖 KOSCOM 코딩 Agent
### AI 기반 코드 품질 개선 및 표준화 솔루션

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://korean-code-standardizer.streamlit.app/)

KOSCOM 코딩 Agent는 AI 기술을 활용하여 Python 코드의 변수명을 표준화하고 코드 품질을 개선하는 웹 애플리케이션입니다. 용어사전 기반으로 일관된 명명 규칙을 적용하고, 대화형 인터페이스를 통해 쉽게 사용할 수 있습니다.

## ✨ 주요 기능

### 1. 🔄 코드 변환
- **AST 기반 코드 분석**: Python AST를 사용한 정확한 변수명 추출
- **용어사전 기반 표준화**: CSV 기반 표준 용어사전 활용
- **명명 규칙 자동 감지**: snake_case, camelCase, PascalCase 등
- **신뢰도 기반 변환**: 설정 가능한 신뢰도 임계값

### 2. 📚 용어사전 관리
- **표준 용어 관리**: 한국어-영어 표준 용어 매핑
- **검색 및 필터링**: 카테고리별, 태그별 검색
- **용어 추가/수정/삭제**: 직관적인 CRUD 인터페이스
- **CSV 가져오기/내보내기**: 대량 용어 관리

### 3. 📊 통계 및 분석
- **변환 이력 추적**: 모든 변환 세션 기록
- **시각화 대시보드**: 일별/주별/월별 통계
- **품질 지표**: 평균 신뢰도, 이슈 분포 등
- **생산성 메트릭**: 변환 효율성 측정

### 4. ⚙️ 설정 관리
- **UI 커스터마이징**: 테마, 언어, 표시 옵션
- **변환 설정**: 명명 규칙, 신뢰도 설정
- **통계 설정**: 보관 기간, 내보내기 옵션
- **고급 설정**: 성능 및 디버그 옵션

## 🚀 시작하기

### 온라인 버전 (권장)
[https://korean-code-standardizer.streamlit.app/](https://korean-code-standardizer.streamlit.app/)에서 바로 사용할 수 있습니다.

### 로컬 설치

1. **저장소 클론**
```bash
git clone https://github.com/humanist96/korean-code-standardizer.git
cd korean-code-standardizer
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **애플리케이션 실행**
```bash
streamlit run professional_code_transformer_ui.py
```

## 📂 프로젝트 구조

```
korean-code-standardizer/
├── professional_code_transformer_ui.py  # 메인 UI 애플리케이션
├── enhanced_code_reviewer.py           # 코드 리뷰 엔진
├── terminology_manager.py              # 용어사전 관리
├── statistics_manager.py               # 통계 관리
├── settings_manager.py                 # 설정 관리
├── visualization_dashboard.py          # 시각화 대시보드
├── code_examples.py                    # 코드 예제
├── 용어사전.csv                         # 표준 용어사전
└── requirements.txt                    # 의존성 목록
```

## 🔧 사용 예시

### 변환 전
```python
def process_usr_data(usr_id, pwd):
    usr_obj = get_user(usr_id)
    err_msg = ""
    res = None
```

### 변환 후
```python
def process_user_data(user_id, password):
    user_object = get_user(user_id)
    error_message = ""
    result = None
```

## 📊 통계 기능

- **일별/주별/월별 변환 추이**
- **이슈 타입별 분포**
- **가장 많이 변환된 패턴**
- **평균 신뢰도 및 생산성 지표**

## ⚙️ 설정 옵션

- **표시 설정**: 테마, 언어, 줄 번호 표시
- **변환 설정**: 명명 규칙, 신뢰도 임계값
- **통계 설정**: 데이터 보관 기간, 자동 내보내기
- **UI 설정**: 애니메이션, 알림음, 툴팁

## 🤝 기여하기

이 프로젝트에 기여하고 싶으시다면:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📧 문의

프로젝트 관련 문의사항은 [humanist96@gmail.com](mailto:humanist96@gmail.com)으로 연락주세요.

---

Made with ❤️ by humanist96