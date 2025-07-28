"""
Terminology Management UI Component
Provides interface for adding, editing, and deleting terms
"""

import streamlit as st
import pandas as pd
from typing import Optional
from terminology_manager import TerminologyManager, Term

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class TerminologyUI:
    """UI component for terminology management"""
    
    def __init__(self, manager: TerminologyManager):
        self.manager = manager
    
    def render(self):
        """Render the terminology management interface"""
        st.header("📚 표준 용어사전 관리")
        
        # Statistics
        stats = self.manager.get_statistics()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("전체 용어", f"{stats['total_terms']:,}개")
        
        with col2:
            st.metric("CSV 용어", f"{stats['csv_terms']:,}개")
        
        with col3:
            st.metric("사용자 정의", f"{stats['custom_terms']:,}개")
        
        with col4:
            st.metric("검색 가능", f"{stats['total_lookups']:,}개")
        
        st.divider()
        
        # Tabs for different functions
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 검색", "➕ 추가", "📋 전체 목록", "📊 통계"])
        
        with tab1:
            self._render_search()
        
        with tab2:
            self._render_add_term()
        
        with tab3:
            self._render_all_terms()
        
        with tab4:
            self._render_statistics()
    
    def _render_search(self):
        """Render search interface"""
        st.subheader("용어 검색")
        
        search_query = st.text_input("검색어 입력", placeholder="한글명, 영문명, 약어로 검색...")
        
        if search_query:
            results = self.manager.search_terms(search_query)
            
            if results:
                st.success(f"{len(results)}개의 용어를 찾았습니다.")
                
                for term in results:
                    with st.expander(f"**{term.standard_variable}** - {term.description}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**한글명:**", term.korean_name or "-")
                            st.write("**영문명:**", term.english_name)
                            st.write("**약어:**", term.abbreviation or "-")
                            st.write("**표준 변수명:**", term.standard_variable)
                        
                        with col2:
                            st.write("**설명:**", term.description)
                            st.write("**관련 용어:**", ", ".join(term.related_terms) if term.related_terms else "-")
                            st.write("**출처:**", "CSV" if term.source == 'csv' else "사용자 정의")
                            st.write("**추가일:**", term.added_date[:10])
                        
                        # Edit/Delete buttons for custom terms
                        if term.source == 'manual':
                            col1, col2, col3 = st.columns([1, 1, 3])
                            
                            with col1:
                                if st.button("✏️ 수정", key=f"edit_{term.standard_variable}"):
                                    st.session_state.editing_term = term.standard_variable
                            
                            with col2:
                                if st.button("🗑️ 삭제", key=f"delete_{term.standard_variable}"):
                                    if self.manager.delete_term(term.standard_variable):
                                        st.success("용어가 삭제되었습니다.")
                                        st.rerun()
                                    else:
                                        st.error("삭제 실패")
                        
                        # Edit form if editing
                        if hasattr(st.session_state, 'editing_term') and st.session_state.editing_term == term.standard_variable:
                            self._render_edit_form(term)
            else:
                st.info("검색 결과가 없습니다.")
    
    def _render_add_term(self):
        """Render add term interface"""
        st.subheader("새 용어 추가")
        
        with st.form("add_term_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                korean_name = st.text_input("한글명", placeholder="예: 사용자")
                english_name = st.text_input("영문명 *", placeholder="예: user")
                abbreviation = st.text_input("약어", placeholder="예: usr")
            
            with col2:
                description = st.text_area("설명", placeholder="용어에 대한 설명...")
                related_terms = st.text_input("관련 용어", placeholder="쉼표로 구분 (예: usr, usuario)")
            
            submitted = st.form_submit_button("➕ 용어 추가", type="primary")
            
            if submitted:
                if not english_name:
                    st.error("영문명은 필수입니다.")
                else:
                    # Parse related terms
                    related_list = [t.strip() for t in related_terms.split(',') if t.strip()] if related_terms else []
                    
                    if self.manager.add_term(
                        korean_name=korean_name,
                        english_name=english_name,
                        abbreviation=abbreviation,
                        description=description,
                        related_terms=related_list
                    ):
                        st.success("용어가 추가되었습니다!")
                        st.balloons()
                        # Clear form
                        st.rerun()
                    else:
                        st.error("용어 추가 실패. 영문명을 확인해주세요.")
    
    def _render_edit_form(self, term: Term):
        """Render edit form for a term"""
        st.divider()
        st.subheader("용어 수정")
        
        with st.form(f"edit_form_{term.standard_variable}"):
            col1, col2 = st.columns(2)
            
            with col1:
                korean_name = st.text_input("한글명", value=term.korean_name)
                english_name = st.text_input("영문명 *", value=term.english_name)
                abbreviation = st.text_input("약어", value=term.abbreviation)
            
            with col2:
                description = st.text_area("설명", value=term.description)
                related_terms = st.text_input("관련 용어", value=", ".join(term.related_terms))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 저장", type="primary"):
                    # Parse related terms
                    related_list = [t.strip() for t in related_terms.split(',') if t.strip()] if related_terms else []
                    
                    if self.manager.update_term(
                        term.standard_variable,
                        korean_name=korean_name,
                        english_name=english_name,
                        abbreviation=abbreviation,
                        description=description,
                        related_terms=related_list
                    ):
                        st.success("용어가 수정되었습니다!")
                        del st.session_state.editing_term
                        st.rerun()
                    else:
                        st.error("수정 실패")
            
            with col2:
                if st.form_submit_button("❌ 취소"):
                    del st.session_state.editing_term
                    st.rerun()
    
    def _render_all_terms(self):
        """Render all terms in a table"""
        st.subheader("전체 용어 목록")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            source_filter = st.selectbox("출처", ["전체", "CSV", "사용자 정의"])
        
        with col2:
            sort_by = st.selectbox("정렬", ["표준 변수명", "한글명", "영문명", "추가일"])
        
        with col3:
            items_per_page = st.selectbox("페이지당 항목", [20, 50, 100, 200])
        
        # Get all terms
        all_terms = self.manager.get_all_terms()
        
        # Apply filter
        if source_filter == "CSV":
            filtered_terms = [t for t in all_terms if t.source == 'csv']
        elif source_filter == "사용자 정의":
            filtered_terms = [t for t in all_terms if t.source == 'manual']
        else:
            filtered_terms = all_terms
        
        # Sort
        sort_map = {
            "표준 변수명": lambda t: t.standard_variable,
            "한글명": lambda t: t.korean_name or "",
            "영문명": lambda t: t.english_name,
            "추가일": lambda t: t.added_date
        }
        filtered_terms.sort(key=sort_map[sort_by])
        
        # Pagination
        total_pages = max(1, (len(filtered_terms) - 1) // items_per_page + 1) if filtered_terms else 1
        if 'term_list_page' not in st.session_state:
            st.session_state.term_list_page = 1
        
        # Ensure page number is valid
        if st.session_state.term_list_page > total_pages:
            st.session_state.term_list_page = total_pages
        if st.session_state.term_list_page < 1:
            st.session_state.term_list_page = 1
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("◀ 이전") and st.session_state.term_list_page > 1:
                st.session_state.term_list_page -= 1
        
        with col2:
            st.write(f"페이지 {st.session_state.term_list_page} / {total_pages}")
        
        with col3:
            if st.button("다음 ▶") and st.session_state.term_list_page < total_pages:
                st.session_state.term_list_page += 1
        
        # Display terms
        start_idx = (st.session_state.term_list_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_terms = filtered_terms[start_idx:end_idx]
        
        # Create DataFrame
        df_data = []
        for term in page_terms:
            df_data.append({
                '표준 변수명': term.standard_variable,
                '한글명': term.korean_name or "-",
                '영문명': term.english_name,
                '약어': term.abbreviation or "-",
                '설명': term.description[:50] + "..." if len(term.description) > 50 else term.description,
                '출처': "CSV" if term.source == 'csv' else "사용자",
                '추가일': term.added_date[:10]
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("표시할 용어가 없습니다.")
        
        # Export options
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 CSV로 내보내기"):
                # Export all terms to CSV
                export_data = []
                for term in all_terms:
                    export_data.append({
                        '한글명': term.korean_name,
                        '영문명': term.english_name,
                        '약어': term.abbreviation,
                        '표준변수명': term.standard_variable,
                        '설명': term.description,
                        '관련용어': ", ".join(term.related_terms),
                        '출처': term.source,
                        '추가일': term.added_date,
                        '수정일': term.modified_date
                    })
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="💾 다운로드",
                    data=csv,
                    file_name="terminology_export.csv",
                    mime="text/csv"
                )
    
    def _render_statistics(self):
        """Render statistics about terminology"""
        st.subheader("용어사전 통계")
        
        stats = self.manager.get_statistics()
        all_terms = self.manager.get_all_terms()
        
        # Basic stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("전체 고유 용어", f"{stats['total_terms']:,}개")
            st.metric("CSV 출처", f"{stats['csv_terms']:,}개")
            st.metric("사용자 정의", f"{stats['custom_terms']:,}개")
        
        with col2:
            st.metric("총 검색 가능 항목", f"{stats['total_lookups']:,}개")
            st.metric("한글명 보유", f"{stats['korean_terms']:,}개")
            st.metric("약어 보유", f"{stats['abbreviations']:,}개")
        
        # Length distribution
        st.divider()
        st.subheader("변수명 길이 분포")
        
        lengths = [len(t.standard_variable) for t in all_terms]
        if lengths and PLOTLY_AVAILABLE:
            fig = px.histogram(
                x=lengths,
                nbins=20,
                title="표준 변수명 길이 분포",
                labels={'x': '길이 (문자)', 'y': '개수'}
            )
            st.plotly_chart(fig, use_container_width=True)
        elif lengths:
            st.info("Plotly가 설치되지 않아 차트를 표시할 수 없습니다.")
        
        # Most common prefixes
        st.subheader("자주 사용되는 접두사")
        
        prefixes = {}
        for term in all_terms:
            if '_' in term.standard_variable:
                prefix = term.standard_variable.split('_')[0]
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
        
        if prefixes:
            sorted_prefixes = sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:10]
            
            df = pd.DataFrame(sorted_prefixes, columns=['접두사', '사용 횟수'])
            st.bar_chart(df.set_index('접두사'))