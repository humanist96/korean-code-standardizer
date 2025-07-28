"""
Global error handler for the Code Transformer system
"""

import functools
import traceback
import streamlit as st
from typing import Any, Callable


def safe_execute(func: Callable) -> Callable:
    """Decorator to safely execute functions with error handling"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            st.error(f"파일을 찾을 수 없습니다: {str(e)}")
            return None
        except UnicodeDecodeError as e:
            st.error(f"파일 인코딩 오류: {str(e)}")
            st.info("다른 인코딩(cp949, euc-kr)으로 시도해보세요.")
            return None
        except KeyError as e:
            st.error(f"데이터 키 오류: {str(e)}")
            return None
        except ValueError as e:
            st.error(f"값 오류: {str(e)}")
            return None
        except Exception as e:
            st.error(f"예상치 못한 오류 발생: {str(e)}")
            if st.checkbox("상세 오류 정보 보기"):
                st.code(traceback.format_exc())
            return None
    return wrapper


def safe_file_operation(func: Callable) -> Callable:
    """Decorator for safe file operations"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except PermissionError:
            st.error("파일 접근 권한이 없습니다. 파일이 다른 프로그램에서 사용 중인지 확인하세요.")
            return None
        except IOError as e:
            st.error(f"파일 입/출력 오류: {str(e)}")
            return None
        except Exception as e:
            st.error(f"파일 작업 중 오류 발생: {str(e)}")
            return None
    return wrapper


def validate_input(value: Any, expected_type: type, name: str) -> bool:
    """Validate input type and value"""
    if value is None:
        st.warning(f"{name}이(가) 비어있습니다.")
        return False
    
    if not isinstance(value, expected_type):
        st.error(f"{name}의 타입이 올바르지 않습니다. 예상: {expected_type.__name__}")
        return False
    
    if expected_type == str and not value.strip():
        st.warning(f"{name}이(가) 비어있습니다.")
        return False
    
    return True


class ErrorContext:
    """Context manager for error handling"""
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            st.error(f"{self.operation_name} 중 오류 발생: {exc_val}")
            if st.checkbox(f"{self.operation_name} 오류 상세 정보"):
                st.code(traceback.format_exc())
            return True  # Suppress the exception
        return False