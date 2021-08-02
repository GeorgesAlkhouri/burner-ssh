from typing import Dict, Optional

from onionssh.cmd import run


class CommandMixin:
    def build_cmd(self, config: Optional[Dict[str, str]] = None) -> str:
        ...


class TorMixin(CommandMixin):
    # TODO config
    def build_cmd(self, config: Optional[Dict[str, str]] = None) -> str:
        if not config:
            ...
        cmd = "tor"
        for key, value in config.items():
            cmd = cmd + f' --{key} "{value}"'

        return cmd

    def execute(self):
        ...
