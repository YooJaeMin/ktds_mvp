"""
RFP 분석 및 제안서 지원 플랫폼 메인 애플리케이션
"""
import streamlit as st
from azure_services import AzureServices
from modules import main_page, rfp_analysis, business_insight, proposal_quality, chatbot, styles

# 페이지 설정
st.set_page_config(
    page_title="RFP 분석 플랫폼",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """메인 애플리케이션 함수"""
    
    # 세션 상태 초기화
    if 'azure_services' not in st.session_state:
        st.session_state.azure_services = AzureServices()
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "메인"
    
    # 챗봇 초기화
    try:
        chatbot.initialize_chatbot()
    except Exception as e:
        st.error(f"챗봇 초기화 오류: {str(e)}")
    
    # 스타일 로드
    try:
        styles.load_main_styles()
    except Exception as e:
        st.error(f"스타일 로드 오류: {str(e)}")
    
    # 기본 레이아웃으로 시작 (안전한 방식)
    st.title("📋 RFP 분석 플랫폼")
    
    # 사이드바 네비게이션
    nav_options = [
        "메인",
        "RFP 분석",
        "비즈니스 인사이트 향상",
        "제안서 품질 관리",
        "지식기반 검색"
    ]

    nav_labels = {
        "메인": "🏠 메인",
        "RFP 분석": "📊 RFP 분석",
        "비즈니스 인사이트 향상": "💡 비즈니스 인사이트 향상",
        "제안서 품질 관리": "🛠️ 제안서 품질 관리",
        "지식기반 검색": "🔍 지식기반 검색"
    }

    with st.sidebar:
        st.markdown("### 메뉴 선택")
        page = st.radio(
            "페이지",
            nav_options,
            index=nav_options.index(st.session_state.current_page),
            label_visibility="collapsed",
            format_func=lambda option: nav_labels.get(option, option)
        )
        st.session_state.current_page = page
    
    # 메인 콘텐츠 영역
    if page == "메인":
        main_page.show()
    elif page == "RFP 분석":
        rfp_analysis.show()
    elif page == "비즈니스 인사이트 향상":
        business_insight.show()
    elif page == "제안서 품질 관리":
        proposal_quality.show()
    elif page == "지식기반 검색":
        chatbot.show_chatbot_panel()

if __name__ == "__main__":
    main()

