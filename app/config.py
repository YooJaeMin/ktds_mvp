import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AzureConfig:
    openai_endpoint: str
    openai_api_key: str
    openai_api_version: str
    openai_deployment_name: str
    
    document_intelligence_endpoint: str
    document_intelligence_key: str
    
    text_analytics_endpoint: str
    text_analytics_key: str
    
    storage_connection_string: str

def load_config() -> AzureConfig:
    """환경 변수에서 Azure 설정을 로드합니다."""
    return AzureConfig(
        openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
        openai_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
        
        document_intelligence_endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        document_intelligence_key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
        
        text_analytics_endpoint=os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT", ""),
        text_analytics_key=os.getenv("AZURE_TEXT_ANALYTICS_KEY", ""),
        
        storage_connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    )

config = load_config()