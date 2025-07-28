"""
Enhanced Code Reviewer that uses TerminologyManager
Provides better integration with the new terminology system
"""

from typing import List, Set, Optional
import re
from variable_name_standardizer import ReviewResult, NamingConvention, VariableNameAnalyzer
from terminology_manager import TerminologyManager


class EnhancedCodeReviewer:
    """Enhanced code reviewer using TerminologyManager"""
    
    def __init__(self, term_manager: TerminologyManager):
        self.term_manager = term_manager
        self.analyzer = EnhancedVariableAnalyzer(term_manager)
    
    def review_code(self, code: str, convention: NamingConvention = None) -> dict:
        """Review code and return transformation results"""
        # Detect naming convention if not provided
        if convention is None:
            convention = self._detect_naming_convention(code)
        
        # Extract all variable names
        variables = self._extract_variables(code)
        
        # Analyze each variable
        results = []
        for var in variables:
            result = self.analyzer.analyze_variable_name(var, convention)
            if result:
                results.append(result)
        
        # Apply transformations to code
        improved_code = code
        suggestions = []
        
        for result in results:
            if result.suggested_name != result.original_name:
                # Apply the transformation
                improved_code = self._apply_transformation(
                    improved_code, 
                    result.original_name, 
                    result.suggested_name
                )
                
                # Add to suggestions list
                suggestions.append({
                    'original': result.original_name,
                    'suggestion': result.suggested_name,
                    'reason': result.reason,
                    'severity': 'high' if result.confidence > 0.8 else 'medium',
                    'confidence': result.confidence
                })
        
        # Return in expected format
        return {
            'improved_code': improved_code,
            'issues_count': len(suggestions),
            'suggestions': suggestions,
            'confidence': sum(s['confidence'] for s in suggestions) / len(suggestions) if suggestions else 1.0
        }
    
    def _detect_naming_convention(self, code: str) -> NamingConvention:
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
    
    def _apply_transformation(self, code: str, original: str, suggestion: str) -> str:
        """Apply variable name transformation to code"""
        # Use word boundary regex to avoid partial matches
        pattern = r'\b' + re.escape(original) + r'\b'
        return re.sub(pattern, suggestion, code)


class EnhancedVariableAnalyzer:
    """Enhanced variable analyzer using TerminologyManager"""
    
    def __init__(self, term_manager: TerminologyManager):
        self.term_manager = term_manager
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
            term = self.term_manager.get_term(expanded)
            if term:
                suggested = self._apply_convention(term.standard_variable, 
                                                 target_convention)
                return ReviewResult(
                    original_name=variable_name,
                    suggested_name=suggested,
                    reason="의미 없는 약어 사용",
                    evidence_term=term.english_name,
                    confidence=0.85
                )
        
        # Check against terminology manager
        term = self.term_manager.get_term(variable_name)
        if term and term.standard_variable != variable_name.lower():
            suggested = self._apply_convention(term.standard_variable, 
                                             target_convention)
            if suggested != variable_name:
                return ReviewResult(
                    original_name=variable_name,
                    suggested_name=suggested,
                    reason="표준 용어사전 불일치",
                    evidence_term=term.english_name,
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
        # Search for Korean terms in terminology
        korean_pattern = r'[가-힣]+'
        korean_matches = re.findall(korean_pattern, variable_name)
        
        result = variable_name
        for korean_word in korean_matches:
            term = self.term_manager.get_term(korean_word)
            if term:
                result = result.replace(korean_word, term.english_name)
        
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