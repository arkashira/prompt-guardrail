import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

@dataclass
class Policy:
    name: str
    description: str

@dataclass
class GuardrailConfig:
    policies: List[Policy]

def load_schema() -> dict:
    try:
        with open("schema.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def validate_config(config: GuardrailConfig) -> None:
    schema = load_schema()
    config_dict = asdict(config)
    if not isinstance(config_dict, dict):
        raise ValueError("Config is not a dictionary")
    if not isinstance(config_dict["policies"], list):
        raise ValueError("Policies is not a list")
    for policy in config_dict["policies"]:
        if not isinstance(policy, dict):
            raise ValueError("Policy is not a dictionary")
        if not isinstance(policy["name"], str):
            raise ValueError("Policy name is not a string")
        if policy["description"] is None:
            raise ValueError("Policy description is None")
        if not isinstance(policy["description"], str):
            raise ValueError("Policy description is not a string")

def create_config_file() -> None:
    config = GuardrailConfig(
        policies=[
            Policy(name="Example Policy", description="This is an example policy"),
            Policy(name="Another Policy", description="This is another example policy"),
        ]
    )
    validate_config(config)
    with open("guardrail.config.json", "w") as f:
        json.dump(asdict(config), f, indent=4)

def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a guardrail config file")
    parser.add_argument("--init", action="store_true", help="Create a new config file")
    args = parser.parse_args()
    if args.init:
        create_config_file()

if __name__ == "__main__":
    main()
