# executes the commands for docker-compose
import subprocess
import os


class Commands:

    def __init__(self, compose_name, path):
        self.compose_name = compose_name
        self.path = '/etc/docker/' + compose_name
        self.newpath = path
        print(self.path)

    def start(self):
        subprocess.run(['docker-compose', 'start'], cwd=self.path)

    def stop(self):
        subprocess.run(['docker-compose', 'stop'], cwd=self.path)

    def restart(self):
        subprocess.run(['docker-compose', 'restart'], cwd=self.path)

    def ps(self):
        subprocess.run(['docker-compose', 'ps'], cwd=self.path)

    def up(self):
        subprocess.run(['docker-compose', 'up -d'], cwd=self.path)

    def kill(self):
        subprocess.run(['docker-compose', 'kill'], cwd=self.path)

    def pull(self):
        subprocess.run(['docker-compose', 'pull'], cwd=self.path)

    def push(self):
        subprocess.run(['docker-compose', 'push'], cwd=self.path)

    def rm(self):
        subprocess.run(['docker-compose', 'rm'], cwd=self.path)

    def top(self):
        subprocess.run(['docker-compose', 'top'], cwd=self.path)

    def pause(self):
        subprocess.run(['docker-compose', 'pause'], cwd=self.path)

    def unpause(self):
        subprocess.run(['docker-compose', 'unpause'], cwd=self.path)

    def images(self):
        subprocess.run(['docker-compose', 'images'], cwd=self.path)

    def port(self):
        subprocess.run(['docker-compose', 'port'], cwd=self.path)

    def logs(self):
        subprocess.run(['docker-compose', 'logs'], cwd=self.path)

    #Beginning of own commands
    def add(self):
        if not self.newpath:
            Commands(self.compose_name, os.curdir+"/").add
        elif "docker-compose.yaml" in self.newpath:
            Commands(self.compose_name, self.newpath.rstrip("docker-compose.yaml")).add
        elif "docker-compose.yml" in self.newpath:
            Commands(self.compose_name, self.newpath.rstrip("docker-compose.yml")).add
        else:
            self.newpath = self.newpath.rstrip("/")
            os.symlink(self.newpath, self.path)

    def remove(self):
        os.remove(self.path)
