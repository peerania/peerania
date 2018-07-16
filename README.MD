# Peerania - Decentralized Professional Q&A Platform

## Environment Setup

### Clone all submodules

1. cd peerania-dev
1. Clone submodules `git submodule update --init --recursive`
1. Clone dependencies by running script `./clone`

### Build and install EOS

1. `cd eos`
1. `./eosio_build.sh`
1. `cd build`
1. `make install`

### Build EOSFactory

1. Install Python 3
1. Install *termcolor* by running command
`python3 -m pip install termcolor`
1. `cd eosfactory`
1. Run command  
`./build.sh -e <peerania-repo-path>/eos -w <peerania-repo-path>/src/contracts`  
*peerania-repo-path* is path to directory where you cloned *peerania* repository
1. Test that EOSFactory installed propery by running commands  
`python3 ./tests/unittest1.py`  
`python3 ./tests/unittest2.py`  
`python3 ./tests/unittest3.py`  

## Running Local Node

The scripts and configurations to run local node are located in *eos-node* folder  

* `./run` starts node
* `./init-accounts` initiates wallet with accounts
* `./deploy` example of deploying contract (make sure that contract is compiled using `./compile` script)
* `./call-action` example of calling action


## Developing

### Smart Contracts

Smart contracts location is *src/contracts*

### Unit Tests

Run `./test` to compile contracts and run unit tests

