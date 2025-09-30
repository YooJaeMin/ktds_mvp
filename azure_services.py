"""
Azure 서비스 연동 모듈
"""
import os
import requests
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
import openai
from config import *

class AzureServices:
    def __init__(self):
        """Azure 서비스 초기화"""
        self.blob_client = None
        self.search_client = None
        self.openai_client = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Azure 서비스들 초기화"""
        try:
            # Blob Storage 클라이언트 초기화
            if AZURE_STORAGE_CONNECTION_STRING:
                self.blob_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
            else:
                credential = DefaultAzureCredential()
                self.blob_client = BlobServiceClient(
                    account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                    credential=credential
                )
            
            # Azure AI Search 클라이언트 초기화
            if AZURE_SEARCH_ADMIN_KEY:
                credential = AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY)
                self.search_client = SearchClient(
                    endpoint=f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net",
                    index_name=AZURE_SEARCH_INDEX_NAME,
                    credential=credential
                )
            
            # OpenAI 클라이언트는 필요시 동적으로 초기화
            if OPENAI_API_KEY and OPENAI_API_BASE:
                self.openai_configured = True
            else:
                self.openai_configured = False
                
        except Exception as e:
            print(f"Azure 서비스 초기화 오류: {e}")
    
    def _get_configuration_error_message(self):
        """OpenAI 설정 오류 메시지 반환"""
        return """
## ⚠️ Azure OpenAI 설정 오류

### 문제 상황
Azure OpenAI API 설정이 완료되지 않았습니다.

### 해결 방법

#### 1. 환경 변수 설정
`.env` 파일에 다음 변수들을 설정해주세요:

```env
# Azure OpenAI 설정
OPENAI_API_KEY=your_azure_openai_api_key
OPENAI_API_BASE=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2023-12-01-preview
OPENAI_API_TYPE=azure
```

#### 2. Azure OpenAI 리소스 확인
- Azure Portal에서 OpenAI 리소스가 생성되어 있는지 확인
- API 키가 유효한지 확인
- 엔드포인트 URL이 정확한지 확인

#### 3. 모델 배포 확인
- Azure OpenAI Studio에서 모델이 배포되어 있는지 확인
- 배포 이름이 올바른지 확인

