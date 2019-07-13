# executes the commands for docker-compose

import os


def start(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose start')


def stop(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose stop')


def restart(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose restart')


def processes(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose ps')


def up(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose up -d')


def kill(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose kill')


def pull(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose pull')


def push(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose push')


def rm(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose rm')


def top(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose top')


def pause(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose pause')


def unpause(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose unpause')


def images(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose images')


def port(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose port')


def logs(compose_name):
    os.chdir('/etc/docker/' + compose_name)
    os.system('docker-compose logs')


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
