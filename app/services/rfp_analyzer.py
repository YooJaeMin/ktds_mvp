from typing import Dict, Any, List
import re
from datetime import datetime

from app.utils.document_utils import DocumentProcessor
from app.utils.azure_client import azure_client
from app.models.schemas import RFPAnalysisResult

class RFPAnalyzer:
    """RFP 문서 분석 자동화 서비스"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
    
    async def analyze_document(self, content: bytes, filename: str) -> Dict[str, Any]:
        """RFP 문서를 종합적으로 분석합니다."""
        
        # 1. 문서에서 텍스트 추출
        text = self.document_processor.extract_text_from_file(content, filename)
        
        # 2. Azure AI를 사용한 구조 분석
        try:
            document_structure = await azure_client.analyze_document_structure(content)
        except:
            document_structure = {"pages": 1, "tables": [], "key_value_pairs": []}
        
        # 3. 주요 섹션 분석
        requirements = await self._extract_requirements(text)
        technical_specs = await self._extract_technical_specs(text)
        timeline = await self._extract_timeline(text)
        budget_info = await self._extract_budget_info(text)
        compliance_requirements = await self._extract_compliance_requirements(text)
        evaluation_criteria = await self._extract_evaluation_criteria(text)
        
        # 4. 위험도 평가
        risk_assessment = await self._assess_risks(text, requirements, technical_specs)
        
        # 5. 신뢰도 점수 계산
        confidence_score = self._calculate_confidence_score(text, requirements, technical_specs)
        
        result = {
            "document_info": {
                "filename": filename,
                "pages": document_structure.get("pages", 1),
                "analyzed_at": datetime.now().isoformat(),
                "text_length": len(text)
            },
            "requirements": requirements,
            "technical_specs": technical_specs,
            "timeline": timeline,
            "budget_info": budget_info,
            "risk_assessment": risk_assessment,
            "compliance_requirements": compliance_requirements,
            "evaluation_criteria": evaluation_criteria,
            "confidence_score": confidence_score,
            "document_structure": document_structure
        }
        
        return result
    
    async def _extract_requirements(self, text: str) -> List[str]:
        """주요 요구사항을 추출합니다."""
        
        # 키워드 기반 요구사항 추출
        requirement_patterns = [
            r'(?:요구사항|요구|필수|반드시|의무)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:Must|SHALL|MUST)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:기능|Function|Functionality)[:：]?\s*(.+?)(?:\n|\.)'
        ]
        
        requirements = []
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            requirements.extend([match.strip() for match in matches if len(match.strip()) > 10])
        
        # Azure AI를 사용한 추가 분석
        try:
            prompt = f"""
다음 RFP 문서에서 주요 요구사항을 추출해주세요. 각 요구사항은 한 줄로 요약해주세요.

문서 내용:
{text[:2000]}...

