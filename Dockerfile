FROM eosio/eos

ADD eos-node peerania/eos-node
ADD src peerania/src
ADD compile peerania/compile

RUN mkdir build
RUN mkdir build/contracts
#RUN cp -a contracts/eosio.bios build/contracts/eosio.bios
RUN apt update
RUN apt install wget -y
RUN apt install sudo -y
RUN apt install git -y
RUN git clone --recursive https://github.com/eosio/eosio.cdt
RUN 'cd eosio.cdt; yes 1 | ./build.sh'
RUN 'cd eosio.cdt; sudo ./install.sh'
CMD ["bin/bash"]