"""
OpenAI API Client Wrapper
Handles chat completions, embeddings, and error handling.
"""

import os
from typing import Optional, List
import time

try:
    from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
except ImportError:
    OpenAI = None

from config import OPENAI_CONFIG


class OpenAIClient:
    """Wrapper around OpenAI API with retry logic and error handling."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key."""
        if not OpenAI:
            raise ImportError("openai package not installed. Install with: pip install openai")

        self.api_key = api_key or OPENAI_CONFIG.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Set via environment variable or pass api_key parameter.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=OPENAI_CONFIG.get("base_url"),
            timeout=OPENAI_CONFIG.get("timeout", 30),
        )
        self.model = OPENAI_CONFIG.get("model", "gpt-4-turbo")
        self.max_retries = OPENAI_CONFIG.get("max_retries", 3)

    def chat_completion(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        retry_count: int = 0,
    ) -> str:
        """
        Send a chat completion request to OpenAI.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Max tokens in response
            retry_count: Current retry attempt

        Returns:
            Response text from OpenAI
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                time.sleep(wait_time)
                return self.chat_completion(
                    messages, temperature, max_tokens, retry_count + 1
                )
            raise ValueError(f"Rate limited after {self.max_retries} retries: {str(e)}")
        except APIConnectionError as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self.chat_completion(
                    messages, temperature, max_tokens, retry_count + 1
                )
            raise ValueError(f"Connection error after {self.max_retries} retries: {str(e)}")
        except APITimeoutError as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self.chat_completion(
                    messages, temperature, max_tokens, retry_count + 1
                )
            raise ValueError(f"Timeout after {self.max_retries} retries: {str(e)}")

    def system_prompt_completion(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Chat completion with a system prompt.

        Args:
            system_prompt: System instructions
            user_message: User's input
            temperature: Sampling temperature
            max_tokens: Max tokens in response

        Returns:
            Response text
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        return self.chat_completion(messages, temperature, max_tokens)

    def streaming_completion(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        """
        Stream a chat completion response.

        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Max tokens

        Yields:
            Text chunks from response
        """
        try:
            with self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            ) as response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
        except Exception as e:
            raise ValueError(f"Streaming error: {str(e)}")

    def embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"Embedding error: {str(e)}")
