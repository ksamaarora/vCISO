import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.plan_generator import PlanGeneratorService
from app.models.plan import OnboardingData, ToolsData, SecurityLead


class TestPlanGeneratorService:
    """Test PlanGeneratorService"""
    
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
            currentSecurity=["MFA"],
            mainConcerns=["Ransomware"],
            securityLead=SecurityLead(type="owner")
        )
    
    @pytest.fixture
    def mock_llm_response(self):
        """Mock LLM response"""
        mock_response = Mock()
        mock_response.content = [Mock(text="# IR Plan\n\nTest content")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=200)
        return mock_response
    
    @pytest.mark.asyncio
    async def test_generate_plan_success(self, sample_data, mock_llm_response):
        """Test successful plan generation"""
        with patch('app.services.plan_generator.OpenAIClient') as mock_client_class, \
             patch('app.services.plan_generator.PII_Redactor') as mock_redactor_class:
            
            # Setup mocks
            mock_client = Mock()
            mock_client.generate_plan = AsyncMock(return_value="# IR Plan\n\nTest content")
            mock_client_class.return_value = mock_client
            
            mock_redactor = Mock()
            mock_redactor.redact = Mock(return_value="# IR Plan\n\nTest content")
            mock_redactor_class.return_value = mock_redactor
            
            # Test
            service = PlanGeneratorService()
            result = await service.generate(sample_data)
            
            assert result.markdown == "# IR Plan\n\nTest content"
            assert result.metadata["company"] == "Test Corp"
            assert result.metadata["industry"] == "tech"
            assert "generated_at" in result.metadata
    
    def test_validate_plan_structure_complete(self):
        """Test plan structure validation with complete plan"""
        service = PlanGeneratorService()
        plan = """
        # IR Plan
        
        ## 1. Executive Summary
        Overview here
        
        ## 2. Incident Response Team
        Team info
        
        ## 4. Response Procedures
        Procedures here
        
        ## 5. Communication Plan
        Communication details
        """
        result = service._validate_plan_structure(plan)
        assert result == plan
    
    def test_validate_plan_structure_missing_sections(self):
        """Test plan structure validation with missing sections"""
        service = PlanGeneratorService()
        plan = "# IR Plan\n\nSome content"
        # Should still return the plan but log warning
        result = service._validate_plan_structure(plan)
        assert result == plan
