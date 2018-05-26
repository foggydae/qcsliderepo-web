#
# First Flask App Dockerfile
#

# Pull base image.
FROM ubuntu:latest

# Build commands
RUN apt-get update
RUN apt-get install -y mysql-server
RUN apt-get install -y python3.5 python3.5-dev python3-pip
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y openslide-tools
RUN python3.5 -m pip install pip --upgrade
RUN apt-get install -y vim
RUN mkdir /opt/qcsliderepo
WORKDIR /opt/qcsliderepo
ADD requirements.txt /opt/qcsliderepo/
RUN pip install -r requirements.txt
ADD . /opt/qcsliderepo
