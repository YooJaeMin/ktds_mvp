"""
애플리케이션 스타일 정의
"""
import streamlit as st

def load_main_styles():
    """메인 애플리케이션 스타일 로드"""
    st.markdown("""
    <style>
    .main .block-container {
        padding: 2rem 2.5rem;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1.25rem 2rem 1.25rem;
    }

    /* 사이드바 라디오 그룹을 카드처럼 */
    div[data-testid="stSidebar"] [data-testid="stRadio"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 0.9rem 0.85rem;
        box-shadow: 0 16px 30px rgba(15, 23, 42, 0.08);
    }

    div[data-testid="stSidebar"] [data-testid="stRadio"] legend {
        display: none;
    }

    div[data-testid="stSidebar"] [data-testid="stRadio"] > div:nth-child(2) {
        gap: 0.5rem;
    }

    div[data-testid="stSidebar"] label[data-baseweb="radio"] {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.75rem 0.85rem;
        border-radius: 12px;
        border: 1px solid transparent;
        background: white;
        color: #1f2937;
        font-weight: 600;
        letter-spacing: 0.01em;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        position: relative;
    }

    div[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        border-color: #c7d2fe;
        box-shadow: 0 10px 22px rgba(59, 130, 246, 0.15);
        transform: translateY(-1px);
    }

    div[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] {
        background: linear-gradient(135deg, #4f46e5, #2563eb);
        color: #ffffff;
        border-color: transparent;
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.35);
    }

    div[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
        display: none;
    }

    div[data-testid="stSidebar"] label[data-baseweb="radio"] > div:last-child {
        width: 100%;
    }

    h1 {
        color: #1f2937;
    }

    h2, h3, h4, h5, h6 {
        color: #1f2937;
    }

    .stMarkdown p, .stMarkdown span, .stMarkdown li {
        color: #334155;
    }

    button[kind="primary"], button.st-emotion-cache-7ym5gk {
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1, #2563eb);
        border: none;
        box-shadow: 0 10px 24px rgba(99, 102, 241, 0.25);
    }

    button[kind="secondary"] {
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)