"""
System-wide fixes and improvements for the Code Transformer system
"""

import os
import json
import pandas as pd
from typing import Dict, Any

def fix_statistics_file():
    """Fix the statistics file structure"""
    stats_file = "transformation_statistics.json"
    
    if os.path.exists(stats_file):
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            
            # Add missing fields
            if 'total_files' not in stats:
                stats['total_files'] = stats.get('total_transformations', 0)
            if 'total_lines' not in stats:
                stats['total_lines'] = stats.get('total_lines_processed', 0)
            
            # Save updated stats
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            print("[OK] Statistics file fixed successfully")
        except Exception as e:
            print(f"[ERROR] Error fixing statistics file: {e}")

def create_custom_terms_file():
    """Create custom terms file if it doesn't exist"""
    custom_terms_file = "custom_terms.json"
    
    if not os.path.exists(custom_terms_file):
        try:
            with open(custom_terms_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print("[OK] Custom terms file created")
        except Exception as e:
            print(f"[ERROR] Error creating custom terms file: {e}")

def validate_csv_encoding():
    """Validate and report CSV encoding"""
    csv_file = "용어사전.csv"
    
    if os.path.exists(csv_file):
        encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_file, encoding=encoding, header=None, nrows=5)
                print(f"[OK] CSV can be read with {encoding} encoding")
                print(f"   First row sample: {df.iloc[0, 0][:20]}...")
                return encoding
            except Exception as e:
                print(f"[FAIL] Failed with {encoding}: {str(e)[:50]}...")
        
        print("[WARNING] CSV file has encoding issues")
    else:
        print("[ERROR] CSV file not found")
    
    return None

def create_required_directories():
    """Create required directories if they don't exist"""
    directories = ['logs', 'exports', 'backups']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"[OK] Created directory: {directory}")
            except Exception as e:
                print(f"[ERROR] Error creating directory {directory}: {e}")

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"[OK] {package_name} is installed")
        except ImportError:
            missing_packages.append(package_name)
            print(f"[ERROR] {package_name} is NOT installed")
    
    if missing_packages:
        print(f"\n[WARNING] Install missing packages with: pip install {' '.join(missing_packages)}")
    
    return len(missing_packages) == 0

def run_all_fixes():
    """Run all system fixes"""
    print("Running system-wide fixes...\n")
    
    # 1. Check dependencies
    print("1. Checking dependencies...")
    check_dependencies()
    print()
    
    # 2. Create directories
    print("2. Creating required directories...")
    create_required_directories()
    print()
    
    # 3. Fix statistics file
    print("3. Fixing statistics file...")
    fix_statistics_file()
    print()
    
    # 4. Create custom terms file
    print("4. Creating custom terms file...")
    create_custom_terms_file()
    print()
    
    # 5. Validate CSV encoding
    print("5. Validating CSV encoding...")
    validate_csv_encoding()
    print()
    
    print("[OK] All fixes completed!")

if __name__ == "__main__":
    run_all_fixes()