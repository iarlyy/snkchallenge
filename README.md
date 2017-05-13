snkchallenge
======================
snkchallenge is a demonstration project that implements a virtual environment composed by two instances(aka sensors) that send data to a messaging broker, a indexer instance responsible for indexing all messages received by the broker and a web instance that enables internet users to view the indexed data.

## Table of content
- [Overview](#overview)
- [Installation](#installation)
- [Automating and Scaling](#automating-and-scaling)
- [TO DO](#todo)
- [License](#license)
- [Links](#links)

### Overview
The snkchallenge demonstrates how to implement the set of minimum applications to have a reliable distributed network of IoT devices and how they should communicate to each other. 

All components were shipped within docker containers, which brings flexibility to scale and automate the whole solution. 

Components of the solution:
- Sensors (2 containers)
Responsible for collecting and pushing environmental data to the MQ broker through the protocol MQTT(ISO/IEC 20922:2016). In this demonstration, the sensors are pushing simulated data by sending random numbers between 1-1000 to the message broker. No QoS levels were set for this demonstration.

- MQ Broker (1 container)
Responsible for receiving all data pushed by the sensors and responsible for providing a channel that the indexer can use to pull the messages sent by the sensors. We are using in this demonstration mosquitto as MQTT broker for our solution.

- Indexer (1 container)
Responsible for subscribing the messages sent by the sensors to the MQ broker and indexing in a way that it can be searched and retrieved. The indexer stores all the messages in a local SQLite database, the same database used by the web instace to present the data to the internet users. SQLite was used only to demonstrate the application architecture, in a production environment a reliable database backend should be considered to be deployed.

- Web Instance (1 container)
Provides HTTP channel to internet users view all sensors' data already indexed in the database. In this demonstration the Web instance only returns in a JSON format the average number of all messages sent by all sensors in the last 5 seconds. The web interface was developed using cherrypy, a minimalist python web framework.

Software and versions used:
- CentOS 7.3
- python 2.7.5
- python-paho-mqtt 1.2.3
- Cherrypy 10.2.1
- docker-ce 17.03
- docker-compose 1.13
- mosquito (latest docker build)

### Installation
The steps below describe how to install and start snkchallenge in a CentOS 7.3 host, if using a different host OS, make sure you are installing the same softwares and versions as found on CentOS 7.3.

###### Yum repositories
- EPEL
```
# rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```
- Docker
```
# yum install yum-utils -y
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```
###### Disable SELinux
We are not going to dive into SELinux policies for this demonstration
```
# setenforce 0
# sed -i s/'SELINUX=enforcing'/'SELINUX=disabled'/g /etc/selinux/config
```
###### Install packages
#
```
# yum install python-pip docker-ce git -y
# pip install --upgrade pip
# pip install docker-compose
```
###### Start docker engine and enable boot startup for it
#
```
# systemctl start docker
# systemctl enable docker
```
### Download and build project
###### Clone the repository
#
```
# cd /opt/
# git clone https://git@github.com/iarlyy/snkchallenge
```
###### Build and start the environment
#
```
# cd /opt/snkchallenge
# docker-compose up -d
```
Now you are be able to access the web interface:
- http://SERVER_IP_ADDRESS:8080

### Automating and Scaling
To automate all building process and introduce scaling to our project we are going to use Saltstack as orquestrator. 
SaltStack is an orchestration and automation platform to manage all layers of the data center infrastructure. It can be used to manage and automate infrastructure and applications, Internet of things, dynamic storage, software-defined networking, server security, hardening and compliance, high performance computing and much more.

A minimum saltstack infrastructure is composed by:
- salt-master - Server side application responsible for compiling host states and triggering the enforcement of the states on the minions
- salt-minion - Clients (aka app servers, web servers, database servers, sensors etc)

It is still possible to implement saltstack without need of installing salt-minion on the clients, instead saltstack will use ssh to push the states to the clients.

In our demonstration we are going to install only the salt-minion and make use of a tool called salt-call that enables us to execute/test states locally without the need of having a salt-master installed.

Our sls(salt state file) contains the full definition of our virtual environment and its dependencies, after completed the installation of the salt-minion and the repository is downloaded, we will run only one command and everything will setup without additional intervention.

****IMPORTANT: USE A FRESH AND DEDICATED INSTALL OF CENTOS 7.3****

###### Installing salt-minion
#
```
# rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# cat << EOF > /etc/yum.repos.d/saltstack.repo
[saltstack-repo]
name=SaltStack repo for Red Hat Enterprise Linux $releasever
baseurl=https://repo.saltstack.com/yum/redhat/\$releasever/\$basearch/latest
enabled=1
gpgcheck=1
gpgkey=https://repo.saltstack.com/yum/redhat/\$releasever/\$basearch/latest/SALTSTACK-GPG-KEY.pub
       https://repo.saltstack.com/yum/redhat/\$releasever/\$basearch/latest/base/RPM-GPG-KEY-CentOS-7
EOF
# yum install salt salt-minion git -y
```
###### Clone the repository
#
```
# cd /opt/
# git clone https://git@github.com/iarlyy/snkchallenge
```
###### Salt time
#
```
# salt-call --local state.apply --saltfile=/opt/snkchallenge/salt/snkchallenge.sls --file-root=/opt/snkchallenge/salt/ -l error
```
Now you should be able to access the web interface:
- http://SERVER_IP_ADDRESS:8080

### Todo
 * Add method that enables data to be stored temporary on the sensor's disk in case of MQ broker failure
 * Create MQ object
 
### Known issues
 * Indexer doesn't timeout the loop_forever and container must be restarted
 * Error downloading docker images from dockerhub when docker-compose is already installed on the host

### License

The snkchallenge is licensed under the terms of the GPL Open Source license and is available for free.

### Links 

[MQTT reference](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)

[MQTT best pratices](http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices)

[Python-mqtt documentation](https://github.com/eclipse/paho.mqtt.python)

[Docker-compose reference](https://docs.docker.com/compose/compose-file/)

[Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

[Dockerfile best practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)

[Salt-call reference](https://docs.saltstack.com/en/latest/ref/cli/salt-call.html)

[Saltstack Masterless Quickstart](https://docs.saltstack.com/en/latest/topics/tutorials/quickstart.html)

[Cherrypy documentation](http://docs.cherrypy.org/en/latest/)

[Python JSON documentation](https://docs.python.org/2/library/json.html)
