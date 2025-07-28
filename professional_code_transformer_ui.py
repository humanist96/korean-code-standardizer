"""
Professional Enhanced Code Transformer UI
Production-ready interface with modern design
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
from code_examples import CodeExamples
from settings_manager import SettingsManager
from settings_ui import SettingsUI


# Page configuration
st.set_page_config(
    page_title="코드 변수명 표준화 변환기",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* CSS Variables */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #818cf8;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
        --dark: #1e293b;
        --gray: #64748b;
        --light: #f8fafc;
        --border: #e2e8f0;
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Home Navigation */
    .home-nav {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    .home-link {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 12px;
        color: var(--dark);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .home-link:hover {
        background: white;
        border-color: var(--primary);
        color: var(--primary);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: -200px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Card Styles */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, white 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary Button */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
    }
    
    [data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
    }
    
    /* Code Editor Styles */
    .stCodeBlock {
        border-radius: 12px;
        border: 1px solid var(--border);
        background: #f8fafc;
    }
    
    .stTextArea > div > div > textarea {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        line-height: 1.6;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: white;
    }
    
    /* Tab Styles */
    .stTabs > div > div > div > div {
        background: white;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        margin: 0 0.25rem;
        transition: all 0.3s ease;
        border: 1px solid var(--border);
    }
    
    .stTabs > div > div > div > div:hover {
        background: var(--light);
        border-color: var(--primary);
    }
    
    .stTabs > div > div > div > div[data-baseweb="tab-highlight"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: white;
        border-right: 1px solid var(--border);
    }
    
    /* Expander Styles */
    .streamlit-expanderHeader {
        background: var(--light);
        border-radius: 10px;
        border: 1px solid var(--border);
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: white;
        border-color: var(--primary);
    }
    
    /* Diff Styles */
    .diff-added {
        background-color: #d4f4dd;
        color: #22863a;
        padding: 2px 4px;
        border-radius: 3px;
        text-decoration: none;
    }
    
    .diff-removed {
        background-color: #ffeef0;
        color: #cb2431;
        padding: 2px 4px;
        border-radius: 3px;
        text-decoration: line-through;
    }
    
    /* Animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Loading Spinner */
    .spinner {
        border: 3px solid var(--border);
        border-top: 3px solid var(--primary);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Toast Notification */
    .toast {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-left: 4px solid var(--success);
        animation: slideInRight 0.3s ease-out;
        z-index: 1000;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Glassmorphism Effect */
    .glass {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: var(--gray);
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: var(--light);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: var(--success);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning);
        color: white;
    }
    
    .badge-danger {
        background: var(--danger);
        color: white;
    }
    
    .badge-info {
        background: var(--info);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Home navigation
st.markdown("""
<div class="home-nav">
    <a href="#" class="home-link" onclick="window.location.reload()">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" fill="currentColor"/>
        </svg>
        홈
    </a>
