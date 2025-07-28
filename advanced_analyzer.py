"""
Advanced Variable Name Analyzer with Evidence-Based Reasoning
Provides detailed analysis with confidence scoring and contextual evidence
"""

import ast
import re
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
import difflib


@dataclass
class Evidence:
    """Evidence supporting a recommendation"""
    source: str  # Where the evidence comes from
    detail: str  # Specific detail
    weight: float  # How much this evidence contributes to confidence


@dataclass
class ContextInfo:
    """Context information about a variable"""
    scope: str  # function, class, module
    usage_type: str  # parameter, local, attribute, global
    data_type: Optional[str]  # inferred data type
    usage_count: int
    related_variables: List[str]


@dataclass
class AdvancedReviewResult:
    """Enhanced review result with detailed evidence"""
    original_name: str
    suggested_name: str
    reason: str
    evidence_term: str
    confidence: float
    evidences: List[Evidence]
    context: ContextInfo
    alternative_suggestions: List[Tuple[str, float]]  # (name, confidence)


class CodeContext:
    """Analyzes code context using AST"""
    
    def __init__(self, code: str):
        self.code = code
        try:
            self.tree = ast.parse(code)
        except:
            self.tree = None
        self.variables: Dict[str, ContextInfo] = {}
        self._analyze()
    
    def _analyze(self):
        """Analyze the code and extract variable contexts"""
        if not self.tree:
            return
        
        class VariableVisitor(ast.NodeVisitor):
            def __init__(self, parent):
                self.parent = parent
                self.current_scope = "module"
                self.variables = {}
            
            def visit_FunctionDef(self, node):
                old_scope = self.current_scope
                self.current_scope = f"function:{node.name}"
                
                # Function parameters
                for arg in node.args.args:
                    self._add_variable(arg.arg, "parameter", self.current_scope)
                
                self.generic_visit(node)
                self.current_scope = old_scope
            
            def visit_ClassDef(self, node):
                old_scope = self.current_scope
                self.current_scope = f"class:{node.name}"
                self.generic_visit(node)
                self.current_scope = old_scope
            
            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_type = self._infer_type(node.value)
                        self._add_variable(target.id, "local", self.current_scope, var_type)
                self.generic_visit(node)
            
            def visit_For(self, node):
                if isinstance(node.target, ast.Name):
                    self._add_variable(node.target.id, "iterator", self.current_scope)
                self.generic_visit(node)
            
            def _add_variable(self, name: str, usage_type: str, scope: str, 
                            data_type: Optional[str] = None):
                if name not in self.variables:
                    self.variables[name] = ContextInfo(
                        scope=scope,
                        usage_type=usage_type,
                        data_type=data_type,
                        usage_count=1,
                        related_variables=[]
                    )
                else:
                    self.variables[name].usage_count += 1
            
            def _infer_type(self, node) -> Optional[str]:
                """Simple type inference"""
                if isinstance(node, ast.Constant):
                    return type(node.value).__name__
                elif isinstance(node, ast.List):
                    return "list"
                elif isinstance(node, ast.Dict):
                    return "dict"
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        return f"{node.func.id}_result"
                return None
        
        visitor = VariableVisitor(self)
        visitor.visit(self.tree)
        self.variables = visitor.variables


