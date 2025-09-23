from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from typing import List, Optional

from app.services.rfp_analyzer import RFPAnalyzer
from app.services.strategy_support import StrategySupport
from app.services.quality_manager import QualityManager
from app.services.knowledge_manager import KnowledgeManager

app = FastAPI(
    title="KTDS MVP - AI Financial Business Strategy Services",
    description="AI services for IT company financial business acquisition strategy team",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize services
rfp_analyzer = RFPAnalyzer()
strategy_support = StrategySupport()
quality_manager = QualityManager()
knowledge_manager = KnowledgeManager()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Service 1: RFP Analysis Automation
@app.post("/api/rfp/analyze")
async def analyze_rfp(file: UploadFile = File(...)):
    """RFP 문서를 분석하여 주요 요구사항과 위험도를 평가합니다."""
    try:
        content = await file.read()
        analysis = await rfp_analyzer.analyze_document(content, file.filename)
        return JSONResponse(content=analysis)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/rfp-analyzer", response_class=HTMLResponse)
async def rfp_analyzer_page(request: Request):
    return templates.TemplateResponse("rfp_analyzer.html", {"request": request})

# Service 2: Business Understanding & Strategy Support
@app.post("/api/strategy/analyze")
async def analyze_strategy(
    industry: str = Form(...),
    client_info: str = Form(...),
    project_scope: str = Form(...)
):
    """사업 분야와 고객 정보를 바탕으로 전략적 분석을 제공합니다."""
    try:
        analysis = await strategy_support.analyze_business_context(
            industry, client_info, project_scope
        )
        return JSONResponse(content=analysis)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/strategy-support", response_class=HTMLResponse)
async def strategy_support_page(request: Request):
    return templates.TemplateResponse("strategy_support.html", {"request": request})

# Service 3: Proposal Quality Management
@app.post("/api/quality/check")
async def check_proposal_quality(file: UploadFile = File(...)):
    """제안서의 품질을 평가하고 개선 사항을 제안합니다."""
    try:
        content = await file.read()
        quality_report = await quality_manager.evaluate_proposal(content, file.filename)
        return JSONResponse(content=quality_report)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/quality-manager", response_class=HTMLResponse)
async def quality_manager_page(request: Request):
    return templates.TemplateResponse("quality_manager.html", {"request": request})

# Service 4: Knowledge Management
@app.post("/api/knowledge/search")
async def search_knowledge(
    query: str = Form(...),
    category: Optional[str] = Form(None)
):
    """지식 베이스에서 관련 정보를 검색합니다."""
    try:
        results = await knowledge_manager.search_knowledge(query, category)
        return JSONResponse(content=results)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/knowledge/upload")
async def upload_knowledge(
    file: UploadFile = File(...),
    category: str = Form(...),
    description: str = Form(...)
):
    """새로운 지식 문서를 업로드하고 인덱싱합니다."""
    try:
        content = await file.read()
        result = await knowledge_manager.add_document(content, file.filename, category, description)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/knowledge-manager", response_class=HTMLResponse)
async def knowledge_manager_page(request: Request):
    return templates.TemplateResponse("knowledge_manager.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )