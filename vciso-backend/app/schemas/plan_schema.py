# vciso-backend/app/schemas/plan_schema.py
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from app.models.plan import OnboardingData

# plan_schema.py - Schemas for API requests and responses
# This module defines Pydantic schemas for the onboarding request data and the generated plan response.
# It includes conversion methods to transform request schemas into internal models used for plan generation.

# ToolsDataSchema: 
# Schema for technology tools used by the company.
# email, storage, communication, crm

class ToolsDataSchema(BaseModel):
    """Technology tools schema for API"""
    email: List[str] = Field(default_factory=list)
    storage: List[str] = Field(default_factory=list)
    communication: List[str] = Field(default_factory=list)
    crm: List[str] = Field(default_factory=list)

# SecurityLeadSchema: 
# Schema for security lead information.
# type (dedicated, consultant, owner, none), name (if dedicated)

class SecurityLeadSchema(BaseModel):
    """Security lead schema for API"""
    type: str = Field(..., description="Type: dedicated, consultant, owner, none")
    name: Optional[str] = Field(None, description="Name if type is 'dedicated'")

# OnboardingRequest:
# Request schema for onboarding data
# companyName, employeeCount, industry, tools, currentSecurity, mainConcerns, securityLead

class OnboardingRequest(BaseModel):
    """Request schema for onboarding data"""
    companyName: str = Field(..., min_length=2, description="Company name")
    employeeCount: str = Field(..., description="10-50, 51-200, 201-500, 500+")
    industry: str = Field(..., description="healthcare, finance, retail, manufacturing, tech, services, other")
    tools: ToolsDataSchema
    currentSecurity: List[str] = Field(default_factory=list)
    mainConcerns: List[str] = Field(..., min_length=1, description="At least one concern required")
    securityLead: SecurityLeadSchema

    # Convert schema to internal model
    # This method transforms the OnboardingRequest schema into the OnboardingData model used internally.
    # How this works:
    # 1. It imports the necessary models from app.models.plan.
    # 2. It constructs and returns an OnboardingData instance using the data from the schema.
    # 3. It maps nested schemas (ToolsDataSchema and SecurityLeadSchema) to their corresponding models.
    # This allows seamless integration between the API layer and the business logic layer.

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

# PlanResponse:
# Response schema for generated plan
# success, plan, metadata

class PlanResponse(BaseModel):
    """Response schema for generated plan"""
    success: bool = Field(..., description="Whether generation was successful")
    plan: str = Field(..., description="Generated plan in Markdown format")
    metadata: Dict[str, Any] = Field(..., description="Plan metadata")
