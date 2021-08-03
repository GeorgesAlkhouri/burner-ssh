import shlex
import subprocess
import threading
from threading import Event
from threading import Thread as PyThread
from typing import Callable, Dict, Optional, Union, cast


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

    thread = cast(Thread, threading.currentThread())
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


class StoppableMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


class Thread(StoppableMixin, PyThread):
    def __init__(
        self,
        cmd: str,
        *args,
        on_exit: Optional[Callable[[int, Optional[str]], None]] = None,
        on_output: Optional[Callable[[Union[str, bytes]], None]] = None,
        cmd_kwargs: Optional[Dict] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._cmd = cmd
        self._cmd_kwargs = cmd_kwargs
        if not self._cmd_kwargs:
            self._cmd_kwargs = {}
        self._on_exit = on_exit
        self._on_output = on_output
        self._exc: Optional[Exception] = None

    def join(self, timeout: Optional[float] = None) -> None:
        threading.Thread.join(self, timeout)

        if self._exc:
            raise self._exc

    def run(self):
        _cmd = shlex.split(self._cmd)

        shell = self._cmd_kwargs.get("shell", None)
        if shell:
            _cmd = self._cmd

        _run(_cmd, self._on_exit, self._on_output, self._cmd_kwargs)
