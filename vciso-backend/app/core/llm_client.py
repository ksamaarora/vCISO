# /app/core/llm_client.py
import anthropic
from typing import Optional, Dict, Any
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class ClaudeClient:
    def __init__(self):
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables")
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.CLAUDE_MAX_TOKENS
    
    async def generate_plan(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: Optional[float] = None
    ) -> str:
        """Generate IR plan using Claude"""
        
        if temperature is None:
            temperature = settings.CLAUDE_TEMPERATURE
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract text from response
            plan_text = response.content[0].text
            
            # Log usage for cost tracking
            self._log_usage(response.usage)
            
            return plan_text
            
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def _log_usage(self, usage: Dict[str, Any]):
        """Log token usage for cost tracking"""
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        
        # Claude Sonnet 4 pricing (as of Jan 2025)
        input_cost = (input_tokens / 1_000_000) * 3.00  # $3 per 1M input tokens
        output_cost = (output_tokens / 1_000_000) * 15.00  # $15 per 1M output tokens
        total_cost = input_cost + output_cost
        
        logger.info(f"API Usage - Input: {input_tokens}, Output: {output_tokens}, Cost: ${total_cost:.4f}")