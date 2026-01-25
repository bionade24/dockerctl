# Parsing of the command options for this program

import sys
import getopt
from dockerctl.executor import Commands
from dockerctl import help_page

VERSION_NR = "1.2"


def main(argv):
    path_arg = None

    # Parse command-line options using getopt
    # Short options: -v (version), -h (help), -l (list)
    # Long options: --version, --help, --list, --path=PATH
    try:
        opts, args = getopt.getopt(argv, 'vhl', ['version', 'help', 'list', 'path='])
    except getopt.GetoptError as e:
        print("Error: {}".format(str(e)), file=sys.stderr)
        sys.exit(1)

    # Process options
    for opt, arg in opts:
        if opt in ('-v', '--version'):
            print('dockerctl ' + VERSION_NR)
            sys.exit(0)
        elif opt in ('-h', '--help'):
            print(help_page.explanation)
            sys.exit(0)
        elif opt in ('-l', '--list'):
            Commands.ls()
            sys.exit(0)
        elif opt == '--path':
            path_arg = arg

    # Parse positional arguments
    if len(args) < 2:
        print("Error: Missing required arguments COMMAND and COMPOSE_NAME", file=sys.stderr)
        sys.exit(1)

    command = args[0]
    compose_name = args[1]
    additional_args = args[2:] if len(args) > 2 else []

    # Create executor and run command
    cmd_executor = Commands(compose_name, path_arg, additional_args)
    cmd_executor.exec_cmd(command)


if __name__ == '__main__':
    main(sys.argv[1:])
