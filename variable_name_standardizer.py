"""
Variable Name Standardization System
A code review tool that analyzes variable names and suggests standardized alternatives
based on an organization's terminology dictionary.
"""

import re
import os
import csv
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum


class NamingConvention(Enum):
    """Supported naming conventions"""
    SNAKE_CASE = "snake_case"
    CAMEL_CASE = "camelCase"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    UPPER_SNAKE_CASE = "UPPER_SNAKE_CASE"


@dataclass
class TermEntry:
    """Represents an entry in the terminology dictionary"""
    term: str
    standard_variable_name: str
    description: str
    related_terms: List[str] = None
    
    def __post_init__(self):
        if self.related_terms is None:
            self.related_terms = []


@dataclass
class ReviewResult:
    """Represents a variable name review result"""
    original_name: str
    suggested_name: str
    reason: str
    evidence_term: str
    confidence: float


class TerminologyDictionary:
    """Manages the organization's standard terminology"""
    
    def __init__(self, csv_path: str = None):
        self.terms: Dict[str, TermEntry] = {}
        self.terms_count = 0
        if csv_path and os.path.exists(csv_path):
            self._load_from_csv(csv_path)
        else:
            self._initialize_default_terms()
    
    def _initialize_default_terms(self):
        """Initialize with common terminology"""
        # User-related terms
        self.add_term("user", "user", "System user or account holder", 
                     ["usr", "usuario", "customer", "client"])
        self.add_term("user_id", "user_id", "Unique identifier for a user",
                     ["uid", "userid", "user_identifier", "usr_id"])
        self.add_term("username", "username", "User's login name",
                     ["user_name", "uname", "login_name", "user_nm"])
        
        # Authentication terms
        self.add_term("password", "password", "User authentication credential",
                     ["pwd", "pass", "passwd", "pw"])
        self.add_term("token", "token", "Authentication or session token",
                     ["tkn", "auth_token", "session_token"])
        
        # Data-related terms
        self.add_term("data", "data", "Information or dataset",
                     ["datos", "info", "information"])
        self.add_term("result", "result", "Output or return value",
                     ["res", "resultado", "output", "ret"])
        self.add_term("error", "error", "Error condition or exception",
                     ["err", "erro", "exception", "exc"])
        self.add_term("message", "message", "Communication or notification",
                     ["msg", "mensaje", "mensagem", "notification"])
        
        # Status and state terms
        self.add_term("status", "status", "Current state or condition",
                     ["stat", "estado", "state", "sts"])
        self.add_term("active", "is_active", "Active state indicator",
                     ["activo", "enabled", "act"])
        self.add_term("deleted", "is_deleted", "Deletion state indicator",
                     ["del", "removed", "eliminado"])
        
        # Time-related terms
        self.add_term("created_at", "created_at", "Creation timestamp",
                     ["created", "creation_date", "create_time", "created_dt"])
        self.add_term("updated_at", "updated_at", "Last update timestamp",
                     ["updated", "modified", "update_time", "updated_dt"])
        
        # Quantity and measurement
        self.add_term("count", "count", "Number or quantity",
                     ["cnt", "cantidad", "num", "number"])
        self.add_term("total", "total", "Sum or aggregate amount",
                     ["tot", "sum", "total_amount"])
        self.add_term("amount", "amount", "Quantity or monetary value",
                     ["amt", "monto", "value"])
        
        # Object and entity terms
        self.add_term("object", "object", "Data object or entity",
                     ["obj", "objeto", "entity"])
        self.add_term("item", "item", "Individual element or entry",
                     ["itm", "elemento", "element"])
        self.add_term("list", "list", "Collection of items",
                     ["lst", "lista", "array", "collection"])
        
        # Request and response
        self.add_term("request", "request", "API or service request",
                     ["req", "solicitud", "petition"])
        self.add_term("response", "response", "API or service response",
                     ["resp", "res", "respuesta", "reply"])
        
        # Configuration
        self.add_term("configuration", "config", "System configuration",
                     ["cfg", "conf", "configuration", "settings"])
        self.add_term("parameter", "parameter", "Function or method parameter",
                     ["param", "prm", "arg", "argument"])
    
    def _load_from_csv(self, csv_path: str):
        """Load terminology from CSV file"""
        encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr']
        
        for encoding in encodings:
            try:
                with open(csv_path, 'r', encoding=encoding) as f:
                    reader = csv.reader(f)
                    terms_loaded = 0
                    
                    for row in reader:
                        if len(row) >= 3:
                            # CSV format: 한글명, 영문명, 약어, ...
                            korean_name = row[0].strip()
                            english_name = row[1].strip() if row[1] else ""
                            abbreviation = row[2].strip() if row[2] else ""
                            
                            # Skip empty rows
                            if not korean_name and not english_name:
                                continue
                                
                            # Clean up the data
                            if english_name and len(english_name) > 2:
                                # Create variable name from abbreviation or english name
                                if abbreviation and len(abbreviation) >= 2 and abbreviation.replace('_', '').isalnum():
                                    standard_name = abbreviation.lower().replace('-', '_')
                                else:
                                    # Convert english name to snake_case
                                    standard_name = english_name.lower()
                                    standard_name = re.sub(r'[^\w\s]', '', standard_name)
                                    standard_name = standard_name.replace(' ', '_')
                                    standard_name = re.sub(r'_+', '_', standard_name).strip('_')
                                
                                if standard_name and len(standard_name) > 1:
                                    # Prepare related terms
                                    related = []
                                    
                                    # Add abbreviation as related term
                                    if abbreviation and abbreviation.lower() != standard_name:
                                        related.append(abbreviation.lower())
                                    
                                    # Add variations of english name
                                    eng_variations = [
                                        english_name.lower().replace(' ', '_'),
                                        english_name.lower().replace(' ', ''),
                                        english_name.lower().replace(' ', '-')
                                    ]
                                    for var in eng_variations:
                                        if var != standard_name and len(var) > 2:
                                            related.append(var)
                                    
                                    # Remove duplicates
                                    related = list(set(related))
                                    
                                    # Add the term
                                    self.add_term(
                                        key=standard_name,
                                        standard_name=standard_name,
                                        description=f"{korean_name} ({english_name})" if korean_name else english_name,
                                        related_terms=related
                                    )
                                    
                                    # Also add Korean term for lookup if exists
                                    if korean_name and korean_name.strip():
                                        self.terms[korean_name.lower()] = TermEntry(
                                            term=standard_name,
                                            standard_variable_name=standard_name,
                                            description=korean_name,
                                            related_terms=related
                                        )
                                    
                                    terms_loaded += 1
                    
                    if terms_loaded > 0:
                        self.terms_count = terms_loaded
                        # Don't print in production, just return
                        return
                        
            except UnicodeDecodeError:
                continue
            except Exception as e:
                # Don't print errors in production
                continue
        
        # If we get here, no encoding worked - use default terms
        self._initialize_default_terms()
    
    def add_term(self, key: str, standard_name: str, description: str, 
                 related_terms: List[str] = None):
        """Add a term to the dictionary"""
        entry = TermEntry(key, standard_name, description, related_terms or [])
        self.terms[key.lower()] = entry
        
        # Also index related terms for reverse lookup
        if related_terms:
            for related in related_terms:
                self.terms[related.lower()] = entry
    
    def find_matching_term(self, variable_name: str) -> Optional[TermEntry]:
        """Find a matching term for a given variable name"""
        # Direct match
        lower_name = variable_name.lower()
        if lower_name in self.terms:
            return self.terms[lower_name]
        
        # Try to match parts of the variable name
        parts = self._split_variable_name(variable_name)
        for part in parts:
            if part.lower() in self.terms:
                return self.terms[part.lower()]
        
        return None
    
    def _split_variable_name(self, name: str) -> List[str]:
        """Split variable name into parts based on naming convention"""
        # Handle snake_case
        if '_' in name:
            return name.split('_')
        
        # Handle camelCase and PascalCase
        parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
        if parts:
            return parts
        
        # Handle kebab-case
        if '-' in name:
            return name.split('-')
        
        return [name]


