# type: ignore
from typing import Callable, Dict, Optional

from onionssh.cmd import run


class CommandMixin:
    def build_cmd(self, config: Optional[Dict[str, str]] = None) -> str:
        ...


class TorMixin(CommandMixin):
    def build_cmd(self, config: Optional[Dict[str, str]] = None) -> str:
        if not config:
            config = self.get_config("TOR")
        cmd = "tor"
        for key, value in config.items():
            cmd = cmd + f' --{key} "{value}"'

        return cmd

    def execute(self, run_func: Callable = run, **kwargs):
        cmd = self.build_cmd()

        def _on_exit(returncode, stderr):
            if not self._tor_thread.is_stopped():
                raise RuntimeError(
                    f"Tor stopped unintentionally with {returncode} and "
                    f"message: '{stderr}'"
                )

        def _on_output(msg):
            assert self._tor_thread
            self.outputs[self._tor_thread.name].append(msg)

        thread = run_func(cmd, on_exit=_on_exit, output=_on_output, **kwargs)
        assert (
            thread.name not in self.threads
        ), f"Thread ID {thread.name} already exists"
        self.threads[thread.name] = thread
        self._tor_thread = thread
