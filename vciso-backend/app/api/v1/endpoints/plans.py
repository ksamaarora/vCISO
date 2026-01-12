# /app/api/v1/endpoints/plans.py
from fastapi import APIRouter, HTTPException
from app.schemas.plan_schema import OnboardingRequest, PlanResponse
from app.services.plan_generator import PlanGeneratorService
import logging

# plans.py - API endpoint for generating IR plans
# This module defines the /generate endpoint for creating incident response plans based on onboarding data.
# It uses the PlanGeneratorService to process the data and return the generated plan.
# It includes error handling for validation and general exceptions.

# Endpoint to generate IR plan
# POST /generate
# Request Body: OnboardingRequest
# Response Body: PlanResponse
# Errors: 400 (Validation Error), 500 (Internal Server Error)

logger = logging.getLogger(__name__)

router = APIRouter()
plan_service = PlanGeneratorService()

# How the code works:
# 1. The endpoint accepts a POST request with onboarding data.
# 2. It converts the request data into the OnboardingData model.
# 3. It calls the PlanGeneratorService to generate the IR plan.
# 4. It returns the generated plan in the response.
# 5. It handles validation errors and other exceptions, logging them appropriately.

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