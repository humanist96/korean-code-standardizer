"""
AI Chatbot Interface for Code Transformation
Provides conversational interface for code transformation services
"""

import streamlit as st
from datetime import datetime
import json
from typing import List, Dict, Tuple, Optional
import re

from enhanced_code_reviewer import EnhancedCodeReviewer
from terminology_manager import TerminologyManager
from statistics_manager import StatisticsManager, TransformationRecord
from code_examples import CodeExamples


class CodeTransformationChatbot:
    """AI Chatbot for code transformation assistance"""
    
    def __init__(self, terminology_manager: TerminologyManager, stats_manager: StatisticsManager):
        self.terminology_manager = terminology_manager
        self.stats_manager = stats_manager
        self.reviewer = EnhancedCodeReviewer(terminology_manager)
        self.code_examples = CodeExamples()
        
    def process_message(self, message: str) -> Dict[str, any]:
        """Process user message and return response"""
        
        # Analyze message intent
        intent = self._analyze_intent(message)
        
        if intent == "transform_code":
            return self._handle_code_transformation(message)
        elif intent == "show_example":
            return self._handle_show_example(message)
        elif intent == "explain_issue":
            return self._handle_explain_issue(message)
        elif intent == "show_statistics":
            return self._handle_show_statistics()
        elif intent == "search_term":
            return self._handle_search_term(message)
        elif intent == "help":
            return self._handle_help()
        else:
            return self._handle_general_query(message)
    
    def _analyze_intent(self, message: str) -> str:
        """Analyze user message intent"""
        message_lower = message.lower()
        
        # Check if message contains code first
        if "```" in message or self._contains_code_pattern(message):
            return "transform_code"
        
        # Code transformation intent - more flexible detection
        if any(keyword in message_lower for keyword in ["변환", "transform", "분석", "analyze", "수정", "fix", "개선", "improve", "검토", "review"]):
            return "transform_code"
        
        # Example request
        if any(keyword in message_lower for keyword in ["예제", "example", "보여", "show"]):
            return "show_example"
        
        # Explanation request
        if any(keyword in message_lower for keyword in ["설명", "explain", "이유", "why", "무엇", "what"]):
            return "explain_issue"
        
        # Statistics request
        if any(keyword in message_lower for keyword in ["통계", "statistics", "얼마나", "how many"]):
            return "show_statistics"
        
        # Term search
        if any(keyword in message_lower for keyword in ["용어", "term", "찾", "search", "검색"]):
            return "search_term"
        
        # Help request
        if any(keyword in message_lower for keyword in ["도움", "help", "사용법", "how to"]):
            return "help"
        
        return "general"
    
    def _contains_code_pattern(self, message: str) -> bool:
        """Check if message contains code patterns"""
        code_patterns = [
            r'def\s+\w+',
            r'class\s+\w+',
            r'import\s+\w+',
            r'from\s+\w+',
            r'\w+\s*=\s*[\w\'"()]',  # Variable assignment
            r'\w+\s*\([^)]*\)',  # Function call
            r'if\s+.*:',  # If statement
            r'for\s+\w+\s+in',  # For loop
            r'while\s+.*:',  # While loop
            r'return\s+',  # Return statement
            r'print\s*\(',  # Print statement
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def _extract_code_from_message(self, message: str) -> Optional[str]:
        """Extract code from message"""
        # Check for code blocks
        code_block_match = re.search(r'```(?:python)?\n?(.*?)\n?```', message, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # Check for backtick inline code
        inline_code_match = re.search(r'`([^`]+)`', message)
        if inline_code_match and self._contains_code_pattern(inline_code_match.group(1)):
            return inline_code_match.group(1)
        
        # Try to extract code from the entire message
        lines = message.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            # Skip obvious non-code lines
            if line.strip().startswith(('이', '이것', '이거', '여기', '코드', '변환', '분석', '수정')):
                continue
            
            # Check if line looks like code
            if self._contains_code_pattern(line) or in_code_block:
                code_lines.append(line)
                in_code_block = True
            elif in_code_block and line.strip() == '':
                # Empty line in code block
                code_lines.append(line)
            elif in_code_block and not line.strip().startswith(' '):
                # End of code block
                in_code_block = False
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        return None
    
    def _handle_code_transformation(self, message: str) -> Dict[str, any]:
        """Handle code transformation request"""
        code = self._extract_code_from_message(message)
        
        if not code:
            # Provide helpful guidance
            return {
                "type": "help",
                "commands": [
                    {
                        "command": "코드 변환 방법",
                        "description": "다음과 같은 방법으로 코드를 입력해주세요:",
                        "example": "```python\ndef process_usr_data(usr_id):\n    return usr_id\n```"
                    },
                    {
                        "command": "간단한 코드",
                        "description": "한 줄 코드도 분석 가능합니다:",
                        "example": "usr_cnt = len(usr_list)"
                    }
                ]
            }
        
        # Transform code
        result = self.reviewer.review_code(code)
        
        # Record statistics
        record = TransformationRecord(
            timestamp=datetime.now().isoformat(),
            file_name="챗봇 입력",
            file_path="chatbot",
            original_code=code,
            transformed_code=result['improved_code'],
            issues_found=result['issues_count'],
            confidence_score=result['confidence'],
            transformation_details=result['suggestions']
        )
        self.stats_manager.record_transformation(record)
        
        # Format response
        response = {
            "type": "transformation",
            "original_code": code,
            "transformed_code": result['improved_code'],
            "issues_found": result['issues_count'],
            "suggestions": result['suggestions'],
            "confidence": result['confidence']
        }
        
        return response
    
    def _handle_show_example(self, message: str) -> Dict[str, any]:
        """Handle example request"""
        message_lower = message.lower()
        
        # Determine example type
        if "랜덤" in message_lower or "random" in message_lower:
            # Generate random code
            code, description, pattern = self.code_examples.generate_random_code()
            return {
                "type": "example",
                "example_type": "random",
                "code": code,
                "description": description,
                "issues": ["의미 없는 약어 사용", "한글 변수명 사용", "명명 규칙 불일치"]
            }
        elif "약어" in message_lower or "abbreviation" in message_lower:
            examples = self.code_examples.get_examples_by_category("basic")
            example = examples[0] if examples else None
            example_type = "abbreviation"
        else:
            # Default to showing a basic example
            examples = self.code_examples.get_all_examples()
            example = examples[0] if examples else None
            example_type = "basic"
        
        if example:
            return {
                "type": "example",
                "example_type": example_type,
                "code": example["code"],
                "description": example["description"],
                "issues": example["common_issues"]
            }
        else:
            return {
                "type": "error",
                "content": "예제를 찾을 수 없습니다."
            }
    
    def _handle_explain_issue(self, message: str) -> Dict[str, any]:
        """Handle explanation request"""
        explanations = {
            "약어": {
                "title": "의미 없는 약어 사용",
                "description": "코드에서 usr, pwd, msg 같은 약어는 가독성을 떨어뜨립니다.",
                "solution": "명확한 전체 단어를 사용하세요: user, password, message",
                "example": "usr_cnt → user_count"
            },
            "명명규칙": {
                "title": "명명 규칙 불일치",
                "description": "한 프로젝트에서 camelCase와 snake_case를 혼용하면 일관성이 없습니다.",
                "solution": "프로젝트 전체에서 하나의 명명 규칙을 일관되게 사용하세요.",
                "example": "userId (camelCase) → user_id (snake_case)"
            },
            "한글변수": {
                "title": "한글 변수명 사용",
                "description": "한글 변수명은 인코딩 문제와 협업 시 어려움을 일으킬 수 있습니다.",
                "solution": "영문 변수명을 사용하되, 용어사전을 참고하여 표준 용어를 사용하세요.",
                "example": "사용자정보 → user_info"
            }
        }
        
        # Find matching explanation
        for keyword, explanation in explanations.items():
            if keyword in message.lower():
                return {
                    "type": "explanation",
                    "content": explanation
                }
        
        # Default explanation
        return {
            "type": "explanation",
            "content": {
                "title": "코드 변수명 표준화",
                "description": "좋은 변수명은 코드의 가독성과 유지보수성을 크게 향상시킵니다.",
                "solution": "명확하고 일관된 명명 규칙을 사용하고, 약어 대신 전체 단어를 사용하세요.",
                "example": "표준 용어사전을 참고하여 조직 전체에서 일관된 용어를 사용하세요."
            }
        }
    
    def _handle_show_statistics(self) -> Dict[str, any]:
        """Handle statistics request"""
        stats = self.stats_manager.get_summary_stats()
        today_stats = self.stats_manager.get_today_statistics()
        
        return {
            "type": "statistics",
            "total_transformations": stats['total_transformations'],
            "total_changes": stats['total_changes'],
            "average_confidence": stats['average_confidence'],
            "today_files": today_stats['total_files'],
            "today_changes": today_stats['total_changes'],
            "most_common_issue": stats['most_common_issue']
        }
    
    def _handle_search_term(self, message: str) -> Dict[str, any]:
        """Handle term search request"""
        # Extract search term
        search_patterns = [
            r'"([^"]+)"',  # Quoted term
            r'\'([^\']+)\'',  # Single quoted term
            r'검색\s+(\w+)',  # Korean search pattern
            r'search\s+(\w+)',  # English search pattern
            r'찾기\s+(\w+)',  # Korean find pattern
        ]
        
        search_term = None
        for pattern in search_patterns:
            match = re.search(pattern, message)
            if match:
                search_term = match.group(1)
                break
        
        if not search_term:
            # Try to extract the last word as search term
            words = message.split()
            if len(words) > 1:
                search_term = words[-1]
        
        if search_term:
            # Search in terminology
            results = self.terminology_manager.search_terms(search_term)
            
            # Convert Term objects to dictionaries
            term_dicts = []
            for term in results[:5]:  # Limit to 5 results
                term_dict = {
                    'korean': term.korean_name,
                    'english': term.english_name,
                    'abbreviation': term.abbreviation,
                    'category': term.category,
                    'tags': term.tags if hasattr(term, 'tags') else [],
                    'description': term.description if hasattr(term, 'description') else ''
                }
                term_dicts.append(term_dict)
            
            return {
                "type": "term_search",
                "search_term": search_term,
                "results": term_dicts
            }
        
        return {
            "type": "error",
            "content": "검색할 용어를 찾을 수 없습니다. '용어 검색 user' 형식으로 입력해주세요."
        }
    
    def _handle_help(self) -> Dict[str, any]:
        """Handle help request"""
        return {
            "type": "help",
            "commands": [
                {
                    "command": "코드 변환",
                    "description": "Python 코드를 입력하면 변수명을 표준화합니다",
                    "example": "```python\ndef process_usr_data(usr_id):\n    pass\n```"
                },
                {
                    "command": "예제 보기",
                    "description": "변환 예제를 보여줍니다",
                    "example": "예제 보여줘"
                },
                {
                    "command": "용어 검색",
                    "description": "표준 용어사전에서 용어를 검색합니다",
                    "example": "용어 검색 user"
                },
                {
                    "command": "통계 보기",
                    "description": "변환 통계를 보여줍니다",
                    "example": "통계 보여줘"
                },
                {
                    "command": "설명",
                    "description": "특정 이슈에 대한 설명을 보여줍니다",
                    "example": "약어 사용에 대해 설명해줘"
                }
            ]
        }
    
    def _handle_general_query(self, message: str) -> Dict[str, any]:
        """Handle general queries"""
        # Check if user might be trying to input code without proper markers
        if any(char in message for char in ['=', '(', ')', 'def', 'class', 'import']):
            return {
                "type": "general",
                "content": "코드를 입력하신 것 같습니다. 코드 블록을 사용해주세요:\n\n```python\n여기에 코드 입력\n```\n\n또는 '코드 변환' 키워드와 함께 입력해주세요."
            }
        
        return {
            "type": "general",
            "content": "안녕하세요! 저는 코드 변수명 표준화 AI입니다. 🤖\n\n다음과 같이 사용해주세요:\n• Python 코드를 ``` 블록 안에 입력\n• '예제 보여줘'로 예제 확인\n• '통계'로 변환 통계 확인\n• '도움말'로 전체 명령어 확인"
        }


class ChatbotUI:
    """Chatbot UI component"""
    
    def __init__(self, chatbot: CodeTransformationChatbot):
        self.chatbot = chatbot
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for chat"""
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
            # Add welcome message
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "안녕하세요! 코드 변수명 표준화 AI 챗봇입니다. 🤖\n\n" +
                          "Python 코드를 입력하시면 변수명을 분석하고 개선해드립니다.\n" +
                          "도움이 필요하시면 '도움말'을 입력해주세요!",
                "type": "welcome"
            })
    
    def render(self):
        """Render chatbot interface"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Chat header
        col1, col2 = st.columns([6, 1])
        with col1:
            st.subheader("💬 AI 코드 변환 챗봇")
        with col2:
            if st.button("대화 초기화", use_container_width=True):
                st.session_state.chat_messages = []
                self._initialize_session_state()
                st.rerun()
        
        # Chat container
        chat_container = st.container()
        
        # Display chat messages
        with chat_container:
            for message in st.session_state.chat_messages:
                self._render_message(message)
        
        # Chat input
        user_input = st.chat_input("코드를 입력하거나 질문해주세요...")
        
        if user_input:
            # Add user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Process message and get response
            with st.spinner("분석 중..."):
                response = self.chatbot.process_message(user_input)
            
            # Add assistant response
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response,
                "type": response["type"]
            })
            
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### 🚀 빠른 실행")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 예제 코드", use_container_width=True):
                code, description, pattern = self.chatbot.code_examples.generate_random_code()
                user_message = f"이 코드를 변환해줘:\n```python\n{code}\n```"
                
                # Add user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Process and add response
                response = self.chatbot.process_message(user_message)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response,
                    "type": response["type"]
                })
                st.rerun()
        
        with col2:
            if st.button("📊 통계 보기", use_container_width=True):
                user_message = "통계 보여줘"
                
                # Add user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Process and add response
                response = self.chatbot.process_message(user_message)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response,
                    "type": response["type"]
                })
                st.rerun()
        
        with col3:
            if st.button("🔍 용어 검색", use_container_width=True):
                user_message = "용어 검색 방법 알려줘"
                
                # Add user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Process and add response
                response = self.chatbot.process_message(user_message)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response,
                    "type": response["type"]
                })
                st.rerun()
        
        with col4:
            if st.button("❓ 도움말", use_container_width=True):
                user_message = "도움말"
                
                # Add user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Process and add response
                response = self.chatbot.process_message(user_message)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response,
                    "type": response["type"]
                })
                st.rerun()
    
    def _render_message(self, message: Dict):
        """Render a single message"""
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.write(message["content"])
            else:
                # Assistant message
                if isinstance(message["content"], dict):
                    self._render_response(message["content"])
                else:
                    st.write(message["content"])
    
    def _render_response(self, response: Dict):
        """Render different types of responses"""
        response_type = response.get("type", "general")
        
        if response_type == "transformation":
            self._render_transformation_response(response)
        elif response_type == "example":
            self._render_example_response(response)
        elif response_type == "explanation":
            self._render_explanation_response(response)
        elif response_type == "statistics":
            self._render_statistics_response(response)
        elif response_type == "term_search":
            self._render_term_search_response(response)
        elif response_type == "help":
            self._render_help_response(response)
        elif response_type == "error":
            st.error(response["content"])
        else:
            st.write(response.get("content", ""))
    
    def _render_transformation_response(self, response: Dict):
        """Render code transformation response"""
        issues_found = response.get('issues_found', 0)
        st.success(f"✅ {issues_found}개의 개선사항을 발견했습니다!")
        
        # Show transformation details
        suggestions = response.get('suggestions', [])
        if suggestions:
            st.markdown("**발견된 이슈:**")
            for suggestion in suggestions:
                original = suggestion.get('original', '')
                suggested = suggestion.get('suggestion', suggestion.get('suggested', ''))
                reason = suggestion.get('reason', '')
                st.markdown(f"- `{original}` → `{suggested}` ({reason})")
        
        # Show code comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**원본 코드:**")
            original_code = response.get('original_code', '')
            st.code(original_code, language="python")
        
        with col2:
            st.markdown("**개선된 코드:**")
            transformed_code = response.get('transformed_code', '')
            st.code(transformed_code, language="python")
        
        confidence = response.get('confidence', 0)
        if confidence and isinstance(confidence, (int, float)):
            st.info(f"신뢰도: {confidence:.1%}")
        else:
            st.info("신뢰도: N/A")
    
    def _render_example_response(self, response: Dict):
        """Render example response"""
        description = response.get('description', '예제 코드')
        st.markdown(f"**{description}**")
        
        code = response.get('code', '')
        if code:
            st.code(code, language="python")
        
        issues = response.get('issues', [])
        if issues:
            st.markdown("**예상되는 이슈:**")
            for issue in issues:
                st.markdown(f"- {issue}")
    
    def _render_explanation_response(self, response: Dict):
        """Render explanation response"""
        content = response.get('content', {})
        
        if isinstance(content, dict):
            title = content.get('title', '설명')
            st.markdown(f"### {title}")
            
            description = content.get('description', '')
            if description:
                st.write(description)
            
            solution = content.get('solution', '')
            if solution:
                st.info(f"**해결 방법:** {solution}")
            
            example = content.get('example', '')
            if example:
                st.code(example)
        else:
            st.write(content)
    
    def _render_statistics_response(self, response: Dict):
        """Render statistics response"""
        st.markdown("### 📊 변환 통계")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("전체 변환", f"{response.get('total_transformations', 0):,}회")
            st.metric("오늘 변환", f"{response.get('today_files', 0)}개 파일")
        
        with col2:
            st.metric("총 개선사항", f"{response.get('total_changes', 0):,}개")
            st.metric("오늘 개선", f"{response.get('today_changes', 0)}개")
        
        with col3:
            avg_confidence = response.get('average_confidence', 0)
            if avg_confidence and isinstance(avg_confidence, (int, float)):
                st.metric("평균 신뢰도", f"{avg_confidence:.1%}")
            else:
                st.metric("평균 신뢰도", "0.0%")
            
            if response.get('most_common_issue'):
                st.metric("가장 많은 이슈", response['most_common_issue'])
    
    def _render_term_search_response(self, response: Dict):
        """Render term search response"""
        search_term = response.get('search_term', '')
        st.markdown(f"### 🔍 '{search_term}' 검색 결과")
        
        results = response.get('results', [])
        if results:
            for term in results:
                korean = term.get('korean', '')
                english = term.get('english', '')
                
                with st.expander(f"{korean} → {english}"):
                    if term.get('abbreviation'):
                        st.write(f"**약어:** {term['abbreviation']}")
                    if term.get('category'):
                        st.write(f"**카테고리:** {term['category']}")
                    if term.get('tags'):
                        tags = term['tags']
                        if isinstance(tags, list):
                            st.write(f"**태그:** {', '.join(tags)}")
                        else:
                            st.write(f"**태그:** {tags}")
                    if term.get('description'):
                        st.write(f"**설명:** {term['description']}")
        else:
            st.info("검색 결과가 없습니다.")
    
    def _render_help_response(self, response: Dict):
        """Render help response"""
        st.markdown("### ❓ 사용 가능한 명령어")
        
        commands = response.get('commands', [])
        for cmd in commands:
            with st.expander(cmd.get('command', '명령어')):
                st.write(cmd.get('description', ''))
                if cmd.get('example'):
                    st.code(cmd['example'])