from __future__ import with_statement
from fabric.api import local
from fabric.colors import green, magenta, yellow, red
from fabric.context_managers import hide

hosts = []
switches = []
ips = 2
faces = {}
links = {}

def minishell():
    try:
        cmd = raw_input("console> ")
        if cmd.split()[0] in hosts: # host commands
            try:
                local("docker exec -it " + cmd)
	    except:
                pass # prevent the exit(!0)
            print
        elif cmd.split()[0] in ("ls", "cat", "mv", "cp", "clear"): # console reserve words
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

def addController(controller):
    if controller == "floodlight"
        local("docker run -d --name floodlight -p 6653:6653 -p 8080:8080 rf37535/floodlight", capture=True)
    elif controller == "ryu"
        local("docker run -d --name ryu -p 6653:6633 -p 8080:8080 -v `pwd`:/source -w `pwd`/controller/test rf37535/ryu ryu-manager app.py", capture=True)
    else:
        print red("unknown controller type", bold=True)

def addSwitch(switches, mode="secure"):
    for s in switches:
        local("sudo ovs-vsctl add-br " + s)
        local("sudo ovs-vsctl set-fail-mode " + s + " " + mode)
        local("sudo ovs-vsctl set-controller " + s + " tcp:127.0.0.1:6653")

def addLink(links):
    global ips
    fr_type = None
    to_type = None
    s = None
    h = None
    
    for key in links:
        fr, to = key, links[key]
        if fr in hosts:
            fr_type = "host"
            h = fr
        elif fr in switches:
            fr_type = "switch"
            s = fr
        if to in hosts:
            to_type = "host"
            h = to
        elif to in switches:
            to_type = "switch"
            s = to

        if fr_type != to_type: # link switch and host
            local("sudo pipework " + s + " -l " + s + "-eth" + str(faces[s]) + " " + h + " 192.168.1." + str(ips) + "/24")
            faces[s] += 1
            ips += 1
        else: # link switch to switch
            local("sudo ip link add name " + fr + "-eth" + str(faces[fr]) + " type veth peer name " + to + "-eth" + str(faces[to]))
            local("sudo ovs-vsctl add-port " + fr + " " + fr + "-eth" + str(faces[fr]))
            local("sudo ovs-vsctl add-port " + to + " " + to + "-eth" + str(faces[to]))
            faces[fr] += 1
            faces[to] += 1


def addHost(hosts):
    for h in hosts:
        local("docker run -d --log-driver=fluentd --log-opt fluentd-tag=den." + h + "  -v `pwd`:`pwd` -w `pwd` --name " + h + " rf37535/nfd nfd", capture=True)

def parseTopo(topo):
    parseflag = [False, False, False]
    with open(topo) as f:
        for lines in f:
            line = lines.rstrip('\n')
                  
            if parseflag[0] and len(line.split()):
                hosts.append(line.split()[0])
            elif parseflag[1] and len(line.split()):
                switches.append(line.split()[0])
                faces[line.split()[0]] = 1
            elif parseflag[2] and len(line.split()):
                fr, to = line.split()
                links[fr] = to

            if len(line.split()) and line.split()[0] == "[host]":
                parseflag = [True, False, False]
            elif len(line.split()) and line.split()[0] == "[switch]":
                parseflag = [False, True, False]
            elif len(line.split()) and line.split()[0] == "[link]":
                parseflag = [False, False, True]
            elif not len(line.split()):
                parseflag = [False, False, False]

def up(topo='', script='',controller='floodlight'):
    global hosts, switches, links, faces
    with hide('running'):
        if topo != '':
            parseTopo(topo)
        else: # Default topology (h1 -- s1 -- s2 -- h2)
            hosts = ['h1', 'h2']
            switches = ['s1', 's2']
            faces = {'s1':1, 's2':1}
            links = {'h1':'s1', 'h2':'s2', 's1':'s2'}
        addController(controller)
        addSwitch(switches)
        addHost(hosts)
        addLink(links)
        minishell()



def down():
    with hide('running'):
        print yellow("*** Shut down NDN hosts", bold=True)
        for _ in hosts:
            local("docker rm -f " + _, capture=True)
        print yellow("*** Clean the Open vSwitch", bold=True)
        local("sudo mn -c", capture=True)
        print yellow("*** Shut down the default controller", bold=True)
        try:
            local("docker rm -f floodlight", capture=True)
            local("docker rm -f ryu", capture=True)
        except:
            pass
        print yellow("*** bye", bold=True)



