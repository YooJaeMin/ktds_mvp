from typing import Dict, Any, List
from datetime import datetime
import re

from app.utils.document_utils import DocumentProcessor, TextAnalyzer
from app.utils.azure_client import azure_client
from app.models.schemas import QualityCheckResult

class QualityManager:
    """제안서 품질 관리 서비스"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.text_analyzer = TextAnalyzer()
        
        # 제안서 필수 섹션 정의
        self.required_sections = {
            "사업 이해": ["사업", "이해", "분석", "현황"],
            "기술 솔루션": ["기술", "솔루션", "아키텍처", "설계"],
            "프로젝트 수행방법론": ["방법론", "수행", "프로세스", "절차"],
            "일정 계획": ["일정", "계획", "스케줄", "마일스톤"],
            "인력 구성": ["인력", "조직", "팀", "전문가"],
            "예산 및 비용": ["예산", "비용", "가격", "견적"],
            "기대효과": ["효과", "성과", "ROI", "개선"]
        }
        
        # 품질 평가 기준
        self.quality_criteria = {
            "완성도": 25,      # 필수 섹션 포함도
            "논리성": 20,      # 논리적 구성과 일관성
            "구체성": 20,      # 구체적 방안과 세부사항
            "차별성": 15,      # 독창성과 차별화
            "실현가능성": 20   # 현실적 실행 가능성
        }
    
    async def evaluate_proposal(self, content: bytes, filename: str) -> Dict[str, Any]:
        """제안서의 종합적인 품질을 평가합니다."""
        
        # 1. 문서에서 텍스트 추출
        text = self.document_processor.extract_text_from_file(content, filename)
        
        # 2. 섹션별 분석
        section_analysis = await self._analyze_sections(text)
        
        # 3. 내용 품질 평가
        content_quality = await self._evaluate_content_quality(text)
        
        # 4. 가독성 평가
        readability_score = self.text_analyzer.calculate_readability_score(text)
        
        # 5. 컴플라이언스 체크
        compliance_check = await self._check_compliance(text)
        
        # 6. 강점과 약점 분석
        strengths, weaknesses = await self._analyze_strengths_weaknesses(text, section_analysis)
        
        # 7. 개선 제안사항 생성
        improvement_suggestions = await self._generate_improvement_suggestions(
            section_analysis, content_quality, weaknesses
        )
        
        # 8. 전체 점수 계산
        overall_score = self._calculate_overall_score(
            section_analysis, content_quality, readability_score, compliance_check
        )
        
        result = {
            "evaluation_date": datetime.now().isoformat(),
            "document_info": {
                "filename": filename,
                "text_length": len(text),
                "estimated_pages": len(text) // 2000  # 대략적인 페이지 수
            },
            "overall_score": overall_score,
            "section_scores": {section: analysis["score"] for section, analysis in section_analysis.items()},
            "content_quality": content_quality,
            "readability_score": readability_score,
            "compliance_check": compliance_check,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_suggestions": improvement_suggestions,
            "detailed_analysis": {
                "section_analysis": section_analysis,
                "missing_sections": self._find_missing_sections(section_analysis)
            }
        }
        
        return result
    
    async def _analyze_sections(self, text: str) -> Dict[str, Any]:
        """제안서의 각 섹션을 분석합니다."""
        
        section_analysis = {}
        
        for section_name, keywords in self.required_sections.items():
            analysis = await self._analyze_single_section(text, section_name, keywords)
            section_analysis[section_name] = analysis
        
        return section_analysis
    
    async def _analyze_single_section(self, text: str, section_name: str, keywords: List[str]) -> Dict[str, Any]:
        """개별 섹션을 분석합니다."""
        
        # 키워드 매칭으로 섹션 존재 여부 확인
        keyword_matches = sum(1 for keyword in keywords if keyword in text)
        keyword_score = min(keyword_matches * 25, 100)
        
        # 섹션별 상세 내용 분석
        section_content = self._extract_section_content(text, keywords)
        
        # 내용 길이 기반 점수
        content_length_score = min(len(section_content) // 100 * 10, 50)
        
        # 구체성 평가
        specificity_score = await self._evaluate_section_specificity(section_content, section_name)
        
        # 최종 섹션 점수
        section_score = (keyword_score * 0.4 + content_length_score * 0.3 + specificity_score * 0.3)
        
        return {
            "score": round(section_score, 1),
            "keyword_matches": keyword_matches,
            "content_length": len(section_content),
            "specificity_score": specificity_score,
            "exists": keyword_score > 0,
            "content_preview": section_content[:200] + "..." if len(section_content) > 200 else section_content
        }
    
    def _extract_section_content(self, text: str, keywords: List[str]) -> str:
        """키워드 주변의 내용을 추출합니다."""
        
        content_parts = []
        for keyword in keywords:
            pattern = rf'.{{0,200}}{re.escape(keyword)}.{{0,500}}'
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            content_parts.extend(matches)
        
        return " ".join(content_parts)
    
    async def _evaluate_section_specificity(self, content: str, section_name: str) -> float:
        """섹션의 구체성을 평가합니다."""
        
        if not content:
            return 0.0
        
        specificity_indicators = {
            "사업 이해": ["분석", "현황", "문제점", "요구사항"],
            "기술 솔루션": ["아키텍처", "기술스택", "데이터베이스", "보안"],
            "프로젝트 수행방법론": ["단계", "프로세스", "절차", "방법"],
            "일정 계획": ["월", "주", "일정", "마일스톤"],
            "인력 구성": ["경력", "역할", "책임", "전문가"],
            "예산 및 비용": ["원", "비용", "예산", "견적"],
            "기대효과": ["개선", "효율", "절감", "향상"]
        }
        
        indicators = specificity_indicators.get(section_name, [])
        indicator_count = sum(1 for indicator in indicators if indicator in content)
        
        # 숫자와 구체적 데이터 존재 여부
        numbers = re.findall(r'\d+', content)
        has_numbers = len(numbers) > 0
        
        specificity_score = (indicator_count * 15) + (20 if has_numbers else 0)
        return min(specificity_score, 100)
    
    async def _evaluate_content_quality(self, text: str) -> Dict[str, float]:
        """내용의 품질을 다각도로 평가합니다."""
        
        quality_scores = {}
        
        # 1. 논리성 평가 (문장 구조와 연결성)
        logical_connectors = ['따라서', '그러므로', '이에 따라', '결과적으로', '또한', '더불어']
        connector_count = sum(1 for connector in logical_connectors if connector in text)
        quality_scores['논리성'] = min(connector_count * 10, 100)
        
        # 2. 전문성 평가 (전문 용어 사용)
        technical_terms = ['아키텍처', '프레임워크', '데이터베이스', '보안', '성능', '확장성', '인터페이스']
        tech_count = sum(1 for term in technical_terms if term in text)
        quality_scores['전문성'] = min(tech_count * 12, 100)
        
        # 3. 구체성 평가 (수치와 구체적 정보)
        numbers = re.findall(r'\d+', text)
        quality_scores['구체성'] = min(len(numbers) * 5, 100)
        
        # 4. 완성도 평가 (문서 길이와 구조)
        word_count = len(text.split())
        if word_count > 5000:
            quality_scores['완성도'] = 100
        elif word_count > 2000:
            quality_scores['완성도'] = 80
        elif word_count > 1000:
            quality_scores['완성도'] = 60
        else:
            quality_scores['완성도'] = 40
        
        # Azure AI를 사용한 추가 품질 분석
        try:
            sentiment_analysis = await azure_client.analyze_sentiment(text[:1000])
            if sentiment_analysis['sentiment'] == 'positive':
                quality_scores['긍정성'] = sentiment_analysis['confidence'] * 100
            else:
                quality_scores['긍정성'] = 50
        except:
            quality_scores['긍정성'] = 70
        
        return quality_scores
    
    async def _check_compliance(self, text: str) -> Dict[str, bool]:
        """컴플라이언스 요구사항을 확인합니다."""
        
        compliance_checks = {}
        
        # 필수 포함 사항 체크
        compliance_checks['회사소개_포함'] = any(keyword in text for keyword in ['회사', '소개', '연혁', '실적'])
        compliance_checks['기술역량_포함'] = any(keyword in text for keyword in ['기술', '역량', '경험', '전문성'])
        compliance_checks['프로젝트경험_포함'] = any(keyword in text for keyword in ['프로젝트', '경험', '수행', '사례'])
        compliance_checks['보안방안_포함'] = any(keyword in text for keyword in ['보안', '암호화', '인증', '권한'])
        
        # 금지 사항 체크
        prohibited_words = ['100%', '완벽', '절대', '무조건']
        compliance_checks['과장표현_없음'] = not any(word in text for word in prohibited_words)
        
        # 형식 요구사항 체크
        compliance_checks['목차_존재'] = any(keyword in text for keyword in ['목차', '차례', 'Contents'])
        compliance_checks['페이지번호_존재'] = bool(re.search(r'페이지|\d+\s*page|\d+\s*/\s*\d+', text))
        
        return compliance_checks
    
    async def _analyze_strengths_weaknesses(self, text: str, section_analysis: Dict) -> tuple:
        """강점과 약점을 분석합니다."""
        
        strengths = []
        weaknesses = []
        
        # 섹션 분석 기반 강점/약점
        for section, analysis in section_analysis.items():
            if analysis['score'] >= 80:
                strengths.append(f"{section} 섹션이 충실하게 작성됨")
            elif analysis['score'] < 50:
                weaknesses.append(f"{section} 섹션이 부족하거나 미흡함")
        
        # 내용 분석 기반
        if len(text) > 10000:
            strengths.append("충분한 분량의 상세한 제안서")
        elif len(text) < 3000:
            weaknesses.append("제안서 분량이 부족함")
        
        # 구조적 분석
        if '목차' in text or 'Contents' in text:
            strengths.append("체계적인 문서 구조")
        else:
            weaknesses.append("명확한 문서 구조가 부족함")
        
        # 기술적 내용 분석
        tech_keywords = ['API', '데이터베이스', '아키텍처', '보안', '성능']
        tech_count = sum(1 for keyword in tech_keywords if keyword in text)
        if tech_count >= 3:
            strengths.append("기술적 내용이 풍부함")
        else:
            weaknesses.append("기술적 세부사항이 부족함")
        
        return strengths[:5], weaknesses[:5]
    
    async def _generate_improvement_suggestions(self, section_analysis: Dict, 
                                               content_quality: Dict, weaknesses: List[str]) -> List[str]:
        """개선 제안사항을 생성합니다."""
        
        suggestions = []
        
        # 섹션별 개선사항
        for section, analysis in section_analysis.items():
            if analysis['score'] < 60:
                suggestions.append(f"{section} 섹션을 더 구체적으로 작성하세요")
        
        # 품질 기반 개선사항
        if content_quality.get('구체성', 0) < 60:
            suggestions.append("구체적인 수치와 데이터를 더 많이 포함하세요")
        
        if content_quality.get('전문성', 0) < 60:
            suggestions.append("기술적 전문 용어와 상세한 설명을 추가하세요")
        
        # 약점 기반 개선사항
        for weakness in weaknesses:
            if "구조" in weakness:
                suggestions.append("명확한 목차와 문서 구조를 추가하세요")
            elif "분량" in weakness:
                suggestions.append("각 섹션의 내용을 더 상세히 기술하세요")
        
        # Azure AI를 사용한 추가 제안사항
        try:
            prompt = f"""
