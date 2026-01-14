# vciso-backend/app/api/v1/endpoints/gap_analysis.py
from fastapi import APIRouter, HTTPException
from app.schemas.gap_schema import GapAnalysisRequest, GapAnalysisResponse
from app.services.gap_analyzer import GapAnalyzer
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
gap_analyzer = GapAnalyzer()

@router.post("/analyze", response_model=GapAnalysisResponse)
async def analyze_plan(request: GapAnalysisRequest):
    """
    Analyze an IR plan and identify gaps against frameworks
    
    Request Body:
    {
        "plan_markdown": "# Incident Response Plan...",
        "company_name": "Acme Corp"
    }
    
    Response:
    {
        "success": true,
        "gap_analysis": {
            "company_name": "Acme Corp",
            "overall_score": 78,
            "gaps": [...],
            "strengths": [...],
            "priority_actions": [...],
            "framework_compliance": {"NIST": 75, "CISA": 68, "SANS": 82}
        }
    }
    """
    try:
        logger.info(f"Analyzing plan for: {request.company_name}")
        
        # Perform gap analysis
        result = await gap_analyzer.analyze_plan(
            plan_markdown=request.plan_markdown,
            company_name=request.company_name
        )
        
        return GapAnalysisResponse(
            success=True,
            gap_analysis=result
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing plan: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze plan: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check for gap analysis service"""
    try:
        # Test vector DB connectivity
        from app.core.vector_db import VectorDBService
        vector_db = VectorDBService()
        stats = vector_db.index.describe_index_stats()
        
        return {
            "status": "healthy",
            "vector_db_status": "connected",
            "total_vectors": stats.total_vector_count
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Gap analysis service unhealthy"
        )