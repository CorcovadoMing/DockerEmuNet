from __future__ import with_statement
from fabric.api import local
from fabric.colors import green, magenta, yellow
from fabric.context_managers import hide

active_host = {}

def up():
    with hide('running'):
        #print green(local("docker-compose up -d", capture=True))
        active_host['h1'] = local("docker run -d --name h1 rf37535/nfd nfd")
        print green(local("docker logs " + active_host['h1']))

def mn(topology=3):
    with hide('running'):
        #local("docker-compose run mininet mn --link tc,bw=0.1 --custom /source/topo" + str(topology) + ".py --topo project --switch user --controller remote,ip=192.168.59.103 --mac")
        pass

def ps():
    with hide('running'):
        #print yellow(local("docker-compose ps", capture=True))
        pass

def rm():
    with hide('running'):
        #print magenta("[1/2] Stop all service...", bold=True)
        #print green(local("docker-compose stop", capture=True))

        #print magenta("[2/2] Remove all container...", bold=True)
        #print green(local("docker-compose rm -f", capture=True))
        pass

def down():
    with hide('running'):
        print yellow("*** Clean the emulator", bold=True)
        local("sudo mn -c", capture=True)
        print yellow("*** bye", bold=True)
