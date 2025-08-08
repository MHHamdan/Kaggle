"""
GPT-OSS-20B Client for Red-Teaming Challenge

This module provides a client wrapper for interacting with the OpenAI gpt-oss-20b model
with built-in safety features, logging, and rate limiting for red-teaming purposes.
"""

import os
import time
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import openai
from openai import OpenAI
from loguru import logger
import json


@dataclass
class ModelResponse:
    """Structured response from the model."""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    timestamp: float
    metadata: Dict[str, Any]


class GPTOSSClient:
    """
    Client for interacting with the gpt-oss-20b model.
    
    Features:
    - Rate limiting and retry logic
    - Response logging and caching
    - Safety content filtering
    - Usage tracking and monitoring
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-oss-20b",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        max_retries: int = 3,
        rate_limit_delay: float = 1.0,
        safe_mode: bool = True,
        enable_logging: bool = True
    ):
        """
        Initialize the GPT-OSS client.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            max_retries: Maximum retry attempts for failed requests
            rate_limit_delay: Delay between requests in seconds
            safe_mode: Enable content filtering and safety checks
            enable_logging: Enable detailed logging
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.safe_mode = safe_mode
        self.enable_logging = enable_logging
        
        # Initialize logging
        if enable_logging:
            logger.add("logs/gpt_oss_interactions.log", rotation="1 day", retention="30 days")
        
        # Usage tracking
        self.usage_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
        
        # Response cache for reproducibility
        self.response_cache = {}
        
        logger.info(f"GPTOSSClient initialized with model: {model}")
    
    def generate_response(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        cache_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ModelResponse:
        """
        Generate a response from the model.
        
        Args:
            prompt: User prompt (string or messages format)
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            cache_key: Optional cache key for reproducibility
            metadata: Additional metadata to store with response
            
        Returns:
            ModelResponse object with content and metadata
        """
        # Check cache first
        if cache_key and cache_key in self.response_cache:
            logger.info(f"Returning cached response for key: {cache_key}")
            return self.response_cache[cache_key]
        
        # Prepare messages
        messages = self._prepare_messages(prompt, system_prompt)
        
        # Safety check in safe mode
        if self.safe_mode:
            safety_check = self._safety_check(messages)
            if not safety_check["safe"]:
                logger.warning(f"Safety check failed: {safety_check['reason']}")
                # Could either block or log and continue based on requirements
        
        # Use provided parameters or defaults
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens
        
        # Attempt generation with retries
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                # Add rate limiting
                if attempt > 0:
                    time.sleep(self.rate_limit_delay * attempt)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=max_tok
                )
                
                # Extract response data
                content = response.choices[0].message.content
                usage = response.usage.__dict__ if response.usage else {}
                finish_reason = response.choices[0].finish_reason
                
                # Create structured response
                model_response = ModelResponse(
                    content=content,
                    model=self.model,
                    usage=usage,
                    finish_reason=finish_reason,
                    timestamp=time.time(),
                    metadata=metadata or {}
                )
                
                # Update usage statistics
                self._update_usage_stats(usage)
                
                # Cache response if key provided
                if cache_key:
                    self.response_cache[cache_key] = model_response
                
                # Log successful request
                if self.enable_logging:
                    self._log_interaction(messages, model_response, attempt + 1)
                
                logger.info(f"Generated response in {time.time() - start_time:.2f}s")
                return model_response
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    self.usage_stats["failed_requests"] += 1
                    raise e
                time.sleep(self.rate_limit_delay * (attempt + 1))
        
        raise RuntimeError(f"Failed to generate response after {self.max_retries} attempts")
    
    def batch_generate(
        self,
        prompts: List[Union[str, List[Dict[str, str]]]],
        system_prompt: Optional[str] = None,
        batch_size: int = 5,
        **kwargs
    ) -> List[ModelResponse]:
        """
        Generate responses for multiple prompts with batching.
        
        Args:
            prompts: List of prompts to process
            system_prompt: Optional system prompt for all
            batch_size: Number of concurrent requests
            **kwargs: Additional arguments for generate_response
            
        Returns:
            List of ModelResponse objects
        """
        responses = []
        
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i:i + batch_size]
            batch_responses = []
            
            for j, prompt in enumerate(batch):
                try:
                    cache_key = f"batch_{i}_{j}" if kwargs.get("use_cache") else None
                    response = self.generate_response(
                        prompt=prompt,
                        system_prompt=system_prompt,
                        cache_key=cache_key,
                        **{k: v for k, v in kwargs.items() if k != "use_cache"}
                    )
                    batch_responses.append(response)
                    
                    # Rate limiting between requests
                    if j < len(batch) - 1:
                        time.sleep(self.rate_limit_delay)
                        
                except Exception as e:
                    logger.error(f"Failed to process prompt {i + j}: {str(e)}")
                    # Create error response
                    error_response = ModelResponse(
                        content=f"ERROR: {str(e)}",
                        model=self.model,
                        usage={},
                        finish_reason="error",
                        timestamp=time.time(),
                        metadata={"error": True, "error_message": str(e)}
                    )
                    batch_responses.append(error_response)
            
            responses.extend(batch_responses)
            
            # Delay between batches
            if i + batch_size < len(prompts):
                time.sleep(self.rate_limit_delay * 2)
        
        return responses
    
    def _prepare_messages(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Prepare messages in the correct format."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if isinstance(prompt, str):
            messages.append({"role": "user", "content": prompt})
        elif isinstance(prompt, list):
            messages.extend(prompt)
        else:
            raise ValueError("Prompt must be string or list of message dicts")
        
        return messages
    
    def _safety_check(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Perform safety checks on the conversation.
        
        This is a placeholder for more sophisticated safety checking.
        In a real implementation, this might check for:
        - Harmful content
        - PII exposure attempts
        - Jailbreak patterns
        - etc.
        """
        # Simple safety check implementation
        combined_text = " ".join([msg["content"] for msg in messages])
        
        # Check for obvious harmful keywords (basic implementation)
        harmful_keywords = [
            "bypass safety", "ignore instructions", "jailbreak",
            "harmful content", "illegal activities"
        ]
        
        for keyword in harmful_keywords:
            if keyword.lower() in combined_text.lower():
                return {
                    "safe": False,
                    "reason": f"Detected potentially harmful keyword: {keyword}",
                    "confidence": 0.8
                }
        
        return {"safe": True, "reason": "No safety issues detected", "confidence": 0.9}
    
    def _update_usage_stats(self, usage: Dict[str, int]):
        """Update usage statistics."""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["successful_requests"] += 1
        self.usage_stats["total_tokens"] += usage.get("total_tokens", 0)
        
        # Estimate cost (placeholder - real costs depend on model pricing)
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        estimated_cost = (prompt_tokens * 0.00001) + (completion_tokens * 0.00002)
        self.usage_stats["total_cost"] += estimated_cost
    
    def _log_interaction(
        self,
        messages: List[Dict[str, str]],
        response: ModelResponse,
        attempt: int
    ):
        """Log the interaction for analysis and debugging."""
        log_entry = {
            "timestamp": response.timestamp,
            "model": response.model,
            "messages": messages,
            "response": {
                "content": response.content,
                "finish_reason": response.finish_reason,
                "usage": response.usage
            },
            "attempt": attempt,
            "metadata": response.metadata
        }
        
        logger.info(f"Model interaction logged: {json.dumps(log_entry, indent=2)}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return self.usage_stats.copy()
    
    def clear_cache(self):
        """Clear the response cache."""
        self.response_cache.clear()
        logger.info("Response cache cleared")
    
    def export_cache(self, filepath: str):
        """Export response cache to file for reproducibility."""
        with open(filepath, 'w') as f:
            cache_data = {}
            for key, response in self.response_cache.items():
                cache_data[key] = {
                    "content": response.content,
                    "model": response.model,
                    "usage": response.usage,
                    "finish_reason": response.finish_reason,
                    "timestamp": response.timestamp,
                    "metadata": response.metadata
                }
            json.dump(cache_data, f, indent=2)
        logger.info(f"Cache exported to {filepath}")
    
    def import_cache(self, filepath: str):
        """Import response cache from file."""
        with open(filepath, 'r') as f:
            cache_data = json.load(f)
            for key, data in cache_data.items():
                self.response_cache[key] = ModelResponse(**data)
        logger.info(f"Cache imported from {filepath}")
