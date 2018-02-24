import pytest


def test_nothing():
    with pytest.raises(ValueError):
        raise ValueError("Just iniital test for bootstrapping the project. Stay tuned!")
