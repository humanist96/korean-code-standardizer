"""
Final validation script for the Code Transformer system
"""

import os
import sys
import json
import pandas as pd
from typing import Dict, List, Tuple


def validate_system() -> Tuple[List[str], List[str]]:
    """Validate the entire system and return (successes, failures)"""
    successes = []
    failures = []
    
    # 1. Check required files
    required_files = [
        "professional_code_transformer_ui.py",
        "variable_name_standardizer.py",
        "terminology_manager.py",
        "statistics_manager.py",
        "visualization_dashboard.py",
        "code_examples.py",
        "enhanced_code_reviewer.py",
        "용어사전.csv"
    ]
    
    print("1. Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            successes.append(f"File exists: {file}")
        else:
            failures.append(f"Missing file: {file}")
    
    # 2. Check data files
    print("\n2. Checking data files...")
    if os.path.exists("transformation_statistics.json"):
        try:
            with open("transformation_statistics.json", 'r', encoding='utf-8') as f:
                stats = json.load(f)
            if 'total_files' in stats and 'total_lines' in stats:
                successes.append("Statistics file is properly structured")
            else:
                failures.append("Statistics file missing required fields")
        except Exception as e:
            failures.append(f"Error reading statistics file: {e}")
    
    if os.path.exists("custom_terms.json"):
        try:
            with open("custom_terms.json", 'r', encoding='utf-8') as f:
                terms = json.load(f)
            successes.append("Custom terms file is valid")
        except Exception as e:
            failures.append(f"Error reading custom terms file: {e}")
    
    # 3. Validate CSV encoding
    print("\n3. Validating CSV file...")
    if os.path.exists("용어사전.csv"):
        encodings = ['cp949', 'utf-8-sig', 'utf-8', 'euc-kr']
        csv_valid = False
        
        for encoding in encodings:
            try:
                df = pd.read_csv("용어사전.csv", encoding=encoding, header=None, nrows=5)
                successes.append(f"CSV readable with {encoding} encoding")
                csv_valid = True
                break
            except:
                continue
        
        if not csv_valid:
            failures.append("CSV file has unresolvable encoding issues")
    
    # 4. Check imports
    print("\n4. Checking Python imports...")
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        successes.append("All required packages are importable")
    except ImportError as e:
        failures.append(f"Import error: {e}")
    
    # 5. Check directories
    print("\n5. Checking directories...")
    dirs = ['logs', 'exports', 'backups']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            successes.append(f"Directory exists: {dir_name}")
        else:
            failures.append(f"Missing directory: {dir_name}")
    
    return successes, failures


def print_validation_report():
    """Print a formatted validation report"""
    print("=" * 60)
    print("Code Transformer System Validation Report")
    print("=" * 60)
    
    successes, failures = validate_system()
    
    print(f"\nTotal checks: {len(successes) + len(failures)}")
    print(f"Passed: {len(successes)}")
    print(f"Failed: {len(failures)}")
    
    if successes:
        print("\n[PASSED]")
        for success in successes:
            print(f"  + {success}")
    
    if failures:
        print("\n[FAILED]")
        for failure in failures:
            print(f"  - {failure}")
    
    print("\n" + "=" * 60)
    
    if not failures:
        print("System validation PASSED! Ready to run.")
        print("\nTo start the application, run:")
        print("  streamlit run professional_code_transformer_ui.py")
    else:
        print("System validation FAILED. Please fix the issues above.")
    
    print("=" * 60)


if __name__ == "__main__":
    print_validation_report()