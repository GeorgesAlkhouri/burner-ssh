from ..tor_mixin import TorMixin


def test_tor_cmd():

    config = {
        "SOCKSPort": "0",
        "HiddenServiceDir": "test",
        "HiddenServicePort": "80 127.0.0.1:80",
        "ExitPolicy": "reject *:*",
    }
    cmd = TorMixin().build_cmd(config=config)
    assert (
        cmd
        == 'tor --SOCKSPort "0" --HiddenServiceDir "test" --HiddenServicePort "80 127.0.0.1:80" --ExitPolicy "reject *:*"'
    )
