"""Check if working correctly as service"""
# TBD
import os
import subprocess
import time

import pytest
from ocomone import BaseUrlSession

from web_server.configuration import CONFIGURATION
from web_server.run import PID_FILE

skip_on_win = pytest.mark.skipif(os.name != "posix", reason="Running on windows")

MODULE_NAME = "web_server"


def _wait_for_server(status_code, message):
    session = BaseUrlSession(f"http://localhost:{CONFIGURATION.SERVER_PORT}")
    session.trust_env = False
    end_time = time.monotonic() + 10
    while session.get("").status_code != status_code:  # wait until server is up and running
        time.sleep(0.1)
        if time.monotonic() > end_time:
            raise AssertionError(message)


@skip_on_win
class TestService:

    def test_service_lifecycle(self):
        """Test server start/stop"""
        subprocess.run("python -m web_server --debug start", shell=True)
        _wait_for_server(200, "Server is not started in 10 seconds")
        assert os.path.exists(PID_FILE)
        subprocess.run("python -m web_server stop", shell=True)
        with pytest.raises(ConnectionError):
            _wait_for_server(-1, "Server is not stopped in 10 seconds")
        assert not os.path.exists(PID_FILE)
