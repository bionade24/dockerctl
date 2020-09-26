# Parsing of the command options for this program

import sys
import argparse
from dockerctl.executer import Commands
from dockerctl import actions
from dockerctl import help_page

VERSION_NR = "0.5"


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-v', '--version', action="version", version='dockerctl ' + VERSION_NR,
                         help="Print version number")
    parser.add_argument('-h', '--help', action=actions.ShowText, text=help_page.explanation)
    parser.add_argument('-l', '--list', action=actions.ListServices)
    # common commands
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'ps', 'up', ' kill', 'rm', 'top', 'logs',
                                            'images', 'port', 'pull', 'push', 'pause', 'unpause', 'add', 'remove',
                                            'exec', 'edit', 'show', 'create', 'update'])
    parser.add_argument('compose_name', type=str)
    parser.add_argument('additional args passed to compose command', action='store_true', default=None)
    # command options
    parser.add_argument('--path', metavar='PATH', type=str, help="Link path to yaml into /etc/docker/name")

    argvlen = len(argv)
    narg = argvlen
    if argvlen > 2:
        if '--path' in argv:
            if argvlen > 4:
                narg = 4
        else:
            narg = 2
    args = parser.parse_args(argv[:narg])
    getattr(Commands(args.compose_name, args.path, argv[narg:]), args.command)()


if __name__ == '__main__':
    main(sys.argv[1:])
