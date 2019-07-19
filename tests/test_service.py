"""Check if working correctly as service"""
# TBD
import multiprocessing
import os
import time

import pytest
import requests
from ocomone import BaseUrlSession
from pytest import skip

from web_server.configuration import CONFIGURATION
from web_server.run import PID_FILE, main

skip_on_win = pytest.mark.skipif(os.name != "posix", reason="Running on windows")

MODULE_NAME = "web_server"


def _wait_for_server(status_code, message, error_is_ok=False):
    session = BaseUrlSession(f"http://localhost:{CONFIGURATION.SERVER_PORT}")
    session.trust_env = False
    end_time = time.monotonic() + 10

    def _not_up():
        """Returns True if server is down"""
        try:
            return session.get("").status_code != status_code
        except requests.ConnectionError:
            return not error_is_ok

    while _not_up():  # wait until server is up and running
        time.sleep(0.1)
        if time.monotonic() > end_time:
            raise AssertionError(message)


@skip_on_win
class TestService:

    def test_service_start(self):
        multiprocessing.Process(target=main, args=("start", True), daemon=True).start()
        _wait_for_server(200, "Server is not started in 10 seconds")

    @pytest.mark.skip("Not working in any CI")
    def test_service_lifecycle(self):
        """Test server start/stop"""
        multiprocessing.Process(target=main, args=("start", True)).start()
        _wait_for_server(200, "Server is not started in 10 seconds")
        assert os.path.exists(PID_FILE)
        multiprocessing.Process(target=main, args=("stop", True)).run()
        _wait_for_server(-1, "Server is not stopped in 10 seconds", error_is_ok=True)
        assert not os.path.exists(PID_FILE)
