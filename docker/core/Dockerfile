FROM ubuntu:bionic

SHELL ["/bin/bash", "-c"] 

RUN apt-get -y update
RUN apt-get -y install net-tools iputils-ping git nano software-properties-common iptables

# Install srsEPC
RUN add-apt-repository -y ppa:softwareradiosystems/srsran
RUN apt-get -y update
RUN apt-get -y install srsran

COPY core.conf .
COPY user_db.csv .
COPY run_core.sh .