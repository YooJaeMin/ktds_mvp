# 🚀 RFP 분석 및 제안서 지원 플랫폼

> Azure Open AI GPT-4.1를 활용한 스마트 RFP 분석 솔루션

---
✅ 테스트용 url : https://rfp-analysis-jm3-gfh0d2ath5dde5be.koreacentral-01.azurewebsites.net/

## 📋 목차
- [프로젝트 개요](#-프로젝트-개요)
- [핵심 기능](#-핵심-기능)
- [기술 스택](#-기술-스택)
- [시스템 아키텍처](#-시스템-아키텍처)
- [빠른 시작](#-빠른-시작)
- [프로젝트 구조](#-프로젝트-구조)

---

## 🎯 프로젝트 개요

**RFP 분석 플랫폼**은 제안서 작성 과정에서 AI 에이전트를 활용하여 생산성을 향상시키는 도구입니다.

### 해결하는 문제
❌ RFP 분석에 오랜 소요
❌ 요구사항 누락
❌ 과거 자료 활용 어려움

### 제공하는 가치
- **분석 시간 절감**: 자동 분석
- **사업이해도 향상**: 비즈니스 인사이트 제공
- **검색 개선**: RAG 기반 지식 검색
- **품질 개선**: AI 기반 요구사항 매핑

---

## 🎨 핵심 기능

### 1️⃣ 📊 RFP 자동 분석
```
📄 PDF/Word RFP 업로드 → AI 자동 분석 → Word 결과 생성
```

**분석 결과물:**
- ✅ **핵심 요약**: 프로젝트 개요, 예산, 일정
- ✅ **요구사항 추출**: 기능/비기능 요구사항 자동 분류
- ✅ **제약사항 체크리스트**: 준수해야 할 사항 목록화

**스마트 기능:**
- 🔄 재분석 기능: 저장된 RFP 다시 분석
- 📁 한글명 관리: "rfp20241001_123456" → "한국은행 전자계약시스템 구축"
- 💾 자동 저장: Azure Blob Storage에 분석 결과 저장

### 2️⃣ 💡 비즈니스 인사이트 생성
```
업종 + 비즈니스 특성 입력 → AI 인사이트 생성
```

**제공 인사이트:**
- 📈 **업계 트렌드 분석**: 최신 산업 동향
- 🎯 **차별화 전략**: 경쟁력 있는 제안 방향
- 📝 **스토리라인 자동 생성**: 설득력 있는 제안 구조

### 3️⃣ 🛠️ 제안서 품질 관리
```
RFP + 제안서 업로드 → 자동 매핑 및 검증
```

**품질 관리 항목:**
- ✅ 요구사항 매핑: RFP 요구사항 vs 제안서 내용 매칭
- ⚠️ 누락 항목 감지: 미달성 요구사항 자동 발견


### 14️⃣ 🔍 지식기반 검색 (RAG 챗봇)
```
💡 과거 제안서를 학습한 AI 어시스턴트
- Azure AI Search를 통한 의미 기반 검색
- GPT-4.1 기반 맥락 이해 및 답변 생성
- 쿼리 자동 개선 (예: "한국은행 관련 자료" → "한국은행 전자계약시스템 RFP 분석")
```

**주요 특징:**
- 📚 내부 지식 베이스 + 웹 검색 통합
- 🧠 AI 쿼리 개선으로 검색 정확도 향상
- 📊 검색 결과 투명성 (점수, 출처 표시)

---


## 🏗️ 기술 스택

### Frontend
- **Streamlit**: 빠른 웹 UI 구축
- **Python**: 백엔드 로직

### Backend & AI
- **Azure OpenAI (GPT-4.1)**: 
- **Azure AI Search**: 
- **Azure Blob Storage**: 

### Document Processing
- **PyPDF2 / pdfplumber**: PDF 추출
- **python-docx**: Word 문서 생성/편집

---

## 🔧 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                     │
├─────────────────────────────────────────────────────────┤
│  🏠 메인  │ 📊 RFP 분석 │ 💡 인사이트 │ 🛠️ 품질관리  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                     Python Backend                      │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│Azure OpenAI        │ AI Search              │   Blob    │
│   GPT-4.1          │                        │   Storage │
└─────────────────────────────────────────────────────────┘
```

### 데이터 흐름
1. **사용자 입력** → Streamlit UI
2. **문서 업로드** → Azure Blob Storage
3. **텍스트 추출** → Python (PyPDF2/pdfplumber)
4. **AI 분석** → Azure OpenAI (GPT-4.1)
5. **검색 쿼리** → Azure AI Search
6. **결과 저장** → Azure Blob Storage

---

## 🚀 빠른 시작

### 1️⃣ 사전 요구사항
- Python 3.11+
- Azure 구독 (OpenAI, AI Search, Blob Storage)
- Git

### 2️⃣ 설치

```bash
# 저장소 클론
git clone https://github.com/your-repo/ktds_mvp.git
cd ktds_mvp

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3️⃣ 환경 변수 설정

`.env` 파일 생성:

```env
# Azure Storage
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_storage_key
AZURE_STORAGE_CONNECTION_STRING=your_connection_string

# Azure AI Search
AZURE_SEARCH_SERVICE_NAME=your_search_service
AZURE_SEARCH_ADMIN_KEY=your_search_key
AZURE_SEARCH_INDEX_NAME=rfp-documents

# Azure OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2023-12-01-preview
OPENAI_API_TYPE=azure


### 4️⃣ Azure 서비스 초기화

```bash
# Azure 리소스 자동 설정
python setup_azure.py
```

이 스크립트는 다음을 수행합니다:
- ✅ Blob Storage 컨테이너 생성 (rfp-documents, analysis-results, proposals)
- ✅ AI Search 인덱스 생성 
- ✅ 환경 변수 검증

### 5️⃣ 애플리케이션 실행

```bash
streamlit run app.py
```
---

## 📂 프로젝트 구조

```
ktds_mvp/
├── app.py                      # 메인 애플리케이션
├── config.py                   # 환경 변수 관리
├── azure_services.py           # Azure 서비스 통합
├── setup_azure.py              # Azure 초기 설정 스크립트
├── requirements.txt            # Python 의존성
├── .env                        # 환경 변수 (gitignore)
├── .gitignore                  # Git 제외 파일
├── README.md                   # 프로젝트 문서
│
└── modules/                    # 기능 모듈
    ├── __init__.py
    ├── main_page.py            # 메인 페이지
    ├── chatbot.py              # 지식기반 검색 챗봇
    ├── rfp_analysis.py         # RFP 분석 기능
    ├── business_insight.py     # 비즈니스 인사이트
    ├── proposal_quality.py     # 제안서 품질 관리
    ├── performance.py          # 성능 최적화 (캐싱)
    └── styles.py               # UI 스타일
```

*Last Updated: 2025-09-30*