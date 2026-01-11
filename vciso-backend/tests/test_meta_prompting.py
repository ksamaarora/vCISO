import pytest
from app.core.meta_prompting import MetaPromptEngine
from app.models.plan import OnboardingData, ToolsData, SecurityLead


class TestMetaPromptEngine:
    """Test meta-prompting engine"""
    
    @pytest.fixture
    def engine(self):
        return MetaPromptEngine()
    
    @pytest.fixture
    def sample_data(self):
        return OnboardingData(
            companyName="Test Corp",
            employeeCount="10-50",
            industry="tech",
            tools=ToolsData(
                email=["Gmail"],
                storage=["Google Drive"],
                communication=["Slack"]
            ),
            currentSecurity=["MFA", "Antivirus"],
            mainConcerns=["Ransomware", "Phishing"],
            securityLead=SecurityLead(type="dedicated", name="John Doe")
        )
    
    def test_system_prompt_loaded(self, engine):
        """Test that system prompt is loaded"""
        assert engine.system_prompt is not None
        assert "cybersecurity expert" in engine.system_prompt.lower()
        assert "Incident Response" in engine.system_prompt
    
    def test_build_prompt(self, engine, sample_data):
        """Test prompt building"""
        prompt = engine.build_prompt(sample_data)
        
        assert "Test Corp" in prompt
        assert "tech" in prompt
        assert "10-50" in prompt
        assert "Gmail" in prompt
        assert "Google Drive" in prompt
        assert "Slack" in prompt
        assert "MFA" in prompt
        assert "Ransomware" in prompt
        assert "Phishing" in prompt
        assert "John Doe" in prompt
    
    def test_format_security_lead_dedicated(self, engine):
        """Test formatting dedicated security lead"""
        lead = SecurityLead(type="dedicated", name="Jane Smith")
        result = engine._format_security_lead(lead)
        assert "Dedicated IT person" in result
        assert "Jane Smith" in result
    
    def test_format_security_lead_consultant(self, engine):
        """Test formatting consultant security lead"""
        lead = SecurityLead(type="consultant")
        result = engine._format_security_lead(lead)
        assert "External IT consultant" in result
    
    def test_format_security_lead_owner(self, engine):
        """Test formatting owner security lead"""
        lead = SecurityLead(type="owner")
        result = engine._format_security_lead(lead)
        assert "CEO/Business Owner" in result
    
    def test_format_security_lead_none(self, engine):
        """Test formatting no security lead"""
        lead = SecurityLead(type="none")
        result = engine._format_security_lead(lead)
        assert "No designated security lead" in result
    
    def test_apply_guardrails(self, engine, sample_data):
        """Test guardrails application"""
        prompt = engine.build_prompt(sample_data)
        validated = engine.apply_guardrails(prompt)
        # Currently just returns the prompt, but structure is there for future enhancement
        assert validated == prompt
