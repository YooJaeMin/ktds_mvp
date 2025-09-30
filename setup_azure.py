"""
Azure 서비스 초기 설정 스크립트
"""
import os
from azure.storage.blob import BlobServiceClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField, ComplexField
from azure.core.credentials import AzureKeyCredential
from config import *

def setup_azure_search_index():
    """Azure AI Search 인덱스 설정"""
    try:
        credential = AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY)
        search_client = SearchIndexClient(
            endpoint=f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net",
            credential=credential
        )
        
        # 인덱스 정의
        index = SearchIndex(
            name=AZURE_SEARCH_INDEX_NAME,
            fields=[
                SimpleField(name="id", type="Edm.String", key=True),
                SimpleField(name="container_name", type="Edm.String", filterable=True),
                SimpleField(name="file_name", type="Edm.String", filterable=True),
                SimpleField(name="file_type", type="Edm.String", filterable=True),
                SearchableField(name="content", type="Edm.String", analyzer="ko.lucene"),
                SimpleField(name="upload_date", type="Edm.DateTimeOffset", filterable=True, sortable=True),
                SimpleField(name="industry", type="Edm.String", filterable=True),
                SimpleField(name="client_name", type="Edm.String", filterable=True)
            ]
        )
        
        # 인덱스 생성
        search_client.create_index(index)
        print(f"✅ Azure AI Search 인덱스 '{AZURE_SEARCH_INDEX_NAME}' 생성 완료")
        
    except Exception as e:
        print(f"❌ Azure AI Search 인덱스 생성 오류: {e}")

def setup_azure_storage():
    """Azure Blob Storage 초기 설정"""
    try:
        if AZURE_STORAGE_CONNECTION_STRING:
            blob_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        else:
            from azure.identity import DefaultAzureCredential
            credential = DefaultAzureCredential()
            blob_client = BlobServiceClient(
                account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                credential=credential
            )
        
        # 기본 컨테이너 생성
        containers = ["rfp-documents", "analysis-results", "proposals"]
        
        for container_name in containers:
            try:
                blob_client.create_container(container_name)
                print(f"✅ 컨테이너 '{container_name}' 생성 완료")
            except Exception as e:
                if "ContainerAlreadyExists" in str(e):
                    print(f"ℹ️ 컨테이너 '{container_name}' 이미 존재")
                else:
                    print(f"❌ 컨테이너 '{container_name}' 생성 오류: {e}")
        
    except Exception as e:
        print(f"❌ Azure Storage 설정 오류: {e}")

def main():
    """메인 설정 함수"""
    print("🚀 Azure 서비스 초기 설정을 시작합니다...")
    
    # 환경 변수 확인
    required_vars = [
        "AZURE_STORAGE_ACCOUNT_NAME",
        "AZURE_SEARCH_SERVICE_NAME", 
        "AZURE_SEARCH_ADMIN_KEY",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 다음 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        print("📝 .env 파일을 확인하고 필요한 변수를 설정해주세요.")
        return
    
    # Azure Storage 설정
    print("\n📦 Azure Blob Storage 설정 중...")
    setup_azure_storage()
    
    # Azure AI Search 설정
    print("\n🔍 Azure AI Search 설정 중...")
    setup_azure_search_index()
    
    print("\n✅ Azure 서비스 초기 설정이 완료되었습니다!")
    print("\n📋 다음 단계:")
    print("1. streamlit run app.py 명령으로 애플리케이션 실행")
    print("2. 브라우저에서 http://localhost:8501 접속")
    print("3. RFP 문서 업로드 및 분석 시작")

if __name__ == "__main__":
    main()






