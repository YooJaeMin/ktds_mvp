from openai import AsyncAzureOpenAI
from typing import Dict, Any, List
import json

from app.config import config

class AzureAIClient:
    """Azure AI 서비스와의 통합을 위한 클라이언트 클래스"""
    
    def __init__(self):
        self._setup_openai()
        self._setup_document_intelligence()
        self._setup_text_analytics()
    
    def _setup_openai(self):
        """Azure OpenAI 설정"""
        if config.openai_endpoint and config.openai_api_key:
            try:
                self.openai_client = AsyncAzureOpenAI(
                    api_key=config.openai_api_key,
                    api_version=config.openai_api_version,
                    azure_endpoint=config.openai_endpoint
                )
                self.openai_available = True
            except Exception:
                self.openai_available = False
        else:
            self.openai_available = False
    
    def _setup_document_intelligence(self):
        """Azure Document Intelligence 설정"""
        try:
            if config.document_intelligence_endpoint and config.document_intelligence_key:
                from azure.ai.formrecognizer import DocumentAnalysisClient
                from azure.core.credentials import AzureKeyCredential
                
                self.document_client = DocumentAnalysisClient(
                    endpoint=config.document_intelligence_endpoint,
                    credential=AzureKeyCredential(config.document_intelligence_key)
                )
                self.document_intelligence_available = True
            else:
                self.document_intelligence_available = False
        except ImportError:
            self.document_intelligence_available = False
    
    def _setup_text_analytics(self):
        """Azure Text Analytics 설정"""
        try:
            if config.text_analytics_endpoint and config.text_analytics_key:
                from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
                from azure.core.credentials import AzureKeyCredential
                
                self.text_analytics_client = TextAnalyticsClient(
                    endpoint=config.text_analytics_endpoint,
                    credential=AzureKeyCredential(config.text_analytics_key)
                )
                self.text_analytics_available = True
            else:
                self.text_analytics_available = False
        except ImportError:
            self.text_analytics_available = False
    
    async def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """Azure OpenAI를 사용하여 텍스트 생성"""
        if not self.openai_available:
            # Mock response when Azure OpenAI is not available
            return self._generate_mock_completion(prompt)
        
        try:
            response = await self.openai_client.completions.create(
                model=config.openai_deployment_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=None
            )
            return response.choices[0].text.strip()
        except Exception as e:
            # Fall back to mock response
            return self._generate_mock_completion(prompt)
    
    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Azure OpenAI Chat Completion API 사용"""
        if not self.openai_available:
            # Mock response when Azure OpenAI is not available
            return self._generate_mock_chat_completion(messages)
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=config.openai_deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fall back to mock response
            return self._generate_mock_chat_completion(messages)
    
    def _generate_mock_completion(self, prompt: str) -> str:
        """Mock completion response for demo purposes"""
        if "요구사항" in prompt or "requirement" in prompt.lower():
            return "1. 시스템 안정성 확보\n2. 사용자 편의성 개선\n3. 보안 강화\n4. 성능 최적화\n5. 확장성 고려"
        elif "전략" in prompt or "strategy" in prompt.lower():
            return "1. 단계적 접근을 통한 점진적 개선\n2. 기존 시스템과의 호환성 확보\n3. 사용자 교육 및 지원 체계 구축"
        elif "개선" in prompt or "improvement" in prompt.lower():
            return "1. 문서 구조를 더 체계적으로 정리\n2. 구체적인 수치와 근거 자료 보완\n3. 시각적 요소를 활용한 가독성 향상"
        else:
            return "AI 분석을 통해 도출된 인사이트를 제공합니다. 더 정확한 분석을 위해서는 Azure OpenAI 서비스 설정이 필요합니다."
    
    def _generate_mock_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Mock chat completion response for demo purposes"""
        last_message = messages[-1].get("content", "") if messages else ""
        return self._generate_mock_completion(last_message)
    
    async def analyze_document_structure(self, document_content: bytes) -> Dict[str, Any]:
        """Azure Document Intelligence를 사용하여 문서 구조 분석"""
        if not self.document_intelligence_available:
            # Document Intelligence가 없는 경우 기본 분석 수행
            return {"pages": 1, "tables": [], "key_value_pairs": []}
        
        try:
            poller = self.document_client.begin_analyze_document(
                "prebuilt-document", document_content
            )
            result = poller.result()
            
            return {
                "pages": len(result.pages),
                "tables": [{"row_count": table.row_count, "column_count": table.column_count} 
                          for table in result.tables],
                "key_value_pairs": [{"key": kv.key.content, "value": kv.value.content if kv.value else ""} 
                                   for kv in result.key_value_pairs]
            }
        except Exception as e:
            # Fall back to basic analysis
            return {"pages": 1, "tables": [], "key_value_pairs": []}
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Azure Text Analytics를 사용하여 감정 분석"""
        if not self.text_analytics_available:
            # Text Analytics가 없는 경우 기본값 반환
            return {"sentiment": "neutral", "confidence": 0.7, "scores": {"positive": 0.3, "negative": 0.2, "neutral": 0.5}}
        
        try:
            documents = [text]
            response = self.text_analytics_client.analyze_sentiment(documents=documents)
            
            result = response[0]
            return {
                "sentiment": result.sentiment,
                "confidence": result.confidence_scores.positive + result.confidence_scores.negative + result.confidence_scores.neutral,
                "scores": {
                    "positive": result.confidence_scores.positive,
                    "negative": result.confidence_scores.negative,
                    "neutral": result.confidence_scores.neutral
                }
            }
        except Exception as e:
            # Fall back to mock response
            return {"sentiment": "neutral", "confidence": 0.7, "scores": {"positive": 0.3, "negative": 0.2, "neutral": 0.5}}
    
    async def extract_key_phrases(self, text: str) -> List[str]:
        """Azure Text Analytics를 사용하여 주요 구문 추출"""
        if not self.text_analytics_available:
            # Text Analytics가 없는 경우 간단한 키워드 추출
            words = text.split()
            return [word for word in words if len(word) > 5][:10]
        
        try:
            documents = [text]
            response = self.text_analytics_client.extract_key_phrases(documents=documents)
            
            return response[0].key_phrases
        except Exception as e:
            # Fall back to simple keyword extraction
            words = text.split()
            return [word for word in words if len(word) > 5][:10]

# 전역 Azure AI 클라이언트 인스턴스
azure_client = AzureAIClient()