# Parsing of the command options for this program

import sys
import argparse
from dockerctl import executer

version_nr = "0.1"


def compose_start(option, compose_name):
    for name in compose_name:
        if option == "start":
            executer.start(name)
        elif option == "stop":
            executer.stop(name)
        elif option == "restart":
            executer.restart(name)
        elif option == "ps":
            executer.processes(name)
        else:
            break


def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=True)
    exgroup = parser.add_mutually_exclusive_group()

    exgroup.add_argument('-v', '--version', action="version", version='dockerctl ' + version_nr,
                         help="print version number")
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'ps'])
    parser.add_argument('compose_name', type=str, nargs='+')

    args = parser.parse_args(argv)
    compose_start(args.action, args.compose_name)


if __name__ == '__main__':
    main(sys.argv[1:])
