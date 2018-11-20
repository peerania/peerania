FROM eosio/eos:v1.4.3

ADD eos-node peerania/eos-node
ADD src peerania/src
ADD compile peerania/compile

RUN apt update
RUN apt install wget -y
RUN wget https://github.com/eosio/eosio.cdt/releases/download/v1.4.1/eosio.cdt-1.4.1.x86_64.deb
RUN apt install ./eosio.cdt-1.4.1.x86_64.deb

CMD ["bin/bash"]


