FROM ubuntu:18.04

ADD eos-node peerania/eos-node
ADD src peerania/src
ADD compile peerania/compile
ADD test peerania/test
ADD config.json peerania/config.json

RUN apt update
RUN apt install wget -y
RUN apt install git -y
RUN apt install cmake -y 
RUN wget https://github.com/eosio/eosio.cdt/releases/download/v1.6.1/eosio.cdt_1.6.1-1_amd64.deb
RUN apt install ./eosio.cdt_1.6.1-1_amd64.deb -y
RUN wget https://github.com/eosio/eos/releases/download/v1.8.1/eosio_1.8.1-1-ubuntu-18.04_amd64.deb
RUN apt install ./eosio_1.8.1-1-ubuntu-18.04_amd64.deb -y

RUN git clone https://github.com/EOSIO/eosio.contracts
#RUN cd eosio.contracts && mkdir -p build && cd build && cmake ../ && make -j4; exit 0
ENV EOSIO_BUILD_DIR /eosio.contracts/build/

RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install termcolorс
RUN pip3 install requests

CMD ["peerania/eos-node/run"]