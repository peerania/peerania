FROM ubuntu:18.04

RUN apt update
RUN apt -y install wget
RUN wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.3.1/eosio.cdt-1.3.1.x86_64.deb
RUN apt -y install ./eosio.cdt-1.3.1.x86_64.deb
RUN apt -y install python3-setuptools python3-wheel python3-pip
RUN python3 -m pip install requests
RUN python3 -m pip install requests
RUN python3 -m pip install termcolor

CMD [ "bash"]