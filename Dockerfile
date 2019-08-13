FROM ubuntu:18.04

ADD eos-node peeranha/eos-node
ADD src peeranha/src
ADD compile peeranha/compile
ADD test peeranha/test
ADD config.json peeranha/config.json

RUN apt update
RUN apt install wget -y
RUN wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.6.2/eosio.cdt_1.6.2-1-ubuntu-18.04_amd64.deb
RUN apt install ./eosio.cdt_1.6.2-1-ubuntu-18.04_amd64.deb -y
RUN wget https://github.com/eosio/eos/releases/download/v1.8.1/eosio_1.8.1-1-ubuntu-18.04_amd64.deb
RUN apt install ./eosio_1.8.1-1-ubuntu-18.04_amd64.deb -y

RUN mkdir -p /eosio.contracts/build/contracts/eosio.bios
ADD stub/eosio.bios /eosio.contracts/build/contracts/eosio.bios
ENV EOSIO_BUILD_DIR /eosio.contracts/build/

RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install termcolor
RUN pip3 install requests

CMD ["peeranha/eos-node/run"]