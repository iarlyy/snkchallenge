mandatory-pkgs:
  pkg.installed:
    - pkgs:
      - python2-pip

epel:
  pkg.installed:
    - sources:
      - epel-release: https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

dockerrepo:
  cmd.run:
    - name: curl https://download.docker.com/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
    - unless: test -f /etc/yum.repos.d/docker-ce.repo
    - require:
      - pkg: mandatory-pkgs

docker-py:
  pip.installed:
    - name: docker-py
    - require:
      - pkg: mandatory-pkgs

disable-selinux:
  cmd.run:
    - name: setenforce 0 && sed -i s/'SELINUX=enforcing'/'SELINUX=disabled'/g /etc/selinux/config
    - unless: grep 'SELINUX=disabled' /etc/selinux/config

docker-ce:
  pkg.installed:
    - require:
      - cmd: dockerrepo

docker:
  service.running:
    - enable: True
    - require:
      - pkg: docker-ce
      - pip: docker-py

# docker images
centos:7:
  dockerng.image_present:
    - name: centos:7
    - require:
      - service: docker

img-toke/mostquitto:
  dockerng.image_present:
    - name: toke/mosquitto
    - require:
      - service: docker

img-snkweb:
  dockerng.image_present:
    - name: snkweb:latest
    - build: /opt/snkchallenge/snkweb/
    - require:
      - service: docker

img-snkindexer:
  dockerng.image_present:
    - name: snkindexer:latest
    - build: /opt/snkchallenge/snkindexer/
    - require:
      - service: docker

img-snksensor:
  dockerng.image_present:
    - name: snksensor:latest
    - build: /opt/snkchallenge/snksensor/
    - require:
      - service: docker

# docker containers

snkbroker:
  dockerng.running:
    - image: toke/mosquitto:latest
    - port_bindings:
      - 1883:1883

snkweb:
  dockerng.running:
    - image: snkweb:latest
    - port_bindings:
      - 8080:8080
    - binds:
      - /opt/snk-dockerdata:/opt/snkdb:rw

snkindexer:
  dockerng.running:
    - image: snkindexer:latest
    - binds:
      - /opt/snk-dockerdata:/opt/snkdb:rw
    - environment:
      - MQHOST: snkbroker

snksensor1:
  dockerng.running:
    - image: snksensor:latest
    - environment:
      - MQHOST: snkbroker
      - SENSOR_ID: sensor1

snksensor2:
  dockerng.running:
    - image: snksensor:latest
    - environment:
      - MQHOST: snkbroker
      - SENSOR_ID: sensor2

snk_netdefault:
  dockerng.network_present:
    - name: snk_netdefault
    - containers:
      - snkbroker
      - snkweb
      - snkindexer
      - snksensor1
      - snksensor2
