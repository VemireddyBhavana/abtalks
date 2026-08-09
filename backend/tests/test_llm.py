from app.providers.model_provider import MockLLMProvider
from app.services.llm_service import LLMService


def test_llm_provider_instance():
    provider = MockLLMProvider()
    assert provider is not None
    chunks = list(provider.stream_generate("Test prompt"))
    assert len(chunks) > 0


def test_llm_service_response():
    svc = LLMService()
    assert svc is not None
