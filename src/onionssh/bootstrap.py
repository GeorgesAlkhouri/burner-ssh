from typing import List

from .cmd import is_installed


def check_dependencies(deps: List[str]):
    for dep in deps:
        assert is_installed(dep), f"{dep} is not installed"
