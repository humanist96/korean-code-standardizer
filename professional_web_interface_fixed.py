"""
Professional Web Interface for Variable Name Standardization System - Fixed Version
Enhanced UI with visualization, random code generation, and advanced features
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import base64
from io import BytesIO
import os
import sys
import io

# Note: Streamlit handles encoding internally, so we don't need to set it manually

from variable_name_standardizer import CodeReviewer, NamingConvention
from advanced_analyzer import AdvancedCodeReviewer
from code_generator import RandomCodeGenerator


# Page configuration
st.set_page_config(
    page_title="변수명 표준화 분석 시스템",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .code-block {
        background-color: #f4f4f4;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
    }
    .suggestion-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    h1 {
        color: #1f2937;
        font-weight: 700;
    }
    h2 {
        color: #374151;
        font-weight: 600;
    }
    h3 {
        color: #4b5563;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


class ProfessionalInterface:
    def __init__(self):
        self.csv_path = "용어사전.csv"
        
        # Initialize reviewers with error handling
        try:
            self.reviewer = CodeReviewer(self.csv_path)
            self.advanced_reviewer = AdvancedCodeReviewer(self.csv_path)
            self.terms_loaded = len(self.reviewer.dictionary.terms)
        except Exception as e:
            st.error(f"용어사전 로드 중 오류 발생: {str(e)}")
            self.reviewer = CodeReviewer()
            self.advanced_reviewer = AdvancedCodeReviewer()
            self.terms_loaded = 0
            
        self.code_generator = RandomCodeGenerator()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'generated_codes' not in st.session_state:
            st.session_state.generated_codes = []
        if 'batch_results' not in st.session_state:
            st.session_state.batch_results = []
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
    
    def run(self):
        """Main application entry point"""
        # Header
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.title("🔍 변수명 표준화 분석 시스템")
            st.caption("Professional Variable Name Standardization & Analysis Platform")
        
        with col2:
            st.metric(
                "용어사전 크기",
                f"{self.terms_loaded:,}개",
                f"+{self.terms_loaded - 50:,}" if self.terms_loaded > 50 else None
            )
        
        with col3:
            analysis_count = len(st.session_state.analysis_history)
            st.metric(
                "분석 횟수",
                f"{analysis_count:,}회",
                f"+{analysis_count}" if analysis_count > 0 else None
            )
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔍 코드 분석",
            "🎲 랜덤 코드 생성",
            "📊 시각화 대시보드",
            "📚 용어사전 관리",
            "📈 분석 리포트",
            "⚙️ 설정"
        ])
        
        with tab1:
            self._render_code_analysis_tab()
        
        with tab2:
            self._render_random_generator_tab()
        
        with tab3:
            self._render_visualization_tab()
        
        with tab4:
            self._render_dictionary_tab()
        
        with tab5:
            self._render_reports_tab()
        
        with tab6:
            self._render_settings_tab()
    
    def _render_code_analysis_tab(self):
        """Render code analysis tab"""
        st.header("코드 분석")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Analysis mode selection
            analysis_mode = st.radio(
                "분석 모드",
                ["기본 분석", "고급 분석 (근거 기반)"],
                horizontal=True
            )
            
            # Code input
            code_input = st.text_area(
                "분석할 코드를 입력하세요",
                height=400,
                placeholder="Python 코드를 입력하세요...",
                key="code_input"
            )
            
            # Analysis button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
            with col_btn1:
                analyze_btn = st.button("🔍 분석 실행", type="primary", use_container_width=True)
            with col_btn2:
                if st.button("🗑️ 초기화", use_container_width=True):
                    st.session_state.code_input = ""
                    st.rerun()
        
        with col2:
            # Analysis options
            st.subheader("분석 옵션")
            
            show_confidence = st.checkbox("신뢰도 표시", value=True)
            show_evidence = st.checkbox("근거 표시", value=True)
            show_alternatives = st.checkbox("대안 제시", value=True)
            
            min_confidence = st.slider(
                "최소 신뢰도",
                0.0, 1.0, 0.7, 0.05,
                help="이 값 이상의 신뢰도를 가진 제안만 표시"
            )
            
            convention = st.selectbox(
                "명명 규칙",
                [NamingConvention.SNAKE_CASE, NamingConvention.CAMEL_CASE],
                format_func=lambda x: x.value
            )
            
            # Quick stats
            if code_input:
                lines = len(code_input.strip().split('\n'))
                chars = len(code_input)
                st.info(f"📝 {lines} 줄, {chars:,} 문자")
        
        # Analysis results
        if analyze_btn and code_input:
            with st.spinner("코드 분석 중..."):
                self._perform_analysis(code_input, analysis_mode, min_confidence, 
                                     show_confidence, show_evidence, show_alternatives)
    
    def _render_random_generator_tab(self):
        """Render random code generator tab"""
        st.header("랜덤 코드 생성기")
        st.markdown("다양한 패턴의 테스트 코드를 자동으로 생성하여 표준화 시스템을 테스트합니다.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Generator controls
            col_gen1, col_gen2, col_gen3 = st.columns(3)
            
            with col_gen1:
                generate_btn = st.button("🎲 랜덤 생성", type="primary", use_container_width=True)
            
            with col_gen2:
                auto_analyze = st.checkbox("자동 분석", value=True)
            
            with col_gen3:
                if st.button("📥 모두 다운로드"):
                    self._download_generated_codes()
        
        with col2:
            # Statistics
            st.metric("생성된 코드", f"{len(st.session_state.generated_codes)}개")
        
        # Generate code
        if generate_btn:
            with st.spinner("코드 생성 중..."):
                try:
                    code, pattern_name, description = self.code_generator.generate_random_code()
                    
                    # Store in session
                    generated_item = {
                        'timestamp': datetime.now().isoformat(),
                        'pattern': pattern_name,
                        'description': description,
                        'code': code,
                        'analyzed': False,
                        'issues': 0
                    }
                    st.session_state.generated_codes.append(generated_item)
                    
                    # Display generated code
                    st.success(f"✅ {pattern_name} 패턴 코드 생성 완료!")
                    
                    with st.expander("📄 생성된 코드", expanded=True):
                        st.code(code, language="python")
                        st.caption(f"설명: {description}")
                    
                    # Auto analyze if enabled
                    if auto_analyze:
                        st.subheader("🔍 자동 분석 결과")
                        results = self.reviewer.review_code(code)
                        
                        if results:
                            # Update analyzed status
                            st.session_state.generated_codes[-1]['analyzed'] = True
                            st.session_state.generated_codes[-1]['issues'] = len(results)
                            
                            # Show results
                            st.warning(f"🚨 {len(results)}개의 개선사항이 발견되었습니다")
                            
                            for result in results:
                                with st.expander(f"💡 {result.original_name} → {result.suggested_name}"):
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"**이유:** {result.reason}")
                                        st.write(f"**근거:** {result.evidence_term}")
                                    with col2:
                                        if show_confidence and hasattr(result, 'confidence'):
                                            st.metric("신뢰도", f"{result.confidence:.0%}")
                        else:
                            st.success("✅ 모든 변수명이 표준을 준수합니다!")
                            st.session_state.generated_codes[-1]['analyzed'] = True
                            
                except Exception as e:
                    st.error(f"코드 생성 중 오류 발생: {str(e)}")
        
        # Show history
        if st.session_state.generated_codes:
            st.divider()
            st.subheader("📜 생성 이력")
            
            try:
                history_df = pd.DataFrame(st.session_state.generated_codes)
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                
                # Display with custom formatting
                st.dataframe(
                    history_df[['timestamp', 'pattern', 'analyzed', 'issues']].tail(10),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn("생성 시간", format="MM/DD HH:mm"),
                        "pattern": "패턴",
                        "analyzed": st.column_config.CheckboxColumn("분석됨"),
                        "issues": st.column_config.NumberColumn("발견된 이슈", format="%d개")
                    }
                )
            except Exception as e:
                st.error(f"이력 표시 중 오류: {str(e)}")
    
    def _render_visualization_tab(self):
        """Render visualization dashboard tab"""
        st.header("📊 시각화 대시보드")
        
        if not st.session_state.analysis_history:
            st.info("아직 분석 데이터가 없습니다. 코드 분석을 먼저 실행해주세요.")
            return
        
        try:
            # Create metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            total_analyses = len(st.session_state.analysis_history)
            total_issues = sum(item.get('issues_found', 0) for item in st.session_state.analysis_history)
            avg_issues = total_issues / total_analyses if total_analyses > 0 else 0
            
            with col1:
                st.metric("총 분석 수", f"{total_analyses:,}회")
            with col2:
                st.metric("총 발견 이슈", f"{total_issues:,}개")
            with col3:
                st.metric("평균 이슈/분석", f"{avg_issues:.1f}개")
            with col4:
                improvement_rate = (total_issues / (total_analyses * 10) * 100) if total_analyses > 0 else 0
                st.metric("개선 필요율", f"{improvement_rate:.1f}%")
            
            # Visualization tabs
            viz_tab1, viz_tab2 = st.tabs(["이슈 유형별 분석", "시간대별 추이"])
            
            with viz_tab1:
                # Issue type analysis
                issue_types = {}
                for item in st.session_state.analysis_history:
                    for issue in item.get('issue_types', []):
                        issue_types[issue] = issue_types.get(issue, 0) + 1
                
                if issue_types:
                    # Create two columns for charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.pie(
                            values=list(issue_types.values()),
                            names=list(issue_types.keys()),
                            title="이슈 유형별 분포"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig2 = px.bar(
                            x=list(issue_types.keys()),
                            y=list(issue_types.values()),
                            title="이슈 유형별 발생 횟수",
                            labels={'x': '이슈 유형', 'y': '발생 횟수'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("아직 이슈 데이터가 없습니다.")
            
            with viz_tab2:
                # Time series analysis
                if len(st.session_state.analysis_history) > 1:
                    df = pd.DataFrame(st.session_state.analysis_history)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp')
                    
                    # Line chart for issues over time
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['issues_found'],
                        mode='lines+markers',
                        name='발견된 이슈',
                        line=dict(color='red', width=2)
                    ))
                    fig.update_layout(
                        title="시간대별 이슈 발견 추이",
                        xaxis_title="시간",
                        yaxis_title="이슈 수"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("시계열 분석을 위해서는 2개 이상의 분석 데이터가 필요합니다.")
                    
        except Exception as e:
            st.error(f"시각화 생성 중 오류 발생: {str(e)}")
    
    def _render_dictionary_tab(self):
        """Render terminology dictionary management tab"""
        st.header("📚 용어사전 관리")
        
        dict_tab1, dict_tab2, dict_tab3 = st.tabs(["사전 조회", "용어 추가", "가져오기/내보내기"])
        
        with dict_tab1:
            # Search and filter
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search_term = st.text_input("🔍 용어 검색", placeholder="검색할 용어를 입력하세요...")
            
            with col2:
                category_filter = st.selectbox(
                    "카테고리",
                    ["전체", "사용자", "시스템", "데이터", "금융", "기타"]
                )
            
            with col3:
                sort_options = {"용어명": "term", "표준 변수명": "standard_name", "설명": "description"}
                sort_display = st.selectbox(
                    "정렬 기준",
                    list(sort_options.keys())
                )
                sort_by = sort_options[sort_display]
            
            # Display dictionary
            try:
                terms_data = []
                displayed_terms = set()
                
                for key, entry in self.reviewer.dictionary.terms.items():
                    if entry.term == key and key not in displayed_terms:
                        if not search_term or search_term.lower() in entry.term.lower():
                            terms_data.append({
                                'term': entry.term,
                                'standard_name': entry.standard_variable_name,
                                'description': entry.description,
                                'related': ', '.join(entry.related_terms) if entry.related_terms else '-'
                            })
                            displayed_terms.add(key)
                
                if terms_data:
                    df = pd.DataFrame(terms_data)
                    
                    # Apply sorting
                    df = df.sort_values(by=sort_by)
                    
                    # Display with pagination
                    items_per_page = 20
                    total_pages = len(df) // items_per_page + (1 if len(df) % items_per_page > 0 else 0)
                    
                    page = st.number_input(
                        f"페이지 (총 {total_pages}페이지)",
                        min_value=1,
                        max_value=max(1, total_pages),
                        value=1
                    )
                    
                    start_idx = (page - 1) * items_per_page
                    end_idx = start_idx + items_per_page
                    
                    st.dataframe(
                        df.iloc[start_idx:end_idx],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.caption(f"총 {len(df):,}개 용어 중 {start_idx + 1}-{min(end_idx, len(df))} 표시")
                else:
                    st.info("검색 결과가 없습니다.")
                    
            except Exception as e:
                st.error(f"용어사전 조회 중 오류 발생: {str(e)}")
        
        with dict_tab2:
            # Add new term
            st.subheader("새 용어 추가")
            
            with st.form("add_term_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_term = st.text_input("용어*", help="표준 용어를 입력하세요")
                    new_standard = st.text_input("표준 변수명*", help="코드에서 사용할 표준 변수명")
                    new_category = st.selectbox("카테고리", ["사용자", "시스템", "데이터", "금융", "기타"])
                
                with col2:
                    new_description = st.text_area("설명*", help="용어에 대한 설명")
                    new_related = st.text_input("관련 용어", help="쉼표로 구분하여 입력")
                
                submitted = st.form_submit_button("➕ 용어 추가", type="primary")
                
                if submitted and new_term and new_standard and new_description:
                    try:
                        related_list = [t.strip() for t in new_related.split(',') if t.strip()]
                        self.reviewer.dictionary.add_term(
                            new_standard,
                            new_standard,
                            f"{new_description} (카테고리: {new_category})",
                            related_list
                        )
                        st.success(f"✅ '{new_term}' 용어가 추가되었습니다!")
                    except Exception as e:
                        st.error(f"용어 추가 중 오류 발생: {str(e)}")
        
        with dict_tab3:
            # Import/Export
            st.subheader("가져오기/내보내기")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("📥 **용어사전 가져오기**")
                uploaded_file = st.file_uploader(
                    "CSV 파일 선택",
                    type=['csv'],
                    help="한글명, 영문명, 약어 순서의 CSV 파일"
                )
                
                if uploaded_file and st.button("⬆️ 가져오기"):
                    try:
                        # Process uploaded file
                        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
                        st.success(f"✅ {len(df)}개 용어를 성공적으로 가져왔습니다!")
                    except Exception as e:
                        st.error(f"파일 가져오기 중 오류 발생: {str(e)}")
            
            with col2:
                st.write("📤 **용어사전 내보내기**")
                
                export_format = st.selectbox(
                    "내보내기 형식",
                    ["CSV", "JSON", "Excel"]
                )
                
                if st.button("⬇️ 내보내기"):
                    self._export_dictionary(export_format)
    
    def _render_reports_tab(self):
        """Render analysis reports tab"""
        st.header("📈 분석 리포트")
        
        if not st.session_state.analysis_history:
            st.info("분석 이력이 없습니다.")
            return
        
        # Report options
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            report_type = st.selectbox(
                "리포트 유형",
                ["요약 리포트", "상세 리포트", "추세 리포트"]
            )
        
        with col2:
            date_range = st.selectbox(
                "기간",
                ["전체", "오늘", "최근 7일", "최근 30일"]
            )
        
        with col3:
            if st.button("📊 리포트 생성", type="primary"):
                self._generate_report(report_type, date_range)
        
        # Display recent analyses
        st.divider()
        st.subheader("최근 분석 내역")
        
        try:
            recent_analyses = st.session_state.analysis_history[-10:]
            for analysis in reversed(recent_analyses):
                with st.expander(
                    f"📅 {analysis['timestamp']} - {analysis.get('issues_found', 0)}개 이슈 발견",
                    expanded=False
                ):
                    st.write(f"**코드 길이:** {analysis.get('code_length', 0)} 문자")
                    st.write(f"**분석 시간:** {analysis.get('analysis_time', 0):.2f}초")
                    st.write(f"**발견된 이슈:**")
                    
                    issues = analysis.get('issues', [])
                    if issues:
                        for issue in issues:
                            st.write(f"- {issue}")
                    else:
                        st.write("- 이슈 없음")
        except Exception as e:
            st.error(f"분석 내역 표시 중 오류 발생: {str(e)}")
    
    def _render_settings_tab(self):
        """Render settings tab"""
        st.header("⚙️ 설정")
        
        settings_tab1, settings_tab2 = st.tabs(["일반 설정", "분석 설정"])
        
        with settings_tab1:
            st.subheader("일반 설정")
            
            # Theme selection
            theme = st.selectbox(
                "테마",
                ["라이트", "다크", "자동"],
                index=0 if st.session_state.theme == 'light' else 1
            )
            
            # Language
            language = st.selectbox(
                "언어",
                ["한국어", "English"],
                index=0
            )
            
            # Notifications
            st.checkbox("분석 완료 알림", value=True)
            st.checkbox("용어사전 업데이트 알림", value=True)
            
            if st.button("💾 설정 저장"):
                st.session_state.theme = 'light' if theme == "라이트" else 'dark'
                st.success("✅ 설정이 저장되었습니다!")
        
        with settings_tab2:
            st.subheader("분석 설정")
            
            # Default settings
            default_convention = st.selectbox(
                "기본 명명 규칙",
                ["snake_case", "camelCase", "PascalCase"],
                index=0
            )
            
            default_confidence = st.slider(
                "기본 최소 신뢰도",
                0.0, 1.0, 0.7, 0.05
            )
            
            # Analysis options
            st.checkbox("자동 대안 제시", value=True)
            st.checkbox("컨텍스트 기반 분석", value=True)
            
            if st.button("🔄 캐시 초기화"):
                st.cache_data.clear()
                st.success("✅ 캐시가 초기화되었습니다!")
    
    def _perform_analysis(self, code, mode, min_confidence, show_confidence, 
                         show_evidence, show_alternatives):
        """Perform code analysis and display results"""
        start_time = datetime.now()
        
        try:
            # Perform analysis based on mode
            if mode == "고급 분석 (근거 기반)":
                results = self.advanced_reviewer.review_with_evidence(code)
            else:
                results = self.reviewer.review_code(code)
            
            # Calculate analysis time
            analysis_time = (datetime.now() - start_time).total_seconds()
            
            # Store in history
            analysis_record = {
                'timestamp': datetime.now().isoformat(),
                'code_length': len(code),
                'issues_found': len(results),
                'analysis_time': analysis_time,
                'mode': mode,
                'issue_types': [r.reason for r in results] if results else [],
                'variables': [r.original_name for r in results] if results else [],
                'issues': [f"{r.original_name} → {r.suggested_name}" for r in results] if results else []
            }
            st.session_state.analysis_history.append(analysis_record)
            
            # Display results
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if results:
                    st.error(f"🚨 {len(results)}개의 개선사항이 발견되었습니다")
                    
                    # Display each result
                    for i, result in enumerate(results):
                        if result.confidence >= min_confidence:
                            with st.expander(
                                f"💡 {result.original_name} → {result.suggested_name}",
                                expanded=i < 3  # Expand first 3
                            ):
                                # Main suggestion
                                st.write(f"**제안:** `{result.original_name}` → `{result.suggested_name}`")
                                st.write(f"**이유:** {result.reason}")
                                
                                if show_evidence:
                                    st.write(f"**근거:** {result.evidence_term}")
                                
                                if show_confidence:
                                    # Confidence meter
                                    confidence_pct = int(result.confidence * 100)
                                    st.progress(confidence_pct, f"신뢰도: {confidence_pct}%")
                                
                                if show_alternatives and hasattr(result, 'alternative_suggestions'):
                                    if result.alternative_suggestions:
                                        st.write("**대안:**")
                                        for alt, conf in result.alternative_suggestions[:3]:
                                            st.write(f"- `{alt}` (신뢰도: {conf:.0%})")
                                
                                # Show fixed code snippet
                                if st.checkbox(f"수정된 코드 보기", key=f"show_fixed_{i}"):
                                    fixed_code = code.replace(result.original_name, result.suggested_name)
                                    st.code(fixed_code, language="python")
                else:
                    st.success("✅ 모든 변수명이 표준을 준수합니다!")
                    
                    # Show clean code metrics
                    lines = len(code.strip().split('\n'))
                    st.info(f"""
                    **코드 품질 지표:**
                    - 총 {lines} 줄
                    - 모든 변수명 표준 준수
                    - 분석 시간: {analysis_time:.2f}초
                    """)
            
            with col2:
                # Analysis metrics
                st.metric("분석 시간", f"{analysis_time:.2f}초")
                st.metric("검토된 변수", f"{len(set(r.original_name for r in results))}개")
                
                if results:
                    avg_confidence = sum(r.confidence for r in results) / len(results)
                    st.metric("평균 신뢰도", f"{avg_confidence:.0%}")
                
                # Quick actions
                st.divider()
                
                if st.button("💾 결과 저장"):
                    self._save_analysis_results(results, code)
                    
        except Exception as e:
            st.error(f"분석 중 오류 발생: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    def _download_generated_codes(self):
        """Download all generated codes"""
        if not st.session_state.generated_codes:
            st.warning("생성된 코드가 없습니다.")
            return
        
        try:
            # Create a text file with all codes
            content = ""
            for item in st.session_state.generated_codes:
                content += f"# {item['pattern']} - {item['timestamp']}\n"
                content += f"# {item['description']}\n\n"
                content += item['code']
                content += "\n\n" + "="*60 + "\n\n"
            
            # Create download button
            st.download_button(
                label="📥 모든 코드 다운로드",
                data=content,
                file_name="generated_codes.py",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"다운로드 생성 중 오류 발생: {str(e)}")
    
    def _export_dictionary(self, format_type):
        """Export terminology dictionary"""
        try:
            terms_data = []
            for key, entry in self.reviewer.dictionary.terms.items():
                if entry.term == key:
                    terms_data.append({
                        'term': entry.term,
                        'standard_name': entry.standard_variable_name,
                        'description': entry.description,
                        'related_terms': ', '.join(entry.related_terms) if entry.related_terms else ''
                    })
            
            df = pd.DataFrame(terms_data)
            
            if format_type == "CSV":
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 CSV 다운로드",
                    data=csv,
                    file_name="terminology_dictionary.csv",
                    mime="text/csv"
                )
            
            elif format_type == "JSON":
                json_str = df.to_json(orient='records', force_ascii=False, indent=2)
                st.download_button(
                    label="📥 JSON 다운로드",
                    data=json_str,
                    file_name="terminology_dictionary.json",
                    mime="application/json"
                )
            
            elif format_type == "Excel":
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    label="📥 Excel 다운로드",
                    data=output.getvalue(),
                    file_name="terminology_dictionary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            st.success(f"✅ {format_type} 형식으로 내보내기 준비 완료!")
            
        except Exception as e:
            st.error(f"내보내기 중 오류 발생: {str(e)}")
    
    def _generate_report(self, report_type, date_range):
        """Generate analysis report"""
        st.info(f"📊 {report_type} 생성 중... ({date_range})")
        
        try:
            # Filter data based on date range
            filtered_history = st.session_state.analysis_history
            
            if date_range != "전체":
                from datetime import timedelta
                now = datetime.now()
                
                if date_range == "오늘":
                    cutoff = now - timedelta(days=1)
                elif date_range == "최근 7일":
                    cutoff = now - timedelta(days=7)
                elif date_range == "최근 30일":
                    cutoff = now - timedelta(days=30)
                
                filtered_history = [
                    h for h in filtered_history 
                    if datetime.fromisoformat(h['timestamp']) > cutoff
                ]
            
            # Generate report content
            total_analyses = len(filtered_history)
            total_issues = sum(item.get('issues_found', 0) for item in filtered_history)
            avg_time = sum(item.get('analysis_time', 0) for item in filtered_history) / total_analyses if total_analyses > 0 else 0
            
            st.success("✅ 리포트가 생성되었습니다!")
            
            # Show report content
            st.markdown(f"""
            ### 📊 {report_type}
            
            **기간:** {date_range}
            
            **주요 지표:**
            - 총 분석: {total_analyses}회
            - 발견된 이슈: {total_issues}개
            - 평균 분석 시간: {avg_time:.2f}초
            - 평균 이슈/분석: {total_issues/total_analyses if total_analyses > 0 else 0:.1f}개
            
            **권장사항:**
            1. 약어 사용을 줄이고 명확한 변수명 사용
            2. 일관된 명명 규칙 준수
            3. 용어사전 기반 표준화 적용
            """)
            
        except Exception as e:
            st.error(f"리포트 생성 중 오류 발생: {str(e)}")
    
    def _save_analysis_results(self, results, code):
        """Save analysis results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_results_{timestamp}.json"
            
            data = {
                'timestamp': timestamp,
                'code': code,
                'results': [
                    {
                        'original': r.original_name,
                        'suggested': r.suggested_name,
                        'reason': r.reason,
                        'confidence': r.confidence
                    }
                    for r in results
                ]
            }
            
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            
            st.download_button(
                label="💾 결과 다운로드",
                data=json_str,
                file_name=filename,
                mime="application/json"
            )
            st.success("✅ 분석 결과가 저장되었습니다!")
            
        except Exception as e:
            st.error(f"결과 저장 중 오류 발생: {str(e)}")


def main():
    try:
        app = ProfessionalInterface()
        app.run()
    except Exception as e:
        st.error(f"애플리케이션 실행 중 오류 발생: {str(e)}")
        st.code(f"Error details:\n{str(e)}")


if __name__ == "__main__":
    main()