class VariableNameAnalyzer:
    """Analyzes variable names and suggests improvements"""
    
    def __init__(self, dictionary: TerminologyDictionary):
        self.dictionary = dictionary
        self.common_abbreviations = {
            'usr': 'user',
            'pwd': 'password',
            'msg': 'message',
            'err': 'error',
            'res': 'result',
            'req': 'request',
            'resp': 'response',
            'cfg': 'config',
            'cnt': 'count',
            'amt': 'amount',
            'obj': 'object',
            'lst': 'list',
            'num': 'number',
            'temp': 'temporary',
            'val': 'value',
            'idx': 'index',
            'btn': 'button',
            'img': 'image',
            'src': 'source',
            'dest': 'destination',
            'dir': 'directory',
            'db': 'database'
        }
    
    def detect_naming_convention(self, code: str) -> NamingConvention:
        """Detect the predominant naming convention in the code"""
        conventions_count = {
            NamingConvention.SNAKE_CASE: 0,
            NamingConvention.CAMEL_CASE: 0,
            NamingConvention.PASCAL_CASE: 0
        }
        
        # Extract variable names using regex
        variable_pattern = r'\b([a-zA-Z_]\w*)\b'
        variables = re.findall(variable_pattern, code)
        
        for var in variables:
            if '_' in var and var.islower():
                conventions_count[NamingConvention.SNAKE_CASE] += 1
            elif var[0].islower() and any(c.isupper() for c in var[1:]):
                conventions_count[NamingConvention.CAMEL_CASE] += 1
            elif var[0].isupper() and any(c.islower() for c in var):
                conventions_count[NamingConvention.PASCAL_CASE] += 1
        
        return max(conventions_count, key=conventions_count.get)
    
    def analyze_variable_name(self, variable_name: str, 
                            target_convention: NamingConvention) -> Optional[ReviewResult]:
        """Analyze a single variable name and suggest improvements"""
        # Check if variable uses mixed languages
        if self._has_mixed_languages(variable_name):
            suggested = self._standardize_mixed_language(variable_name, target_convention)
            if suggested and suggested != variable_name:
                return ReviewResult(
                    original_name=variable_name,
                    suggested_name=suggested,
                    reason="혼용된 언어 사용",
                    evidence_term="표준 영문 용어",
                    confidence=0.9
                )
        
        # Check for meaningless abbreviations
        expanded = self._expand_abbreviations(variable_name)
        if expanded != variable_name:
            term = self.dictionary.find_matching_term(expanded)
            if term:
                suggested = self._apply_convention(term.standard_variable_name, 
                                                 target_convention)
                return ReviewResult(
                    original_name=variable_name,
                    suggested_name=suggested,
                    reason="의미 없는 약어 사용",
                    evidence_term=term.term,
                    confidence=0.85
                )
        
        # Check against terminology dictionary
        term = self.dictionary.find_matching_term(variable_name)
        if term and term.standard_variable_name != variable_name:
            suggested = self._apply_convention(term.standard_variable_name, 
                                             target_convention)
            return ReviewResult(
                original_name=variable_name,
                suggested_name=suggested,
                reason="표준 용어사전 불일치",
                evidence_term=term.term,
                confidence=0.95
            )
        
        # Check naming convention consistency
        if not self._matches_convention(variable_name, target_convention):
            suggested = self._apply_convention(variable_name, target_convention)
            return ReviewResult(
                original_name=variable_name,
                suggested_name=suggested,
                reason="명명 규칙 불일치",
                evidence_term="naming convention",
                confidence=0.8
            )
        
        return None
    
    def _has_mixed_languages(self, variable_name: str) -> bool:
        """Check if variable name contains mixed languages (Korean + English)"""
        korean_pattern = r'[가-힣]'
        english_pattern = r'[a-zA-Z]'
        
        has_korean = bool(re.search(korean_pattern, variable_name))
        has_english = bool(re.search(english_pattern, variable_name))
        
        return has_korean and has_english
    
    def _standardize_mixed_language(self, variable_name: str, 
                                   convention: NamingConvention) -> Optional[str]:
        """Standardize mixed language variable names"""
        # Common Korean to English mappings
        korean_mappings = {
            '사용자': 'user',
            '비밀번호': 'password',
            '이름': 'name',
            '번호': 'number',
            '데이터': 'data',
            '결과': 'result',
            '상태': 'status',
            '메시지': 'message',
            '오류': 'error',
            '목록': 'list',
            '개수': 'count',
            '합계': 'total',
            '설정': 'config',
            '요청': 'request',
            '응답': 'response'
        }
        
        result = variable_name
        for korean, english in korean_mappings.items():
            result = result.replace(korean, english)
        
        if result != variable_name:
            return self._apply_convention(result, convention)
        
        return None
    
    def _expand_abbreviations(self, variable_name: str) -> str:
        """Expand common abbreviations"""
        parts = self._split_name_parts(variable_name)
        expanded_parts = []
        
        for part in parts:
            lower_part = part.lower()
            if lower_part in self.common_abbreviations:
                expanded_parts.append(self.common_abbreviations[lower_part])
            else:
                expanded_parts.append(part)
        
        return '_'.join(expanded_parts)
    
    def _split_name_parts(self, name: str) -> List[str]:
        """Split variable name into parts"""
        # Handle different naming conventions
        if '_' in name:
            return name.split('_')
        elif '-' in name:
            return name.split('-')
        else:
            # Handle camelCase/PascalCase
            return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
    
    def _matches_convention(self, variable_name: str, 
                          convention: NamingConvention) -> bool:
        """Check if variable name matches the target convention"""
        if convention == NamingConvention.SNAKE_CASE:
            return bool(re.match(r'^[a-z]+(_[a-z]+)*$', variable_name))
        elif convention == NamingConvention.CAMEL_CASE:
            return bool(re.match(r'^[a-z]+([A-Z][a-z]+)*$', variable_name))
        elif convention == NamingConvention.PASCAL_CASE:
            return bool(re.match(r'^[A-Z][a-z]+([A-Z][a-z]+)*$', variable_name))
        return True
    
    def _apply_convention(self, name: str, convention: NamingConvention) -> str:
        """Apply naming convention to a variable name"""
        parts = self._split_name_parts(name)
        
        if convention == NamingConvention.SNAKE_CASE:
            return '_'.join(part.lower() for part in parts)
        elif convention == NamingConvention.CAMEL_CASE:
            if not parts:
                return name
            return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
        elif convention == NamingConvention.PASCAL_CASE:
            return ''.join(part.capitalize() for part in parts)
        
        return name


