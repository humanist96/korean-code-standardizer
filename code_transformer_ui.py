"""
Enhanced Code Transformer UI with Before/After Comparison
Focus on terminology dictionary-based code transformation
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import difflib
import json
import re
from typing import List, Dict, Tuple
import os

from variable_name_standardizer import CodeReviewer, NamingConvention
from advanced_analyzer import AdvancedCodeReviewer
from statistics_manager import StatisticsManager, TransformationRecord
from visualization_dashboard import VisualizationDashboard
from terminology_manager import TerminologyManager
from terminology_ui import TerminologyUI
from enhanced_code_reviewer import EnhancedCodeReviewer


# Page configuration
st.set_page_config(
    page_title="코드 변수명 표준화 변환기",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --primary-hover: #4f46e5;
        --primary-light: #e0e7ff;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --info-color: #3b82f6;
        --dark-bg: #1e293b;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --border-color: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main {
        padding: 0;
        background-color: var(--light-bg);
        min-height: 100vh;
    }
    
    /* Header styles */
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 0 0 1.5rem 1.5rem;
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 40%;
        height: 200%;
        background: rgba(255, 255, 255, 0.1);
        transform: rotate(45deg);
        pointer-events: none;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }
    
    /* Home button */
    .home-button {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        font-weight: 500;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s ease;
        backdrop-filter: blur(10px);
    }
    
    .home-button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* Metric cards */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-light);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0.5rem 0;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-unit {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* Modern buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Primary button style */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--success-color), #059669);
        font-size: 1.1rem;
        padding: 1rem 2rem;
    }
    
    /* Secondary button style */
    .stButton > button[kind="secondary"] {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--primary-color);
        background: var(--primary-light);
    }
    
    /* Input fields */
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border: 2px solid var(--border-color);
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        background: var(--card-bg);
    }
    
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px var(--primary-light);
        outline: none;
    }
    
    /* Code comparison styles */
    .code-container {
        display: flex;
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .code-panel {
        flex: 1;
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .code-panel:hover {
        border-color: var(--primary-light);
        box-shadow: var(--shadow-lg);
    }
    
    .code-header {
        font-weight: 600;
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, var(--primary-light), rgba(99, 102, 241, 0.1));
        border-radius: 0.5rem;
        color: var(--primary-color);
    }
    
    /* Diff highlighting with modern colors */
    .diff-added {
        background-color: rgba(16, 185, 129, 0.1);
        color: #059669;
        padding: 0.25rem 0.5rem;
        border-left: 3px solid var(--success-color);
        margin: 0.25rem 0;
    }
    
    .diff-removed {
        background-color: rgba(239, 68, 68, 0.1);
        color: #dc2626;
        text-decoration: line-through;
        padding: 0.25rem 0.5rem;
        border-left: 3px solid var(--danger-color);
        margin: 0.25rem 0;
    }
    
    .diff-unchanged {
        color: var(--text-secondary);
        padding: 0.25rem 0.5rem;
    }
    
    /* Issue cards with modern design */
    .issue-card {
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .issue-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .issue-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateX(4px);
        border-color: var(--primary-light);
    }
    
    .issue-card:hover::before {
        transform: scaleY(1);
    }
    
    .issue-change {
        font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
        font-size: 1rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, var(--light-bg), #f1f5f9);
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        margin: 0.5rem 0;
    }
    
    /* Progress indicators */
    .progress-container {
        background: var(--border-color);
        border-radius: 1rem;
        padding: 3px;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        height: 24px;
        border-radius: 0.75rem;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Metric display improvements */
    .stMetric {
        background: var(--card-bg);
        padding: 1.25rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        transition: all 0.2s ease;
    }
    
    .stMetric:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card-bg);
        border-radius: 0.75rem;
        padding: 0.25rem;
        border: 1px solid var(--border-color);
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .stCheckbox > label:hover {
        background: var(--primary-light);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 0.75rem;
        padding: 1rem 1.25rem;
        font-weight: 500;
        border: none;
        box-shadow: var(--shadow-sm);
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    }
    
    /* Animation for fade-in */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main > * {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.5rem;
        }
        
        .code-container {
            flex-direction: column;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .home-button {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
        }
    }
</style>
""", unsafe_allow_html=True)


