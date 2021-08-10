import time
from collections import defaultdict

import psutil

from onionssh.config import get_tor_config, set_tor_config_value

from ..tor_mixin import TorMixin


def test_tor_cmd():

    config = {
        "SOCKSPort": "0",
        "HiddenServiceDir": "test",
        "HiddenServicePort": "80 127.0.0.1:80",
        "ExitPolicy": "reject *:*",
    }
    cmd = TorMixin().build_cmd(config=config)
    assert cmd == (
        'tor --SOCKSPort "0" --HiddenServiceDir "test" '
        '--HiddenServicePort "80 127.0.0.1:80" --ExitPolicy "reject *:*"'
    )


class Mock(TorMixin):
    def __init__(self) -> None:
        self.outputs = defaultdict(list)
        self.threads = {}


def _mock_config(key):
    assert key == "TOR"
    set_tor_config_value("HiddenServiceDir", "test2")
    set_tor_config_value("HiddenServicePort", "80 0.0.0.0:80")
    set_tor_config_value("SOCKSPort", "0")
    set_tor_config_value("ExitPolicy", "reject *:*")
    return get_tor_config()


def test_tor_mixin_build_cmd():

    mock = Mock()
    setattr(mock, "get_config", _mock_config)

    cmd = mock.build_cmd()
    assert cmd == (
        'tor --SOCKSPort "0" --ExitPolicy "reject *:*" '
        '--HiddenServiceDir "test2" --HiddenServicePort "80 0.0.0.0:80"'
    )


def _assert_not_tor():
    for proc in psutil.process_iter(["name"]):
        assert (
            "tor " not in proc.info["name"].lower()
        ), f"Tor is already running\n{proc}"


def test_tor_run_mixin():
    _assert_not_tor()
    mock = Mock()
    setattr(mock, "get_config", _mock_config)
    assert len(mock.threads) == 0
    assert len(mock.outputs) == 0
    mock.execute()
    assert len(mock.threads) == 1
    assert mock._tor_thread
    assert mock._tor_thread.is_alive()
    # let tor bootstrap and run into idle
    mock._tor_thread.join(timeout=5.0)
    assert mock._tor_thread.is_alive()
    mock._tor_thread.stop()
    time.sleep(2.0)
    assert not mock._tor_thread.is_alive()
    _assert_not_tor()
    # assert len(mock.threads) == 0
    # assert len(mock.outputs) == 0
    # assert not mock._tor_thread
