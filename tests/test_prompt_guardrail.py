import json
import pytest
from prompt_guardrail import GuardrailConfig, Policy, load_schema, validate_config, create_config_file

def test_create_config_file() -> None:
    create_config_file()
    with open("guardrail.config.json") as f:
        config = json.load(f)
    assert isinstance(config, dict)
    assert config["policies"][0]["name"] == "Example Policy"
    assert config["policies"][1]["description"] == "This is another example policy"

def test_validate_config() -> None:
    config = GuardrailConfig(
        policies=[
            Policy(name="Example Policy", description="This is an example policy"),
            Policy(name="Another Policy", description="This is another example policy"),
        ]
    )
    validate_config(config)

def test_invalid_config() -> None:
    with pytest.raises(ValueError):
        config = GuardrailConfig(
            policies=[
                Policy(name="Example Policy", description="This is an example policy"),
                Policy(name="Another Policy", description="This is another example policy"),
                Policy(name="Invalid Policy", description=None),
            ]
        )
        validate_config(config)