class EvidenceBasedAnalyzer:
    """Advanced analyzer with evidence-based reasoning"""
    
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.confidence_weights = {
            'exact_match': 1.0,
            'partial_match': 0.8,
            'abbreviation': 0.7,
            'convention': 0.6,
            'context': 0.5,
            'similarity': 0.4
        }
    
    def analyze_with_evidence(self, variable_name: str, 
                            context: ContextInfo,
                            target_convention) -> Optional[AdvancedReviewResult]:
        """Perform deep analysis with evidence collection"""
        evidences = []
        suggestions = []
        
        # 1. Dictionary exact match
        term = self.dictionary.find_matching_term(variable_name)
        if term:
            evidences.append(Evidence(
                source="terminology_dictionary",
                detail=f"Exact match found: {term.term}",
                weight=self.confidence_weights['exact_match']
            ))
            suggestions.append((term.standard_variable_name, 0.95))
        
        # 2. Partial matches and abbreviations
        expanded = self._check_abbreviations(variable_name)
        if expanded != variable_name:
            evidences.append(Evidence(
                source="abbreviation_expansion",
                detail=f"Abbreviation detected: {variable_name} → {expanded}",
                weight=self.confidence_weights['abbreviation']
            ))
            
            # Check if expanded version exists in dictionary
            expanded_term = self.dictionary.find_matching_term(expanded)
            if expanded_term:
                suggestions.append((expanded_term.standard_variable_name, 0.85))
        
        # 3. Context-based analysis
        context_suggestion = self._analyze_by_context(variable_name, context)
        if context_suggestion:
            evidences.append(Evidence(
                source="context_analysis",
                detail=f"Context suggests: {context_suggestion} (scope: {context.scope})",
                weight=self.confidence_weights['context']
            ))
            suggestions.append((context_suggestion, 0.75))
        
        # 4. Similarity matching
        similar_terms = self._find_similar_terms(variable_name)
        for similar, score in similar_terms[:3]:
            evidences.append(Evidence(
                source="similarity_matching",
                detail=f"Similar to standard term: {similar} (score: {score:.2f})",
                weight=self.confidence_weights['similarity'] * score
            ))
            suggestions.append((similar, 0.6 * score))
        
        # 5. Convention analysis
        convention_issue = self._check_convention_issues(variable_name, target_convention)
        if convention_issue:
            evidences.append(Evidence(
                source="naming_convention",
                detail=convention_issue,
                weight=self.confidence_weights['convention']
            ))
        
        # Calculate final suggestion and confidence
        if suggestions:
            # Sort by confidence
            suggestions.sort(key=lambda x: x[1], reverse=True)
            best_suggestion = suggestions[0][0]
            
            # Apply naming convention
            best_suggestion = self._apply_convention(best_suggestion, target_convention)
            
            # Calculate overall confidence
            total_weight = sum(e.weight for e in evidences)
            confidence = min(total_weight / len(evidences) if evidences else 0, 1.0)
            
            # Determine primary reason
            primary_evidence = max(evidences, key=lambda e: e.weight)
            reason = self._get_reason_from_evidence(primary_evidence)
            
            return AdvancedReviewResult(
                original_name=variable_name,
                suggested_name=best_suggestion,
                reason=reason,
                evidence_term=best_suggestion,
                confidence=confidence,
                evidences=evidences,
                context=context,
                alternative_suggestions=suggestions[1:4]  # Top 3 alternatives
            )
        
        return None
    
    def _check_abbreviations(self, name: str) -> str:
        """Check and expand abbreviations with enhanced logic"""
        common_abbreviations = {
            'usr': 'user', 'pwd': 'password', 'msg': 'message',
            'err': 'error', 'res': 'result', 'req': 'request',
            'resp': 'response', 'cfg': 'config', 'cnt': 'count',
            'amt': 'amount', 'obj': 'object', 'lst': 'list',
            'num': 'number', 'temp': 'temporary', 'val': 'value',
            'idx': 'index', 'btn': 'button', 'img': 'image',
            'src': 'source', 'dest': 'destination', 'dir': 'directory',
            'db': 'database', 'ctx': 'context', 'mgr': 'manager',
            'ctrl': 'controller', 'svc': 'service', 'repo': 'repository',
            'impl': 'implementation', 'util': 'utility', 'helper': 'helper',
            'exc': 'exception', 'env': 'environment', 'conf': 'configuration',
            'auth': 'authentication', 'perm': 'permission', 'admin': 'administrator'
        }
        
        parts = self._split_name_parts(name)
        expanded_parts = []
        
        for part in parts:
            lower_part = part.lower()
            if lower_part in common_abbreviations:
                expanded_parts.append(common_abbreviations[lower_part])
            else:
                expanded_parts.append(part)
        
        return '_'.join(expanded_parts)
    
    def _analyze_by_context(self, name: str, context: ContextInfo) -> Optional[str]:
        """Suggest variable name based on context"""
        # Context-based patterns
        patterns = {
            'parameter': {
                'user': ['user_id', 'username', 'user_data'],
                'data': ['input_data', 'request_data', 'payload'],
                'config': ['configuration', 'settings', 'options']
            },
            'iterator': {
                'item': ['item', 'element', 'entry'],
                'user': ['user', 'account', 'member'],
                'data': ['record', 'row', 'entry']
            },
            'local': {
                'result': ['result', 'response', 'output'],
                'error': ['error', 'exception', 'failure'],
                'temp': ['temporary', 'buffer', 'cache']
            }
        }
        
        # Check if context suggests a better name
        for pattern_key, suggestions in patterns.get(context.usage_type, {}).items():
            if pattern_key in name.lower():
                return suggestions[0]
        
        return None
    
    def _find_similar_terms(self, name: str) -> List[Tuple[str, float]]:
        """Find similar terms in dictionary using fuzzy matching"""
        similar_terms = []
        
        for term_key, entry in self.dictionary.terms.items():
            # Skip if it's a related term entry
            if term_key != entry.term:
                continue
                
            # Calculate similarity
            similarity = difflib.SequenceMatcher(None, name.lower(), 
                                               entry.term.lower()).ratio()
            
            if similarity > 0.6:  # Threshold for similarity
                similar_terms.append((entry.standard_variable_name, similarity))
        
        similar_terms.sort(key=lambda x: x[1], reverse=True)
        return similar_terms
    
    def _check_convention_issues(self, name: str, convention) -> Optional[str]:
        """Check for naming convention issues"""
        if convention == "snake_case" and not re.match(r'^[a-z]+(_[a-z]+)*$', name):
            return f"Does not follow snake_case convention"
        elif convention == "camelCase" and not re.match(r'^[a-z]+([A-Z][a-z]+)*$', name):
            return f"Does not follow camelCase convention"
        return None
    
    def _apply_convention(self, name: str, convention) -> str:
        """Apply naming convention"""
        parts = self._split_name_parts(name)
        
        if convention == "snake_case" or convention.value == "snake_case":
            return '_'.join(part.lower() for part in parts)
        elif convention == "camelCase" or convention.value == "camelCase":
            if not parts:
                return name
            return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
        
        return name
    
    def _split_name_parts(self, name: str) -> List[str]:
        """Split variable name into parts"""
        if '_' in name:
            return name.split('_')
        elif '-' in name:
            return name.split('-')
        else:
            # Handle camelCase/PascalCase
            parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
            return parts if parts else [name]
    
    def _get_reason_from_evidence(self, evidence: Evidence) -> str:
        """Convert evidence to user-friendly reason"""
        reason_map = {
            'terminology_dictionary': '표준 용어사전 불일치',
            'abbreviation_expansion': '의미 없는 약어 사용',
            'context_analysis': '컨텍스트 기반 개선 제안',
            'similarity_matching': '유사 표준 용어 존재',
            'naming_convention': '명명 규칙 불일치'
        }
        return reason_map.get(evidence.source, '개선 필요')


