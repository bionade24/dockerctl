# Parsing of the command options for this program

import sys
import argparse
from dockerctl import executer

version_nr = "0.1"


def compose_start(option, compose_name):
    args = {
        "start" : executer.start(compose_name),
        "stop" : executer.stop(compose_name),
        "restart" : executer.restart(compose_name),
        "ps": executer.processes(compose_name),
        "up" : executer.up(compose_name),
        "kill" : executer.kill(compose_name),
        "pull" : executer.pull(compose_name),
        "push" : executer.push(compose_name),
        "rm" : executer.remove(compose_name),
        "top" : executer.top(compose_name),
        "pause" : executer.pause(compose_name),
        "unpause" : executer.unpause(compose_name),
        "images" : executer.images(compose_name),
        "port" : executer.port(compose_name),
        "logs" : executer.logs(compose_name),
    }
    for i in option[1:]:
        args[option](compose_name)


def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=True)
    exgroup = parser.add_mutually_exclusive_group()

    exgroup.add_argument('-v', '--version', action="version", version='dockerctl ' + version_nr,
                         help="Print version number")
    # common commands
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'ps', 'up', ' kill', 'rm', 'top', 'logs',
                                            'images', 'port', 'pull', 'push', 'pause', 'unpause', 'add', 'remove'])
    parser.add_argument('compose_name', type=str)
    # command options
    parser.add_argument('--path', metavar='PATH', type=str, help="Link path to yaml into /etc/docker/name")

    args = parser.parse_args(argv)

    if args.path and args.command == "add":
        executer.add(args.compose_name, args.path)
    compose_start(args.command, args.compose_name)


if __name__ == '__main__':
    main(sys.argv[1:])
