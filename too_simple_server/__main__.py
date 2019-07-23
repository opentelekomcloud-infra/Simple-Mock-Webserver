"""Run server as module"""
from argparse import ArgumentParser

from too_simple_server.run import main

AGP = ArgumentParser(description="Mock server with simple DB interactions")
AGP.add_argument("--debug", action="store_true", default=False)
AGP.add_argument("action", default="start", choices=["start", "stop"])
ARGS = AGP.parse_args()

main(ARGS.action, ARGS.debug)
