import requests
import subprocess
import unittest
import json
from termcolor import cprint
import os
import signal
from time import sleep

def replace_ipfs_with_bytearray(obj):
    if isinstance(obj, dict):
        for k in obj:
            if k.startswith('ipfs_'):
                obj[k] = [x for x in obj[k].encode()]
            else:
                replace_ipfs_with_bytearray(obj[k])
    elif isinstance(obj, list):
        for item in obj:
            replace_ipfs_with_bytearray(item)
    return obj

def replace_bytearr_with_ipfs(obj):
    if isinstance(obj, dict):
        for k in obj:
            if k.startswith('ipfs_'):
                obj[k] = bytearray(obj[k]).decode('utf8')
            else:
                replace_bytearr_with_ipfs(obj[k])
    elif isinstance(obj, list):
        for item in obj:
            replace_bytearr_with_ipfs(item)
    return obj


class EOSTest(unittest.TestCase):
    WAIT_FOR_NEW_BLOCK = 0.51
    contracts = {}
    accounts = []
    verbose = True

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        with open('config.json', 'r') as configfile:
            cls.config = json.load(configfile)
        stop()

        to_execute = [
            'cleos wallet create --name default --to-console',
            'cleos wallet import --private-key 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3',
            'cleos set contract eosio $EOSIO_BUILD_DIR/contracts/eosio.bios -p eosio'
        ]
        for contract in cls.config['contracts']:
            cls.contracts[contract['name']] = contract['deployer']
            to_execute.append(
                'cleos wallet import --private-key {}'.format(contract['private-key']))
            to_execute.append('cleos create account eosio {0} {1} {1}'.format(
                contract['deployer'], contract['public-key']))
            to_execute.append(
                'cleos set contract {0} {1} -p {0}'.format(contract['deployer'], contract['contract']))
        for user in cls.config['users']:
            cls.accounts.append(user['name'])
            to_execute.append(
                'cleos wallet import --private-key {}'.format(user['private-key']))
            to_execute.append(
                'cleos create account eosio {0} {1} {1}'.format(user['name'], user['public-key']))
        if 'verbose' in cls.config:
            cls.verbose = cls.config['verbose']
        if cls.config['terminal'] == False:
            cls.eosnode = subprocess.Popen('cd {}; {}'.format(
                cls.config['eos-node'], './run'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            with subprocess.Popen("gnome-terminal -- sh -c 'cd {}; {}'".format(cls.config['eos-node'], './run'), stdout=subprocess.PIPE, shell=True) as nodeos:
                nodeos.wait()
        count = 7
        while count != 0:
            try:
                count -= 1
                sleep(1)
                p = requests.post('http://127.0.0.1:8888/v1/chain/get_info')
                if p.status_code == 200:
                    cprint('Node succesfully started!', color='cyan')
                    if cls.verbose:
                        cprint('Node info:\n{}'.format(
                            p.json()), color='yellow')
                    break
            except:
                pass
        if count == 0:
            stop()
            raise Exception('Set up node error')

        for command in to_execute:
            with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                process.wait()
                if(cls.verbose):
                    out, err = process.communicate()
                    print('command: ' + command)
                    print(out.decode())
                    print(err.decode())
                if process.returncode != 0:
                    stop()
                    raise Exception(command + ' NOT EXECUTED')

    @classmethod
    def tearDownClass(cls):
        if cls.config['terminal'] == False:
            cls.eosnode.terminate()
            stop()
        else:
            stop()

    def action(self, action_name, action_body, action_auth, action_text, wait=False, contract=None, suppress_output=False):
        if not suppress_output or self.verbose:
            cprint(action_text, end='', color='yellow')
        if contract is None:
            contract = self.config['default-contract']
        replace_ipfs_with_bytearray(action_body)
        cleos_cmd = "cleos push action {} {} '{}' -p {}".format(
            self.contracts[contract], action_name, json.dumps(action_body), action_auth)
        out = None
        with subprocess.Popen(cleos_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as transaction:
            transaction.wait()
            out, _ = transaction.communicate()
            if(transaction.returncode != 0):
                print(out.decode())
            if(wait):
                input()
            self.assertTrue(transaction.returncode == 0)
        if not suppress_output or self.verbose: cprint('  OK', color='green')
        if self.verbose:
            print(out.decode())

    def failed_action(self, action_name, action_body, action_auth, action_text, errormsg='', wait=False, contract=None):
        cprint(action_text + ' - Error expected', color='yellow')
        if contract is None:
            contract = self.config['default-contract']
        replace_ipfs_with_bytearray(action_body)
        cleos_cmd = "cleos push action {} {} '{}' -p {}".format(
            self.contracts[contract], action_name, json.dumps(action_body), action_auth)
        if(wait):
            input()
        out = None
        with subprocess.Popen(cleos_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as transaction:
            transaction.wait()
            out, _ = transaction.communicate()
            if(transaction.returncode == 0):
                print(out.decode())
            if(wait):
                input()
            self.assertFalse(transaction.returncode == 0)
        if(errormsg == 'auth'):
            errormsg = 'Error 3090004' #Missing required authority
        elif(errormsg == 'assert'):
            errormsg = 'Error 3050003' #check_message assertion failure
        if(errormsg != ''):
            self.assertTrue(errormsg in out.decode())
        cprint('Get correct error', end='',  color='yellow')
        cprint('  OK', color='green')
        if self.verbose:
            print(out.decode())

    def wait(self, secs=None):
        if secs is None:
            secs = self.WAIT_FOR_NEW_BLOCK
        info('Wait {} sec until new block is generated'.format(secs))
        sleep(secs)

    def table(self, table, scope, upperBound=None, lowerBound=None, limit=30, indexPosition=None, keyType=None, contract=None, ignoreMore=False): #limit=10
        if contract is None:
            contract = self.config['default-contract']
        data = {'table': table,
                'scope': scope,
                'code': self.contracts[contract],
                'limit': limit,
                'json': True}
        if (upperBound != None):
            data['upper_bound'] = upperBound
        if (lowerBound != None):
            data['lower_bound'] = lowerBound
        if (indexPosition != None):
            data['index_position'] = indexPosition
        if (keyType != None):
            data['key_type'] = keyType
        with requests.post('http://127.0.0.1:8888/v1/chain/get_table_rows', json.dumps(data)) as t:
            if t.status_code == 200:
                if self.verbose:
                    cprint('Fetch from "{}" with scope "{}":\n{}'.format(
                        table, scope, t.json()), color='yellow')
                tb = t.json()
                replace_bytearr_with_ipfs(tb)
                if not ignoreMore:
                    self.assertFalse(tb['more'])
                return tb['rows']
            else:
                cprint('Error fetching table data:\n' + str(t))
            self.assertTrue(t.status_code == 200)

    def get_contract_deployer(self, contract):
        return self.contracts[contract]

    def get_default_contract(self):
        return self.config['default-contract']

    def get_all_contracts(self):
        return self.contracts.keys()

    def get_all_accounts(self):
        return self.accounts


def stop():
    subprocess.call(['pkill', 'nodeos'])


def info(text, data=None):
    cprint(text, color='yellow')
    if data != None:
        print(json.dumps(data, indent=2))
