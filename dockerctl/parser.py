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
    positional = list(args[1:])
    update_mode = None

    if command == 'update' and positional and positional[0].startswith('--'):
        update_mode = positional[0]
        positional = positional[1:]

    if not positional:
        print("Error: Missing required COMPOSE_NAME argument", file=sys.stderr)
        print("\nUsage: dockerctl [OPTIONS] {} COMPOSE_NAME [COMPOSE_NAME ...] [ARGS]".format(command), file=sys.stderr)
        print("\nCOMMAND: The docker-compose command to execute (e.g., start, stop, logs)", file=sys.stderr)
        print("COMPOSE_NAME: Name of the compose service in /etc/dockerctl/", file=sys.stderr)
        print("Use 'dockerctl --help' for more information.", file=sys.stderr)
        sys.exit(1)

    compose_names = []
    additional_args = []
    commands_with_additional_args = {'exec', 'logs', 'port'}

    if command in commands_with_additional_args:
        if not positional:
            print("Error: Missing required COMPOSE_NAME argument", file=sys.stderr)
            print("\nUsage: dockerctl [OPTIONS] {} COMPOSE_NAME [ARGS]".format(command), file=sys.stderr)
            print("\nCOMMAND: The docker-compose command to execute (e.g., start, stop, logs)", file=sys.stderr)
            print("COMPOSE_NAME: Name of the compose service in /etc/dockerctl/", file=sys.stderr)
            print("Use 'dockerctl --help' for more information.", file=sys.stderr)
            sys.exit(1)
        compose_names = [positional[0]]
        additional_args = positional[1:]
    else:
        for index, item in enumerate(positional):
            if item.startswith('-'):
                additional_args = positional[index:]
                break
            compose_names.append(item)

        if not compose_names:
            print("Error: Missing required COMPOSE_NAME argument", file=sys.stderr)
            print("\nUsage: dockerctl [OPTIONS] {} COMPOSE_NAME [COMPOSE_NAME ...] [ARGS]".format(command), file=sys.stderr)
            print("\nCOMMAND: The docker-compose command to execute (e.g., start, stop, logs)", file=sys.stderr)
            print("COMPOSE_NAME: Name of the compose service in /etc/dockerctl/", file=sys.stderr)
            print("Use 'dockerctl --help' for more information.", file=sys.stderr)
            sys.exit(1)

    if path_arg is not None and len(compose_names) > 1:
        print("Error: --path can only be used when a single compose name is provided.", file=sys.stderr)
        sys.exit(1)

    if update_mode is not None:
        additional_args = [update_mode] + additional_args

    for compose_name in compose_names:
        cmd_executor = Commands(compose_name, path_arg if len(compose_names) == 1 else None, additional_args)
        cmd_executor.exec_cmd(command)


if __name__ == '__main__':
    main(sys.argv[1:])
