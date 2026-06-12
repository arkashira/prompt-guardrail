import pytest
import sys
sys.path.insert(0, './src')
from guardrail import Guardrail, ValidatorResult, pci_dss_validator

def test_guardrail_constructor():
    guardrail = Guardrail()
    assert guardrail.custom_validators == []

def test_guardrail_custom_validator():
    def custom_validator(output: str) -> bool:
        return "allowed" in output
    guardrail = Guardrail([custom_validator])
    result = guardrail.validate("allowed phrase")
    assert result.valid

def test_guardrail_pci_dss_validator():
    guardrail = Guardrail([pci_dss_validator])
    result = guardrail.validate("credit card number")
    assert not result.valid

def test_guardrail_custom_validator_error():
    def custom_validator(output: str) -> bool:
        raise Exception("Custom validator error")
    guardrail = Guardrail([custom_validator])
    result = guardrail.validate("test output")
    assert not result.valid
    assert result.error == "Custom validator error"
