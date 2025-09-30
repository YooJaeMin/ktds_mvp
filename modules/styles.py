import streamlit as st

def load_main_styles():
    """메인 스타일 로드 (기존 함수명 호환성 유지)"""
    apply_custom_styles()

def apply_custom_styles():
    """커스텀 스타일 적용"""
    st.markdown("""
    <style>
    /* 전체 페이지 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 카드 스타일 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* 스크롤 컨테이너 스타일 */
    .scrollable-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #fafafa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 스크롤바 스타일링 */
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* 텍스트 가독성 개선 */
    .scrollable-container h1,
    .scrollable-container h2,
    .scrollable-container h3 {
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .scrollable-container ul,
    .scrollable-container ol {
        margin-left: 20px;
        line-height: 1.6;
    }
    
    .scrollable-container li {
        margin-bottom: 8px;
    }
    
    /* 강조 텍스트 스타일 */
    .scrollable-container strong {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* 코드 블록 스타일 */
    .scrollable-container code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    /* 성공/에러 메시지 스타일 */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* 로딩 스피너 스타일 */
    .stSpinner {
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

def add_scrollable_container_styles():
    """스크롤 가능한 컨테이너를 위한 CSS 스타일 추가"""
    st.markdown("""
    <style>
    /* 스크롤 컨테이너 스타일 */
    .scrollable-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #fafafa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 스크롤바 스타일링 */
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* 텍스트 가독성 개선 */
    .scrollable-container h1,
    .scrollable-container h2,
    .scrollable-container h3 {
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .scrollable-container ul,
    .scrollable-container ol {
        margin-left: 20px;
        line-height: 1.6;
    }
    
    .scrollable-container li {
        margin-bottom: 8px;
    }
    
    /* 강조 텍스트 스타일 */
    .scrollable-container strong {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* 코드 블록 스타일 */
    .scrollable-container code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)