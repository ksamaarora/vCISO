# /app/api/v1/endpoints/plans.py
from fastapi import APIRouter, HTTPException
from app.schemas.plan_schema import OnboardingRequest, PlanResponse
from app.services.plan_generator import PlanGeneratorService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
plan_service = PlanGeneratorService()


@router.post("/generate", response_model=PlanResponse)
async def generate_plan(request: OnboardingRequest):
    """Generate IR plan from onboarding data"""
    try:
        # Convert request schema to OnboardingData model
        onboarding_data = request.to_onboarding_data()
        
        # Generate plan
        plan = await plan_service.generate(onboarding_data)
        
        return PlanResponse(
            success=True,
            plan=plan.markdown,
            metadata=plan.metadata
        )
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating plan: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")