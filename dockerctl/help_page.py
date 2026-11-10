explanation = '''
usage: dockerctl [--path PATH] COMMAND COMPOSE_NAME [COMPOSE_NAME ...] [extra ARGS passed to docker-compose]

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
             images: Shows images used by the services in the composition.
             port: Shows ports used and mapped by the composition.
             pull: Pull images needed by one or more compositions.
             push: Push built images of the composition.
             pause: Pause services in one or more compositions.
             unpause: Unpause services in one or more compositions.
             add: Links the current dir to a folder with the compose_name under /etc/docker.
                Use [--path] only when exactly one compose name is supplied.
             remove: Removes composition folder or link under /etc/docker
             exec: Exec something in a service of a container. [ARGS] can optionally be used to write the command.
             edit: Edit the docker-compose.yml. Uses the EDITOR env var.
             show: Shows the docker-compose.yml in less.
             create: Create dir with compose_name under /etc/docker
             update: Runs pull and up in one command to update a composition.
                     Supports update --backup NAME, update --rollback NAME, and update --commit NAME.
    '''