다음 제안서 약점들을 개선하기 위한 구체적인 제안사항 3가지를 제시해주세요:

약점들:
{', '.join(weaknesses)}

개선 제안사항:
"""
            ai_suggestions = await azure_client.generate_completion(prompt, max_tokens=300)
            ai_suggestion_list = [s.strip() for s in ai_suggestions.split('\n') if s.strip()]
            suggestions.extend(ai_suggestion_list[:3])
        except:
            pass
        
        return suggestions[:8]
    
    def _find_missing_sections(self, section_analysis: Dict) -> List[str]:
        """누락된 섹션을 찾습니다."""
        
        missing_sections = []
        for section, analysis in section_analysis.items():
            if not analysis['exists'] or analysis['score'] < 30:
                missing_sections.append(section)
        
        return missing_sections
    
    def _calculate_overall_score(self, section_analysis: Dict, content_quality: Dict, 
                                readability_score: float, compliance_check: Dict) -> float:
        """전체 점수를 계산합니다."""
        
        # 섹션 점수 평균 (40%)
        section_scores = [analysis['score'] for analysis in section_analysis.values()]
        avg_section_score = sum(section_scores) / len(section_scores) if section_scores else 0
        
        # 내용 품질 점수 평균 (30%)
        quality_scores = list(content_quality.values())
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # 가독성 점수 (15%)
        readability_weight = readability_score
        
        # 컴플라이언스 점수 (15%)
        compliance_rate = sum(compliance_check.values()) / len(compliance_check) * 100
        
        overall_score = (
            avg_section_score * 0.40 +
            avg_quality_score * 0.30 +
            readability_weight * 0.15 +
            compliance_rate * 0.15
        )
        
        return round(overall_score, 1)