class CodeTransformerUI:
    def __init__(self):
        self.csv_path = "용어사전.csv"
        
        # Initialize terminology manager
        self.term_manager = TerminologyManager(self.csv_path)
        self.term_ui = TerminologyUI(self.term_manager)
        
        # Initialize reviewers
        try:
            # Use enhanced reviewer with terminology manager
            self.reviewer = EnhancedCodeReviewer(self.term_manager)
            self.advanced_reviewer = AdvancedCodeReviewer(self.csv_path)
            # Get actual count from terminology manager
            self.terms_loaded = len(self.term_manager.get_all_terms())
        except Exception as e:
            st.error(f"용어사전 로드 오류: {str(e)}")
            self.reviewer = CodeReviewer()
            self.advanced_reviewer = AdvancedCodeReviewer()
            self.terms_loaded = 0
        
        # Initialize statistics manager
        self.stats_manager = StatisticsManager()
        self.viz_dashboard = VisualizationDashboard(self.stats_manager)
        
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'original_code' not in st.session_state:
            st.session_state.original_code = ""
        if 'transformed_code' not in st.session_state:
            st.session_state.transformed_code = ""
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = []
        if 'transformation_history' not in st.session_state:
            st.session_state.transformation_history = []
        if 'selected_changes' not in st.session_state:
            st.session_state.selected_changes = {}
    
    def run(self):
        """Main application entry point"""
        # Professional header with gradient background
        st.markdown("""
        <div class="header-container">
            <div class="header-content">
                <div>
                    <h1 class="header-title">코드 변수명 표준화 변환기</h1>
                    <p class="header-subtitle">용어사전 기반 자동 변환 시스템 · """ + f"{self.terms_loaded:,}" + """개 표준 용어</p>
                </div>
                <a href="/" class="home-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                    Home
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats cards with modern design
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            self._render_modern_metric_card("📚", "용어사전", f"{self.terms_loaded:,}", "개 용어")
        
        with col2:
            summary = self.stats_manager.get_summary_stats()
            self._render_modern_metric_card("✅", "총 변환", f"{summary['total_transformations']:,}", "건")
        
        with col3:
            # Calculate success rate
            success_rate = summary.get('success_rate', 0)
            self._render_modern_metric_card("📈", "성공률", f"{success_rate:.1f}", "%")
        
        with col4:
            # Calculate average confidence
            avg_confidence = summary.get('average_confidence', 0) * 100
            self._render_modern_metric_card("🎯", "평균 신뢰도", f"{avg_confidence:.0f}", "%")
        
        # Main interface with spacing
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Quick action buttons with professional design
        st.markdown("### 🚀 빠른 실행")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📋 예제 코드", use_container_width=True, help="미리 준비된 예제 코드를 로드합니다"):
                self._load_example_code()
        
        with col2:
            if st.button("🎲 랜덤 생성", use_container_width=True, help="다양한 패턴의 코드를 랜덤으로 생성합니다"):
                self._generate_random_code()
        
        with col3:
            if st.button("📁 파일 업로드", use_container_width=True, help="Python 파일을 업로드하여 변환합니다"):
                st.session_state.show_upload = True
        
        with col4:
            if st.button("📚 용어사전", use_container_width=True, help="표준 용어사전을 확인하고 관리합니다"):
                st.session_state.show_dictionary = True
        
        with col5:
            if st.button("📊 고급통계", use_container_width=True, help="상세한 통계 및 분석을 확인합니다"):
                st.session_state.show_advanced_stats = True
        
        # Main content area
        if hasattr(st.session_state, 'show_upload') and st.session_state.show_upload:
            self._render_file_upload()
        elif hasattr(st.session_state, 'show_dictionary') and st.session_state.show_dictionary:
            self._render_dictionary_view()
        elif hasattr(st.session_state, 'show_stats') and st.session_state.show_stats:
            self._render_statistics()
        elif hasattr(st.session_state, 'show_advanced_stats') and st.session_state.show_advanced_stats:
            self._render_advanced_statistics()
        else:
            self._render_main_transformer()
    
    def _render_main_transformer(self):
        """Render the main code transformation interface"""
        # Professional container with card design
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Main content in a card-like container
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 📝 코드 입력")
            code_input = st.text_area(
                "변환할 코드를 입력하세요",
                height=400,
                placeholder="Python 코드를 여기에 입력하거나 붙여넣으세요...\n\n예시:\ndef process_usr_data(usr_id, pwd):\n    사용자정보 = get_user_info(usr_id)\n    ...",
                value=st.session_state.original_code,
                key="code_input_area",
                label_visibility="collapsed"
            )
        
        with col2:
            # Options in a styled container
            st.markdown("### ⚙️ 변환 옵션")
            
            # Professional select box with icons
            naming_convention = st.selectbox(
                "명명 규칙",
                ["snake_case", "camelCase", "PascalCase"],
                index=0,
                help="변환할 변수명의 명명 규칙을 선택하세요"
            )
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # Styled checkboxes
            apply_all = st.checkbox("✅ 모든 제안 자동 적용", value=True, help="발견된 모든 변환 제안을 자동으로 적용합니다")
            show_confidence = st.checkbox("📊 신뢰도 표시", value=True, help="각 변환 제안의 신뢰도를 표시합니다")
            highlight_changes = st.checkbox("🔍 변경사항 강조", value=True, help="변경된 부분을 시각적으로 강조합니다")
            
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            
            # Transform button with enhanced style
            if st.button("🚀 변환 실행", type="primary", use_container_width=True):
                if code_input:
                    self._perform_transformation(code_input, naming_convention, apply_all)
                else:
                    st.warning("⚠️ 변환할 코드를 입력해주세요.")
        
        # Results section
        if st.session_state.analysis_results:
            st.divider()
            self._render_transformation_results(highlight_changes, show_confidence)
        
        # Code comparison section
        if st.session_state.transformed_code:
            st.divider()
            self._render_code_comparison()
    
    def _perform_transformation(self, code: str, convention: str, apply_all: bool):
        """Perform code transformation"""
        start_time = datetime.now()
        
        with st.spinner("코드 분석 및 변환 중..."):
            # Store original code
            st.session_state.original_code = code
            
            # Analyze code with convention
            convention_map = {
                "snake_case": NamingConvention.SNAKE_CASE,
                "camelCase": NamingConvention.CAMEL_CASE,
                "PascalCase": NamingConvention.PASCAL_CASE
            }
            naming_conv = convention_map.get(convention, NamingConvention.SNAKE_CASE)
            results = self.reviewer.review_code(code, naming_conv)
            st.session_state.analysis_results = results
            
            # Create transformed code
            if apply_all and results:
                transformed = self._apply_all_transformations(code, results)
                st.session_state.transformed_code = transformed
            else:
                st.session_state.transformed_code = code
                st.session_state.selected_changes = {i: True for i in range(len(results))}
            
            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()
            
            # Record statistics
            if results:
                # Group changes by type
                changes_by_type = {}
                for result in results:
                    reason = result.reason
                    changes_by_type[reason] = changes_by_type.get(reason, 0) + 1
                
                # Create transformation record
                record = TransformationRecord(
                    timestamp=datetime.now().isoformat(),
                    code_length=len(code),
                    lines_of_code=len(code.strip().split('\n')),
                    total_changes=len(results),
                    changes_by_type=changes_by_type,
                    variables_transformed=[
                        {'original': r.original_name, 'suggested': r.suggested_name}
                        for r in results
                    ],
                    confidence_scores=[r.confidence for r in results if hasattr(r, 'confidence')],
                    naming_convention=convention,
                    duration_seconds=duration,
                    applied_changes=len(results) if apply_all else 0
                )
                
                # Save to statistics
                self.stats_manager.record_transformation(record)
            
            # Add to history
            history_item = {
                'timestamp': datetime.now().isoformat(),
                'original_lines': len(code.strip().split('\n')),
                'changes': len(results),
                'convention': convention
            }
            st.session_state.transformation_history.append(history_item)
            
            # Show success message
            if results:
                st.success(f"✅ {len(results)}개의 변환 가능한 항목을 발견했습니다!")
            else:
                st.info("모든 변수명이 이미 표준을 준수하고 있습니다.")
    
    def _apply_all_transformations(self, code: str, results: List) -> str:
        """Apply all transformations to code"""
        transformed = code
        
        # Sort results by position in reverse order to avoid position shifts
        sorted_results = sorted(results, key=lambda r: code.rfind(r.original_name), reverse=True)
        
        for result in sorted_results:
            transformed = transformed.replace(result.original_name, result.suggested_name)
        
        return transformed
    
    def _render_transformation_results(self, highlight: bool, show_confidence: bool):
        """Render transformation results with interactive selection"""
        st.markdown("### 🔍 발견된 변환 항목")
        
        # Summary stats with modern cards
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.5])
        
        total_changes = len(st.session_state.analysis_results)
        selected_changes = sum(1 for v in st.session_state.selected_changes.values() if v)
        
        with col1:
            st.metric("총 변경사항", f"{total_changes}", "개")
        
        with col2:
            st.metric("선택된 항목", f"{selected_changes}", "개")
        
        with col3:
            # Selection percentage
            selection_pct = (selected_changes / total_changes * 100) if total_changes > 0 else 0
            st.metric("선택률", f"{selection_pct:.0f}", "%")
        
        with col4:
            if st.button("✅ 선택 항목 적용", use_container_width=True, type="primary"):
                self._apply_selected_transformations()
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Individual results with enhanced cards
        for i, result in enumerate(st.session_state.analysis_results):
            # Create a professional issue card
            st.markdown(f"""
            <div class="issue-card">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <div style="flex: 0 0 auto;">
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([0.1, 11])
            
            with col1:
                # Checkbox for selection
                selected = st.checkbox(
                    "",
                    value=st.session_state.selected_changes.get(i, True),
                    key=f"select_{i}",
                    label_visibility="collapsed"
                )
                st.session_state.selected_changes[i] = selected
            
            with col2:
                subcol1, subcol2, subcol3 = st.columns([3, 2, 1])
                
                with subcol1:
                    # Change display with better formatting
                    st.markdown(
                        f"""<div class='issue-change'>
                        <span style='color: var(--danger-color); font-weight: 600;'>{result.original_name}</span>
                        <span style='color: var(--text-secondary); margin: 0 0.5rem;'>→</span>
                        <span style='color: var(--success-color); font-weight: 600;'>{result.suggested_name}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
                
                with subcol2:
                    # Reason and evidence with better styling
                    st.markdown(f"**📌 이유:** {result.reason}")
                    st.caption(f"💡 근거: {result.evidence_term}")
                
                with subcol3:
                    # Confidence with visual indicator
                    if show_confidence and hasattr(result, 'confidence'):
                        confidence_pct = result.confidence * 100
                        if confidence_pct >= 80:
                            confidence_color = "var(--success-color)"
                            confidence_icon = "🟢"
                        elif confidence_pct >= 60:
                            confidence_color = "var(--warning-color)"
                            confidence_icon = "🟡"
                        else:
                            confidence_color = "var(--danger-color)"
                            confidence_icon = "🔴"
                        
                        st.markdown(
                            f"""<div style='text-align: center;'>
                            <div style='font-size: 1.5rem;'>{confidence_icon}</div>
                            <div style='color: {confidence_color}; font-size: 1.1rem; font-weight: 600;'>{confidence_pct:.0f}%</div>
                            <div style='font-size: 0.75rem; color: var(--text-secondary);'>신뢰도</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    def _apply_selected_transformations(self):
        """Apply only selected transformations"""
        code = st.session_state.original_code
        
        # Get selected results
        selected_results = [
            result for i, result in enumerate(st.session_state.analysis_results)
            if st.session_state.selected_changes.get(i, False)
        ]
        
        # Apply transformations
        transformed = self._apply_all_transformations(code, selected_results)
        st.session_state.transformed_code = transformed
        
        st.success(f"✅ {len(selected_results)}개의 변환을 적용했습니다!")
        st.rerun()
    
    def _render_code_comparison(self):
        """Render side-by-side code comparison"""
        st.markdown("### 📊 코드 비교")
        
        # Professional action bar
        col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1])
        
        with col1:
            download_btn = st.download_button(
                label="💾 코드 다운로드",
                data=st.session_state.transformed_code,
                file_name=f"transformed_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                mime="text/plain",
                use_container_width=True,
                help="변환된 코드를 파일로 다운로드합니다"
            )
        
        with col2:
            if st.button("📋 클립보드 복사", use_container_width=True, help="변환된 코드를 클립보드에 복사합니다"):
                # Add JavaScript for clipboard copy
                st.markdown(f"""
                <script>
                navigator.clipboard.writeText(`{st.session_state.transformed_code}`);
                </script>
                """, unsafe_allow_html=True)
                st.success("✅ 클립보드에 복사되었습니다!")
        
        with col3:
            if st.button("↩️ 원본 복원", use_container_width=True, help="변환 전 원본 코드로 되돌립니다"):
                st.session_state.transformed_code = st.session_state.original_code
                st.rerun()
        
        with col4:
            view_mode = st.selectbox(
                "보기 모드",
                ["🔄 나란히", "🔍 차이점만", "📝 통합"],
                index=0,
                label_visibility="collapsed"
            )
        
        # Spacing
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Code display with enhanced styling
        if view_mode == "🔄 나란히":
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="code-panel">
                    <div class="code-header">
                        <span style="font-size: 1.1rem;">⭕ 변환 전</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.code(st.session_state.original_code, language="python", line_numbers=True)
            
            with col2:
                st.markdown("""
                <div class="code-panel">
                    <div class="code-header">
                        <span style="font-size: 1.1rem;">✅ 변환 후</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.code(st.session_state.transformed_code, language="python", line_numbers=True)
        
        elif view_mode == "🔍 차이점만":
            st.markdown("""
            <div class="code-panel">
                <div class="code-header">
                    <span style="font-size: 1.1rem;">🔍 변경사항 비교</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            diff_html = self._generate_diff_view(
                st.session_state.original_code,
                st.session_state.transformed_code
            )
            st.markdown(diff_html, unsafe_allow_html=True)
        
        else:  # 통합 보기
            st.markdown("""
            <div class="code-panel">
                <div class="code-header">
                    <span style="font-size: 1.1rem;">📝 통합 비교 보기</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            unified_diff = self._generate_unified_diff(
                st.session_state.original_code,
                st.session_state.transformed_code
            )
            st.code(unified_diff, language="diff", line_numbers=True)
        
        # Statistics
        self._render_transformation_stats()
    
    def _generate_diff_view(self, original: str, transformed: str) -> str:
        """Generate HTML diff view with enhanced styling"""
        differ = difflib.unified_diff(
            original.splitlines(keepends=True),
            transformed.splitlines(keepends=True),
            fromfile='변환 전',
            tofile='변환 후',
            lineterm=''
        )
        
        html_parts = ['''
        <div style="font-family: 'JetBrains Mono', 'Consolas', monospace; 
                    background: var(--card-bg); 
                    padding: 1.5rem; 
                    border-radius: 0.75rem; 
                    border: 1px solid var(--border-color);
                    box-shadow: var(--shadow-sm);">
        ''']
        
        line_num = 0
        for line in differ:
            line_num += 1
            if line.startswith('+') and not line.startswith('+++'):
                html_parts.append(f'''
                <div class="diff-added" style="display: flex; align-items: center;">
                    <span style="color: var(--success-color); font-weight: 600; margin-right: 1rem;">+</span>
                    <span>{line[1:]}</span>
                </div>
                ''')
            elif line.startswith('-') and not line.startswith('---'):
                html_parts.append(f'''
                <div class="diff-removed" style="display: flex; align-items: center;">
                    <span style="color: var(--danger-color); font-weight: 600; margin-right: 1rem;">-</span>
                    <span>{line[1:]}</span>
                </div>
                ''')
            elif line.startswith('@'):
                html_parts.append(f'''
                <div style="color: var(--info-color); 
                           font-weight: 600; 
                           margin: 1rem 0; 
                           padding: 0.5rem 0;
                           border-bottom: 1px solid var(--border-color);">
                    {line}
                </div>
                ''')
            else:
                html_parts.append(f'<div class="diff-unchanged">{line}</div>')
        
        html_parts.append('</div>')
        return ''.join(html_parts)
    
    def _generate_unified_diff(self, original: str, transformed: str) -> str:
        """Generate unified diff"""
        return '\n'.join(difflib.unified_diff(
            original.splitlines(keepends=False),
            transformed.splitlines(keepends=False),
            fromfile='변환 전',
            tofile='변환 후',
            lineterm=''
        ))
    
    def _render_transformation_stats(self):
        """Render transformation statistics with professional design"""
        if not st.session_state.analysis_results:
            return
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("### 📈 변환 통계")
        
        # Calculate stats
        total_changes = len(st.session_state.analysis_results)
        lines_original = len(st.session_state.original_code.strip().split('\n'))
        
        # Group by change type
        change_types = {}
        for result in st.session_state.analysis_results:
            change_types[result.reason] = change_types.get(result.reason, 0) + 1
        
        # Summary metrics with enhanced cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 1.5rem;">📝</div>
                <div class="metric-label">총 변경사항</div>
                <div class="metric-value">{}</div>
                <div class="metric-unit">개</div>
            </div>
            """.format(total_changes), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 1.5rem;">📄</div>
                <div class="metric-label">코드 라인</div>
                <div class="metric-value">{}</div>
                <div class="metric-unit">줄</div>
            </div>
            """.format(lines_original), unsafe_allow_html=True)
        
        with col3:
            # Most common issue
            if change_types:
                most_common = max(change_types.items(), key=lambda x: x[1])
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem;">🎯</div>
                    <div class="metric-label">주요 이슈</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-unit">{} 건</div>
                </div>
                """.format(most_common[1], most_common[0][:10] + "..."), unsafe_allow_html=True)
        
        with col4:
            # Improvement rate
            improvement_rate = (total_changes / lines_original) * 100 if lines_original > 0 else 0
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 1.5rem;">📊</div>
                <div class="metric-label">개선율</div>
                <div class="metric-value">{:.1f}</div>
                <div class="metric-unit">%</div>
            </div>
            """.format(improvement_rate), unsafe_allow_html=True)
        
        # Change type breakdown with modern progress bars
        if change_types:
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            st.markdown("#### 🔍 변경 유형별 분포")
            
            for change_type, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
                progress = count / total_changes
                
                # Create custom progress bar
                st.markdown(f"""
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: var(--text-primary);">{change_type}</span>
                        <span style="color: var(--text-secondary);">{count}개 ({progress:.0%})</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {progress * 100}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def _save_transformed_code(self):
        """Save transformed code"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transformed_code_{timestamp}.py"
        
        st.download_button(
            label="💾 파일 다운로드",
            data=st.session_state.transformed_code,
            file_name=filename,
            mime="text/plain"
        )
    
    def _load_example_code(self):
        """Load example code"""
        example_code = """def process_usr_data(usr_id, pwd):
    # 사용자 정보 처리
    사용자정보 = get_user_info(usr_id)
    err_msg = ""
    res = None
    
    try:
        if 사용자정보 and check_pwd(pwd, 사용자정보):
            res = create_session(usr_id)
            usr_cnt = increment_login_count(usr_id)
        else:
            err_msg = "Invalid credentials"
    except Exception as e:
        err_msg = str(e)
    
    return res, err_msg

class UserMgr:
    def __init__(self):
        self.usr_lst = []
        self.db_conn = None
        
    def add_usr(self, usr_nm, 이메일):
        usr_obj = {
            'name': usr_nm,
            'email': 이메일,
            'created_dt': datetime.now()
        }
        self.usr_lst.append(usr_obj)
        return True"""
        
        st.session_state.original_code = example_code
        st.rerun()
    
    def _generate_random_code(self):
        """Generate random code using code generator"""
        try:
            from code_generator import RandomCodeGenerator
            generator = RandomCodeGenerator()
            code, pattern, desc = generator.generate_random_code()
            st.session_state.original_code = code
            st.rerun()
        except Exception as e:
            st.error(f"랜덤 코드 생성 중 오류: {str(e)}")
    
    def _render_file_upload(self):
        """Render file upload interface"""
        st.subheader("📁 파일 업로드")
        
        uploaded_file = st.file_uploader(
            "Python 파일을 선택하세요",
            type=['py'],
            help="변환할 Python 코드 파일을 업로드하세요"
        )
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            st.session_state.original_code = content
            st.session_state.show_upload = False
            st.success(f"✅ {uploaded_file.name} 파일을 성공적으로 로드했습니다!")
            st.rerun()
        
        if st.button("❌ 취소"):
            st.session_state.show_upload = False
            st.rerun()
    
    def _render_dictionary_view(self):
        """Render terminology dictionary view"""
        # Use the new terminology UI
        self.term_ui.render()
        
        st.divider()
        if st.button("❌ 메인으로 돌아가기", type="secondary"):
            st.session_state.show_dictionary = False
            st.rerun()
    
    def _render_statistics(self):
        """Render transformation statistics"""
        st.subheader("📊 변환 통계")
        
        if st.session_state.transformation_history:
            # Create DataFrame
            df = pd.DataFrame(st.session_state.transformation_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("총 변환 수", f"{len(df)}건")
            
            with col2:
                total_changes = df['changes'].sum()
                st.metric("총 변경사항", f"{total_changes}개")
            
            with col3:
                avg_changes = df['changes'].mean()
                st.metric("평균 변경/변환", f"{avg_changes:.1f}개")
            
            with col4:
                total_lines = df['original_lines'].sum()
                st.metric("처리된 코드", f"{total_lines:,}줄")
            
            # History table
            st.divider()
            st.subheader("변환 이력")
            
            display_df = df[['timestamp', 'original_lines', 'changes', 'convention']].tail(20)
            display_df.columns = ['시간', '코드 라인', '변경사항', '규칙']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "시간": st.column_config.DatetimeColumn(format="MM/DD HH:mm"),
                    "코드 라인": st.column_config.NumberColumn(format="%d줄"),
                    "변경사항": st.column_config.NumberColumn(format="%d개"),
                }
            )
        else:
            st.info("아직 변환 이력이 없습니다.")
        
        if st.button("❌ 닫기"):
            st.session_state.show_stats = False
            st.rerun()
    
    def _render_metric_card(self, label: str, value: str, unit: str, color: str):
        """Render a metric card"""
        st.markdown(
            f"""
            <div style='background: {color}; color: white; padding: 1rem; border-radius: 8px; text-align: center;'>
                <div style='font-size: 0.8em; opacity: 0.8;'>{label}</div>
                <div style='font-size: 1.8em; font-weight: bold; margin: 0.2rem 0;'>{value}</div>
                <div style='font-size: 0.7em; opacity: 0.8;'>{unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _render_modern_metric_card(self, icon: str, label: str, value: str, unit: str):
        """Render a modern metric card with icon"""
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _render_advanced_statistics(self):
        """Render advanced statistics dashboard"""
        # Back button
        if st.button("← 메인으로 돌아가기"):
            st.session_state.show_advanced_stats = False
            st.rerun()
        
        # Render the visualization dashboard
        self.viz_dashboard.render_dashboard()
        
        # Export options
        st.divider()
        st.subheader("📤 통계 내보내기")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 JSON", use_container_width=True):
                json_data = self.stats_manager.export_statistics('json')
                st.download_button(
                    label="JSON 다운로드",
                    data=json_data,
                    file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 CSV", use_container_width=True):
                csv_data = self.stats_manager.export_statistics('csv')
                st.download_button(
                    label="CSV 다운로드",
                    data=csv_data,
                    file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📈 Excel", use_container_width=True):
                self.stats_manager.export_statistics('excel')
                st.success("Excel 파일이 생성되었습니다: transformation_statistics.xlsx")
        
        with col4:
            if st.button("🔄 통계 초기화", type="secondary", use_container_width=True):
                if st.checkbox("정말로 모든 통계를 초기화하시겠습니까?"):
                    self.stats_manager.reset_statistics()
                    st.success("통계가 초기화되었습니다.")
                    st.rerun()


def main():
    app = CodeTransformerUI()
    app.run()


if __name__ == "__main__":
    main()