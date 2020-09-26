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
usage: dockerctl [-h] [-v] [-l] [--list] [--path PATH] COMMAND COMPOSE_NAME [extra ARGS passed to docker-compose]
                 start: Start the composition
                 stop: Stop the composition
                 restart: Restart it.
                 ps: Show processes of services in composition.
                 up: Calls docker-compose up -d, composition runs as daemon afterwards.
                 kill: Kill the whole composition, if you don't pass extra args.
                 rm: Removes all volumes created by the compose yaml.
                 top: Get information about the processes in the services.
                 logs: Get the logs of the whole composition. Pass -f to get ongoing information.
                 images: Shows images used by the services in the composition.
                 port: Shows the port used and mapped by the composition.
                 pull: Pull images needed by the composition.
                 push: Push built images of the composition.
                 pause: Pause all services in the composition.
                 unpause: Unpause them.
                 add: Links the current dir to a folder with the compose_name under /etc/docker. Use [--path] to link an other path than curdir.
                 remove: Removes composition folder or link under /etc/docker
                 exec: Exec something in a service of a container. [ARGS] can optionally be used to write the command.
                 edit: Edit the docker-compose.yml. Uses the EDITOR env var.
                 show: Shows the docker-compose.yml in less.
                 create: Create dir with compos_name under /etc/docker
                 update: Runs pull and up in one command to update a composition.
```