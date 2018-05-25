#
# First Flask App Dockerfile
#

# Pull base image.
FROM ubuntu:latest

# Build commands
RUN apt-get update
RUN apt-get install -y python3.6 python3.6-dev python3-pip
RUN apt-get install -y libmysqlclient-dev
RUN python3.6 -m pip install pip --upgrade
RUN apt-get install -y openslide-tools
RUN apt-get install -y git
RUN apt-get install -y vim
RUN mkdir /opt/histoqc
WORKDIR /opt/histoqc
ADD requirements.txt /opt/histoqc/
RUN pip install -r requirements.txt
ADD . /opt/histoqc
