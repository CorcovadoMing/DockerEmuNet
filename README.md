# DockerEmuNet
*Docker-based generic network emulator*

##### The purpose of this project is to emulate the different types of networking which includes SDN and NDN by using the docker as the virtualized host

### Features:

1. Ability to emulate SDN (Software-Defined Network), NDN(Named-Data Network) or conventional network
2. Isolated file system per host
3. Support virtual network topology
4. Integrate the log system (i.e. fluentd)

### Usage:

To run the default topology (h1 <--> s1 <--> s2 <--> h2)
```
./den
```

Also, you may want to pass your own topology configure file to it

```
./den --topo topo.config
```

The topology configuration file is defined as below

```
[host]
h1  
h2
h3

[switch]
s1
s2
s3

[link]
h1 s1
h2 s2
h3 s3
s1 s2
s2 s3
```

which defines the topology

```
s1 <--> s2 <--> s3
|       |       |
h1      h2      h3
```

### Dependencies:

1. Docker
2. Open vSwitch
3. OpenVirteX (Optional)
4. Fluentd (Optional)
