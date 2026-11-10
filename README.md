# dockerctl

Python Script to steer docker-compose-yaml's from everywhere.

https://pypi.org/project/dockerctl/

Installation:
==

Installation from PyPi: `pip install dockerctl`  
Manual installation: Type `pip install .` in the project's directory  
  
*Be aware that you have to call python3 pip, so if you're on an distro that defaults to py2, use* `python3 -m pip`

This program is released under the GPLv3. See "LICENSE" for further information.

This program is going to have the first release soon, please report bugs and propose enhancements.

```
usage: dockerctl [-h] [-v] [-l] [--list] [--path PATH] COMMAND COMPOSE_NAME [COMPOSE_NAME ...] [extra ARGS passed to docker-compose]

             start: Start one or more compositions.
             stop: Stop one or more compositions.
             restart: Restart one or more compositions.
             ps: Show processes of services in one or more compositions.
             up: Calls docker-compose up -d for one or more compositions.
             down: Calls docker-compose down for one or more compositions.
             kill: Kill one or more compositions.
             rm: Remove volumes created by one or more compose files.
             top: Get information about processes in one or more services.
             logs: Get logs for one or more compositions. Pass -f for ongoing output.
             images: Show the images used by the services in the composition.
             port: Show the ports used and mapped by the composition.
             pull: Pull images needed by one or more compositions.
             push: Push built images of the composition.
             pause: Pause one or more compositions.
             unpause: Unpause one or more compositions.
             add: Link the current dir to a folder with the compose_name under /etc/docker.
                 Use [--path] only when exactly one compose name is supplied.
             remove: Remove a composition folder or link under /etc/docker.
             exec: Execute something in a service of a container. [ARGS] can optionally be used to write the command.
             edit: Edit the docker-compose.yml. Uses the EDITOR env var.
             show: Show the docker-compose.yml in less.
             create: Create a dir with compose_name under /etc/docker.
             update: Pull and recreate a composition.
                     Supports --backup, --rollback, and --commit for image backup/restore/commit flows.
```

Notes:
- `--path` is still supported when exactly one compose name is supplied.
- When more than one compose name is passed, the same command is applied to each in order.
- `--path` is not applied for multi-compose invocations because a single custom root path would be ambiguous.

Update transaction workflow:

The backup suffix uses the current image tag plus a timestamp, for example:
`myimage:1.2.3-backup-10-11-16-45`

```text
backup: tags the original image before the pull/up cycle and stores the backup mapping
rollback: retags the backup back to the original image name for recovery
commit: clears the saved backup state once the update is accepted
```

DISCLAIMER: Almost everything in the diff between version 1.1 and 1.2 has been vibe-coded to try out its possibilities.