import time

import pytest
from onionssh.thread import Thread

from ..cmd import is_installed, run


def test_is_installed():
    assert is_installed("which")
    assert not is_installed("this-does-not-exist")


@pytest.mark.parametrize(
    ("output", "cmd", "kwargs"),
    [(["1"], "echo 1", {}), (["1", "61"], "echo 1 && echo 61", {"shell": True})],
)
def test_run_output(output, cmd, kwargs):

    _res = []

    def _output(msg):
        nonlocal _res
        _res.extend(msg)

    thread = run(cmd, output=_output, **kwargs)
    time.sleep(1)
    thread.join()

    assert output == _res


@pytest.mark.parametrize(
    ("exce", "cmd", "kwargs"),
    [
        # catched FileNotFoundError return code
        (FileNotFoundError, "does-not-exist", {}),
    ],
)
def test_run_exception(exce, cmd, kwargs):

    _res = None

    def _on_exit(_, __):
        nonlocal _res
        _res = False

    with pytest.raises(exce):
        thread = run(cmd, on_exit=_on_exit, **kwargs)
        time.sleep(1)
        thread.join()

    assert _res is None


@pytest.mark.parametrize(
    ("result", "cmd", "kwargs"),
    [
        (1, "exit 1", {"shell": True}),
        (0, "ls", {}),
        # shell return code for command not found
        # this will not raise an exception from
        # Popen
        (127, "does-not-exist", {"shell": True}),
    ],
)
def test_run(result, cmd, kwargs):

    _res = None

    def _on_exit(returncode, _):
        nonlocal _res
        _res = returncode

    thread = run(cmd, on_exit=_on_exit, **kwargs)
    time.sleep(1)
    thread.join()

    assert _res is not None
    assert result == _res


def test_run_kill():

    _res = None
    _stderr = None

    def _on_exit(returncode, stderr):
        nonlocal _res, _stderr
        _res = returncode
        _stderr = stderr

    thread = run("sleep 3", on_exit=_on_exit)
    thread.stop()
    time.sleep(2)
    thread.join()

    assert not _stderr
    assert _res
    # < 0 means killed by signal -N
    assert _res < 0


def test_run_raise_shell_daemon():
    with pytest.raises(RuntimeError):
        run("echo 2", thread_kwargs={"daemon": True}, shell=True)
