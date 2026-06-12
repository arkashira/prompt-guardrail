from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Protocol, Any, Dict, Optional, runtime_checkable

@runtime_checkable
class LLMClient(Protocol):
    """Standard interface for LLM providers."""
    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Synchronously generate a completion for *prompt*.
        
        Args:
        prompt: The text prompt.
        options: Optional provider-specific options.
        
        Returns:
        The generated text.
        """
class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        return f"OpenAI response to: {prompt}"
class AnthropicAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        return f"Anthropic response to: {prompt}"
class CohereAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        return f"Cohere response to: {prompt}"
def guardrail(client: LLMClient, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
    if not isinstance(client, LLMClient):
        raise TypeError("Invalid client")
    return client.generate(prompt, options)
