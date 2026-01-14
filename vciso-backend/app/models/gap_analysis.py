# vciso-backend/app/models/gap_analysis.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class GapSeverity(str, Enum):
    """Severity levels for identified gaps"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Gap(BaseModel):
    """Individual gap in the IR plan"""
    id: str = Field(..., description="Unique gap identifier")
    section: str = Field(..., description="IR plan section with gap")
    severity: GapSeverity = Field(..., description="Gap severity level")
    description: str = Field(..., description="What's missing or inadequate")
    recommendation: str = Field(..., description="How to fix the gap")
    framework_references: List[str] = Field(
        default_factory=list,
        description="Citations from frameworks (e.g., 'NIST SP 800-61, Section 3.2')"
    )
    estimated_effort: str = Field(..., description="Time to implement (e.g., '1-2 weeks')")

class GapAnalysisResult(BaseModel):
    """Complete gap analysis result"""
    company_name: str
    analysis_timestamp: str
    overall_score: int = Field(..., ge=0, le=100, description="Overall compliance score (0-100)")
    gaps: List[Gap] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list, description="What the plan does well")
    priority_actions: List[str] = Field(
        default_factory=list,
        description="Top 3-5 actions to take first"
    )
    framework_compliance: Dict[str, int] = Field(
        default_factory=dict,
        description="Compliance scores per framework (e.g., {'NIST': 75, 'CISA': 68})"
    )
    enhanced_plan: Optional[str] = Field(
        None,
        description="Enhanced IR plan with gaps addressed (Markdown)"
    )