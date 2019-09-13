"""Check if working correctly as service"""
import multiprocessing
import os
import time
from typing import Any

import pytest
import requests
from ocomone.session import BaseUrlSession

from too_simple_server.configuration import load_configuration
from too_simple_server.run import PID_FILE, main

skip_on_win = pytest.mark.skipif(os.name != "posix", reason="Running on windows")

configuration = load_configuration()


def _wait_for_server(ok):
    session = BaseUrlSession(f"http://localhost:{configuration.server_port}")
    session.trust_env = False

    def _server_expected(_ok=True):
        """Returns True if server is down"""
        try:
            response = session.get("/").status_code
            print(response)
            return (response == 200) is _ok
        except requests.RequestException:
            return not _ok

    _wait(_server_expected, ok, error=AssertionError(f"Server is not {'started' if ok else 'stopped'}"))
    session.close()


def _wait(condition, *args, timeout=10, error: Any = AssertionError):
    end_time = time.monotonic() + timeout
    while time.monotonic() < end_time:
        if condition(*args):
            return
        time.sleep(0.1)
    raise error


@skip_on_win
def test_service_lifecycle():
    """Test server start/stop"""
    process = multiprocessing.Process(target=main, args=("start", True), daemon=True)
    process.start()
    _wait_for_server(True)
    _wait(os.path.exists, PID_FILE)
    process.terminate()
    main("stop")
    _wait_for_server(False)
    _wait(lambda p: not os.path.exists(p), PID_FILE)
