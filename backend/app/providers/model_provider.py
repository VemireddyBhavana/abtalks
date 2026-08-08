import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Iterator
from app.core.config import settings
from app.core.logging_config import logger
from app.exceptions.llm_exception import (
    LLMProviderError,
    LLMApiKeyMissingError,
)


class AbstractModelProvider(ABC):
    """Abstract Interface contract for LLM Model Providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generates raw response text given a structured system/user prompt.
        """
        pass

    @abstractmethod
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """
        Streaming interface method for future real-time audio/text responses.
        """
        pass


class MockLLMProvider(AbstractModelProvider):
    """
    Offline deterministic Model Provider used for testing and standalone execution.
    Outputs clean JSON format without external API calls.
    """

    def generate(self, prompt: str) -> str:
        logger.info("MockLLMProvider: Generating simulated LLM question response.")
        topic = "General AI Architecture"
        if "CURRENT TOPIC:" in prompt:
            try:
                line = [l for l in prompt.split("\n") if "CURRENT TOPIC:" in l][0]
                topic = line.split("CURRENT TOPIC:")[1].strip()
            except Exception:
                pass

        mock_payload = {
            "question_text": f"Can you explain the core concepts of {topic} and how it applies to full stack AI engineering?",
            "difficulty": "Intermediate",
            "reasoning": "Mock provider generated structured question."
        }
        return json.dumps(mock_payload)

    def stream_generate(self, prompt: str) -> Iterator[str]:
        response = self.generate(prompt)
        for chunk in response.split(" "):
            yield chunk + " "


class GeminiProvider(AbstractModelProvider):
    """
    Google Gemini Model Provider implementation.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model_name = model_name or settings.LLM_MODEL_NAME or "gemini-1.5-flash"
        if not self.api_key:
            logger.error("LLMApiKeyMissingError: Gemini API key is missing.")
            raise LLMApiKeyMissingError("Gemini API key is required when LLM_PROVIDER is set to 'gemini'.")

    def generate(self, prompt: str) -> str:
        logger.info(f"GeminiProvider: Requesting completion from model '{self.model_name}'...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": settings.LLM_TEMPERATURE,
                    "max_output_tokens": settings.LLM_MAX_TOKENS,
                    "response_mime_type": "application/json",
                }
            )
            logger.info("GeminiProvider: Successfully received completion.")
            return response.text
        except Exception as exc:
            logger.error(f"GeminiProvider Error: {str(exc)}")
            raise LLMProviderError(f"Gemini generation failed: {str(exc)}") from exc

    def stream_generate(self, prompt: str) -> Iterator[str]:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                yield chunk.text
        except Exception as exc:
            raise LLMProviderError(f"Gemini streaming failed: {str(exc)}") from exc


class OpenAIProvider(AbstractModelProvider):
    """
    OpenAI Model Provider implementation.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model_name = model_name or settings.LLM_MODEL_NAME or "gpt-4o-mini"
        if not self.api_key:
            logger.error("LLMApiKeyMissingError: OpenAI API key is missing.")
            raise LLMApiKeyMissingError("OpenAI API key is required when LLM_PROVIDER is set to 'openai'.")

    def generate(self, prompt: str) -> str:
        logger.info(f"OpenAIProvider: Requesting completion from model '{self.model_name}'...")
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a professional AI Interview Question Generator. Respond ONLY in valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                response_format={"type": "json_object"},
            )
            logger.info("OpenAIProvider: Successfully received completion.")
            return response.choices[0].message.content
        except Exception as exc:
            logger.error(f"OpenAIProvider Error: {str(exc)}")
            raise LLMProviderError(f"OpenAI generation failed: {str(exc)}") from exc

    def stream_generate(self, prompt: str) -> Iterator[str]:
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as exc:
            raise LLMProviderError(f"OpenAI streaming failed: {str(exc)}") from exc


class ClaudeProvider(AbstractModelProvider):
    """
    Anthropic Claude Model Provider implementation.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model_name = model_name or settings.LLM_MODEL_NAME or "claude-3-5-sonnet-20241022"
        if not self.api_key:
            logger.error("LLMApiKeyMissingError: Claude API key is missing.")
            raise LLMApiKeyMissingError("Claude API key is required when LLM_PROVIDER is set to 'claude'.")

    def generate(self, prompt: str) -> str:
        logger.info(f"ClaudeProvider: Requesting completion from model '{self.model_name}'...")
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model_name,
                max_tokens=settings.LLM_MAX_TOKENS,
                temperature=settings.LLM_TEMPERATURE,
                system="You are a professional AI Interview Question Generator. Respond ONLY in valid JSON.",
                messages=[{"role": "user", "content": prompt}],
            )
            logger.info("ClaudeProvider: Successfully received completion.")
            return response.content[0].text
        except Exception as exc:
            logger.error(f"ClaudeProvider Error: {str(exc)}")
            raise LLMProviderError(f"Claude generation failed: {str(exc)}") from exc

    def stream_generate(self, prompt: str) -> Iterator[str]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            with client.messages.stream(
                model=self.model_name,
                max_tokens=settings.LLM_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as exc:
            raise LLMProviderError(f"Claude streaming failed: {str(exc)}") from exc


class LLMProviderFactory:
    """
    Factory Pattern with Instance Caching for LLM Model Providers.
    """

    _cached_providers: Dict[str, AbstractModelProvider] = {}

    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None) -> AbstractModelProvider:
        provider = (provider_name or settings.LLM_PROVIDER).lower().strip()
        
        if provider not in cls._cached_providers:
            logger.info(f"Provider Selected: Initializing LLM provider '{provider}'.")
            if provider == "mock":
                cls._cached_providers[provider] = MockLLMProvider()
            elif provider == "gemini":
                cls._cached_providers[provider] = GeminiProvider()
            elif provider == "openai":
                cls._cached_providers[provider] = OpenAIProvider()
            elif provider == "claude":
                cls._cached_providers[provider] = ClaudeProvider()
            else:
                logger.warning(f"Unknown LLM provider '{provider}', falling back to MockLLMProvider.")
                cls._cached_providers[provider] = MockLLMProvider()

        return cls._cached_providers[provider]
