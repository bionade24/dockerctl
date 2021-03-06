# executes the commands for docker-compose
import subprocess
import os
import shutil
import shlex
import glob


class Base__funcs:

    def __init__(self, path, compose_name, append):
        self.path = path
        self.compose_name = compose_name
        self.append = append

    def checkpath(self):
        if not os.path.exists(self.path):
            if os.stat(self.path).st_gid not in os.getresgid():
                raise RuntimeError("{0} This user doesn't have access".format(self.compose_name))
            else:
                raise RuntimeError("{0} does not exist".format(self.compose_name))
        elif not os.path.isdir(self.path):
            raise RuntimeError("{0} is not a directory".format(self.compose_name))

    def map_cmd(self, cmd):
        self.checkpath()
        if len(self.append) == 0:
            subprocess.run(['docker-compose', cmd], cwd=self.path)
        else:
            subprocess.run(['docker-compose', cmd] + self.append, cwd=self.path)


class Commands(Base__funcs):

    EDITOR = os.environ.get('EDITOR', 'vi')

    def __init__(self, compose_name, path_arg, append=None):
        self.compose_name = compose_name
        self.path = '/etc/docker/' + compose_name
        self.path_arg = path_arg
        self.append = append
        super().__init__(self.path, self.compose_name, self.append)

    #Command mapping for docker-compose

    def start(self):
        self.map_cmd("start")

    def stop(self):
        self.map_cmd("stop")

    def restart(self):
        self.map_cmd("restart")

    def ps(self):
        self.map_cmd("ps")

    def up(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'up', '-d'], cwd=self.path)

    def kill(self):
        self.map_cmd("kill")

    def pull(self):
        self.map_cmd("pull")

    def push(self):
        self.map_cmd("push")

    def rm(self):
        self.map_cmd("rm")

    def top(self):
        self.map_cmd("top")

    def pause(self):
        self.map_cmd("pause")

    def unpause(self):
        self.map_cmd("unpause")

    def images(self):
        self.map_cmd("images")

    def port(self):
        self.map_cmd("port")

    def logs(self):
        self.map_cmd("logs")

    def exec(self):
        self.checkpath()
        get_service_list = subprocess.Popen(['docker-compose', 'config', '--services'],
        cwd=self.path, stdout=subprocess.PIPE).communicate()
        service_list = get_service_list[0].split(b'\n')
        service_list.remove(b'') #Removing last element of list because it' empty
        outline = "Which service do you want to choose?: \n"
        i = 1
        for service in service_list:
            outline += "{}: {}\n".format(i, service.decode("utf-8"))
            i += 1
        print(outline)
        nr_input = input("Enter number of container: ")
        if nr_input == '':
            RuntimeError("Please specify a container from the list, e.g. 1")
        serv_nr = int(nr_input)
        if not self.append:
            self.append = shlex.split(input("Command to execute: "))
        if serv_nr > len(service_list) or serv_nr < 2:
            RuntimeError("Specified index doesn't match to a container in that service!")
        subprocess.run(['docker-compose', 'exec', service_list[serv_nr - 1]] + self.append, cwd=self.path)

    #Beginning of own commands
    def add(self):
        if not self.path_arg:
            Commands(self.compose_name, os.getcwd()+"/").add()
        elif "docker-compose.yaml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yaml")).add()
        elif "docker-compose.yml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yml")).add()
        else:
            self.path_arg = self.path_arg.rstrip("/")
            os.symlink(self.path_arg, self.path)

    def remove(self):
        self.checkpath()
        if os.path.islink(self.path):
            os.remove(self.path)
            print("Symlink: origin still exists")
        elif os.path.isdir(self.path):
            shutil.rmtree(self.path)
        else:
            raise RuntimeError("Can't remove: Neither link nor directory")

    def edit(self):
        self.checkpath()
        available_files = os.listdir(self.path)
        filepath = ""
        if "docker-compose.yml" in available_files and "docker-compose.yaml" in available_files:
            raise RuntimeError("More than one compose YAML in {0}".format(self.path))
        elif "docker-compose.yml" in available_files:
            filepath = os.path.join(self.path, "docker-compose.yml")
        elif "docker-compose.yaml" in available_files:
            filepath = os.path.join(self.path, "docker-compose.yaml")
        else:
            raise RuntimeError("No docker-compose.y*ml in {0}".format(self.path))
        subprocess.call([self.EDITOR, filepath])

    def show(self):
        self.EDITOR = 'less'
        self.edit()

    def create(self):
        os.mkdir(self.path)
        with open(os.path.join(self.path, "docker-compose.yaml"), "w") as fobj:
            fobj.writelines("#This is a autogenerated compose-yaml by dockerctl")
        self.edit()

    def update(self):
        #TODO:Can I check if it was updated?
        self.pull()
        self.up()

    @staticmethod
    def ls():
        services_paths = glob.glob('/etc/docker/*/docker-compose.y*')
        for service in services_paths:
            print(service.split('/')[3])
