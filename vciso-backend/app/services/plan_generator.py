# /app/services/plan_generator.py
from app.core.meta_prompting import MetaPromptEngine
from app.core.llm_client import OpenAIClient
from app.core.guardrails import PII_Redactor
from app.models.plan import OnboardingData, GeneratedPlan
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PlanGeneratorService:
    def __init__(self):
        self.meta_engine = MetaPromptEngine()
        self.llm_client = OpenAIClient()
        self.pii_redactor = PII_Redactor()
    
    async def generate(self, data: OnboardingData) -> GeneratedPlan:
        """Generate IR plan from onboarding data"""
        
        logger.info(f"Generating plan for: {data.companyName}")
        
        # Step 1: Build meta-prompt
        system_prompt = self.meta_engine.system_prompt
        user_prompt = self.meta_engine.build_prompt(data)
        
        # Step 2: Apply guardrails (query classification)
        validated_prompt = self.meta_engine.apply_guardrails(user_prompt)
        
        # Step 3: Call OpenAI API
        plan_markdown = await self.llm_client.generate_plan(
            system_prompt=system_prompt,
            user_prompt=validated_prompt
        )
        
        # Step 4: Post-process (PII redaction)
        clean_plan = self.pii_redactor.redact(plan_markdown)
        
        # Step 5: Validate output structure
        validated_plan = self._validate_plan_structure(clean_plan)
        
        # Step 6: Return structured response
        return GeneratedPlan(
            markdown=validated_plan,
            metadata={
                "company": data.companyName,
                "industry": data.industry,
                "employee_count": data.employeeCount,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }
        )
    
    def _validate_plan_structure(self, plan: str) -> str:
        """Ensure plan has required sections"""
        required_sections = [
            "Executive Summary",
            "Incident Response Team",
            "Response Procedures",
            "Communication Plan"
        ]
        
        missing_sections = [s for s in required_sections if s not in plan]
        
        if missing_sections:
            logger.warning(f"Plan missing sections: {missing_sections}")
            # In production, you might retry or add missing sections
        
        return plan