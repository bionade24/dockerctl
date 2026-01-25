# executes the commands for docker-compose
import subprocess
import os
import shutil
import shlex
import glob


DOCKER_COMPOSE_CMD = ["docker", "compose"]
DOCKER_COMPOSE_CMD_OLD =  ["docker-compose",]
DOCKERCTL_DIR = "/etc/dockerctl/"
DOCKERCTL_DIR_OLD = "/etc/docker/"


class Base__funcs:

    def __init__(self, path, compose_name, append):
        self.path = path
        self.compose_name = compose_name
        self.append = append

    def checkpath(self, check_compose_yml=False):
        if not os.path.exists(self.path):
            raise RuntimeError(
                "Composition '{0}' not found.\n"
                "Looked in: {1}\n"
                "Available compositions can be listed with 'dockerctl --list'".format(
                    self.compose_name, self.path))
        elif not os.path.isdir(self.path):
            raise RuntimeError(
                "Composition path '{0}' exists but is not a directory.\n"
                "Expected: {1}".format(self.compose_name, self.path))
        if check_compose_yml and not (os.path.exists(os.path.join(self.path, "docker-compose.yml")) or \
            os.path.exists(os.path.join(self.path, "docker-compose.yaml"))):
            raise RuntimeError(
                "No docker-compose.yml or docker-compose.yaml found in '{0}'.".format(self.path))

    def map_cmd(self, cmd):
        self.checkpath(check_compose_yml=True)
        if len(self.append) == 0:
            subprocess.run(DOCKER_COMPOSE_CMD + shlex.split(cmd), cwd=self.path)
        else:
            subprocess.run(DOCKER_COMPOSE_CMD + shlex.split(cmd + " " + " ".join(self.append)), cwd=self.path)


