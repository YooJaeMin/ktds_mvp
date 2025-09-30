"""
지식 기반 챗봇 모듈
"""
import streamlit as st
from datetime import datetime

def initialize_chatbot():
    """챗봇 초기화"""
    if 'chatbot_messages' not in st.session_state:
        st.session_state.chatbot_messages = []
    
    if 'chatbot_expanded' not in st.session_state:
        st.session_state.chatbot_expanded = True

def search_knowledge_base(query, azure_services):
    """Azure AI Search를 통한 지식 베이스 검색"""
    try:
        # Azure AI Search 검색 (실제 구현은 Azure 서비스에 따라 조정 필요)
        search_results = azure_services.search_knowledge_base(query)
        return search_results
    except Exception as e:
        st.error(f"지식 베이스 검색 중 오류: {str(e)}")
        return []

def search_web(query, azure_services):
    """웹 검색 기능"""
    try:
        # Azure OpenAI의 웹 검색 기능 사용
        web_results = azure_services.search_web(query)
        return web_results
    except Exception as e:
        st.error(f"웹 검색 중 오류: {str(e)}")
        return []

def analyze_query_intent(query, azure_services):
    """사용자 쿼리의 의도를 분석하고 개선된 쿼리를 제안"""
    try:
        messages = [
            {
                "role": "system",
                "content": """당신은 RFP 분석 및 제안서 작성 전문가입니다. 
                사용자의 질문을 분석하여 다음을 수행하세요:
                1. 질문의 의도와 핵심 키워드를 파악
                2. RFP/제안서 도메인에 맞게 더 구체적이고 효과적인 검색 쿼리로 개선
                3. JSON 형태로 응답 (original_query, intent, improved_query, keywords 포함)
                
                응답 형식:
                {
                    "original_query": "원본 질문",
                    "intent": "질문의 의도 (예: RFP 분석 방법론, 제안서 구조, 비즈니스 전략 등)",
                    "improved_query": "개선된 검색 쿼리",
                    "keywords": ["핵심", "키워드", "목록"]
                }"""
            },
            {
                "role": "user",
                "content": f"다음 질문을 분석해주세요: {query}"
            }
        ]
        
        response = azure_services.call_openai(messages)
        
        # JSON 파싱 시도
        import json
        try:
            query_analysis = json.loads(response)
            return query_analysis
        except:
            # JSON 파싱 실패시 기본값 반환
            return {
                "original_query": query,
                "intent": "일반 질문",
                "improved_query": query,
                "keywords": [query]
            }
            
    except Exception as e:
        return {
            "original_query": query,
            "intent": "분석 실패",
            "improved_query": query,
            "keywords": [query]
        }

