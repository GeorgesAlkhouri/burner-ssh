import shlex
import subprocess
import threading
from shutil import which
from typing import Callable, Optional, Union, cast

from .thread import Thread


def is_installed(name: str) -> bool:
    return which(name) is not None


def run(
    cmd: str,
    on_exit: Optional[Callable[[int, Optional[str]], None]] = None,
    output: Optional[Callable[[Union[str, bytes]], None]] = None,
    **kwargs
) -> Thread:
    """Run a command in a separate thread."""

    thread = Thread(cmd, on_exit=on_exit, on_output=output, cmd_kwargs=kwargs)
    thread.start()
    return thread