</div>
""", unsafe_allow_html=True)


class ProfessionalCodeTransformerUI:
    def __init__(self):
        # Initialize settings manager first
        self.settings_manager = SettingsManager()
        self.settings_ui = SettingsUI(self.settings_manager)
        
        # Initialize managers
        self.terminology_manager = TerminologyManager()
        self.terminology_ui = TerminologyUI(self.terminology_manager)
        self.reviewer = EnhancedCodeReviewer(self.terminology_manager)
        
        # Initialize statistics manager
        self.stats_manager = StatisticsManager()
        self.viz_dashboard = VisualizationDashboard(self.stats_manager)
        
        # Initialize code examples
        self.code_examples = CodeExamples()
        
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
        if 'original_code' not in st.session_state:
            st.session_state.original_code = ""
        if 'show_upload' not in st.session_state:
            st.session_state.show_upload = False
        if 'show_examples' not in st.session_state:
            st.session_state.show_examples = False
    
    def run(self):
        """Run the application"""
        # Sidebar navigation
        with st.sidebar:
            st.markdown("### 🔄 코드 변수명 표준화")
            st.markdown("---")
            
            if st.button("🏠 홈", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("💻 코드 변환", use_container_width=True):
                st.session_state.page = 'transformer'
                st.rerun()
            
            if st.button("📚 용어사전", use_container_width=True):
                st.session_state.page = 'terminology'
                st.rerun()
            
            if st.button("📊 통계", use_container_width=True):
                st.session_state.page = 'statistics'
                st.rerun()
            
            if st.button("⚙️ 설정", use_container_width=True):
                st.session_state.page = 'settings'
                st.rerun()
            
            st.markdown("---")
            st.caption("v1.0.0")
        
        # Main content
        if st.session_state.page == 'home':
            self._render_home()
        elif st.session_state.page == 'transformer':
            self._render_transformer()
        elif st.session_state.page == 'terminology':
            self._render_terminology()
        elif st.session_state.page == 'statistics':
            self._render_statistics()
        elif st.session_state.page == 'settings':
            self._render_settings()
    
    def _render_home(self):
        """Render home page with modern design"""
        # Hero Section
        st.markdown('<div class="main-header animate-slide-in">', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="margin: 0;">🔄 코드 변수명 표준화 시스템</h1>
        <p style="margin-top: 0.5rem; font-size: 1.2rem;">엔터프라이즈급 코드 품질 관리 솔루션</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Metrics
        self._render_key_metrics()
        
        # Feature Grid
        st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="feature-card" onclick="window.location.hash='transformer'">
                <div class="feature-icon">🔄</div>
                <div class="feature-title">코드 변환</div>
                <div class="feature-desc">변수명 표준화 및 코드 품질 개선</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("시작하기", key="transform_btn", use_container_width=True):
                st.session_state.page = 'transformer'
                st.rerun()
        
        with col2:
            st.markdown("""
            <div class="feature-card" onclick="window.location.hash='terminology'">
                <div class="feature-icon">📚</div>
                <div class="feature-title">용어사전 관리</div>
                <div class="feature-desc">표준 용어 관리 및 검색</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("시작하기", key="term_btn", use_container_width=True):
                st.session_state.page = 'terminology'
                st.rerun()
        
        with col3:
            st.markdown("""
            <div class="feature-card" onclick="window.location.hash='statistics'">
                <div class="feature-icon">📊</div>
                <div class="feature-title">통계 & 분석</div>
                <div class="feature-desc">변환 이력 및 품질 지표</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("시작하기", key="stats_btn", use_container_width=True):
                st.session_state.page = 'statistics'
                st.rerun()
        
        with col4:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⚙️</div>
                <div class="feature-title">설정</div>
                <div class="feature-desc">시스템 설정 및 환경 구성</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("시작하기", key="settings_btn", use_container_width=True):
                st.session_state.page = 'settings'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent Activities
        self._render_recent_activities()
    
    def _render_transformer(self):
        """Render code transformer page"""
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="margin: 0;">🔄 코드 변수명 표준화</h1>
        <p style="margin-top: 0.5rem;">용어사전 기반 자동 변환 시스템</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        stats = self.terminology_manager.get_statistics()
        
        with col1:
            st.metric("표준 용어", f"{stats['total_terms']:,}개")
        
        with col2:
            today_stats = self.stats_manager.get_today_statistics()
            st.metric("오늘 변환", f"{today_stats.get('total_files', 0)}개 파일")
        
        with col3:
            all_time_stats = self.stats_manager.get_all_time_statistics()
            st.metric("누적 개선", f"{all_time_stats.get('total_issues_found', 0):,}개")
        
        # Spacing
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'show_upload') and st.session_state.show_upload:
            self._render_file_upload()
        elif hasattr(st.session_state, 'show_examples') and st.session_state.show_examples:
            self._render_code_examples()
        else:
            self._render_main_transformer()
    
    def _render_key_metrics(self):
        """Render key metrics in professional cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        stats = self.terminology_manager.get_statistics()
        today_stats = self.stats_manager.get_today_statistics()
        all_time_stats = self.stats_manager.get_all_time_statistics()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_terms']:,}</div>
                <div class="metric-label">표준 용어</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{today_stats.get('total_files', 0)}</div>
                <div class="metric-label">오늘 변환</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{all_time_stats.get('total_issues_found', 0):,}</div>
                <div class="metric-label">누적 개선</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            success_rate = all_time_stats.get('average_confidence', 0) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{success_rate:.1f}%</div>
                <div class="metric-label">성공률</div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_recent_activities(self):
        """Render recent activities section"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 최근 활동")
        
        recent_records = self.stats_manager.get_recent_records(5)
        
        if recent_records:
            for record in recent_records:
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{record['file_name']}**")
                    st.caption(record['timestamp'])
                
                with col2:
                    issues = record.get('issues_found', 0)
                    severity = "danger" if issues > 10 else "warning" if issues > 5 else "success"
                    st.markdown(f'<span class="badge badge-{severity}">{issues} 이슈</span>', unsafe_allow_html=True)
                
                with col3:
                    confidence = record.get('confidence_score', 0) * 100
                    st.markdown(f"신뢰도: {confidence:.0f}%")
            
            st.markdown("---")
            
            # View all button
            if st.button("전체 기록 보기", use_container_width=True):
                st.session_state.page = 'statistics'
                st.rerun()
        else:
            st.info("아직 변환 기록이 없습니다. 코드 변환을 시작해보세요!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_main_transformer(self):
        """Render main transformer interface"""
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📁 파일 업로드", use_container_width=True, help="Python 파일을 업로드합니다"):
                st.session_state.show_upload = True
                st.rerun()
        
        with col2:
            if st.button("📋 코드 예제", use_container_width=True, help="예제 코드를 사용합니다"):
                st.session_state.show_examples = True
                st.rerun()
        
        with col3:
            if st.button("🗑️ 초기화", use_container_width=True, help="입력을 초기화합니다"):
                st.session_state.original_code = ""
                st.rerun()
        
        with col4:
            if st.button("📊 통계", use_container_width=True, help="변환 통계를 확인합니다"):
                st.session_state.page = 'statistics'
                st.rerun()
        
        # Code input/output in two columns
        col_input, col_output = st.columns(2)
        
        with col_input:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📝 원본 코드")
            
            code_input = st.text_area(
                "Python 코드를 입력하세요",
                value=st.session_state.original_code,
                height=500,
                key="code_input",
                help="변환할 Python 코드를 입력하거나 붙여넣으세요"
            )
            
            # Update session state
            st.session_state.original_code = code_input
            
            # Character count
            char_count = len(code_input)
            line_count = len(code_input.split('\n')) if code_input else 0
            st.caption(f"문자: {char_count:,} | 줄: {line_count:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_output:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("✨ 변환된 코드")
            
            if code_input and st.button("🔄 변환 실행", type="primary", use_container_width=True):
                self._process_transformation(code_input)
            elif hasattr(st.session_state, 'transformed_code'):
                # Show previous transformation result
                st.code(st.session_state.transformed_code, language="python")
                
                # Show statistics
                if hasattr(st.session_state, 'last_result'):
                    result = st.session_state.last_result
                    st.success(f"✅ {result['issues_count']}개 변수명 개선 완료!")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "💾 다운로드",
                            data=st.session_state.transformed_code,
                            file_name="transformed_code.py",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        if st.button("📋 복사", use_container_width=True):
                            st.write("클립보드에 복사되었습니다!")
            else:
                st.info("왼쪽에 코드를 입력하고 '변환 실행' 버튼을 클릭하세요.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis results
        if hasattr(st.session_state, 'last_result'):
            self._render_analysis_results(st.session_state.last_result)
    
    def _process_transformation(self, code: str):
        """Process code transformation"""
        with st.spinner("코드 분석 및 변환 중..."):
            try:
                # Review code
                result = self.reviewer.review_code(code)
                
                # Store results
                st.session_state.transformed_code = result['improved_code']
                st.session_state.last_result = result
                
                # Record statistics
                record = TransformationRecord(
                    timestamp=datetime.now().isoformat(),
                    file_name="직접 입력",
                    file_path="N/A",
                    original_code=code,
                    transformed_code=result['improved_code'],
                    issues_found=result['issues_count'],
                    confidence_score=result['confidence'],
                    transformation_details=result['suggestions']
                )
                
                self.stats_manager.record_transformation(record)
                
                # Show success message
                st.success(f"✅ 변환 완료! {result['issues_count']}개의 개선사항을 적용했습니다.")
                
            except Exception as e:
                st.error(f"변환 중 오류 발생: {str(e)}")
    
    def _render_analysis_results(self, result: Dict):
        """Render detailed analysis results"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔍 상세 분석 결과")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["변경 사항", "코드 비교", "분석 지표"])
        
        with tab1:
            st.markdown("#### 🔄 변경된 변수명")
            
            if result['suggestions']:
                # Group by severity
                high_severity = []
                medium_severity = []
                low_severity = []
                
                for suggestion in result['suggestions']:
                    severity = suggestion.get('severity', 'medium')
                    if severity == 'high':
                        high_severity.append(suggestion)
                    elif severity == 'medium':
                        medium_severity.append(suggestion)
                    else:
                        low_severity.append(suggestion)
                
                # Display by severity
                if high_severity:
                    st.markdown("##### 🔴 높은 우선순위")
                    for sug in high_severity:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"`{sug['original']}` → `{sug['suggestion']}`")
                        with col2:
                            st.caption(sug['reason'])
                
                if medium_severity:
                    st.markdown("##### 🟡 중간 우선순위")
                    for sug in medium_severity:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"`{sug['original']}` → `{sug['suggestion']}`")
                        with col2:
                            st.caption(sug['reason'])
                
                if low_severity:
                    st.markdown("##### 🟢 낮은 우선순위")
                    for sug in low_severity:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"`{sug['original']}` → `{sug['suggestion']}`")
                        with col2:
                            st.caption(sug['reason'])
            else:
                st.info("변경 사항이 없습니다. 코드가 이미 표준을 따르고 있습니다!")
        
        with tab2:
            st.markdown("#### 📊 코드 비교 (Diff View)")
            
            if st.session_state.original_code and st.session_state.transformed_code:
                # Create diff
                diff = difflib.unified_diff(
                    st.session_state.original_code.splitlines(keepends=True),
                    st.session_state.transformed_code.splitlines(keepends=True),
                    fromfile='원본',
                    tofile='변환됨',
                    n=3
                )
                
                diff_html = self._format_diff_html(list(diff))
                st.markdown(diff_html, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("#### 📈 분석 지표")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                confidence_percent = result['confidence'] * 100
                st.metric("신뢰도", f"{confidence_percent:.1f}%")
                
                # Progress bar
                st.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {confidence_percent}%"></div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("발견된 이슈", f"{result['issues_count']}개")
                
                # Issue breakdown
                if result['suggestions']:
                    severity_counts = {'high': 0, 'medium': 0, 'low': 0}
                    for sug in result['suggestions']:
                        severity = sug.get('severity', 'medium')
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                    st.caption(f"🔴 {severity_counts['high']} | 🟡 {severity_counts['medium']} | 🟢 {severity_counts['low']}")
            
            with col3:
                # Calculate improvement score
                if result['issues_count'] > 0:
                    improvement_score = min(100, result['issues_count'] * 10)
                else:
                    improvement_score = 100
                
                st.metric("개선 점수", f"{improvement_score}점")
                st.caption("코드 품질 개선 정도")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _format_diff_html(self, diff_lines: List[str]) -> str:
        """Format diff output as HTML"""
        html_lines = ['<div style="font-family: monospace; font-size: 14px; line-height: 1.6;">']
        
        for line in diff_lines:
            if line.startswith('+') and not line.startswith('+++'):
                html_lines.append(f'<div class="diff-added">{self._escape_html(line)}</div>')
            elif line.startswith('-') and not line.startswith('---'):
                html_lines.append(f'<div class="diff-removed">{self._escape_html(line)}</div>')
            elif line.startswith('@'):
                html_lines.append(f'<div style="color: #0066cc; font-weight: bold;">{self._escape_html(line)}</div>')
            else:
                html_lines.append(f'<div>{self._escape_html(line)}</div>')
        
        html_lines.append('</div>')
        return ''.join(html_lines)
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    
    def _render_terminology(self):
        """Render terminology management page"""
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="margin: 0;">📚 표준 용어사전 관리</h1>
        <p style="margin-top: 0.5rem;">조직 표준 용어 관리 시스템</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render terminology UI
        self.terminology_ui.render()
    
    def _render_statistics(self):
        """Render statistics page"""
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="margin: 0;">📊 통계 & 분석</h1>
        <p style="margin-top: 0.5rem;">코드 품질 개선 현황 대시보드</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render visualization dashboard
        self.viz_dashboard.render_dashboard()
    
    def _render_settings(self):
        """Render settings page"""
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="margin: 0;">⚙️ 시스템 설정</h1>
        <p style="margin-top: 0.5rem;">애플리케이션 환경 설정 및 기본값 관리</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render settings UI
        self.settings_ui.render()
    
    def _render_file_upload(self):
        """Render file upload interface"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 파일 업로드")
        
        uploaded_file = st.file_uploader(
            "Python 파일을 선택하세요",
            type=['py'],
            help="변환할 Python 소스 파일을 업로드하세요"
        )
        
        if uploaded_file:
            # Read file content
            content = uploaded_file.read().decode('utf-8')
            
            # Show preview
            st.markdown("#### 📄 파일 미리보기")
            st.code(content[:500] + "..." if len(content) > 500 else content, language="python")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ 이 파일 사용", type="primary", use_container_width=True):
                    st.session_state.original_code = content
                    st.session_state.show_upload = False
                    st.success(f"파일 '{uploaded_file.name}'을 불러왔습니다!")
                    st.rerun()
            
            with col2:
                if st.button("❌ 취소", use_container_width=True):
                    st.session_state.show_upload = False
                    st.rerun()
        else:
            if st.button("❌ 취소", help="파일 업로드를 취소합니다"):
                st.session_state.show_upload = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_code_examples(self):
        """Render code examples selection interface"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 코드 예제")
        st.markdown("테스트에 사용할 코드 예제를 선택하세요")
        
        # Create tabs for different example categories
        tab1, tab2, tab3 = st.tabs(["기본 예제", "문제 유형별 예제", "랜덤 생성"])
        
        with tab1:
            self._render_basic_examples()
        
        with tab2:
            self._render_issue_based_examples()
        
        with tab3:
            self._render_random_generation()
        
        st.divider()
        
        if st.button("❌ 취소", help="메인 화면으로 돌아가기"):
            st.session_state.show_examples = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_basic_examples(self):
        """Render basic example codes"""
        st.markdown("#### 다양한 상황의 예제 코드")
        
        examples = self.code_examples.get_all_basic_examples()
        
        for name, example in examples.items():
            with st.expander(f"**{name}** - {example['description']}", expanded=False):
                # Show code
                st.code(example['code'], language="python")
                
                # Show issues
                st.markdown("##### 발견 가능한 이슈:")
                issue_cols = st.columns(2)
                
                for i, (change, desc, severity) in enumerate(example['issues']):
                    col = issue_cols[i % 2]
                    severity_icon = "🔴" if severity == "high" else "🟡"
                    with col:
                        st.markdown(f"{severity_icon} **{change}** ({desc})")
                
                st.markdown(f"**총 {example['total_issues']}개의 이슈**")
                
                # Use button
                if st.button(f"이 예제 사용하기", key=f"use_basic_{name}"):
                    st.session_state.original_code = example['code']
                    st.session_state.show_examples = False
                    st.success(f"✅ '{name}' 예제를 불러왔습니다!")
                    st.rerun()
    
    def _render_issue_based_examples(self):
        """Render issue-based example codes"""
        st.markdown("#### 특정 문제 유형별 예제")
        
        examples = self.code_examples.get_all_issue_based_examples()
        
        for issue_type, example in examples.items():
            with st.expander(f"**{issue_type}**", expanded=False):
                st.markdown(f"*{example['description']}*")
                
                # Show code
                st.code(example['code'], language="python")
                
                # Show expected changes
                st.markdown("##### 예상 변환:")
                for change in example['expected_changes']:
                    st.markdown(f"• {change}")
                
                st.markdown(f"**총 {example['issues_count']}개의 문제**")
                
                # Use button
                if st.button(f"이 예제 사용하기", key=f"use_issue_{issue_type}"):
                    st.session_state.original_code = example['code']
                    st.session_state.show_examples = False
                    st.success(f"✅ '{issue_type}' 예제를 불러왔습니다!")
                    st.rerun()
    
    def _render_random_generation(self):
        """Render random code generation interface"""
        st.markdown("#### 랜덤 코드 생성")
        st.markdown("특정 패턴과 복잡도를 선택하여 테스트 코드를 생성합니다")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pattern selection
            patterns = self.code_examples.get_pattern_names()
            pattern_names = ["랜덤 선택"] + [name for _, name in patterns]
            pattern_keys = [None] + [key for key, _ in patterns]
            
            selected_idx = st.selectbox(
                "코드 패턴",
                range(len(pattern_names)),
                format_func=lambda x: pattern_names[x],
                help="생성할 코드의 패턴을 선택하세요"
            )
            selected_pattern = pattern_keys[selected_idx]
        
        with col2:
            # Complexity selection
            complexity = st.select_slider(
                "복잡도",
                options=["simple", "medium", "complex"],
                value="medium",
                format_func=lambda x: {"simple": "간단", "medium": "보통", "complex": "복잡"}[x],
                help="생성할 코드의 복잡도를 선택하세요"
            )
        
        # Generate button
        if st.button("🎲 코드 생성", use_container_width=True):
            code, pattern, description = self.code_examples.generate_random_code(selected_pattern, complexity)
            
            # Store in session state temporarily
            st.session_state.temp_random_code = code
            st.session_state.temp_random_desc = description
        
        # Show generated code if available
        if hasattr(st.session_state, 'temp_random_code'):
            st.divider()
            st.markdown(f"##### 생성된 코드: {st.session_state.temp_random_desc}")
            st.code(st.session_state.temp_random_code, language="python")
            
            # Analyze potential issues
            st.markdown("##### 예상되는 이슈:")
            st.markdown("• 약어 사용 (usr, pwd, res, msg 등)")
            st.markdown("• 한글 변수명 사용")
            st.markdown("• 명명 규칙 불일치")
            
            # Use button
            if st.button("이 코드 사용하기", use_container_width=True, type="primary"):
                st.session_state.original_code = st.session_state.temp_random_code
                st.session_state.show_examples = False
                # Clean up temp state
                del st.session_state.temp_random_code
                del st.session_state.temp_random_desc
                st.success("✅ 생성된 코드를 불러왔습니다!")
                st.rerun()


def main():
    app = ProfessionalCodeTransformerUI()
    app.run()


if __name__ == "__main__":
    main()