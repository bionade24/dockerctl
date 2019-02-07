# Parsing of the command options for this program

import sys
import argparse
from executer import Executer


version = "0.1"


def compose_start(option, compose_name):
    for name in compose_name:
        if option == "start":
            Executer.start(name)
        elif option == "stop":
            Executer.stop(name)
        elif option == "restart":
            Executer.restart(name)
        elif option == "ps":
            Executer.processes(name)
        else:
            break



def main(argv):
    parser = argparse.ArgumentParser(prog='dockerctl', add_help=False)
    exgroup = parser.add_mutually_exclusive_group()

    exgroup.add_argument('-v', '--version', action="store_true", help="print version number")
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'ps'])
    parser.add_argument('compose_name', type=str, nargs='+')

    args = parser.parse_args(argv)
    if args.version:
        print("version " + version)
    compose_start(args.action, args.compose_name)


if __name__ == "__main__":
    main(sys.argv[1:])