### 임시 해결책
현재는 샘플 응답을 표시합니다. 
실제 AI 분석을 위해서는 위 설정을 완료해주세요.
"""
    
    def get_containers(self):
        """Blob Storage의 모든 컨테이너 목록 반환"""
        try:
            containers = self.blob_client.list_containers()
            return [container.name for container in containers]
        except Exception as e:
            print(f"컨테이너 목록 조회 오류: {e}")
            return []
    
    def get_directories(self):
        """rfp-documents 컨테이너 내의 RFP 디렉토리 목록 반환"""
        try:
            container_name = "rfp-documents"
            
            # 컨테이너가 존재하지 않으면 생성
            try:
                container_client = self.blob_client.get_container_client(container_name)
                container_client.get_container_properties()
            except Exception:
                print(f"컨테이너 {container_name}이 존재하지 않습니다. 생성 중...")
                self.blob_client.create_container(container_name)
                print(f"컨테이너 {container_name}이 생성되었습니다.")
            
            container_client = self.blob_client.get_container_client(container_name)
            
            # 모든 blob을 조회하여 디렉토리 구조 파악
            blobs = container_client.list_blobs()
            directories = {}
            
            for blob in blobs:
                # 디렉토리 구조: rfp{timestamp}/filename
                if '/' in blob.name:
                    dir_name = blob.name.split('/')[0]
                    if dir_name.startswith('rfp') and dir_name not in directories:
                        # 메타데이터에서 한글명 가져오기
                        metadata = self.get_directory_metadata_from_path(container_name, dir_name)
                        directories[dir_name] = {
                            'name': dir_name,
                            'korean_name': metadata.get('korean_name', dir_name),
                            'created_date': metadata.get('created_date', ''),
                            'project_summary': metadata.get('project_summary', '')
                        }
            
            return list(directories.values())
        except Exception as e:
            print(f"디렉토리 목록 조회 오류: {e}")
            return []
    
    def get_directory_metadata(self, directory_name):
        """디렉토리 메타데이터 조회 (기존 방식 - 컨테이너별)"""
        try:
            # metadata.json 파일에서 메타데이터 읽기
            blob_client = self.blob_client.get_blob_client(
                container=directory_name,
                blob='metadata.json'
            )
            if blob_client.exists():
                metadata_content = blob_client.download_blob().readall()
                import json
                return json.loads(metadata_content.decode('utf-8'))
            return {}
        except Exception as e:
            print(f"메타데이터 조회 오류: {e}")
            return {}
    
    def get_directory_metadata_from_path(self, container_name, directory_name):
        """rfp-documents 컨테이너 내 디렉토리 메타데이터 조회"""
        try:
            # metadata.json 파일에서 메타데이터 읽기
            blob_client = self.blob_client.get_blob_client(
                container=container_name,
                blob=f'{directory_name}/metadata.json'
            )
            if blob_client.exists():
                metadata_content = blob_client.download_blob().readall()
                import json
                return json.loads(metadata_content.decode('utf-8'))
            return {}
        except Exception as e:
            print(f"메타데이터 조회 오류: {e}")
            return {}
    
    def save_directory_metadata(self, directory_name, metadata):
        """디렉토리 메타데이터 저장 (기존 방식 - 컨테이너별)"""
        try:
            import json
            metadata_json = json.dumps(metadata, ensure_ascii=False, indent=2)
            blob_client = self.blob_client.get_blob_client(
                container=directory_name,
                blob='metadata.json'
            )
            blob_client.upload_blob(metadata_json.encode('utf-8'), overwrite=True)
            return True
        except Exception as e:
            print(f"메타데이터 저장 오류: {e}")
            return False
    
    def save_directory_metadata_to_path(self, container_name, directory_name, metadata):
        """rfp-documents 컨테이너 내 디렉토리 메타데이터 저장"""
        try:
            import json
            metadata_json = json.dumps(metadata, ensure_ascii=False, indent=2)
            blob_client = self.blob_client.get_blob_client(
                container=container_name,
                blob=f'{directory_name}/metadata.json'
            )
            blob_client.upload_blob(metadata_json.encode('utf-8'), overwrite=True)
            return True
        except Exception as e:
            print(f"메타데이터 저장 오류: {e}")
            return False
    
    def create_container(self, container_name):
        """새 컨테이너 생성"""
        try:
            self.blob_client.create_container(container_name)
            return True
        except Exception as e:
            print(f"컨테이너 생성 오류: {e}")
            return False
    
    def upload_file(self, container_name, file_name, file_data):
        """파일을 Blob Storage에 업로드"""
        try:
            blob_client = self.blob_client.get_blob_client(
                container=container_name, 
                blob=file_name
            )
            blob_client.upload_blob(file_data, overwrite=True)
            return True
        except Exception as e:
            print(f"파일 업로드 오류: {e}")
            return False
    
    def upload_file_to_directory(self, container_name, directory_name, file_name, file_data):
        """rfp-documents 컨테이너 내 디렉토리에 파일 업로드"""
        try:
            blob_client = self.blob_client.get_blob_client(
                container=container_name, 
                blob=f'{directory_name}/{file_name}'
            )
            
            # 기존 파일이 있는지 확인
            try:
                existing_blob = blob_client.get_blob_properties()
                if existing_blob:
                    # 기존 파일을 백업으로 저장 (타임스탬프 추가)
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{file_name.split('.')[0]}_backup_{timestamp}.{file_name.split('.')[-1]}"
                    backup_client = self.blob_client.get_blob_client(
                        container=container_name,
                        blob=f'{directory_name}/{backup_name}'
                    )
                    # 기존 파일 내용을 백업으로 복사
                    existing_data = blob_client.download_blob().readall()
                    backup_client.upload_blob(existing_data, overwrite=True)
                    print(f"기존 파일을 백업으로 저장: {backup_name}")
            except Exception:
                # 기존 파일이 없으면 무시
                pass
            
            # 새 파일 업로드
            blob_client.upload_blob(file_data, overwrite=True)
            return True
        except Exception as e:
            print(f"파일 업로드 오류: {e}")
            return False
    
    def download_file(self, container_name, file_name):
        """Blob Storage에서 파일 다운로드"""
        try:
            blob_client = self.blob_client.get_blob_client(
                container=container_name, 
                blob=file_name
            )
            return blob_client.download_blob().readall()
        except Exception as e:
            print(f"파일 다운로드 오류: {e}")
            return None
    
    def download_file_from_directory(self, container_name, directory_name, file_name):
        """rfp-documents 컨테이너 내 디렉토리에서 파일 다운로드"""
        try:
            blob_client = self.blob_client.get_blob_client(
                container=container_name, 
                blob=f'{directory_name}/{file_name}'
            )
            return blob_client.download_blob().readall()
        except Exception as e:
            print(f"파일 다운로드 오류: {e}")
            return None
    
    def list_files(self, container_name):
        """컨테이너 내 파일 목록 반환"""
        try:
            # 컨테이너가 존재하지 않으면 생성
            try:
                container_client = self.blob_client.get_container_client(container_name)
                container_client.get_container_properties()
            except Exception:
                print(f"컨테이너 {container_name}이 존재하지 않습니다. 생성 중...")
                self.blob_client.create_container(container_name)
                print(f"컨테이너 {container_name}이 생성되었습니다.")
            
            container_client = self.blob_client.get_container_client(container_name)
            blobs = container_client.list_blobs()
            return [blob.name for blob in blobs]
        except Exception as e:
            print(f"파일 목록 조회 오류: {e}")
            return []
    
    def list_files_in_directory(self, container_name, directory_name):
        """rfp-documents 컨테이너 내 디렉토리의 파일 목록 반환"""
        try:
            # 컨테이너가 존재하지 않으면 생성
            try:
                container_client = self.blob_client.get_container_client(container_name)
                container_client.get_container_properties()
            except Exception:
                print(f"컨테이너 {container_name}이 존재하지 않습니다. 생성 중...")
                self.blob_client.create_container(container_name)
                print(f"컨테이너 {container_name}이 생성되었습니다.")
            
            container_client = self.blob_client.get_container_client(container_name)
            blobs = container_client.list_blobs(name_starts_with=f'{directory_name}/')
            # 디렉토리명 제거하고 파일명만 반환
            return [blob.name.split('/')[-1] for blob in blobs if blob.name != f'{directory_name}/']
        except Exception as e:
            print(f"파일 목록 조회 오류: {e}")
            return []
    
    def search_documents(self, query, top=5):
        """Azure AI Search를 통한 문서 검색"""
        try:
            if not self.search_client:
                return []
            
            results = self.search_client.search(
                search_text=query,
                top=top,
                include_total_count=True
            )
            
            return [result for result in results]
        except Exception as e:
            print(f"문서 검색 오류: {e}")
            return []
    
    def call_openai(self, messages, model="gpt-4.1", temperature=0.7):
        """OpenAI API 호출"""
        try:
            # OpenAI 설정 확인
            if not hasattr(self, 'openai_configured') or not self.openai_configured:
                return self._get_configuration_error_message()
            
            # Azure OpenAI 클라이언트 초기화
            from openai import AzureOpenAI
            
            client = AzureOpenAI(
                api_key=OPENAI_API_KEY,
                api_version=OPENAI_API_VERSION,
                azure_endpoint=OPENAI_API_BASE
            )
            
            # Azure OpenAI API 호출
            response = client.chat.completions.create(
                model=model,  # Azure에서는 배포 이름 사용
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API 호출 오류: {e}")
            # 오류 발생 시 샘플 응답 반환 (개발/테스트용)
            return f"""