class AdvancedCodeReviewer:
    """Enhanced code reviewer with evidence-based analysis"""
    
    def __init__(self, csv_path: str = None):
        from variable_name_standardizer import TerminologyDictionary
        if csv_path is None:
            csv_path = "용어사전.csv"
        self.dictionary = TerminologyDictionary(csv_path)
        self.analyzer = EvidenceBasedAnalyzer(self.dictionary)
    
    def review_with_evidence(self, code: str) -> List[AdvancedReviewResult]:
        """Review code with detailed evidence"""
        # Analyze code context
        context = CodeContext(code)
        
        # Detect naming convention
        from variable_name_standardizer import NamingConvention
        convention = self._detect_convention(code)
        
        results = []
        for var_name, var_context in context.variables.items():
            result = self.analyzer.analyze_with_evidence(
                var_name, var_context, convention
            )
            if result:
                results.append(result)
        
        return results
    
    def _detect_convention(self, code: str):
        """Detect naming convention"""
        from variable_name_standardizer import NamingConvention
        
        snake_count = len(re.findall(r'\b[a-z]+(_[a-z]+)+\b', code))
        camel_count = len(re.findall(r'\b[a-z]+([A-Z][a-z]+)+\b', code))
        
        if snake_count > camel_count:
            return NamingConvention.SNAKE_CASE
        else:
            return NamingConvention.CAMEL_CASE
    
    def format_detailed_results(self, results: List[AdvancedReviewResult]) -> str:
        """Format results with detailed evidence"""
        if not results:
            return "모든 변수명이 표준을 준수합니다."
        
        output = []
        for result in results:
            # Main suggestion
            output.append(f"\n{'='*60}")
            output.append(f"변수: {result.original_name} → {result.suggested_name}")
            output.append(f"이유: {result.reason} (신뢰도: {result.confidence:.0%})")
            output.append(f"컨텍스트: {result.context.scope} ({result.context.usage_type})")
            
            # Evidence details
            output.append("\n근거:")
            for evidence in sorted(result.evidences, key=lambda e: e.weight, reverse=True):
                output.append(f"  - {evidence.detail} (가중치: {evidence.weight:.2f})")
            
            # Alternative suggestions
            if result.alternative_suggestions:
                output.append("\n대안:")
                for alt_name, alt_conf in result.alternative_suggestions:
                    output.append(f"  - {alt_name} (신뢰도: {alt_conf:.0%})")
        
        return '\n'.join(output)


# Example usage
if __name__ == "__main__":
    reviewer = AdvancedCodeReviewer()
    
    sample_code = """
    def validate_usr_data(usr_id, pwd):
        res = None
        err_msg = ""
        cnt = 0
        
        try:
            사용자정보 = get_user_info(usr_id)
            if 사용자정보:
                res = check_pwd(pwd, 사용자정보)
                cnt += 1
        except Exception as e:
            err_msg = str(e)
        
        return res, err_msg, cnt
    """
    
    results = reviewer.review_with_evidence(sample_code)
    print(reviewer.format_detailed_results(results))