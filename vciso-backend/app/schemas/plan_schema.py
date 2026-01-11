from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from app.models.plan import OnboardingData


class ToolsDataSchema(BaseModel):
    """Technology tools schema for API"""
    email: List[str] = Field(default_factory=list)
    storage: List[str] = Field(default_factory=list)
    communication: List[str] = Field(default_factory=list)
    crm: List[str] = Field(default_factory=list)


class SecurityLeadSchema(BaseModel):
    """Security lead schema for API"""
    type: str = Field(..., description="Type: dedicated, consultant, owner, none")
    name: Optional[str] = Field(None, description="Name if type is 'dedicated'")


class OnboardingRequest(BaseModel):
    """Request schema for onboarding data"""
    companyName: str = Field(..., min_length=2, description="Company name")
    employeeCount: str = Field(..., description="10-50, 51-200, 201-500, 500+")
    industry: str = Field(..., description="healthcare, finance, retail, manufacturing, tech, services, other")
    tools: ToolsDataSchema
    currentSecurity: List[str] = Field(default_factory=list)
    mainConcerns: List[str] = Field(..., min_length=1, description="At least one concern required")
    securityLead: SecurityLeadSchema

    def to_onboarding_data(self) -> OnboardingData:
        """Convert schema to OnboardingData model"""
        from app.models.plan import ToolsData, SecurityLead
        
        return OnboardingData(
            companyName=self.companyName,
            employeeCount=self.employeeCount,
            industry=self.industry,
            tools=ToolsData(
                email=self.tools.email,
                storage=self.tools.storage,
                communication=self.tools.communication,
                crm=self.tools.crm
            ),
            currentSecurity=self.currentSecurity,
            mainConcerns=self.mainConcerns,
            securityLead=SecurityLead(
                type=self.securityLead.type,
                name=self.securityLead.name
            )
        )


class PlanResponse(BaseModel):
    """Response schema for generated plan"""
    success: bool = Field(..., description="Whether generation was successful")
    plan: str = Field(..., description="Generated plan in Markdown format")
    metadata: Dict[str, Any] = Field(..., description="Plan metadata")
