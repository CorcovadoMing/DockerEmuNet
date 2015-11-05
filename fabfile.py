from __future__ import with_statement
from fabric.api import local
from fabric.colors import green, magenta, yellow
from fabric.context_managers import hide

hosts = []
switches = []
links = {}

def minishell():
    try:
        cmd = raw_input("console> ")
        if cmd == "status":
            result = local("docker exec -it h1 nfd-status", capture=True)
            print yellow("*** NDN status", bold=True)
            print result
	    print
        elif cmd.split()[0] in ("ls", "cat", "mv", "cp", "clear"):
            try:
                result = local(cmd)
            except:
                pass
            print
        else:
            print cmd + " command not found."
            print
        minishell()
    except (KeyboardInterrupt, EOFError):
        print
        down()

def addSwitch(switches, mode="secure"):
    for s in switches:
        local("sudo ovs-vsctl add-br " + s)
        local("sudo ovs-vsctl set-fail-mode " + s + " " + mode)

def addHost(hosts):
    for h in hosts:
        local("docker run -d --name " + h + " rf37535/nfd nfd", capture=True)

def up(topo='', script=''):
    with hide('running'):
        if topo != '':
            hosts, switches, links = parseTopo(topo)
        else: # Default topology (h1 -- s1 -- s2 -- h2)       
            addSwitch(["s1", "s2"])
            local("sudo ip link add name s1-eth1 type veth peer name s2-eth1")
            local("sudo ovs-vsctl add-port s1 s1-eth1")
            local("sudo ovs-vsctl add-port s2 s2-eth1")
            addHost(["h1", "h2"])
            local("sudo pipework s1 -l s1-eth0 h1 192.168.1.2/24")
            local("sudo pipework s2 -l s2-eth0 h2 192.168.1.3/24")
            minishell()


def down():
    with hide('running'):
        print yellow("*** Shut down NDN hosts", bold=True)
        local("docker rm -f h1", capture=True)
        local("docker rm -f h2", capture=True)
        print yellow("*** Clean the Open vSwitch", bold=True)
        local("sudo mn -c", capture=True)
        print yellow("*** bye", bold=True)