## 분석 결과 (샘플)

### 요청 정보
- 모델: {model}
- 메시지 수: {len(messages)}
- 온도: {temperature}

### 오류 메시지
{str(e)}

### 해결 방법
1. Azure OpenAI 서비스 연결 확인
2. API 키 및 엔드포인트 설정 확인
3. 모델 배포 이름 확인
4. 네트워크 연결 상태 확인

### 샘플 응답
현재 Azure OpenAI API 연결에 문제가 있습니다. 
환경 변수 설정을 확인하고 다시 시도해주세요.

**필요한 환경 변수:**
- OPENAI_API_KEY
- OPENAI_API_BASE (Azure OpenAI 엔드포인트)
- OPENAI_API_VERSION
- OPENAI_API_TYPE
"""
    
    def call_openai_with_files(self, messages, file_paths, model="gpt-4.1", temperature=0.7):
        """파일 첨부와 함께 OpenAI API 호출"""
        try:
            # OpenAI 설정 확인
            if not hasattr(self, 'openai_configured') or not self.openai_configured:
                return self._get_configuration_error_message()
            
            # Azure OpenAI 클라이언트 초기화
            from openai import AzureOpenAI
            
            client = AzureOpenAI(
                api_key=OPENAI_API_KEY,
                api_version=OPENAI_API_VERSION,
                azure_endpoint=OPENAI_API_BASE
            )
            
            # 파일 첨부를 위한 메시지 구성
            enhanced_messages = []
            for message in messages:
                if message["role"] == "user":
                    # 사용자 메시지에 파일 첨부 정보 추가
                    enhanced_content = message["content"]
                    if file_paths:
                        enhanced_content += f"\n\n**첨부 파일:**\n"
                        for i, file_path in enumerate(file_paths, 1):
                            enhanced_content += f"{i}. {file_path}\n"
                    
                    enhanced_messages.append({
                        "role": message["role"],
                        "content": enhanced_content
                    })
                else:
                    enhanced_messages.append(message)
            
            # Azure OpenAI API 호출
            response = client.chat.completions.create(
                model=model,
                messages=enhanced_messages,
                temperature=temperature,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"파일 첨부 OpenAI API 호출 오류: {e}")
            return f"""
