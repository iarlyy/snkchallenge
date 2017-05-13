FROM centos:7
LABEL maintainer "iarlyy@gmail.com"
RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \  
    && yum install python-pip -y \
    && pip install --upgrade pip \
    && pip install paho-mqtt
COPY ./app/app.py /opt/
CMD ["/bin/python2.7","/opt/app.py"]
