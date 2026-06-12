import builtins
from unittest import mock
from prompt_guardrail import (
    OpenAIAdapter,
    AnthropicAdapter,
    CohereAdapter,
    guardrail,
    LLMClient,
)

def test_guardrail_accepts_any_adapter():
    prompt = "Hello world"
    # OpenAI
    openai = OpenAIAdapter(api_key="test")
    result = guardrail(openai, prompt)
    assert result == "OpenAI response to: Hello world"
    # Anthropic
    anthropic = AnthropicAdapter(api_key="test")
    result = guardrail(anthropic, prompt)
    assert result == "Anthropic response to: Hello world"
    # Cohere
    cohere = CohereAdapter(api_key="test")
    result = guardrail(cohere, prompt)
    assert result == "Cohere response to: Hello world"

def test_guardrail_uses_mocked_generate():
    class DummyClient:
        def generate(self, prompt: str, options=None) -> str:
            return f"mocked:{prompt}"
    dummy = DummyClient()
    assert guardrail(dummy, "test") == "mocked:test"

def test_adapter_generate_calls_are_isolated():
    # Ensure that each adapter's generate method can be monkey-patched
    openai = OpenAIAdapter(api_key="k")
    with mock.patch.object(openai, "generate", return_value="patched") as m:
        assert guardrail(openai, "x") == "patched"
        m.assert_called_once_with("x", None)
    anthropic = AnthropicAdapter(api_key="k")
    with mock.patch.object(anthropic, "generate", return_value="patched2") as m:
        assert guardrail(anthropic, "y") == "patched2"
        m.assert_called_once_with("y", None)
    cohere = CohereAdapter(api_key="k")
    with mock.patch.object(cohere, "generate", return_value="patched3") as m:
        assert guardrail(cohere, "z") == "patched3"
        m.assert_called_once_with("z", None)

def test_guardrail_type_check():
    class NotAClient:
        pass
    not_client = NotAClient()
    try:
        guardrail(not_client, "test")  # should raise TypeError
    except TypeError:
        pass
    else:
        raise AssertionError("TypeError not raised for invalid client")
