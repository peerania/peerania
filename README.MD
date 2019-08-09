# peeranha - Decentralized Professional Q&A Platform

## Environment Setup

### Clone all repository and dependencies

1. `git clone https://github.com/peeranha/peeranha.git`
1. `cd peeranha`
1. Clone dependencies by running script `./clone`

### Build and install EOS

1. `cd eos`
1. `./eosio_build.sh`
1. `./eosio_install.sh`

### Install Python 3.6 or higher

1. You could find the latest version on https://www.python.org/downloads/
1. Install *termcolor* by running command `python3 -m pip install termcolor`

### Install eosio.cdt
Follow the instructions on https://github.com/EOSIO/eosio.cdt

## Smart Contracts

Smart contracts are located in folder *src/contracts/peeranha*  

Run `./compile` script to compile the contracts  
Run `./test` script to compile and execute unit tests

## Running Local Node

The scripts and configurations to run local node are located in *eos-node* folder  

* `./run` starts node
* `./init-accounts` initiates wallet with accounts
* `./deploy` example of deploying contract (make sure that contract is compiled using `./compile` script in the repository root folder)
* `./push-action` example of calling action

