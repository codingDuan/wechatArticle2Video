from abc import ABC, abstractmethod
import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

from src.core.config import settings

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
        # Conceptual API call
        # response = openai.ChatCompletion.create(
        #     model=self.model_id,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.choices[0].message.content
        return f"Placeholder OpenAI response for: {prompt}"

class GeminiLLMService(LLMService):
    """Implementation of the LLMService for Google's Gemini models."""

    def __init__(self, model_id: str = "gemini-pro"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_id)
        print("Initialized GeminiLLMService.")

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the Gemini model.
        This is a placeholder for the actual API call.
        """
        print(f"Generating response from Gemini for prompt: '{prompt[:30]}...'")
        # Conceptual API call
        # response = self.model.generate_content(prompt)
        # return response.text
        return f"Placeholder Gemini response for: {prompt}"

def get_llm_service() -> LLMService:
    """
    Factory function to get the appropriate LLM service based on the
    LLM_PROVIDER environment variable.
    """
    provider = settings.LLM_PROVIDER
    if provider.lower() == "openai":
        return OpenAILLMService()
    elif provider.lower() == "gemini":
        return GeminiLLMService()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")