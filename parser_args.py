# Parsing of the command options for this program

import argparse

from executer import Executer

parser = argparse.ArgumentParser()
exgp = parser.add_mutually_exclusive_group()
subparsers = parser.add_subparsers()

exgp.add_argument('--version', help='shows the version of dockerctl', action="store_true")

start_p = subparsers.add_parser('start')
start_p.add_argument('compose_name', type=str, help='name of the docker-compose')

stop_p = subparsers.add_parser('stop')
stop_p.add_argument('compose_name', type=str, help='name of specific docker compose')

restart_p = subparsers.add_parser('restart')
restart_p.add_argument('compose_name', type=str, help='name of specific docker compose')

args = parser.parse_args()

compose_name =

start_p.set_defaults(func=Executer.start(compose_name))

restart_p.set_defaults(func=Executer.restart(compose_name))

stop_p.set_defaults(func=Executer.stop(compose_name))

if args.version:
    print("version 0.1")