주요 요구사항 (최대 10개):
"""
            ai_requirements = await azure_client.generate_completion(prompt, max_tokens=500)
            ai_req_list = [req.strip() for req in ai_requirements.split('\n') if req.strip() and not req.startswith('-')]
            requirements.extend(ai_req_list[:5])
        except:
            pass
        
        # 중복 제거 및 정리
        unique_requirements = list(set(requirements))
        return unique_requirements[:15]  # 최대 15개
    
    async def _extract_technical_specs(self, text: str) -> List[str]:
        """기술 사양을 추출합니다."""
        
        tech_patterns = [
            r'(?:기술|Technology|Tech|시스템|System)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:플랫폼|Platform|OS|운영체제)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:데이터베이스|Database|DB)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:프로그래밍|Programming|언어|Language)[:：]?\s*(.+?)(?:\n|\.)'
        ]
        
        tech_specs = []
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            tech_specs.extend([match.strip() for match in matches if len(match.strip()) > 5])
        
        return list(set(tech_specs))[:10]
    
    async def _extract_timeline(self, text: str) -> str:
        """프로젝트 일정을 추출합니다."""
        
        timeline_patterns = [
            r'(?:기간|기한|납기|Timeline|Schedule|Duration)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:개월|month|주|week|일|day)[\s]*(?:이내|내|within)',
            r'\d+\s*(?:개월|month|주|week|일|day)'
        ]
        
        for pattern in timeline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0] if isinstance(matches[0], str) else str(matches[0])
        
        return "명시되지 않음"
    
    async def _extract_budget_info(self, text: str) -> str:
        """예산 정보를 추출합니다."""
        
        budget_patterns = [
            r'(?:예산|Budget|비용|Cost|금액|Amount)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:원|won|달러|dollar|\$|₩)[\d,]+',
            r'\d+\s*(?:억|만|천)'
        ]
        
        for pattern in budget_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0] if isinstance(matches[0], str) else str(matches[0])
        
        return "명시되지 않음"
    
    async def _extract_compliance_requirements(self, text: str) -> List[str]:
        """컴플라이언스 요구사항을 추출합니다."""
        
        compliance_keywords = [
            '개인정보보호', 'GDPR', 'ISMS', 'ISO27001', '정보보안',
            '감사', 'Audit', '규정', 'Regulation', '표준', 'Standard',
            '인증', 'Certification', '보안', 'Security'
        ]
        
        compliance_reqs = []
        for keyword in compliance_keywords:
            if keyword.lower() in text.lower():
                compliance_reqs.append(keyword)
        
        return compliance_reqs
    
    async def _extract_evaluation_criteria(self, text: str) -> List[str]:
        """평가 기준을 추출합니다."""
        
        criteria_patterns = [
            r'(?:평가|Evaluation|심사|Review)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:기준|Criteria|점수|Score)[:：]?\s*(.+?)(?:\n|\.)',
            r'(?:가점|배점|점수|점)[\s]*\d+'
        ]
        
        criteria = []
        for pattern in criteria_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            criteria.extend([match.strip() for match in matches if len(match.strip()) > 5])
        
        return list(set(criteria))[:8]
    
    async def _assess_risks(self, text: str, requirements: List[str], tech_specs: List[str]) -> Dict[str, str]:
        """위험도를 평가합니다."""
        
        risks = {}
        
        # 기술적 복잡도 평가
        complex_keywords = ['AI', '머신러닝', 'Machine Learning', '빅데이터', 'Big Data', 
                           '클라우드', 'Cloud', '마이크로서비스', 'Microservice']
        tech_complexity = sum(1 for keyword in complex_keywords if keyword.lower() in text.lower())
        
        if tech_complexity > 3:
            risks['기술적 복잡도'] = '높음 - 고급 기술 요구사항이 많습니다'
        elif tech_complexity > 1:
            risks['기술적 복잡도'] = '중간 - 일부 고급 기술이 필요합니다'
        else:
            risks['기술적 복잡도'] = '낮음 - 표준 기술로 구현 가능합니다'
        
        # 일정 위험도 평가
        urgent_keywords = ['긴급', 'urgent', '즉시', 'immediate', '단기', 'short']
        if any(keyword.lower() in text.lower() for keyword in urgent_keywords):
            risks['일정 위험도'] = '높음 - 타이트한 일정으로 예상됩니다'
        else:
            risks['일정 위험도'] = '보통 - 적절한 일정 계획이 필요합니다'
        
        # 요구사항 명확성
        if len(requirements) < 5:
            risks['요구사항 명확성'] = '높음 - 요구사항이 불명확하거나 부족합니다'
        else:
            risks['요구사항 명확성'] = '낮음 - 요구사항이 상세히 기술되어 있습니다'
        
        return risks
    
    def _calculate_confidence_score(self, text: str, requirements: List[str], tech_specs: List[str]) -> float:
        """분석 결과의 신뢰도 점수를 계산합니다."""
        
        score = 0.0
        
        # 문서 길이에 따른 점수
        if len(text) > 5000:
            score += 30
        elif len(text) > 2000:
            score += 20
        else:
            score += 10
        
        # 추출된 요구사항 수에 따른 점수
        score += min(len(requirements) * 5, 30)
        
        # 기술 사양 정보에 따른 점수
        score += min(len(tech_specs) * 3, 20)
        
        # 구조화된 정보 존재 여부
        structured_keywords = ['목차', '색인', '번호', '항목']
        if any(keyword in text for keyword in structured_keywords):
            score += 20
        
        return min(score, 100.0)