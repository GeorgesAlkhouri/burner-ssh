import shlex
import subprocess
import threading
from threading import Event
from threading import Thread as PyThread
from typing import Callable, Dict, Optional, Union, cast


def _format_output(output):
    _out = []
    if isinstance(output, str):
        _out = output.split("\n")

    if isinstance(output, bytes):
        _out = output.decode().split("\n")

    return [_o for _o in _out if _o]


def _get_output(_proc, _thread, _on_output, timeout=0.1, format_output=_format_output):
    if _thread.is_stopped():
        _proc.terminate()
        return "", ""
    stdout, stderr = "", ""
    try:
        stdout, stderr = _proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _get_output(_proc, _thread, _on_output, timeout, format_output)

    if stdout and _on_output:
        _on_output(format_output(stdout))
    return stdout, stderr


def _run(
    _cmd,
    on_exit: Optional[Callable[[int, Optional[str]], None]],
    on_output: Optional[Callable[[Union[str, bytes]], None]],
    kwargs,
    format_output=_format_output,
):
    # Set shell=False to be able to terminate the started thread
    # and not just the shell process without the spawned child
    # process

    thread = cast(Thread, threading.currentThread())
    proc = subprocess.Popen(
        _cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )

    if on_output:
        _get_output(proc, thread, on_output)

    if thread.is_stopped():
        proc.terminate()

    # get return code and remaining output of process
    stdout, stderr = proc.communicate()
    if on_output and stdout:
        on_output(format_output(on_output))
    if on_exit:
        on_exit(proc.returncode, stderr)


class Thread(PyThread):
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
        self._stop_event = Event()
        self._cmd = cmd
        self._cmd_kwargs = cmd_kwargs
        if not self._cmd_kwargs:
            self._cmd_kwargs = {}
        self._on_exit = on_exit
        self._on_output = on_output
        self._exc: Optional[BaseException] = None

    def stop(self):
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()

    def join(self, timeout: Optional[float] = None) -> None:
        threading.Thread.join(self, timeout)

        if self._exc:
            raise self._exc

    def run(self):
        _cmd = shlex.split(self._cmd)

        shell = self._cmd_kwargs.get("shell", None)
        if shell:
            _cmd = self._cmd

        try:
            _run(_cmd, self._on_exit, self._on_output, self._cmd_kwargs)
        except BaseException as exc:
            self._exc = exc