## 파일 첨부 분석 결과 (샘플)

### 요청 정보
- 모델: {model}
- 메시지 수: {len(messages)}
- 첨부 파일 수: {len(file_paths) if file_paths else 0}
- 온도: {temperature}

### 첨부 파일
{chr(10).join([f"- {path}" for path in file_paths]) if file_paths else "첨부 파일 없음"}

### 오류 메시지
{str(e)}

### 해결 방법
1. Azure OpenAI 서비스 연결 확인
2. 파일 경로 및 접근 권한 확인
3. API 키 및 엔드포인트 설정 확인
4. 모델 배포 이름 확인

### 샘플 응답
현재 Azure OpenAI API 연결에 문제가 있습니다. 
파일 첨부 기능을 사용하려면 환경 변수 설정을 확인하고 다시 시도해주세요.
            """
    
    def search_knowledge_base(self, query, top=5):
        """Azure AI Search를 통한 지식 베이스 검색"""
        try:
            if not self.search_client:
                return []
            
            # 검색 실행 - content 필드 중심으로 검색
            results = self.search_client.search(
                search_text=query,
                top=top,
                include_total_count=True,
                search_fields=["content"],  # content 필드에서만 검색
                select=["id", "file_name", "content", "client_name", "industry", "container_name", "upload_date"]
            )
            
            search_results = []
            for result in results:
                # 실제 인덱스 필드에 맞게 매핑
                search_results.append({
                    'title': result.get('file_name', '제목 없음'),
                    'content': result.get('content', ''),
                    'url': f"📁 {result.get('container_name', '')} | 🏢 {result.get('client_name', '')}",
                    'score': result.get('@search.score', 0),
                    'client_name': result.get('client_name', ''),
                    'industry': result.get('industry', ''),
                    'upload_date': result.get('upload_date', ''),
                    'container_name': result.get('container_name', '')
                })
            
            # 검색 결과 디버깅 로그
            print(f"🔍 Azure AI Search 결과: {len(search_results)}개 문서 발견")
            for i, result in enumerate(search_results[:3]):  # 상위 3개만 로그
                print(f"  {i+1}. {result['title']} (점수: {result['score']:.2f}) - {result['client_name']}")
            
            return search_results
            
        except Exception as e:
            print(f"지식 베이스 검색 오류: {str(e)}")
            return []
    
    def search_web(self, query, max_results=3):
        """웹 검색 기능 (Bing Search API 사용)"""
        try:
            # Bing Search API 키가 설정되어 있는지 확인
            bing_api_key = os.getenv('BING_SEARCH_API_KEY')
            if not bing_api_key:
                # Bing API 키가 없으면 Azure OpenAI의 웹 검색 기능 사용
                return self._search_web_with_openai(query)
            
            # Bing Search API 사용
            endpoint = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
            params = {
                "q": query,
                "count": max_results,
                "offset": 0,
                "mkt": "ko-KR",
                "safesearch": "Moderate"
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            search_results = []
            data = response.json()
            
            for item in data.get('webPages', {}).get('value', []):
                search_results.append({
                    'title': item.get('name', ''),
                    'snippet': item.get('snippet', ''),
                    'url': item.get('url', ''),
                    'display_url': item.get('displayUrl', '')
                })
            
            return search_results
            
        except Exception as e:
            print(f"웹 검색 오류: {str(e)}")
            return self._search_web_with_openai(query)
    
    def _search_web_with_openai(self, query):
        """OpenAI를 통한 웹 검색 시뮬레이션"""
        try:
            # OpenAI를 사용하여 웹 검색 결과를 시뮬레이션
            messages = [
                {
                    "role": "system",
                    "content": f"""당신은 웹 검색 전문가입니다. 
                    주어진 질문에 대해 최신 정보를 바탕으로 검색 결과를 제공해주세요.
                    질문: {query}
                    
                    다음 형식으로 검색 결과를 제공해주세요:
                    - 제목: [검색 결과 제목]
                    - 요약: [검색 결과 요약]
                    - URL: [관련 URL]
                    """
                },
                {
                    "role": "user",
                    "content": f"'{query}'에 대한 최신 웹 검색 결과를 제공해주세요."
                }
            ]
            
            response = self.call_openai(messages)
            return [{
                'title': f"{query} 검색 결과",
                'snippet': response,
                'url': 'https://example.com',
                'display_url': 'example.com'
            }]
            
        except Exception as e:
            print(f"OpenAI 웹 검색 시뮬레이션 오류: {str(e)}")
            return []

