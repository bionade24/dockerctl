# Parsing of the command options for this program

import sys
import argparse
from dockerctl import executer

version_nr = "0.2"


def compose_start(option, compose_name):
    args = {
        "start"  : executer.start,
        "stop"   : executer.stop,
        "restart": executer.restart,
        "ps"     : executer.processes,
        "up"     : executer.up,
        "kill"   : executer.kill,
        "pull"   : executer.pull,
        "push"   : executer.push,
        "rm"     : executer.rm,
        "top"    : executer.top,
        "pause"  : executer.pause,
        "unpause": executer.unpause,
        "images" : executer.images,
        "port"   : executer.port,
        "logs"   : executer.logs,
        "add"    : executer.add,
        "remove" : executer.remove,
    }
    args[option](compose_name)


def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=True)
    parser.add_argument('-v', '--version', action="version", version='dockerctl ' + version_nr,
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
