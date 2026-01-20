from abc import ABC, abstractmethod
import os
import openai
from dotenv import load_dotenv

from src.core.config import get_settings

# Load environment variables for API keys
load_dotenv()

class LLMService(ABC):
    """Abstract base class for a generic Language Model service."""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the language model based on a given prompt.
        """
        pass

class OpenAILLMService(LLMService):
    """Implementation of the LLMService for OpenAI's models."""

    def __init__(self, model_id: str = "gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        openai.api_key = self.api_key
        self.model_id = model_id
        print("Initialized OpenAILLMService.")

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the OpenAI model.
        This is a placeholder for the actual API call.
        """
        print(f"Generating response from OpenAI for prompt: '{prompt[:30]}...'")
        return f"Placeholder OpenAI response for: {prompt}"

def get_llm_service() -> LLMService:
    """
    Factory function to get the appropriate LLM service.
    Currently, only OpenAI is supported.
    """
    provider = get_settings().LLM_PROVIDER
    if provider.lower() == "openai":
        return OpenAILLMService()
    else:
        raise ValueError(f"Unsupported or misconfigured LLM provider: {provider}. Only 'openai' is supported.")

