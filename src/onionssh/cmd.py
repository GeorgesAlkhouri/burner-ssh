from shutil import which
from typing import Callable, Dict, Optional, Union

from .thread import Thread


def is_installed(name: str) -> bool:
    return which(name) is not None


def run(
    cmd: str,
    on_exit: Optional[Callable[[int, Optional[str]], None]] = None,
    output: Optional[Callable[[Union[str, bytes]], None]] = None,
    thread_kwargs: Optional[Dict] = None,
    **cmd_kwargs
) -> Thread:
    """Run a command in a separate thread."""
    if not thread_kwargs:
        thread_kwargs = {}
    shell = cmd_kwargs.get("shell")
    daemon = thread_kwargs.get("daemon")

    if shell and daemon:
        raise RuntimeError(
            "Can not run thread in daemon mode when running command with shell=True. Only shell process will be terminated if root thread is killed but not spawned children from shell (like tor)."
        )

    thread = Thread(
        cmd, on_exit=on_exit, on_output=output, cmd_kwargs=cmd_kwargs, **thread_kwargs
    )
    thread.start()
    return thread
