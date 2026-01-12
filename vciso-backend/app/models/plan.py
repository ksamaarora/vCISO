# vciso-backend/app/models/plan.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# plan.py - Models for onboarding data and generated IR plans
# This module defines Pydantic models for the onboarding data collected from users
# and the structure of the generated incident response plans.

# classes:

# - ToolsData: Represents the technology tools used by the company.
#                email, storage, communication, crm

# - SecurityLead: Represents information about who handles security.
#                type (dedicated, consultant, owner, none), name (if dedicated)

# - OnboardingData: Represents the complete onboarding data collected from the user.
#                companyName, employeeCount, industry, tools, currentSecurity, mainConcerns, securityLead

# - GeneratedPlan: Represents the generated IR plan with its content and metadata.
#                 markdown, metadata

class ToolsData(BaseModel):
    """Technology tools used by the company"""
    email: List[str] = Field(default_factory=list, description="Email tools (Gmail, Outlook, etc.)")
    storage: List[str] = Field(default_factory=list, description="Storage tools (Google Drive, Dropbox, etc.)")
    communication: List[str] = Field(default_factory=list, description="Communication tools (Slack, Teams, etc.)")
    crm: List[str] = Field(default_factory=list, description="CRM tools (Salesforce, HubSpot, etc.)")


class SecurityLead(BaseModel):
    """Information about who handles security"""
    type: str = Field(..., description="Type of security lead: dedicated, consultant, owner, none")
    name: Optional[str] = Field(None, description="Name of dedicated IT person (if type is 'dedicated')")


class OnboardingData(BaseModel):
    """Complete onboarding data collected from user"""
    companyName: str = Field(..., min_length=2, description="Company name")
    employeeCount: str = Field(..., description="Employee count range: 10-50, 51-200, 201-500, 500+")
    industry: str = Field(..., description="Industry: healthcare, finance, retail, manufacturing, tech, services, other")
    tools: ToolsData = Field(..., description="Technology tools used")
    currentSecurity: List[str] = Field(default_factory=list, description="Current security measures")
    mainConcerns: List[str] = Field(..., min_length=1, description="Main security concerns")
    securityLead: SecurityLead = Field(..., description="Who handles security")


class GeneratedPlan(BaseModel):
    """Generated IR plan with metadata"""
    markdown: str = Field(..., description="Plan content in Markdown format")
    metadata: Dict[str, Any] = Field(..., description="Plan metadata (company, industry, generated_at, etc.)")
