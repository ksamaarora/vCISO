import pytest
from app.schemas.plan_schema import (
    OnboardingRequest,
    PlanResponse,
    ToolsDataSchema,
    SecurityLeadSchema
)
from pydantic import ValidationError


class TestOnboardingRequest:
    """Test OnboardingRequest schema"""
    
    def test_valid_request(self):
        """Test valid onboarding request"""
        request = OnboardingRequest(
            companyName="Test Company",
            employeeCount="10-50",
            industry="tech",
            tools=ToolsDataSchema(
                email=["Gmail"],
                storage=["Google Drive"],
                communication=["Slack"]
            ),
            mainConcerns=["Ransomware"],
            securityLead=SecurityLeadSchema(type="owner")
        )
        assert request.companyName == "Test Company"
    
    def test_to_onboarding_data(self):
        """Test conversion to OnboardingData"""
        from app.models.plan import OnboardingData
        
        request = OnboardingRequest(
            companyName="Test Company",
            employeeCount="10-50",
            industry="tech",
            tools=ToolsDataSchema(),
            mainConcerns=["Ransomware"],
            securityLead=SecurityLeadSchema(type="dedicated", name="John Doe")
        )
        data = request.to_onboarding_data()
        assert isinstance(data, OnboardingData)
        assert data.companyName == "Test Company"
        assert data.securityLead.name == "John Doe"


class TestPlanResponse:
    """Test PlanResponse schema"""
    
    def test_valid_response(self):
        """Test valid plan response"""
        response = PlanResponse(
            success=True,
            plan="# IR Plan\n\nContent",
            metadata={"company": "Test Corp"}
        )
        assert response.success is True
        assert "# IR Plan" in response.plan
        assert "company" in response.metadata
