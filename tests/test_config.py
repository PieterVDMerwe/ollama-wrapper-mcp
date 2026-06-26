from ollama_wrapper.config import settings

def test_default_settings():
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.request_timeout == 60.0
    assert len(settings.injection_keywords) > 0
    assert "ignore previous instructions" in settings.injection_keywords
