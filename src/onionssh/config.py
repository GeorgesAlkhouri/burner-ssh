from collections import OrderedDict
from typing import Dict

# tor --SOCKSPort 0 --HiddenServiceDir hidden --HiddenServicePort "22 127.0.0.1:22" --ExitPolicy "reject *:*"
# HiddenServiceDir /home/ofungus/.linuxbrew/var/lib/tor/other_hidden_service/
# HiddenServicePort 80 127.0.0.1:80
# ExitPolicy reject *:* # no exits allowed
__TOR_CONFIG = OrderedDict({"SOCKSPort": "0", "ExitPolicy": "reject *:*"})


def get_tor_config() -> Dict[str, str]:
    return __TOR_CONFIG.copy()


def set_tor_config_value(key: str, value: str):
    set_config_value(key, value, __TOR_CONFIG)


def set_config_value(key: str, value: str, config: Dict[str, str]):
    config[key] = value
