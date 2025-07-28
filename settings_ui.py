"""
Settings UI Component for Code Transformer System
Provides user interface for system configuration
"""

import streamlit as st
from typing import Dict, Any
from settings_manager import SettingsManager, SystemSettings


class SettingsUI:
    """Settings user interface component"""
    
    def __init__(self, settings_manager: SettingsManager):
        self.settings_manager = settings_manager
    
    def render(self):
        """Render settings interface"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("⚙️ 시스템 설정")
        
        # Create tabs for different settings categories
        tabs = st.tabs([
            "🎨 표시 설정", 
            "🔄 변환 설정", 
            "📊 통계 설정", 
            "🖥️ UI 설정", 
            "🔧 고급 설정"
        ])
        
        # Display Settings Tab
        with tabs[0]:
            self._render_display_settings()
        
        # Transformation Settings Tab
        with tabs[1]:
            self._render_transformation_settings()
        
        # Statistics Settings Tab
        with tabs[2]:
            self._render_statistics_settings()
        
        # UI Settings Tab
        with tabs[3]:
            self._render_ui_settings()
        
        # Advanced Settings Tab
        with tabs[4]:
            self._render_advanced_settings()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save and Reset buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            if st.button("💾 설정 저장", use_container_width=True, type="primary"):
                self.settings_manager.save_settings()
                st.success("✅ 설정이 저장되었습니다!")
        
        with col2:
            if st.button("🔄 기본값 복원", use_container_width=True):
                if st.checkbox("정말로 모든 설정을 기본값으로 복원하시겠습니까?"):
                    self.settings_manager.reset_to_defaults()
                    st.success("✅ 설정이 기본값으로 복원되었습니다!")
                    st.rerun()
    
    def _render_display_settings(self):
        """Render display settings"""
        st.subheader("표시 설정")
        
        # Theme selection
        theme = st.selectbox(
            "테마",
            options=["light", "dark", "auto"],
            index=["light", "dark", "auto"].index(self.settings_manager.get("theme", "light")),
            help="UI 테마를 선택하세요"
        )
        self.settings_manager.set("theme", theme)
        
        # Language selection
        language = st.selectbox(
            "언어",
            options=["ko", "en"],
            index=["ko", "en"].index(self.settings_manager.get("language", "ko")),
            format_func=lambda x: "한국어" if x == "ko" else "English",
            help="인터페이스 언어를 선택하세요"
        )
        self.settings_manager.set("language", language)
        
        # Items per page
        items_per_page = st.slider(
            "페이지당 항목 수",
            min_value=10,
            max_value=100,
            value=self.settings_manager.get("items_per_page", 20),
            step=10,
            help="목록에서 한 페이지에 표시할 항목 수"
        )
        self.settings_manager.set("items_per_page", items_per_page)
        
        # Show line numbers
        show_line_numbers = st.checkbox(
            "코드에 줄 번호 표시",
            value=self.settings_manager.get("show_line_numbers", True),
            help="코드 표시 시 줄 번호를 함께 표시합니다"
        )
        self.settings_manager.set("show_line_numbers", show_line_numbers)
    
    def _render_transformation_settings(self):
        """Render transformation settings"""
        st.subheader("변환 설정")
        
        # Auto detect convention
        auto_detect = st.checkbox(
            "명명 규칙 자동 감지",
            value=self.settings_manager.get("auto_detect_convention", True),
            help="코드에서 사용된 명명 규칙을 자동으로 감지합니다"
        )
        self.settings_manager.set("auto_detect_convention", auto_detect)
        
        # Preferred convention
        if not auto_detect:
            convention = st.selectbox(
                "선호 명명 규칙",
                options=["snake_case", "camelCase", "PascalCase", "UPPER_CASE"],
                index=["snake_case", "camelCase", "PascalCase", "UPPER_CASE"].index(
                    self.settings_manager.get("preferred_convention", "snake_case")
                ),
                help="변환 시 사용할 기본 명명 규칙"
            )
            self.settings_manager.set("preferred_convention", convention)
        
        # Confidence threshold
        confidence = st.slider(
            "신뢰도 임계값",
            min_value=0.0,
            max_value=1.0,
            value=self.settings_manager.get("confidence_threshold", 0.7),
            step=0.05,
            format="%.2f",
            help="이 값 이상의 신뢰도를 가진 변환만 적용합니다"
        )
        self.settings_manager.set("confidence_threshold", confidence)
    
    def _render_statistics_settings(self):
        """Render statistics settings"""
        st.subheader("통계 설정")
        
        # Keep statistics days
        keep_days = st.number_input(
            "통계 보관 기간 (일)",
            min_value=7,
            max_value=365,
            value=self.settings_manager.get("keep_statistics_days", 90),
            step=7,
            help="통계 데이터를 보관할 기간"
        )
        self.settings_manager.set("keep_statistics_days", keep_days)
        
        # Auto export
        auto_export = st.checkbox(
            "통계 자동 내보내기",
            value=self.settings_manager.get("auto_export", False),
            help="정기적으로 통계를 자동으로 내보냅니다"
        )
        self.settings_manager.set("auto_export", auto_export)
        
        # Export format
        if auto_export:
            export_format = st.selectbox(
                "내보내기 형식",
                options=["json", "csv", "excel"],
                index=["json", "csv", "excel"].index(
                    self.settings_manager.get("export_format", "json")
                ),
                help="통계 내보내기 시 사용할 파일 형식"
            )
            self.settings_manager.set("export_format", export_format)
    
    def _render_ui_settings(self):
        """Render UI settings"""
        st.subheader("UI 설정")
        
        # Show tooltips
        show_tooltips = st.checkbox(
            "도구 설명 표시",
            value=self.settings_manager.get("show_tooltips", True),
            help="UI 요소에 마우스를 올렸을 때 도구 설명을 표시합니다"
        )
        self.settings_manager.set("show_tooltips", show_tooltips)
        
        # Enable animations
        enable_animations = st.checkbox(
            "애니메이션 효과 사용",
            value=self.settings_manager.get("enable_animations", True),
            help="UI 전환 시 애니메이션 효과를 사용합니다"
        )
        self.settings_manager.set("enable_animations", enable_animations)
        
        # Sidebar collapsed
        sidebar_collapsed = st.checkbox(
            "사이드바 기본 접기",
            value=self.settings_manager.get("sidebar_collapsed", False),
            help="앱 시작 시 사이드바를 접은 상태로 표시합니다"
        )
        self.settings_manager.set("sidebar_collapsed", sidebar_collapsed)
        
        # Show success messages
        show_success = st.checkbox(
            "성공 메시지 표시",
            value=self.settings_manager.get("show_success_messages", True),
            help="작업 완료 시 성공 메시지를 표시합니다"
        )
        self.settings_manager.set("show_success_messages", show_success)
        
        # Show transformation details
        show_details = st.checkbox(
            "변환 세부사항 표시",
            value=self.settings_manager.get("show_transformation_details", True),
            help="변환 후 세부 내용을 표시합니다"
        )
        self.settings_manager.set("show_transformation_details", show_details)
        
        # Sound enabled
        sound_enabled = st.checkbox(
            "알림음 사용",
            value=self.settings_manager.get("sound_enabled", False),
            help="중요한 이벤트에 대해 알림음을 재생합니다"
        )
        self.settings_manager.set("sound_enabled", sound_enabled)
    
    def _render_advanced_settings(self):
        """Render advanced settings"""
        st.subheader("고급 설정")
        
        st.warning("⚠️ 고급 설정은 시스템 성능에 영향을 줄 수 있습니다.")
        
        # Max file size
        max_file_size = st.slider(
            "최대 파일 크기 (MB)",
            min_value=1,
            max_value=50,
            value=self.settings_manager.get("max_file_size_mb", 10),
            help="처리할 수 있는 최대 파일 크기"
        )
        self.settings_manager.set("max_file_size_mb", max_file_size)
        
        # Parallel processing
        parallel = st.checkbox(
            "병렬 처리 사용",
            value=self.settings_manager.get("parallel_processing", False),
            help="여러 파일을 동시에 처리합니다 (실험적 기능)"
        )
        self.settings_manager.set("parallel_processing", parallel)
        
        # Debug mode
        debug = st.checkbox(
            "디버그 모드",
            value=self.settings_manager.get("debug_mode", False),
            help="상세한 디버그 정보를 표시합니다"
        )
        self.settings_manager.set("debug_mode", debug)
        
        # Export/Import settings
        st.divider()
        st.subheader("설정 내보내기/가져오기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 설정 내보내기", use_container_width=True):
                settings_json = self.settings_manager.export_settings()
                st.download_button(
                    label="💾 다운로드",
                    data=settings_json,
                    file_name="code_transformer_settings.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_file = st.file_uploader(
                "설정 파일 선택",
                type=["json"],
                key="settings_import"
            )
            
            if uploaded_file is not None:
                settings_content = uploaded_file.read().decode('utf-8')
                if self.settings_manager.import_settings(settings_content):
                    st.success("✅ 설정을 성공적으로 가져왔습니다!")
                    st.rerun()
                else:
                    st.error("❌ 설정 파일을 읽을 수 없습니다.")