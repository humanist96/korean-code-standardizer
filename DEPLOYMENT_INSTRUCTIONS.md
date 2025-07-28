# 🚀 GitHub 및 Streamlit 배포 가이드

## 📋 준비 사항
- GitHub 계정: humanist96@gmail.com
- Streamlit 계정 (GitHub 계정으로 로그인 가능)
- 로컬에 git 설치 완료 ✅

## 🔧 GitHub 배포 단계

### 1. GitHub 저장소 생성
1. [GitHub](https://github.com)에 로그인
2. 우측 상단 '+' 클릭 → 'New repository'
3. 다음 정보 입력:
   - **Repository name**: `korean-code-standardizer`
   - **Description**: `Korean Code Variable Name Standardizer - 한국어 코드 변수명 표준화 시스템`
   - **Public** 선택 (Streamlit 무료 배포를 위해)
   - **Initialize repository** 체크 해제 (이미 로컬에 있으므로)
4. 'Create repository' 클릭

### 2. 로컬 저장소를 GitHub에 연결
GitHub에서 생성된 저장소 페이지에 나온 명령어를 실행:

```bash
# GitHub 원격 저장소 추가
git remote add origin https://github.com/humanist96/korean-code-standardizer.git

# 브랜치 이름을 main으로 변경 (선택사항)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. 파일 확인
GitHub 저장소에서 모든 파일이 정상적으로 업로드되었는지 확인

## 🎈 Streamlit 배포 단계

### 1. Streamlit Cloud 접속
1. [share.streamlit.io](https://share.streamlit.io) 접속
2. 'Continue with GitHub' 클릭하여 GitHub 계정으로 로그인

### 2. 새 앱 배포
1. 'New app' 버튼 클릭
2. 다음 정보 입력:
   - **Repository**: `humanist96/korean-code-standardizer`
   - **Branch**: `main`
   - **Main file path**: `professional_code_transformer_ui.py`
   - **App URL**: `korean-code-standardizer` (또는 원하는 이름)

### 3. 고급 설정 (선택사항)
'Advanced settings' 클릭하여 환경 변수 설정 가능:
```toml
[server]
maxUploadSize = 10

[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### 4. 배포 시작
'Deploy!' 버튼 클릭하여 배포 시작

### 5. 배포 상태 확인
- 배포는 보통 2-5분 정도 소요
- 로그를 확인하여 오류가 없는지 체크
- 배포 완료 후 자동으로 앱이 열림

## 🔗 최종 URL
배포가 완료되면 다음과 같은 URL로 접속 가능:
- `https://korean-code-standardizer.streamlit.app/`

## 📝 추가 작업

### README.md 업데이트
배포 후 README.md의 Streamlit 배지 URL 업데이트:
```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://korean-code-standardizer.streamlit.app/)
```

### 지속적 배포
GitHub 저장소에 푸시하면 Streamlit이 자동으로 재배포:
```bash
git add .
git commit -m "Update: 기능 설명"
git push
```

## 🐛 문제 해결

### 일반적인 오류
1. **ModuleNotFoundError**: requirements.txt 확인
2. **파일을 찾을 수 없음**: 파일 경로 및 이름 확인
3. **메모리 초과**: Streamlit 무료 플랜은 1GB RAM 제한

### 로그 확인
Streamlit Cloud 대시보드에서 앱 로그 확인 가능

## ✅ 체크리스트
- [ ] GitHub 저장소 생성
- [ ] 코드 푸시
- [ ] Streamlit 계정 생성
- [ ] 앱 배포
- [ ] 배포 확인
- [ ] README 업데이트

---

배포 완료 후 앱 URL을 공유해주세요! 🎉