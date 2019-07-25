"""Server control"""

import os
import signal

from lockfile.pidlockfile import PIDLockFile
from wsgiserver import WSGIServer

from .api import SERVER
from .configuration import load_configuration
from .database import init_db


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


def main(action, debug=None):
    """Start/stop running server"""
    import daemon  # *nix only

    configuration = load_configuration()
    if debug is not None:
        configuration.debug = debug

    def _stop():
        with open(PID_FILE) as pid_file:
            pid = int(pid_file.read())
        os.kill(pid, signal.SIGTERM)

    def _start():
        init_db()
        with daemon.DaemonContext(pidfile=PIDLockFile(PID_FILE), detach_process=True):
            WSGIServer(SERVER, port=int(os.getenv("SERVER_PORT", configuration.server_port))).start()

    if action == "start":
        _start()
    elif action == "stop":
        _stop()
    elif action == "restart":
        _stop()
        _start()
    else:
        raise AttributeError(f"Unknown action: {action}")
