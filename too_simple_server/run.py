"""Server control"""

import os
import signal

from lockfile.pidlockfile import PIDLockFile
from wsgiserver import WSGIServer

from .api import SERVER
from .configuration import load_configuration
from .database import init_db


def _pid_dir():
    default = "/tmp/too-simple"
    fallback = os.path.abspath("~/.too-simple")
    os.makedirs(default, exist_ok=True)
    file_name = f"{default}/randomfilename"
    try:
        open(file_name, "w+").close()
        os.remove(file_name)
        return default
    except IOError:
        os.makedirs(fallback, exist_ok=True)
        return fallback


PID_FILE = os.path.abspath(f"{_pid_dir()}/web-server.pid")


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
            WSGIServer(SERVER, port=configuration.server_port).start()

    if action == "start":
        _start()
    elif action == "stop":
        _stop()
    elif action == "restart":
        _stop()
        _start()
    else:
        raise AttributeError(f"Unknown action: {action}")
