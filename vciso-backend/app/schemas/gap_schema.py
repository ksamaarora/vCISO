# vciso-backend/app/schemas/gap_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.models.gap_analysis import GapAnalysisResult

class GapAnalysisRequest(BaseModel):
    """Request schema for gap analysis"""
    plan_markdown: str = Field(
        ...,
        min_length=100,
        description="The IR plan to analyze (Markdown format)"
    )
    company_name: str = Field(
        ...,
        min_length=2,
        description="Company name"
    )

class GapAnalysisResponse(BaseModel):
    """Response schema for gap analysis"""
    success: bool = Field(..., description="Whether analysis succeeded")
    gap_analysis: GapAnalysisResult = Field(..., description="Gap analysis results")