class Commands(Base__funcs):

    EDITOR = os.environ.get('EDITOR', 'vi')
    PASSTROUGH_CMDS = ["start", "stop", "restart", "ps", "down", "kill", "pull", "push", "rm", "pause", "unpause", "images", "port", "logs"]
    DEVIATE_CMDS = {"up": "up -d"}

    def __init__(self, compose_name, path_arg, append=None):
        global DOCKER_COMPOSE_CMD
        self.compose_name = compose_name
        self.path = os.path.join(DOCKERCTL_DIR, compose_name)
        if not os.path.exists(self.path):
            old_path = os.path.join(DOCKERCTL_DIR_OLD, compose_name)
            self.path = old_path if os.path.exists(old_path) else self.path
            if not os.path.exists(DOCKERCTL_DIR):
                os.mkdir(DOCKERCTL_DIR)
        self.path_arg = path_arg
        self.append = append
        output = subprocess.run(DOCKER_COMPOSE_CMD, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        if 1 == output.returncode:
            DOCKER_COMPOSE_CMD = DOCKER_COMPOSE_CMD_OLD
        super().__init__(self.path, self.compose_name, self.append)

    def exec_cmd(self, compose_cmd):
        if compose_cmd in self.PASSTROUGH_CMDS:
            self.map_cmd(compose_cmd)
        elif compose_cmd in self.DEVIATE_CMDS.keys():
            self.map_cmd(self.DEVIATE_CMDS[compose_cmd])
        elif hasattr(self, compose_cmd):
            getattr(self, compose_cmd)()
        else:
            supported_cmds = (self.PASSTROUGH_CMDS + list(self.DEVIATE_CMDS.keys()) + 
                            [attr for attr in dir(self) if not attr.startswith('_') and callable(getattr(self, attr))])
            raise RuntimeError(
                "Unknown command '{0}'.\n"
                "Supported commands: {1}\n"
                "Use 'dockerctl --help' for more information.".format(
                    compose_cmd, ', '.join(sorted(set(supported_cmds)))))

    def exec(self):
        self.checkpath()
        get_service_list = subprocess.Popen(DOCKER_COMPOSE_CMD + ['config', '--services'],
        cwd=self.path, stdout=subprocess.PIPE).communicate()
        service_list = get_service_list[0].split(b'\n')
        service_list.remove(b'') # Removing last element of list because it' empty
        outline = "Which service do you want to choose?: \n"
        i = 1
        for service in service_list:
            outline += "{}: {}\n".format(i, service.decode("utf-8"))
            i += 1
        print(outline)
        nr_input = input("Enter number of container: ")
        if nr_input == '':
            raise RuntimeError("Error: No container selection provided.\nPlease specify a container number from the list (e.g., 1)")
        try:
            serv_nr = int(nr_input)
        except ValueError:
            raise RuntimeError(
                "Error: Invalid container selection '{0}'.\n"
                "Please enter a valid number from the list above.".format(nr_input))
        if not self.append:
            self.append = shlex.split(input("Command to execute: "))
        if serv_nr > len(service_list) or serv_nr < 1:
            raise RuntimeError(
                "Error: Container selection '{0}' out of range.\n"
                "Valid range is 1-{1}. Please select a container from the list above.".format(
                    serv_nr, len(service_list)))
        subprocess.run(DOCKER_COMPOSE_CMD + ['exec', service_list[serv_nr - 1]] + self.append, cwd=self.path)

    # Beginning of own commands
    def add(self):
        if not self.path_arg:
            Commands(self.compose_name, os.getcwd()+"/").add()
        elif "docker-compose.yaml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yaml")).add()
        elif "docker-compose.yml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yml")).add()
        else:
            self.path_arg = self.path_arg.rstrip("/")
            if not os.path.exists(self.path_arg):
                raise RuntimeError(
                    "Error: Path '{0}' does not exist.\n"
                    "Please provide a valid path to a docker-compose directory.".format(self.path_arg))
            if not os.path.isdir(self.path_arg):
                raise RuntimeError(
                    "Error: '{0}' is not a directory.\n"
                    "Please provide a directory containing docker-compose files.".format(self.path_arg))
            try:
                os.symlink(self.path_arg, self.path)
                print("Successfully linked '{0}' to {1}".format(self.compose_name, self.path_arg))
            except FileExistsError:
                raise RuntimeError(
                    "Error: Composition '{0}' already exists at {1}".format(
                        self.compose_name, self.path))
            except PermissionError:
                raise RuntimeError(
                    "Error: Permission denied creating symlink at '{0}'.\n"
                    "You may need sudo privileges.".format(self.path))

    def remove(self):
        self.checkpath()
        if os.path.islink(self.path):
            os.remove(self.path)
            print("Removed symlink for '{0}' (original still exists)".format(self.compose_name))
        elif os.path.isdir(self.path):
            shutil.rmtree(self.path)
            print("Removed composition directory for '{0}'".format(self.compose_name))
        else:
            raise RuntimeError(
                "Error: Cannot remove '{0}'.\n"
                "Path '{1}' is neither a symlink nor a directory.".format(
                    self.compose_name, self.path))

    def edit(self):
        self.checkpath()
        available_files = os.listdir(self.path)
        filepath = ""
        if "docker-compose.yml" in available_files and "docker-compose.yaml" in available_files:
            raise RuntimeError(
                "Error: Multiple docker-compose files found in '{0}'.\n"
                "Found: docker-compose.yml and docker-compose.yaml\n"
                "Please keep only one file.".format(self.path))
        elif "docker-compose.yml" in available_files:
            filepath = os.path.join(self.path, "docker-compose.yml")
        elif "docker-compose.yaml" in available_files:
            filepath = os.path.join(self.path, "docker-compose.yaml")
        else:
            raise RuntimeError(
                "Error: No docker-compose file found in '{0}'.\n"
                "Expected either 'docker-compose.yml' or 'docker-compose.yaml'.".format(self.path))
        subprocess.call([self.EDITOR, filepath])

    def show(self):
        self.EDITOR = 'less'
        self.edit()

    def create(self):
        try:
            os.mkdir(self.path)
        except FileExistsError:
            raise RuntimeError(
                "Error: Composition directory already exists at '{0}'".format(self.path))
        except PermissionError:
            raise RuntimeError(
                "Error: Permission denied creating directory at '{0}'.\n"
                "You may need sudo privileges.".format(self.path))
        try:
            with open(os.path.join(self.path, "docker-compose.yaml"), "w") as fobj:
                fobj.writelines("# Docker Compose file for '{0}'\n# Auto-generated by dockerctl\n".format(self.compose_name))
        except IOError as e:
            raise RuntimeError(
                "Error: Failed to create docker-compose.yaml in '{0}'.\n{1}".format(
                    self.path, str(e)))
        self.edit()

    def update(self):
        # TODO:Can I check if it was updated?
        self.exec_cmd("pull")
        self.exec_cmd("up")

    @staticmethod
    def ls():
        services_paths = glob.glob(DOCKERCTL_DIR + '*/docker-compose.y*')
        for service in services_paths:
            print(service.split('/')[3])
