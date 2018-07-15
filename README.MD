# Peerania - Decentralized Professional Q&A Platform


## Environment Setup

### Clone all submodules

1. cd peerania-dev
1. Clone submodules `git submodule update --init --recursive`
1. Clone dependencies by running script `./clone`

### Build and install EOS

1. `cd eos`
1. `git submodule update --init --recursive`
1. `./eosio_build.sh`
1. `cd build`
1. `make install`

### Build EOSFactory

1. Install Python 3
1. Install *termcolor* by running command
`python3 -m pip install termcolor`
1. `cd eosfactory`
1. `./build.sh -e ../eos -w ../peerania-contracts`




