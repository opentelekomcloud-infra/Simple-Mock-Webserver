"""Server control"""

import os
import signal

from lockfile.pidlockfile import PIDLockFile
from wsgiserver import WSGIServer

from too_simple_server.api import SERVER
from too_simple_server.configuration import CONFIGURATION
from too_simple_server.database import init_db


def _pid_dir_permissions():
    default = "/run"
    file_name = f"{default}/randomfilename"
    try:
        open(file_name, "w+").close()
        os.remove(file_name)
        return True
    except IOError:
        return False


PID_DIR = os.path.abspath("/run" if _pid_dir_permissions() else os.path.abspath("."))
PID_FILE = os.path.abspath(f"{PID_DIR}/web-server.pid")


def main(action, debug):
    """Start/stop running server"""
    import daemon  # *nix only

    CONFIGURATION.DEBUG = debug
    if action == "start":
        init_db()
        with daemon.DaemonContext(pidfile=PIDLockFile(PID_FILE), detach_process=True):
            WSGIServer(SERVER, port=int(os.getenv("SERVER_PORT", CONFIGURATION.SERVER_PORT))).start()
    else:
        with open(PID_FILE) as pid_file:
            pid = int(pid_file.read())
        os.kill(pid, signal.SIGTERM)
