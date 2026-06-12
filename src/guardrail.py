import json
from dataclasses import dataclass
from typing import Callable, List, Optional

@dataclass
class ValidatorResult:
    valid: bool
    error: Optional[str] = None

class Guardrail:
    def __init__(self, custom_validators: Optional[List[Callable]] = None):
        self.custom_validators = custom_validators if custom_validators else []

    def validate(self, output: str) -> ValidatorResult:
        for validator in self.custom_validators:
            try:
                result = validator(output)
                if not result:
                    return ValidatorResult(False, "Custom validator failed")
            except Exception as e:
                return ValidatorResult(False, str(e))
        return ValidatorResult(True)

def pci_dss_validator(output: str) -> bool:
    disallowed_phrases = ["credit card number", "social security number"]
    for phrase in disallowed_phrases:
        if phrase in output:
            return False
    return True
