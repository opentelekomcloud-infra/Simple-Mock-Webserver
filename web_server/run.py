"""Server control"""

import os
import signal

import daemon
from wsgiserver import WSGIServer

from web_server.api import SERVER
from web_server.configuration import CONFIGURATION

PID_FILE = "/tmp/mockserver.pid"


def main(action, debug):
    """Start/stop running server"""

    CONFIGURATION.DEBUG = debug
    if action == "start":
        with daemon.DaemonContext(pidfile=PID_FILE, detach_process=True):
            WSGIServer(SERVER, port=int(os.getenv("SERVER_PORT", 8080)))
    else:
        with open(PID_FILE) as pid_file:
            pid = int(pid_file.read())
        os.kill(pid, signal.SIGTERM)
