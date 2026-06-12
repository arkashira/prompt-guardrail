import pytest

@pytest.fixture(autouse=True)
def cleanup():
    yield
    import os
    try:
        os.remove("guardrail.config.json")
    except FileNotFoundError:
        pass
