FROM eosio/eos

ADD eos-node peerania/eos-node
ADD src peerania/src
ADD compile peerania/compile
ADD test peerania/test
ADD config.json peerania/config.json

RUN apt update
RUN apt install wget -y
RUN wget https://github.com/eosio/eosio.cdt/releases/download/v1.4.1/eosio.cdt-1.4.1.x86_64.deb
RUN apt install ./eosio.cdt-1.4.1.x86_64.deb
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install termcolor
RUN pip3 install requests

CMD ["bin/bash"]