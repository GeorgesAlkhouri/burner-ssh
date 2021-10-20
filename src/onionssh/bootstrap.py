"""Module containing tools and function to support the service bootstrap process"""
from typing import List

from .cmd import is_installed


def check_dependencies(deps: List[str]):
    """Assert that every dependency is installed"""
    for dep in deps:
        assert is_installed(dep), f"{dep} is not installed"
