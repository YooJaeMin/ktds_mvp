"""
메인 페이지
"""
import streamlit as st

def show():
    """메인 페이지 표시"""
    st.title("📋 RFP 분석 및 제안서 지원 플랫폼")
    st.markdown("---")
    
    # 플랫폼 소개
    st.markdown("""
    ### 🎯 플랫폼 개요
    RFP 분석 및 제안서 지원 플랫폼은 금융 업계의 RFP(Request for Proposal) 문서를 분석하고, 
    효과적인 제안서 작성을 지원하는 AI 기반 플랫폼입니다.
    """)
    
    # 주요 기능
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔍 주요 기능
        - **RFP 문서 분석**: PDF, DOCX, TXT 파일 지원
        - **요구사항 추출**: 기능/비기능 요구사항 자동 분류
        - **키워드 분석**: 핵심 키워드 및 트렌드 분석
        - **구조 분석**: RFP 문서 구조 파악 및 분석
        """)

    with col2:
        st.markdown("""
        #### 📈 고급 기능
        - **비즈니스 인사이트**: 업계 트렌드 및 차별화 전략
        - **제안서 품질 관리**: 품질 검증 및 개선 방안
        - **지식 기반 챗봇**: AI 기반 Q&A 지원
        - **결과 다운로드**: 분석 결과 DOCX 형식 다운로드
        """)

    st.markdown("---")

    # 사용 방법
    st.markdown("### 🚀 사용 방법")
    st.markdown("""
    1. **RFP 분석**: 좌측 사이드바의 'RFP 분석' 페이지에서 문서를 업로드하고 분석하세요.
    2. **비즈니스 인사이트**: '비즈니스 인사이트 향상' 페이지에서 업계 트렌드를 확인하세요.
    3. **제안서 품질 관리**: '제안서 품질 관리' 페이지에서 제안서 품질을 검증하세요.
    4. **결과 활용**: 분석 결과를 다운로드하여 제안서 작성에 활용하세요.
    """)

    # 지원 파일 형식
    st.markdown("### 📄 지원 파일 형식")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📋 RFP 문서**
        - PDF 파일
        - DOCX 파일
        - TXT 파일
        """)

    with col2:
        st.markdown("""
        **📊 분석 결과**
        - 요구사항 추출
        - 키워드 분석
        - 구조 분석
        """)

    with col3:
        st.markdown("""
        **💾 다운로드**
        - DOCX 형식
        - 상세 보고서
        - 요약 보고서
        """)

    # # 플랫폼 정보
    # st.markdown("---")
    # st.markdown("### 📊 플랫폼 정보")
    # st.info("""
    # **주요 특징:**
    # - Azure 기반 클라우드 플랫폼
    # - AI 기반 문서 분석
    # - 실시간 분석 결과 제공
    # - 보안성과 확장성 보장
    # """)

    # # 최근 활동 (샘플)
    # st.markdown("---")
    # st.markdown("### 📈 최근 활동")

    # # 샘플 데이터
    # recent_activities = [
    #     {"날짜": "2025-09-29", "활동": "RFP 문서 분석", "상태": "완료"},
    #     {"날짜": "2025-09-29", "활동": "비즈니스 인사이트 생성", "상태": "진행중"},
    #     {"날짜": "2025-09-28", "활동": "제안서 품질 검증", "상태": "완료"},
    # ]

    # df = st.dataframe(recent_activities, width='stretch')

    # # 통계 정보
    # st.markdown("---")
    # st.markdown("### 📊 플랫폼 통계")

    # col1, col2, col3, col4 = st.columns(4)

    # with col1:
    #     st.metric(
    #         label="분석된 RFP",
    #         value="12",
    #         delta="3"
    #     )

    # with col2:
    #     st.metric(
    #         label="생성된 인사이트",
    #         value="8",
    #         delta="2"
    #     )

    # with col3:
    #     st.metric(
    #         label="품질 검증",
    #         value="15",
    #         delta="5"
    #     )

    # with col4:
    #     st.metric(
    #         label="다운로드",
    #         value="24",
    #         delta="7"
    #     )