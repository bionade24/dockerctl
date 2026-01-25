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
        print("Error: Invalid option - {}".format(str(e)), file=sys.stderr)
        print("\nUse 'dockerctl --help' for usage information.", file=sys.stderr)
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
    if len(args) == 0:
        print("Error: Missing required COMMAND argument", file=sys.stderr)
        print("\nUsage: dockerctl [OPTIONS] COMMAND COMPOSE_NAME [ARGS]", file=sys.stderr)
        print("Use 'dockerctl --help' for detailed usage information.", file=sys.stderr)
        sys.exit(1)
    elif len(args) == 1:
        print("Error: Missing required COMPOSE_NAME argument", file=sys.stderr)
        print("\nUsage: dockerctl [OPTIONS] {} COMPOSE_NAME [ARGS]".format(args[0]), file=sys.stderr)
        print("\nCOMMAND: The docker-compose command to execute (e.g., start, stop, logs)", file=sys.stderr)
        print("COMPOSE_NAME: Name of the compose service in /etc/dockerctl/", file=sys.stderr)
        print("Use 'dockerctl --help' for more information.", file=sys.stderr)
        sys.exit(1)

    command = args[0]
    compose_name = args[1]
    additional_args = args[2:] if len(args) > 2 else []

    # Create executor and run command
    cmd_executor = Commands(compose_name, path_arg, additional_args)
    cmd_executor.exec_cmd(command)


if __name__ == '__main__':
    main(sys.argv[1:])
