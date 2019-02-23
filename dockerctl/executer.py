# executes the commands for docker-compose

import os


def path(self):
    if self != "":
        return self + '/'
    else:
        return '/etc/docker/'


def start(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose start')


def stop(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose stop')


def restart(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose restart')


def processes(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose ps')


def up(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose up')


def kill(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose kill')


def pull(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose pull')


def push(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose push')


def rm(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose rm')


def top(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose top')


def pause(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose pause')


def unpause(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose unpause')


def images(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose images')


def port(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose port')


def logss(compose_name):
    compose_dir = path + compose_name
    os.chdir(compose_dir)
    os.system('docker-compose logs')
