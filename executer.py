# executes the commands for docker-compose

import os


class Executer():

    @classmethod
    def start(args):
      compose_dir = '/etc/docker/' + args
      os.chdir(compose_dir)
      os.system('docker-compose start')

    @classmethod
    def stop(args):
      compose_dir = '/etc/docker/' + args
      os.chdir(compose_dir)
      os.system('docker-compose stop')

    @classmethod
    def restart(args):
      compose_dir = '/etc/docker/' + args
      os.chdir(compose_dir)
      os.system('docker-compose restart')