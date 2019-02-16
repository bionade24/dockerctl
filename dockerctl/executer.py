# executes the commands for docker-compose

import os


class Executer():

    def start(compose_name):
        compose_dir = '/etc/docker/' + compose_name
        os.chdir(compose_dir)
        os.system('docker-compose start')

    def stop(compose_name):
        compose_dir = '/etc/docker/' + compose_name
        os.chdir(compose_dir)
        os.system('docker-compose stop')

    def restart(compose_name):
        compose_dir = '/etc/docker/' + compose_name
        os.chdir(compose_dir)
        os.system('docker-compose restart')

    def processes(compose_name):
        compose_dir = '/etc/docker/' + compose_name
        os.chdir(compose_dir)
        os.system('docker-compose ps')
