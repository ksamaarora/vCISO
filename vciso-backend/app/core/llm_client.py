# /app/core/llm_client.py
from openai import AsyncOpenAI
from typing import Optional, Dict, Any
import logging
from app.config import settings

# llm_client.py - Module for interacting with OpenAI API
# This module provides a client for generating incident response plans using OpenAI's language models.
# It handles API requests, responses, error handling, and usage logging for cost tracking.
# The OpenAIClient class encapsulates the functionality to communicate with the OpenAI API asynchronously.
# It includes methods to generate plans based on system and user prompts, and logs token usage for cost analysis.

# How the code works:
# 1. The OpenAIClient class initializes with API key, model, and max tokens from settings.
# 2. The generate_plan method sends a request to the OpenAI API with system and user prompts.
# 3. It processes the response to extract the generated plan text.
# 4. It logs token usage for cost tracking based on the model used.

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        # Initialize OpenAI client - let it handle http client creation internally
        # Initialize with API key from settings
        # Set model and max tokens from settings
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    async def generate_plan(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: Optional[float] = None
    ) -> str:
        """Generate IR plan using OpenAI"""
        
        if temperature is None:
            temperature = settings.OPENAI_TEMPERATURE
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract text from response
            plan_text = response.choices[0].message.content
            
            if not plan_text:
                raise ValueError("Empty response from OpenAI API")
            
            # Log usage for cost tracking
            self._log_usage(response.usage)
            
            return plan_text
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _log_usage(self, usage):
        """Log token usage for cost tracking"""
        if not usage:
            return
            
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        # OpenAI GPT-4o pricing (as of 2025)
        # Pricing varies by model, using GPT-4o as default
        if "gpt-4o" in self.model.lower() or "gpt-4" in self.model.lower():
            input_cost = (input_tokens / 1_000_000) * 2.50  # $2.50 per 1M input tokens
            output_cost = (output_tokens / 1_000_000) * 10.00  # $10 per 1M output tokens
        elif "gpt-3.5" in self.model.lower():
            input_cost = (input_tokens / 1_000_000) * 0.50  # $0.50 per 1M input tokens
            output_cost = (output_tokens / 1_000_000) * 1.50  # $1.50 per 1M output tokens
        else:
            # Default pricing (can be adjusted based on model)
            input_cost = (input_tokens / 1_000_000) * 2.50
            output_cost = (output_tokens / 1_000_000) * 10.00
            
        total_cost = input_cost + output_cost
        
        logger.info(f"API Usage - Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}, Cost: ${total_cost:.4f}")