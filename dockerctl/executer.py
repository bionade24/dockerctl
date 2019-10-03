# executes the commands for docker-compose
import subprocess
import os



def start(compose_name):
    subprocess.run(['docker-compose', 'start'], cwd='/etc/docker' + compose_name)

def stop(compose_name):
    subprocess.run(['docker-compose', 'stop'], cwd='/etc/docker' + compose_name)

def restart(compose_name):
    subprocess.run(['docker-compose', 'restart'], cwd='/etc/docker' + compose_name)

def processes(compose_name):
    subprocess.run(['docker-compose', 'ps'], cwd='/etc/docker' + compose_name)

def up(compose_name):
    subprocess.run(['docker-compose', 'up -d'], cwd='/etc/docker' + compose_name)

def kill(compose_name):
    subprocess.run(['docker-compose', 'kill'], cwd='/etc/docker' + compose_name)

def pull(compose_name):
    subprocess.run(['docker-compose', 'pull'], cwd='/etc/docker' + compose_name)

def push(compose_name):
    subprocess.run(['docker-compose', 'push'], cwd='/etc/docker' + compose_name)

def rm(compose_name):
    subprocess.run(['docker-compose', 'rm'], cwd='/etc/docker' + compose_name)

def top(compose_name):
    subprocess.run(['docker-compose', 'top'], cwd='/etc/docker' + compose_name)

def pause(compose_name):
    subprocess.run(['docker-compose', 'pause'], cwd='/etc/docker' + compose_name)

def unpause(compose_name):
    subprocess.run(['docker-compose', 'unpause'], cwd='/etc/docker' + compose_name)

def images(compose_name):
    subprocess.run(['docker-compose', 'images'], cwd='/etc/docker' + compose_name)

def port(compose_name):
    subprocess.run(['docker-compose', 'port'], cwd='/etc/docker' + compose_name)

def logs(compose_name):
    subprocess.run(['docker-compose', 'logs'], cwd='/etc/docker' + compose_name)


def add(compose_name, path):
    if not path:
        add(compose_name, os.curdir+"/")
    elif "docker-compose.yaml" in path:
        add(compose_name, path.rstrip("docker-compose.yaml"))
    elif "docker-compose.yml" in path:
        add(compose_name, path.rstrip("docker-compose.yml"))
    else:
        path = path.rstrip("/")
        os.symlink(path, "/etc/docker/" + compose_name)


def remove(compose_name):
    os.remove("/etc/docker/" + compose_name)
