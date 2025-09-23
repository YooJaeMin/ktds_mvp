from typing import Dict, Any, List
from datetime import datetime

from app.utils.azure_client import azure_client

class StrategySupport:
    """사업 이해 및 전략 지원 서비스"""
    
    def __init__(self):
        self.industry_knowledge = {
            "금융": {
                "key_trends": ["디지털 트랜스포메이션", "핀테크", "오픈뱅킹", "AI/ML", "블록체인"],
                "regulations": ["금융위원회 규정", "개인정보보호법", "전자금융거래법"],
                "success_factors": ["보안성", "안정성", "사용성", "규제 준수"]
            },
            "제조": {
                "key_trends": ["스마트팩토리", "IoT", "예측 정비", "자동화", "MES"],
                "regulations": ["산업안전보건법", "환경법규", "품질표준"],
                "success_factors": ["효율성", "품질", "안전성", "비용 절감"]
            },
            "공공": {
                "key_trends": ["디지털정부", "AI행정", "빅데이터", "클라우드", "사이버보안"],
                "regulations": ["전자정부법", "정보보호법", "공공데이터법"],
                "success_factors": ["투명성", "효율성", "접근성", "보안성"]
            },
            "교육": {
                "key_trends": ["에듀테크", "원격학습", "개인화 교육", "VR/AR", "LMS"],
                "regulations": ["개인정보보호법", "교육기본법", "저작권법"],
                "success_factors": ["학습효과", "접근성", "사용편의성", "콘텐츠 품질"]
            }
        }
    
    async def analyze_business_context(self, industry: str, client_info: str, project_scope: str) -> Dict[str, Any]:
        """사업 맥락을 분석하고 전략적 인사이트를 제공합니다."""
        
        # 1. 산업 분석
        market_analysis = await self._analyze_market_trends(industry)
        
        # 2. 고객 분석
        client_analysis = await self._analyze_client_context(client_info, industry)
        
        # 3. 경쟁 환경 분석
        competitive_landscape = await self._analyze_competitive_landscape(industry, project_scope)
        
        # 4. 전략적 권고사항 생성
        strategic_recommendations = await self._generate_strategic_recommendations(
            industry, client_info, project_scope, market_analysis
        )
        
        # 5. 성공 요인 분석
        success_factors = await self._identify_success_factors(industry, project_scope)
        
        # 6. 잠재적 도전과제 식별
        potential_challenges = await self._identify_challenges(industry, client_info, project_scope)
        
        # 7. 권장 접근법 제안
        recommended_approach = await self._recommend_approach(
            industry, project_scope, strategic_recommendations
        )
        
        result = {
            "analysis_date": datetime.now().isoformat(),
            "industry": industry,
            "market_analysis": market_analysis,
            "client_analysis": client_analysis,
            "competitive_landscape": competitive_landscape,
            "strategic_recommendations": strategic_recommendations,
            "success_factors": success_factors,
            "potential_challenges": potential_challenges,
            "recommended_approach": recommended_approach
        }
        
        return result
    
    async def _analyze_market_trends(self, industry: str) -> Dict[str, Any]:
        """시장 트렌드를 분석합니다."""
        
        base_analysis = self.industry_knowledge.get(industry, {
            "key_trends": ["디지털 혁신", "클라우드 도입", "데이터 활용"],
            "regulations": ["일반 법규"],
            "success_factors": ["기술력", "비용 효율성"]
        })
        
        # Azure AI를 사용한 추가 시장 분석
        try:
            prompt = f"""
{industry} 산업의 현재 시장 동향과 기술 트렌드를 분석해주세요.

다음 관점에서 분석해주세요:
1. 주요 기술 동향
2. 시장 성장률
3. 주요 플레이어
4. 미래 전망

분석 결과:
"""
            ai_analysis = await azure_client.generate_completion(prompt, max_tokens=800)
            
            market_analysis = {
                "key_trends": base_analysis["key_trends"],
                "market_size": "분석 중",
                "growth_rate": "분석 중",
                "key_players": ["주요 기업 분석 중"],
                "future_outlook": ai_analysis,
                "regulations": base_analysis["regulations"]
            }
        except:
            market_analysis = {
                "key_trends": base_analysis["key_trends"],
                "market_size": "데이터 부족",
                "growth_rate": "추정 중",
                "key_players": ["분석 필요"],
                "future_outlook": f"{industry} 산업은 지속적인 디지털 혁신이 예상됩니다.",
                "regulations": base_analysis["regulations"]
            }
        
        return market_analysis
    
    async def _analyze_client_context(self, client_info: str, industry: str) -> Dict[str, Any]:
        """고객 맥락을 분석합니다."""
        
        client_analysis = {
            "organization_type": "분석 중",
            "size": "분석 중",
            "maturity_level": "중간",
            "key_challenges": [],
            "opportunities": []
        }
        
        # 고객 정보에서 주요 키워드 추출
        if "대기업" in client_info or "대형" in client_info:
            client_analysis["size"] = "대기업"
            client_analysis["opportunities"].append("대규모 프로젝트 수행 가능")
        elif "중소기업" in client_info or "SME" in client_info:
            client_analysis["size"] = "중소기업"
            client_analysis["opportunities"].append("신속한 의사결정 가능")
        
        # 조직 유형 판단
        if "공공" in client_info or "정부" in client_info:
            client_analysis["organization_type"] = "공공기관"
            client_analysis["key_challenges"].append("규제 준수 요구사항")
        elif "은행" in client_info or "금융" in client_info:
            client_analysis["organization_type"] = "금융기관"
            client_analysis["key_challenges"].append("높은 보안 요구사항")
        
        return client_analysis
    
    async def _analyze_competitive_landscape(self, industry: str, project_scope: str) -> List[str]:
        """경쟁 환경을 분석합니다."""
        
        competitive_factors = []
        
        # 산업별 주요 경쟁사 특성
        if industry == "금융":
            competitive_factors = [
                "기존 SI 업체들의 금융 경험",
                "핀테크 기업들의 혁신적 솔루션",
                "글로벌 IT 기업들의 클라우드 서비스",
                "금융권 내부 IT 조직의 역량 강화"
            ]
        elif industry == "제조":
            competitive_factors = [
                "제조 전문 SI 업체들의 도메인 지식",
                "글로벌 MES/ERP 벤더들",
                "IoT/스마트팩토리 전문 업체들",
                "자동화 장비 업체들의 소프트웨어 확장"
            ]
        else:
            competitive_factors = [
                "기존 SI 업체들의 시장 점유율",
                "클라우드 기반 솔루션 제공업체",
                "전문 컨설팅 업체들",
                "글로벌 IT 서비스 기업들"
            ]
        
        # 프로젝트 스코프에 따른 추가 경쟁 요소
        if "AI" in project_scope or "인공지능" in project_scope:
            competitive_factors.append("AI 전문 기업들의 기술적 우위")
        
        if "클라우드" in project_scope:
            competitive_factors.append("클라우드 네이티브 기업들의 전문성")
        
        return competitive_factors
    
    async def _generate_strategic_recommendations(self, industry: str, client_info: str, 
                                                 project_scope: str, market_analysis: Dict) -> List[str]:
        """전략적 권고사항을 생성합니다."""
        
        recommendations = []
        
        # 산업별 기본 전략
        if industry == "금융":
            recommendations.extend([
                "금융 규제 준수를 최우선으로 하는 솔루션 설계",
                "기존 금융 시스템과의 안정적 연동 방안 제시",
                "보안성과 가용성을 강조한 아키텍처 구성"
            ])
        elif industry == "공공":
            recommendations.extend([
                "투명성과 공정성을 보장하는 시스템 구축",
                "시민 접근성 향상을 위한 UI/UX 개선",
                "데이터 개방과 활용을 고려한 설계"
            ])
        
        # 프로젝트 스코프에 따른 전략
        if "디지털 전환" in project_scope:
            recommendations.append("단계적 디지털 전환 로드맵 제시")
        
        if "데이터" in project_scope:
            recommendations.append("데이터 거버넌스 체계 구축 방안 포함")
        
        # 고객 특성에 따른 전략
        if "중소기업" in client_info:
            recommendations.append("비용 효율적이면서 확장 가능한 솔루션 제안")
        
        # Azure AI를 활용한 추가 권고사항 생성
        try:
            prompt = f"""
다음 조건에 맞는 IT 프로젝트 수주를 위한 전략적 권고사항을 3가지 제시해주세요:

산업: {industry}
고객 정보: {client_info}
프로젝트 범위: {project_scope}

권고사항:
"""
            ai_recommendations = await azure_client.generate_completion(prompt, max_tokens=400)
            ai_rec_list = [rec.strip() for rec in ai_recommendations.split('\n') if rec.strip()]
            recommendations.extend(ai_rec_list[:3])
        except:
            pass
        
        return recommendations[:8]  # 최대 8개로 제한
    
    async def _identify_success_factors(self, industry: str, project_scope: str) -> List[str]:
        """성공 요인을 식별합니다."""
        
        base_factors = self.industry_knowledge.get(industry, {}).get("success_factors", [])
        success_factors = base_factors.copy()
        
        # 프로젝트 스코프에 따른 추가 성공 요인
        if "AI" in project_scope:
            success_factors.extend(["데이터 품질", "알고리즘 정확도", "학습 데이터 확보"])
        
        if "클라우드" in project_scope:
            success_factors.extend(["마이그레이션 전략", "클라우드 보안", "비용 최적화"])
        
        if "모바일" in project_scope:
            success_factors.extend(["사용자 경험", "성능 최적화", "다양한 디바이스 지원"])
        
        return list(set(success_factors))[:10]
    
    async def _identify_challenges(self, industry: str, client_info: str, project_scope: str) -> List[str]:
        """잠재적 도전과제를 식별합니다."""
        
        challenges = []
        
        # 산업별 공통 도전과제
        if industry == "금융":
            challenges.extend([
                "엄격한 금융 규제 준수",
                "24/7 무중단 서비스 요구사항",
                "레거시 시스템과의 복잡한 연동"
            ])
        elif industry == "공공":
            challenges.extend([
                "복잡한 행정 절차와 승인 과정",
                "다양한 이해관계자 조율",
                "예산 제약과 투명성 요구"
            ])
        
        # 기술적 도전과제
        if "AI" in project_scope:
            challenges.append("AI 모델의 신뢰성과 설명가능성 확보")
        
        if "빅데이터" in project_scope:
            challenges.append("대용량 데이터 처리와 실시간 분석")
        
        # 조직적 도전과제
        if "대기업" in client_info:
            challenges.append("복잡한 의사결정 구조와 긴 승인 과정")
        
        return challenges[:8]
    
    async def _recommend_approach(self, industry: str, project_scope: str, 
                                 strategic_recommendations: List[str]) -> str:
        """권장 접근법을 제안합니다."""
        
        approach_elements = []
        
        # 산업별 접근법
        if industry == "금융":
            approach_elements.append("금융권 경험이 풍부한 전문가 투입")
        elif industry == "공공":
            approach_elements.append("공공부문 프로젝트 수행 경험 강조")
        
        # 기술적 접근법
        if "AI" in project_scope:
            approach_elements.append("POC를 통한 단계적 AI 도입")
        
        if "클라우드" in project_scope:
            approach_elements.append("하이브리드 클라우드 전략 수립")
        
        # 프로젝트 관리 접근법
        approach_elements.extend([
            "애자일 방법론을 활용한 반복적 개발",
            "고객과의 긴밀한 소통과 피드백 반영",
            "위험 관리와 품질 보증 체계 구축"
        ])
        
        return " → ".join(approach_elements)