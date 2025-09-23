# KTDS MVP - AI 기반 금융사업 전략 서비스

Microsoft Azure AI 기술을 활용한 IT 기업의 대외 금융사업 수주 전략 지원 플랫폼

## 📋 개요

이 MVP는 IT 기업이 금융권 사업을 수주할 때 필요한 다음 4가지 핵심 업무를 AI로 자동화하여 지원합니다:

1. **RFP 분석 자동화** - RFP 문서를 자동 분석하여 요구사항과 위험도 평가
2. **사업 이해 & 전략 지원** - 시장 분석과 전략적 권고사항 제공
3. **제안서 품질 관리** - 제안서 품질 자동 평가 및 개선사항 제안
4. **지식 관리** - 과거 제안서와 사업 자료의 체계적 관리 및 검색

## 🚀 주요 기능

### 1. RFP 분석 자동화
- PDF, DOC, DOCX 파일 업로드 지원
- 주요 요구사항 자동 추출
- 기술 사양 분석
- 프로젝트 일정 및 예산 정보 파악
- 위험도 자동 평가
- 컴플라이언스 요구사항 식별

### 2. 사업 이해 & 전략 지원
- 산업별 시장 동향 분석
- 고객 특성 분석
- 경쟁 환경 분석
- 전략적 권고사항 생성
- 성공 요인 및 도전과제 식별
- 최적 접근법 제안

### 3. 제안서 품질 관리
- 제안서 전체 품질 점수 (100점 만점)
- 섹션별 상세 점수 (사업이해, 기술솔루션, 수행방법론 등)
- 내용 품질 다각도 평가 (논리성, 전문성, 구체성 등)
- 컴플라이언스 체크
- 강점/약점 분석
- 구체적 개선사항 제안

### 4. 지식 관리
- 문서 업로드 및 자동 인덱싱
- 카테고리별 분류 (제안서, 기술문서, 계약서 등)
- 지능형 검색 기능
- 키워드 자동 추출
- 관련도 기반 검색 결과 정렬

## 🛠 기술 스택

- **Backend**: Python 3.8+, FastAPI
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **AI Services**: Azure OpenAI, Azure Document Intelligence, Azure Text Analytics
- **Database**: SQLite (Knowledge Base)
- **Document Processing**: PyPDF2, python-docx
- **Deployment**: Uvicorn

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/YooJaeMin/ktds_mvp.git
cd ktds_mvp
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 Azure 서비스 정보를 설정합니다:

```bash
cp .env.example .env
# .env 파일을 편집하여 Azure 서비스 정보 입력
```

### 5. 애플리케이션 실행
```bash
python run.py
```

또는 직접 실행:
```bash
python main.py
```

### 6. 웹 브라우저에서 접속
- 메인 애플리케이션: http://localhost:8000
- API 문서: http://localhost:8000/docs

## ⚙️ 설정

### Azure 서비스 설정 (선택사항)

Azure AI 서비스를 사용하려면 다음 서비스들이 필요합니다:

1. **Azure OpenAI Service**
   - GPT-4 모델 배포
   - API 키 및 엔드포인트 설정

2. **Azure Document Intelligence**
   - 문서 구조 분석용
   - API 키 및 엔드포인트 설정

3. **Azure Text Analytics**
   - 감정 분석 및 키워드 추출용
   - API 키 및 엔드포인트 설정

4. **Azure Storage Account** (선택사항)
   - 대용량 파일 저장용

### 환경 변수 설명

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key
AZURE_OPENAI_API_VERSION=2023-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Azure Document Intelligence
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-doc-intelligence.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-document-intelligence-key

# Azure Text Analytics
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-text-analytics.cognitiveservices.azure.com/
AZURE_TEXT_ANALYTICS_KEY=your-text-analytics-key

# Azure Storage (선택사항)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...

# 애플리케이션 설정
DEBUG=True
HOST=localhost
PORT=8000
```

## 📖 사용법

### 1. RFP 분석
1. 'RFP 분석' 메뉴 선택
2. RFP 문서 파일 업로드 (PDF, DOC, DOCX 지원)
3. '분석 시작' 버튼 클릭
4. 분석 결과 확인 (요구사항, 기술사양, 위험도 등)

### 2. 전략 분석
1. '전략 지원' 메뉴 선택
2. 산업 분야 선택
3. 고객 정보 및 프로젝트 범위 입력
4. 전략 분석 결과 확인

### 3. 제안서 품질 평가
1. '품질 관리' 메뉴 선택
2. 제안서 파일 업로드
3. 품질 평가 결과 및 개선사항 확인

### 4. 지식 관리
1. '지식 관리' 메뉴 선택
2. 문서 검색 또는 새 문서 업로드
3. 카테고리별 분류 및 검색 활용

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest tests/

# 커버리지 포함 테스트
pytest --cov=app tests/
```

## 📁 프로젝트 구조

```
ktds_mvp/
├── app/
│   ├── services/           # 핵심 AI 서비스
│   │   ├── rfp_analyzer.py
│   │   ├── strategy_support.py
│   │   ├── quality_manager.py
│   │   └── knowledge_manager.py
│   ├── utils/              # 유틸리티
│   │   ├── azure_client.py
│   │   └── document_utils.py
│   ├── models/             # 데이터 모델
│   │   └── schemas.py
│   ├── templates/          # HTML 템플릿
│   └── static/             # 정적 파일 (CSS, JS)
├── tests/                  # 테스트 파일
├── knowledge_base/         # 지식 베이스 저장소
├── uploads/               # 업로드된 파일
├── main.py               # FastAPI 애플리케이션
├── run.py                # 실행 스크립트
├── requirements.txt      # Python 의존성
└── README.md
```

## 🤝 기여

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🆘 지원

문제가 발생하거나 질문이 있으시면 GitHub Issues를 통해 문의해 주세요.

## 🚀 향후 계획

- [ ] 실시간 협업 기능
- [ ] 다국어 지원
- [ ] 모바일 앱 개발
- [ ] 고급 AI 모델 통합
- [ ] 엔터프라이즈 보안 강화