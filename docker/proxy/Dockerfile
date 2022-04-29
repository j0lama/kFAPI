FROM ubuntu:bionic

SHELL ["/bin/bash", "-c"] 

RUN apt-get -y update
RUN apt-get -y install libsctp-dev git build-essential libz-dev net-tools iputils-ping nano

# Clone Proxy
RUN git clone https://github.com/EpiSci/oai-lte-5g-multi-ue-proxy.git
WORKDIR oai-lte-5g-multi-ue-proxy/

RUN make

COPY run_proxy.sh .