def _format_search_results_for_prompt(query, enhanced_query, kb_results, web_results):
    """검색 결과를 프롬프트용으로 포맷팅"""
    # 지식 베이스 결과 포맷팅 (상세하게)
    kb_formatted = ""
    if kb_results:
        kb_formatted = "=== 📚 지식 베이스 검색 결과 (우선 참조) ===\n"
        for i, result in enumerate(kb_results, 1):
            kb_formatted += f"\n【문서 {i}】\n"
            kb_formatted += f"📄 파일명: {result.get('title', '제목 없음')}\n"
            kb_formatted += f"🏢 고객사: {result.get('client_name', '정보 없음')}\n"
            kb_formatted += f"📁 위치: {result.get('container_name', '정보 없음')}\n"
            kb_formatted += f"⭐ 관련도: {result.get('score', 0):.2f}\n"
            kb_formatted += f"📝 상세 내용: {result.get('content', '')[:1000]}\n"  # 더 많은 내용
            if len(result.get('content', '')) > 1000:
                kb_formatted += "...\n"
    else:
        kb_formatted = "=== 📚 지식 베이스 검색 결과 ===\n지식 베이스에서 관련 정보를 찾을 수 없습니다."
    
    # 웹 검색 결과 포맷팅
    web_formatted = ""
    if web_results:
        web_formatted = "=== 🌐 웹 검색 결과 (참고용) ===\n"
        # web_results가 리스트인지 문자열인지 확인
        if isinstance(web_results, list):
            for i, result in enumerate(web_results, 1):
                web_formatted += f"\n【웹 결과 {i}】\n"
                if isinstance(result, dict):
                    web_formatted += f"제목: {result.get('title', '제목 없음')}\n"
                    web_formatted += f"요약: {result.get('snippet', result.get('content', '내용 없음'))}\n"
                    web_formatted += f"URL: {result.get('url', 'URL 없음')}\n"
                else:
                    web_formatted += f"{str(result)}\n"
        else:
            try:
                web_formatted += f"{web_results}\n"
            except Exception:
                web_formatted += "웹 검색 결과를 처리할 수 없습니다.\n"
    else:
        web_formatted = "=== 🌐 웹 검색 결과 ===\n웹에서 관련 정보를 찾을 수 없습니다."
    
    return f"""
    원본 질문: {query}
    {f"개선된 검색 쿼리: {enhanced_query}" if enhanced_query != query else ""}
    
    {kb_formatted}
    
    {web_formatted}
    
    위 정보를 바탕으로 답변을 구성해주세요. 지식 베이스 결과를 우선적으로 활용하고, 웹 검색 결과는 보조적으로 참고해주세요.
    """

def generate_chatbot_response(query, azure_services, use_enhanced_query=True):
    """챗봇 응답 생성"""
    try:
        enhanced_query = query
        query_analysis = None
        
        # 쿼리 개선 기능 사용
        if use_enhanced_query:
            query_analysis = analyze_query_intent(query, azure_services)
            enhanced_query = query_analysis.get('improved_query', query)
            
            # 개선된 쿼리 표시
            if enhanced_query != query:
                st.info(f"🔍 **개선된 검색 쿼리**: {enhanced_query}")
                st.info(f"💡 **질문 의도**: {query_analysis.get('intent', '분석 중')}")
                if query_analysis.get('keywords'):
                    st.info(f"🏷️ **핵심 키워드**: {', '.join(query_analysis['keywords'])}")
        
        # 지식 베이스 검색 (개선된 쿼리 사용)
        kb_results = search_knowledge_base(enhanced_query, azure_services)
        
        # 웹 검색 (개선된 쿼리 사용)
        web_results = search_web(enhanced_query, azure_services)
        
        # 검색 결과 디버깅 정보 (더 상세하게)
        if kb_results:
            st.success(f"📚 지식 베이스에서 {len(kb_results)}개의 관련 문서를 찾았습니다.")
            
        else:
            st.warning("📚 지식 베이스에서 관련 문서를 찾을 수 없습니다.")
        
        if web_results:
            # web_results가 리스트인지 문자열인지 확인
            if isinstance(web_results, list):
                st.info(f"🌐 웹에서 {len(web_results)}개의 관련 정보를 찾았습니다.")
            else:
                try:
                    st.info(f"🌐 웹에서 {len(web_results.split('\\n'))}개의 관련 정보를 찾았습니다.")
                except AttributeError:
                    st.info(f"🌐 웹에서 관련 정보를 찾았습니다.")
        else:
            st.warning("🌐 웹에서 관련 정보를 찾을 수 없습니다.")
        
        # 검색 결과를 종합하여 응답 생성
        system_prompt = """당신은 RFP 분석 및 제안서 작성에 도움을 주는 전문 AI 어시스턴트입니다.

        답변 구조:
        1. 📚 지식 베이스 기반 답변 (우선순위)
           - 지식 베이스 검색 결과가 있으면 이를 기반으로 상세한 답변 제공
           - 문서명, 고객사명, 업종 정보를 활용한 맥락 제공
           - 검색 점수가 높은 결과를 우선적으로 활용
           - 관련 문서의 구체적인 내용을 인용하여 답변
        
        2. 🌐 웹 검색 보조 정보 (참고용)
           - 지식 베이스 결과가 부족한 경우에만 웹 검색 결과 활용
           - 최신 정보나 일반적인 지식이 필요한 경우에만 참조
        
        3. 답변 형식:
           - 한국어로 작성
           - 구체적이고 실용적인 조언 제공
           - 정보 출처를 명확히 구분하여 표시
           - 지식 베이스 정보는 "📚 내부 문서"로, 웹 정보는 "🌐 웹 참조"로 표시"""
        
        if query_analysis:
            system_prompt += f"\n\n질문 분석 결과:\n- 의도: {query_analysis.get('intent')}\n- 핵심 키워드: {', '.join(query_analysis.get('keywords', []))}"
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": _format_search_results_for_prompt(query, enhanced_query, kb_results, web_results)
            }
        ]
        
        response = azure_services.call_openai(messages)
        return response
        
    except Exception as e:
        return f"죄송합니다. 응답을 생성하는 중 오류가 발생했습니다: {str(e)}"

