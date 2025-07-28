"""
Settings Manager for Code Transformer System
Manages application configuration and preferences
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SystemSettings:
    """System configuration settings"""
    # Display settings
    theme: str = "light"
    language: str = "ko"
    items_per_page: int = 20
    show_line_numbers: bool = True
    
    # Transformation settings
    auto_detect_convention: bool = True
    preferred_convention: str = "snake_case"
    confidence_threshold: float = 0.7
    
    # Statistics settings
    keep_statistics_days: int = 90
    auto_export: bool = False
    export_format: str = "json"
    
    # UI settings
    show_tooltips: bool = True
    enable_animations: bool = True
    sidebar_collapsed: bool = False
    
    # Advanced settings
    max_file_size_mb: int = 10
    parallel_processing: bool = False
    debug_mode: bool = False
    
    # Notification settings
    show_success_messages: bool = True
    show_transformation_details: bool = True
    sound_enabled: bool = False


class SettingsManager:
    """Manages application settings"""
    
    def __init__(self, settings_file: str = "app_settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_settings()
        self._ensure_settings_file()
    
    def _ensure_settings_file(self):
        """Ensure settings file exists"""
        if not os.path.exists(self.settings_file):
            self.save_settings()
    
    def _load_settings(self) -> SystemSettings:
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return SystemSettings(**data)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return SystemSettings()
        return SystemSettings()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save_settings()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple settings"""
        for key, value in updates.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = SystemSettings()
        self.save_settings()
    
    def export_settings(self) -> str:
        """Export settings as JSON string"""
        return json.dumps(asdict(self.settings), ensure_ascii=False, indent=2)
    
    def import_settings(self, json_str: str) -> bool:
        """Import settings from JSON string"""
        try:
            data = json.loads(json_str)
            self.settings = SystemSettings(**data)
            self.save_settings()
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return asdict(self.settings)