class CodeReviewer:
    """Main code review system"""
    
    def __init__(self, csv_path: str = None):
        # Try to load from CSV first, otherwise use default
        if csv_path is None:
            csv_path = "용어사전.csv"
        self.dictionary = TerminologyDictionary(csv_path)
        self.analyzer = VariableNameAnalyzer(self.dictionary)
    
    def review_code(self, code: str) -> List[ReviewResult]:
        """Review code and return list of suggestions"""
        # Detect naming convention
        convention = self.analyzer.detect_naming_convention(code)
        
        # Extract all variable names
        variables = self._extract_variables(code)
        
        # Analyze each variable
        results = []
        for var in variables:
            result = self.analyzer.analyze_variable_name(var, convention)
            if result:
                results.append(result)
        
        return results
    
    def _extract_variables(self, code: str) -> Set[str]:
        """Extract variable names from code"""
        # Common patterns for variable declarations
        patterns = [
            r'\b(\w+)\s*=\s*',  # assignment
            r'def\s+\w+\([^)]*(\w+)[^)]*\)',  # function parameters
            r'for\s+(\w+)\s+in',  # for loops
            r'except\s+\w+\s+as\s+(\w+)',  # exception handling
            r'(\w+)\s*\+=',  # augmented assignment
            r'(\w+)\s*-=',
            r'(\w+)\s*\*=',
            r'(\w+)\s*/=',
        ]
        
        variables = set()
        for pattern in patterns:
            matches = re.findall(pattern, code)
            variables.update(matches)
        
        # Filter out language keywords and built-ins
        keywords = {'def', 'class', 'if', 'else', 'elif', 'for', 'while', 
                   'try', 'except', 'finally', 'return', 'import', 'from',
                   'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is'}
        
        return {v for v in variables if v not in keywords and len(v) > 1}
    
    def format_results(self, results: List[ReviewResult]) -> str:
        """Format review results for display"""
        if not results:
            return "모든 변수명이 표준을 준수합니다."
        
        output = []
        for result in results:
            if result.confidence >= 0.8:
                output.append(
                    f"{result.original_name} → {result.suggested_name} : "
                    f"{result.reason} (근거: {result.evidence_term})"
                )
            else:
                output.append(
                    f"{result.original_name} : 해당 변수는 사전에 없음"
                )
        
        return '\n'.join(output)


# Usage example
if __name__ == "__main__":
    reviewer = CodeReviewer()
    
    # Example code to review
    sample_code = """
    def process_사용자_data(usr_id, pwd):
        res = None
        err_msg = ""
        
        try:
            사용자정보 = get_user_info(usr_id)
            if 사용자정보:
                res = validate_pwd(pwd, 사용자정보)
        except Exception as e:
            err_msg = str(e)
        
        return res, err_msg
    """
    
    results = reviewer.review_code(sample_code)
    print(reviewer.format_results(results))