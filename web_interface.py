"""
Web Interface for Variable Name Standardizer
Provides a Streamlit-based UI for code review and variable name standardization
"""

import streamlit as st
from variable_name_standardizer import CodeReviewer, TerminologyDictionary, NamingConvention
import json
import os
from typing import Dict, List
import pandas as pd


class WebInterface:
    def __init__(self):
        # Load reviewer with CSV if exists
        csv_path = "용어사전.csv"
        self.reviewer = CodeReviewer(csv_path)
        self._initialize_session_state()
        
        # Load CSV terms count for display
        self.csv_terms_count = len(self.reviewer.dictionary.terms) if os.path.exists(csv_path) else 0
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'custom_terms' not in st.session_state:
            st.session_state.custom_terms = []
        if 'review_history' not in st.session_state:
            st.session_state.review_history = []
    
    def run(self):
        """Run the web interface"""
        st.set_page_config(
            page_title="변수명 표준화 검토 시스템",
            page_icon="🔍",
            layout="wide"
        )
        
        st.title("🔍 변수명 표준화 검토 시스템")
        st.markdown("""
        조직의 표준 용어사전에 기반하여 코드의 변수명을 검토하고 개선 사항을 제안합니다.
        """)
        
        # Sidebar for terminology management
        with st.sidebar:
            st.header("📚 용어사전 관리")
            if self.csv_terms_count > 0:
                st.success(f"✅ 용어사전 로드됨 ({self.csv_terms_count}개 용어)")
            self._manage_terminology()
        
        # Main content area
        tabs = st.tabs(["코드 검토", "용어사전 보기", "검토 이력"])
        
        with tabs[0]:
            self._code_review_tab()
        
        with tabs[1]:
            self._dictionary_view_tab()
        
        with tabs[2]:
            self._history_tab()
    
    def _manage_terminology(self):
        """Manage custom terminology in sidebar"""
        st.subheader("사용자 정의 용어 추가")
        
        with st.form("add_term"):
            col1, col2 = st.columns(2)
            
            with col1:
                term = st.text_input("용어")
                standard_name = st.text_input("표준 변수명")
            
            with col2:
                description = st.text_input("설명")
                related_terms = st.text_input("관련 용어 (쉼표로 구분)")
            
            if st.form_submit_button("용어 추가"):
                if term and standard_name and description:
                    related_list = [t.strip() for t in related_terms.split(',') if t.strip()]
                    self.reviewer.dictionary.add_term(term, standard_name, description, related_list)
                    st.session_state.custom_terms.append({
                        'term': term,
                        'standard_name': standard_name,
                        'description': description,
                        'related_terms': related_list
                    })
                    st.success(f"✅ 용어 '{term}' 추가됨")
                else:
                    st.error("모든 필수 필드를 입력해주세요")
        
        # Display custom terms
        if st.session_state.custom_terms:
            st.subheader("사용자 정의 용어 목록")
            for term in st.session_state.custom_terms:
                st.text(f"• {term['term']} → {term['standard_name']}")
    
    def _code_review_tab(self):
        """Code review main interface"""
        st.header("코드 검토")
        
        # Code input
        code_input = st.text_area(
            "검토할 코드를 입력하세요:",
            height=300,
            placeholder="""def process_사용자_data(usr_id, pwd):
    res = None
    err_msg = ""
    
    try:
        사용자정보 = get_user_info(usr_id)
        if 사용자정보:
            res = validate_pwd(pwd, 사용자정보)
    except Exception as e:
        err_msg = str(e)
    
    return res, err_msg"""
        )
        
        # Review options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_confidence = st.checkbox("신뢰도 표시", value=True)
        
        with col2:
            min_confidence = st.slider("최소 신뢰도", 0.0, 1.0, 0.8, 0.05)
        
        with col3:
            convention = st.selectbox(
                "명명 규칙",
                options=[NamingConvention.SNAKE_CASE, NamingConvention.CAMEL_CASE],
                format_func=lambda x: x.value
            )
        
        # Review button
        if st.button("🔍 코드 검토", type="primary"):
            if code_input:
                with st.spinner("코드 분석 중..."):
                    results = self.reviewer.review_code(code_input)
                    
                    # Filter by confidence
                    filtered_results = [r for r in results if r.confidence >= min_confidence]
                    
                    # Save to history
                    st.session_state.review_history.append({
                        'code': code_input[:100] + '...' if len(code_input) > 100 else code_input,
                        'results_count': len(filtered_results),
                        'timestamp': pd.Timestamp.now()
                    })
                    
                    # Display results
                    if filtered_results:
                        st.subheader(f"📋 검토 결과 ({len(filtered_results)}개 발견)")
                        
                        for result in filtered_results:
                            with st.expander(f"{result.original_name} → {result.suggested_name}"):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**이유:** {result.reason}")
                                    st.write(f"**근거:** {result.evidence_term}")
                                
                                with col2:
                                    if show_confidence:
                                        st.metric("신뢰도", f"{result.confidence:.0%}")
                                
                                # Code preview with changes
                                st.code(
                                    code_input.replace(result.original_name, 
                                                     f"**{result.suggested_name}**"),
                                    language="python"
                                )
                    else:
                        st.success("✅ 모든 변수명이 표준을 준수합니다!")
                    
                    # Export results
                    if filtered_results:
                        st.download_button(
                            label="📥 결과 다운로드 (JSON)",
                            data=json.dumps([{
                                'original': r.original_name,
                                'suggested': r.suggested_name,
                                'reason': r.reason,
                                'evidence': r.evidence_term,
                                'confidence': r.confidence
                            } for r in filtered_results], ensure_ascii=False, indent=2),
                            file_name="variable_review_results.json",
                            mime="application/json"
                        )
            else:
                st.warning("검토할 코드를 입력해주세요")
    
    def _dictionary_view_tab(self):
        """Display terminology dictionary"""
        st.header("📚 표준 용어사전")
        
        # Search functionality
        search_term = st.text_input("🔍 용어 검색", placeholder="검색할 용어를 입력하세요")
        
        # Get all terms
        terms_data = []
        displayed_terms = set()  # Track displayed terms to avoid duplicates
        
        for key, entry in self.reviewer.dictionary.terms.items():
            if entry.term not in displayed_terms:
                if not search_term or search_term.lower() in entry.term.lower():
                    terms_data.append({
                        '용어': entry.term,
                        '표준 변수명': entry.standard_variable_name,
                        '설명': entry.description,
                        '관련 용어': ', '.join(entry.related_terms) if entry.related_terms else '-'
                    })
                    displayed_terms.add(entry.term)
        
        # Display as dataframe
        if terms_data:
            df = pd.DataFrame(terms_data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "용어": st.column_config.TextColumn("용어", width="small"),
                    "표준 변수명": st.column_config.TextColumn("표준 변수명", width="small"),
                    "설명": st.column_config.TextColumn("설명", width="medium"),
                    "관련 용어": st.column_config.TextColumn("관련 용어", width="medium"),
                }
            )
            
            # Export dictionary
            st.download_button(
                label="📥 용어사전 다운로드 (CSV)",
                data=df.to_csv(index=False, encoding='utf-8-sig'),
                file_name="terminology_dictionary.csv",
                mime="text/csv"
            )
        else:
            st.info("검색 결과가 없습니다")
    
    def _history_tab(self):
        """Display review history"""
        st.header("📋 검토 이력")
        
        if st.session_state.review_history:
            history_df = pd.DataFrame(st.session_state.review_history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "code": st.column_config.TextColumn("검토 코드", width="large"),
                    "results_count": st.column_config.NumberColumn("발견된 이슈", width="small"),
                    "timestamp": st.column_config.DatetimeColumn("검토 시간", width="medium"),
                }
            )
            
            if st.button("🗑️ 이력 초기화"):
                st.session_state.review_history = []
                st.rerun()
        else:
            st.info("아직 검토 이력이 없습니다")


if __name__ == "__main__":
    app = WebInterface()
    app.run()