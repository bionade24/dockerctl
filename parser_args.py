# Parsing of the command options for this program

import argparse
from sys import argv

from executer import Executer

parser = argparse.ArgumentParser()
exgp = parser.add_mutually_exclusive_group()
subparsers = parser.add_subparsers()

exgp.add_argument('--version', help='shows the version of dockerctl', action="store_true")

parser.add_argument("command", choices=['start', 'restart', 'stop', 'ps'], help="Command for docker-compose")
parser.add_argument("compose_name", type=str, help="name of specific docker-compose folder", nargs='?')


def options(args):
    if args.command == 'start':
        Executer.start(args.compose_name)
    elif args.command == 'restart':
        Executer.restart(args.compose_name)
    elif args.command == 'stop':
        Executer.stop(args.compose_name)
    elif args.command == 'ps':
        Executer.processes(args.compose_name)
    elif args.version:
        print("version 0.1")


args = parser.parse_args("start", "call-counter-redis")
options(args)
