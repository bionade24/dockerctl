# executes the commands for docker-compose
import subprocess
import os


class Commands:

    EDITOR = os.environ.get('EDITOR', 'vi')

    def __init__(self, compose_name, path_arg):
        self.compose_name = compose_name
        self.path = '/etc/docker/' + compose_name
        self.path_arg = path_arg

    def start(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'start'], cwd=self.path)

    def stop(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'stop'], cwd=self.path)

    def restart(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'restart'], cwd=self.path)

    def ps(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'ps'], cwd=self.path)

    def up(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'up -d'], cwd=self.path)

    def kill(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'kill'], cwd=self.path)

    def pull(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'pull'], cwd=self.path)

    def push(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'push'], cwd=self.path)

    def rm(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'rm'], cwd=self.path)

    def top(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'top'], cwd=self.path)

    def pause(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'pause'], cwd=self.path)

    def unpause(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'unpause'], cwd=self.path)

    def images(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'images'], cwd=self.path)

    def port(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'port'], cwd=self.path)

    def logs(self):
        self.checkpath()
        subprocess.run(['docker-compose', 'logs'], cwd=self.path)

    #Beginning of own commands
    def add(self):
        if not self.path_arg:
            Commands(self.compose_name, os.curdir+"/").add()
        elif "docker-compose.yaml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yaml")).add()
        elif "docker-compose.yml" in self.path_arg:
            Commands(self.compose_name, self.path_arg.rstrip("docker-compose.yml")).add()
        else:
            self.path_arg = self.path_arg.rstrip("/")
            os.symlink(self.path_arg, self.path)

    def remove(self):
        self.checkpath()
        os.remove(self.path)

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

    def create(self):
        os.mkdir(self.path)
        with open(os.path.join(self.path, "docker-compose.yaml"), "w") as fobj:
            fobj.writelines("#This is a autogenerated compose-yaml by dockerctl")
        self.edit()

    def update(self):
        #TODO:Can I check if it was updated?
        self.pull()
        self.up()

    def checkpath(self):
        if not os.path.exists(self.path):
            raise RuntimeError("{0} does not exist".format(self.compose_name))
        elif not os.path.isdir(self.path):
            raise RuntimeError("{0} is not a directory".format(self.compose_name))
