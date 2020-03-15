# Parsing of the command options for this program

import sys
import argparse
from dockerctl.executer import Commands

VERSION_NR = "0.3"


def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=True)
    parser.add_argument('-v', '--version', action="version", version='dockerctl ' + VERSION_NR,
                         help="Print version number")
    # common commands
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'ps', 'up', ' kill', 'rm', 'top', 'logs',
                                            'images', 'port', 'pull', 'push', 'pause', 'unpause', 'add', 'remove',
                                            'edit', 'create', 'update'])
    parser.add_argument('compose_name', type=str)
    # command options
    parser.add_argument('--path', metavar='PATH', type=str, help="Link path to yaml into /etc/docker/name")

    args = parser.parse_args(argv)
    getattr(Commands(args.compose_name, args.path), args.command)()


if __name__ == '__main__':
    main(sys.argv[1:])
