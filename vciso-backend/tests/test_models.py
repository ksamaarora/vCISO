import pytest
from app.models.plan import OnboardingData, ToolsData, SecurityLead, GeneratedPlan
from pydantic import ValidationError


class TestOnboardingData:
    """Test OnboardingData model"""
    
    def test_valid_onboarding_data(self):
        """Test creating valid onboarding data"""
        data = OnboardingData(
            companyName="Test Company",
            employeeCount="10-50",
            industry="tech",
            tools=ToolsData(
                email=["Gmail"],
                storage=["Google Drive"],
                communication=["Slack"]
            ),
            currentSecurity=["MFA"],
            mainConcerns=["Ransomware"],
            securityLead=SecurityLead(type="owner")
        )
        assert data.companyName == "Test Company"
        assert data.employeeCount == "10-50"
        assert len(data.mainConcerns) >= 1
    
    def test_invalid_company_name_too_short(self):
        """Test validation for company name"""
        with pytest.raises(ValidationError):
            OnboardingData(
                companyName="A",  # Too short
                employeeCount="10-50",
                industry="tech",
                tools=ToolsData(),
                mainConcerns=["Ransomware"],
                securityLead=SecurityLead(type="owner")
            )
    
    def test_invalid_main_concerns_empty(self):
        """Test validation for main concerns"""
        with pytest.raises(ValidationError):
            OnboardingData(
                companyName="Test Company",
                employeeCount="10-50",
                industry="tech",
                tools=ToolsData(),
                mainConcerns=[],  # Empty - should fail
                securityLead=SecurityLead(type="owner")
            )
    
    def test_default_values(self):
        """Test default values for optional fields"""
        data = OnboardingData(
            companyName="Test Company",
            employeeCount="10-50",
            industry="tech",
            tools=ToolsData(),
            mainConcerns=["Ransomware"],
            securityLead=SecurityLead(type="owner")
        )
        assert data.currentSecurity == []
        assert data.tools.email == []
        assert data.tools.storage == []


class TestSecurityLead:
    """Test SecurityLead model"""
    
    def test_dedicated_with_name(self):
        """Test dedicated security lead with name"""
        lead = SecurityLead(type="dedicated", name="John Doe")
        assert lead.type == "dedicated"
        assert lead.name == "John Doe"
    
    def test_dedicated_without_name(self):
        """Test dedicated security lead without name (optional)"""
        lead = SecurityLead(type="dedicated")
        assert lead.type == "dedicated"
        assert lead.name is None


class TestGeneratedPlan:
    """Test GeneratedPlan model"""
    
    def test_valid_generated_plan(self):
        """Test creating valid generated plan"""
        plan = GeneratedPlan(
            markdown="# IR Plan\n\nContent here",
            metadata={"company": "Test Corp", "industry": "tech"}
        )
        assert plan.markdown.startswith("# IR Plan")
        assert "company" in plan.metadata
