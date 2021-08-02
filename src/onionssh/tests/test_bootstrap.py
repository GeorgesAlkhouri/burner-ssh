import pytest

from ..bootstrap import check_dependencies


def test_check_dependencies():
    check_dependencies([])
    check_dependencies(["which", "cd"])
    with pytest.raises(AssertionError, match="this-does-not-exist is not installed"):
        check_dependencies(["this-does-not-exist"])