def show_chatbot_panel():
    """지식기반 검색 화면"""
    st.title("🔍 지식기반 검색")
    st.markdown("RFP 분석 및 제안서 작성에 도움을 주는 AI 어시스턴트입니다.")
    
    # 검색 기능 소개
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📚 검색 기능
        - **Azure AI Search**: 내부 지식 베이스 검색
        - **웹 검색**: 최신 정보 검색
        - **AI 분석**: 종합적인 답변 제공
        """)
    
    with col2:
        st.markdown("""
        ### 💡 활용 방법
        - RFP 분석 방법 문의
        - 제안서 작성 팁 요청
        - 비즈니스 인사이트 생성 문의
        - 품질 관리 방법 문의
        """)
    
    st.markdown("---")
    
    # 검색 입력
    st.markdown("### 🔍 질문하기")
    
    # 쿼리 개선 옵션
    col_option, col_spacer = st.columns([3, 1])
    with col_option:
        use_query_enhancement = st.checkbox(
            "🧠 AI 쿼리 개선 사용", 
            value=True,
            help="AI가 질문을 분석하여 더 효과적인 검색 쿼리로 개선합니다"
        )
    
    # 검색 실행 함수
    def execute_search():
        user_input = st.session_state.get('chatbot_input', '')
        if user_input and user_input.strip():
            # 사용자 메시지 추가
            st.session_state.chatbot_messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # 챗봇 응답 생성
            with st.spinner("🔍 질문을 분석하고 검색하고 있습니다..."):
                response = generate_chatbot_response(
                    user_input, 
                    st.session_state.azure_services,
                    use_enhanced_query=use_query_enhancement
                )
            
            # 챗봇 응답 추가
            st.session_state.chatbot_messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # 입력란 클리어를 위한 플래그 설정
            st.session_state.chatbot_input_clear = True
    
    # 입력란 (클리어 기능 포함)
    if hasattr(st.session_state, 'chatbot_input_clear') and st.session_state.chatbot_input_clear:
        user_input = st.text_input(
            "질문을 입력하세요:",
            placeholder="RFP 분석이나 제안서 작성에 대해 질문해보세요...",
            key="chatbot_input",
            value=""
        )
        # 클리어 플래그 리셋
        st.session_state.chatbot_input_clear = False
    else:
        user_input = st.text_input(
            "질문을 입력하세요:",
            placeholder="RFP 분석이나 제안서 작성에 대해 질문해보세요...",
            key="chatbot_input"
        )
    
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        if st.button("🔍 검색", key="chatbot_send", type="primary"):
            execute_search()
            st.rerun()
    
    with col_clear:
        if st.button("🗑️ 대화 초기화", key="chatbot_clear"):
            st.session_state.chatbot_messages = []
            st.rerun()
    
    st.markdown("---")
    
    # 검색 결과 표시
    st.markdown("### 💬 검색 결과")
    
    if st.session_state.chatbot_messages:
        for i, message in enumerate(st.session_state.chatbot_messages[-10:]):  # 최근 10개 메시지 표시
            if message["role"] == "user":
                with st.expander(f"❓ 질문 {i+1}: {message['content'][:50]}...", expanded=False):
                    st.markdown(f"**질문:** {message['content']}")
                    st.markdown(f"**시간:** {message['timestamp']}")
            else:
                with st.expander(f"💡 답변 {i+1}: {message['content'][:50]}...", expanded=True):
                    # 답변 내용을 지식기반과 웹기반으로 구분하여 표시
                    response_content = message['content']
                    
                    # 지식기반 답변 부분 추출 (📚 표시가 있는 부분)
                    kb_sections = []
                    web_sections = []
                    current_section = []
                    current_type = None
                    
                    lines = response_content.split('\n')
                    for line in lines:
                        if '📚' in line and ('내부 문서' in line or '지식 베이스' in line):
                            if current_section and current_type:
                                if current_type == 'kb':
                                    kb_sections.append('\n'.join(current_section))
                                else:
                                    web_sections.append('\n'.join(current_section))
                            current_section = [line]
                            current_type = 'kb'
                        elif '🌐' in line and ('웹 참조' in line or '웹 검색' in line):
                            if current_section and current_type:
                                if current_type == 'kb':
                                    kb_sections.append('\n'.join(current_section))
                                else:
                                    web_sections.append('\n'.join(current_section))
                            current_section = [line]
                            current_type = 'web'
                        else:
                            current_section.append(line)
                    
                    # 마지막 섹션 처리
                    if current_section and current_type:
                        if current_type == 'kb':
                            kb_sections.append('\n'.join(current_section))
                        else:
                            web_sections.append('\n'.join(current_section))
                    
                    # 지식기반 답변 우선 표시
                    if kb_sections:
                        st.markdown("### 📚 지식 베이스 기반 답변")
                        for kb_section in kb_sections:
                            st.markdown(kb_section)
                    
                    # 웹기반 답변 표시
                    if web_sections:
                        st.markdown("### 🌐 웹 검색 보조 정보")
                        for web_section in web_sections:
                            st.markdown(web_section)
                    
                    # 구분이 없는 경우 전체 답변 표시
                    if not kb_sections and not web_sections:
                        st.markdown(f"**답변:** {response_content}")
                    
                    st.markdown(f"**시간:** {message['timestamp']}")
    else:
        st.info("아직 검색한 내용이 없습니다. 위에서 질문을 입력해보세요!")
    
    # 추가 정보
    st.markdown("---")
    st.markdown("### 📖 추가 정보")
    st.markdown("""
    - **지식 베이스**: Azure AI Search를 통한 내부 문서 검색
    - **웹 검색**: OpenAI를 통한 최신 정보 검색
    - **AI 분석**: Azure OpenAI를 통한 종합적인 답변 생성
    - **🧠 AI 쿼리 개선**: 질문 의도를 분석하여 더 효과적인 검색 쿼리로 자동 변환
    """)
    
    # 쿼리 개선 예시
    with st.expander("💡 쿼리 개선 예시"):
        st.markdown("""
        **원본 질문**: "RFP 어떻게 써?"
        **개선된 쿼리**: "RFP 제안서 작성 방법론 구조 템플릿 가이드라인"
        **질문 의도**: 제안서 작성 방법론
        
        **원본 질문**: "경쟁사 분석 좀"
        **개선된 쿼리**: "경쟁사 분석 방법론 시장조사 SWOT 분석 벤치마킹"
        **질문 의도**: 경쟁 분석 방법론
        
        **원본 질문**: "가격 어떻게 정해?"
        **개선된 쿼리**: "제안서 가격 책정 전략 원가 계산 수익성 분석"
        **질문 의도**: 가격 책정 전략
        """)
