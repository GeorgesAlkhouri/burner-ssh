from typing import Dict

# tor --SOCKSPort 0 --HiddenServiceDir hidden --HiddenServicePort "22 127.0.0.1:22" --ExitPolicy "reject *:*"
# HiddenServiceDir /home/ofungus/.linuxbrew/var/lib/tor/other_hidden_service/
# HiddenServicePort 80 127.0.0.1:80
# ExitPolicy reject *:* # no exits allowed
__CONFIG = {"SOCKSPort": "0", "ExitPolicy": "reject *:*"}


def get_config() -> Dict[str, str]:
    return __CONFIG.copy()


def set_config_value(key: str, value: str):
    __CONFIG[key] = value
