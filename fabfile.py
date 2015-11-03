from __future__ import with_statement
from fabric.api import local
from fabric.colors import green, magenta, yellow
from fabric.context_managers import hide

def minishell():
    try:
        cmd = raw_input("console> ")
        if cmd == 'status':
            result = local("docker exec -it h1 nfd-status", capture=True)
            print yellow("*** NDN status", bold=True)
            print result
	    print
        minishell()
    except (KeyboardInterrupt, EOFError):
        print
        down()

def up():
    with hide('running'):
        local("docker run -d --name h1 rf37535/nfd nfd", capture=True)
        minishell()


def down():
    with hide('running'):
        print yellow("*** Shut down NDN hosts", bold=True)
        local("docker rm -f h1", capture=True)
        print yellow("*** Clean the Open vSwitch", bold=True)
        local("sudo mn -c", capture=True)
        print yellow("*** bye", bold=True)
