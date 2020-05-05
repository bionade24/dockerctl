# Parsing of the command options for this program

import sys
import argparse
from dockerctl.executer import Commands

VERSION_NR = "0.4"


def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=True)
    parser.add_argument('-v', '--version', action="version", version='dockerctl ' + VERSION_NR,
                         help="Print version number")
    # common commands
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'ps', 'up', ' kill', 'rm', 'top', 'logs',
                                            'images', 'port', 'pull', 'push', 'pause', 'unpause', 'add', 'remove',
                                            'exec', 'edit', 'show', 'create', 'update'])
    parser.add_argument('compose_name', type=str)
    parser.add_argument('additional args passed to compose comand', action='store_true', default=None)
    # command options
    parser.add_argument('--path', metavar='PATH', type=str, help="Link path to yaml into /etc/docker/name")

    argvlen = len(argv)
    narg = argvlen
    if argvlen > 2:
        if '-v' in argv or '--verbose' in argv:
            if argvlen > 3:
                narg = 3
        elif '--path' in argv:
            if argvlen > 4:
                narg = 4
        else:
            narg = 2
    args = parser.parse_args(argv[:narg])
    getattr(Commands(args.compose_name, args.path, argv[narg:]), args.command)()


if __name__ == '__main__':
    main(sys.argv[1:])
