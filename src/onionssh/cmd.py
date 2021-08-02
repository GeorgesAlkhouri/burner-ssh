import shlex
import subprocess
import threading
from shutil import which
from typing import Callable, Optional, Union, cast

from .thread import StoppableThread


def is_installed(name: str) -> bool:
    return which(name) is not None


def _run(
    _cmd,
    _on_exit: Optional[Callable[[int, Optional[str]], None]],
    _output: Optional[Callable[[Union[str, bytes]], None]],
    kwargs,
):
    # _cmd, _on_exit, _output = dill.loads(pickled)
    # Set shell=False to be able to terminate the started thread
    # and not just the shell process without the spawned child
    # process

    thread = cast(StoppableThread, threading.currentThread())
    try:
        proc = subprocess.Popen(
            _cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
        )
    except FileNotFoundError as _e:
        if _on_exit:
            _on_exit(1, str(_e))
        else:
            # raise error when no on_exit callback is given
            raise _e
        return

    while proc.poll() is None:
        if thread.is_stopped():
            proc.terminate()
            break
        line = proc.stdout.readline()
        if line and _output:
            _output(line)

    if thread.is_stopped():
        proc.terminate()

    # get return code and remaining output of process
    stdout, stderr = proc.communicate()
    if _output and stdout:
        _output(stdout)
    if _on_exit:
        _on_exit(proc.returncode, stderr)


def run(
    cmd: str,
    on_exit: Optional[Callable[[int, Optional[str]], None]] = None,
    output: Optional[Callable[[Union[str, bytes]], None]] = None,
    **kwargs
) -> StoppableThread:
    """Run a command in a separate thread."""
    _cmd = shlex.split(cmd)

    shell = kwargs.get("shell", None)
    if shell:
        _cmd = cmd

    thread = StoppableThread(target=_run, args=(_cmd, on_exit, output, kwargs))
    thread.start()
    return thread
