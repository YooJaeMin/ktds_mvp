from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class RFPAnalysisRequest(BaseModel):
    document_content: str
    filename: str

class RFPAnalysisResult(BaseModel):
    requirements: List[str]
    technical_specs: List[str]
    timeline: Optional[str]
    budget_info: Optional[str]
    risk_assessment: Dict[str, str]
    compliance_requirements: List[str]
    evaluation_criteria: List[str]
    confidence_score: float

class StrategyAnalysisRequest(BaseModel):
    industry: str
    client_info: str
    project_scope: str

class StrategyAnalysisResult(BaseModel):
    market_analysis: Dict[str, Any]
    competitive_landscape: List[str]
    strategic_recommendations: List[str]
    success_factors: List[str]
    potential_challenges: List[str]
    recommended_approach: str

class QualityCheckResult(BaseModel):
    overall_score: float
    section_scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    compliance_check: Dict[str, bool]
    readability_score: float

class KnowledgeSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None

class KnowledgeSearchResult(BaseModel):
    results: List[Dict[str, Any]]
    total_count: int
    search_time: float

class DocumentUploadResult(BaseModel):
    document_id: str
    filename: str
    category: str
    status: str
    indexed_at: datetime