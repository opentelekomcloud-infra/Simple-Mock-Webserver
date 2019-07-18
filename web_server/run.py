"""Server control"""

import os
import signal

import lockfile
from wsgiserver import WSGIServer

from web_server.api import SERVER
from web_server.configuration import CONFIGURATION
from web_server.database import init_db

PID_FILE = "/tmp/mockserver.pid"


def main(action, debug):
    """Start/stop running server"""
    import daemon  # *nix only

    CONFIGURATION.DEBUG = debug
    if action == "start":
        with daemon.DaemonContext(pidfile=lockfile.FileLock(PID_FILE), detach_process=True):
            init_db()
            WSGIServer(SERVER, port=int(os.getenv("SERVER_PORT", CONFIGURATION.SERVER_PORT)))
    else:
        with open(PID_FILE) as pid_file:
            pid = int(pid_file.read())
        os.kill(pid, signal.SIGTERM)
