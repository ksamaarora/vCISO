from app.core.meta_prompting import MetaPromptEngine
from app.core.llm_client import OpenAIClient
from app.core.guardrails import PII_Redactor
from app.models.plan import OnboardingData, GeneratedPlan
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

"""plan_generator.py - Service for generating incident response plans

How the code works:
1. The PlanGeneratorService class initializes
2. The generate method takes OnboardingData as input
3. It builds system and user prompts using MetaPromptEngine
4. It calls OpenAIClient to generate the plan text
5. It redacts any PII from the plan using PII_Redactor
6. It validates the plan structure and logs any missing sections
7. It returns a GeneratedPlan object containing the plan and metadata
"""


class PlanGeneratorService:
    """Generate incident response plans from onboarding data.

    Builds prompts, applies guardrails, calls the LLM, redacts PII, and returns
    a structured plan. Missing sections are logged but do not fail the request.
    """

    def __init__(self):
        self.meta_engine = MetaPromptEngine()
        self.llm_client = OpenAIClient()
        self.pii_redactor = PII_Redactor()

    async def generate(self, data: OnboardingData) -> GeneratedPlan:
        """Generate an IR plan and metadata for the provided onboarding data."""

        logger.info(f"Generating plan for: {data.companyName}")

        system_prompt = self.meta_engine.system_prompt
        user_prompt = self.meta_engine.build_prompt(data)
        validated_prompt = self.meta_engine.apply_guardrails(user_prompt)

        plan_markdown = await self.llm_client.generate_plan(
            system_prompt=system_prompt,
            user_prompt=validated_prompt,
        )

        clean_plan = self.pii_redactor.redact(plan_markdown)
        validated_plan = self._validate_plan_structure(clean_plan)

        return GeneratedPlan(
            markdown=validated_plan,
            metadata={
                "company": data.companyName,
                "industry": data.industry,
                "employee_count": data.employeeCount,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            },
        )

    def _validate_plan_structure(self, plan: str) -> str:
        """Log missing sections and return the plan unchanged."""
        required_sections = [
            "Executive Summary",
            "Incident Response Team",
            "Response Procedures",
            "Communication Plan",
        ]

        missing_sections = [s for s in required_sections if s not in plan]

        if missing_sections:
            logger.warning(f"Plan missing sections: {missing_sections}")

        return plan
