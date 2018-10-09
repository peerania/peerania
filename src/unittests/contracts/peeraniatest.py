import requests
import subprocess
import unittest
import json
from termcolor import cprint
import os
import signal
from time import sleep
import requests

verbose = False

accounts = {
    "alice": {
        "private-key": "5JkkSVEk5241KjyPnoz68NRBYxH1mRtvK4CQb3u9KA5dp6qEXh5",
        "EOSkey": "EOS5EPkSYwCUx2mFpNo5QjbopCAmL3D13oLgCjsTqEdcXtcscCyYc"
    },
    "bob": {
        "private-key": "5Hu1ok3WxLe9NX1bMWVZfHUfTN4m2wpZcQ1Y2Yr2mthurwqDTxw",
        "EOSkey": "EOS7Cnb8jWq7vtXMFZCjtPpoeEeMLFyy8U7nVaXrzKLYWPq94tNiL"
    },
    "carol": {
        "private-key": "5JeUXvCDWvx6VPPurJGQQTVbtTKoNq8gmFijVkPzinDuDxM8ohx",
        "EOSkey": "EOS6DnDKWzhSwCLoKG4o1Xs1yWa8V6Xf73ZjbeE8yPVaEmRWSRU28"
    },
    "ted": {
        "private-key": "5K1L8wwcsy8BccbLHZd1yevEFaRrMXCBihQmoZb9MNo9xpMSuDw",
        "EOSkey": "EOS68wNfJSdVfH27irn4PyKhhEdwWUHiUmRVFnbxx1iVaHCX8oukd"
    },
    "dan": {
        "private-key": "5KeXEpJ7vVt8YjMhokMSP17k3Bpx7Ai5UuTajLpkrvzBEoZcibm",
        "EOSkey": "EOS7bfNuffVAKekKuBmryumBjoLjCQUN9RVbhQP5KVtmWyZe1p5L2"
    },
    "frank": {
        "private-key": "5K4ftE2YLYc6VumsVW4C7RUCdS13MbaSxYbNDTHAhf6wCD9zHiQ",
        "EOSkey": "EOS5NtdP7ofLYQG3Xwz7PQFHFR8yv1hK3t7AqZA3Bo4PDGnSbtHK5"
    }
}


def stop():
    subprocess.call(['pkill', 'nodeos'])

class PeeraniaTest(unittest.TestCase):
    DEFAULT_RATING = 200
    DEFAULT_MDP = 2
    WAIT_FOR_NEW_BLOCK = 0.51

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        with open('config.json', 'r') as configfile:
            cls.config = json.load(configfile)
        stop()
        if cls.config['terminal'] == False:
            cls.eosnode = subprocess.Popen('cd {}; {}'.format(cls.config['eos-node'], './run'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
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
                    if verbose:
                        cprint('Node info:\n{}'.format(p.json()), color='yellow')
                    break
            except:
                pass
        if count == 0:
            stop()
            raise Exception('Set up node error')

        to_execute = [
            'cleos wallet create --name default --to-console',
            'cleos wallet import --private-key 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3',
            'cleos set contract eosio eos/build/contracts/eosio.bios -p eosio',
            'cleos wallet import --private-key 5JUnu1jgVifdznEHpc9eVedpLXsyDPwu69xziMm9ZvbRSkVKEda',
            'cleos create account eosio {} EOS5hhovSUZFZQPdvVvtCU9JjjZuuoyyQLG8EoY83UTELZtNMRz1b EOS5hhovSUZFZQPdvVvtCU9JjjZuuoyyQLG8EoY83UTELZtNMRz1b'.format(
                cls.config['deployer']),
            'cleos set contract {0} {1} -p {0}'.format(
                cls.config['deployer'], cls.config['contract'])
        ]
        for owner, keys in accounts.items():
            to_execute.append(
                'cleos wallet import --private-key {}'.format(keys['private-key']))
            to_execute.append(
                'cleos create account eosio {0} {1} {1}'.format(owner, keys['EOSkey']))
        for command in to_execute:
            with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                process.wait()
                if(verbose):
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

    def action(self, action_name, action_body, action_auth, action_text, wait=False):
        cprint(action_text, end='', color='yellow')
        cleos_cmd = "cleos push action {} {} '{}' -p {}".format(
            self.config['deployer'], action_name, json.dumps(action_body), action_auth)
        out = None
        with subprocess.Popen(cleos_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as transaction:
            transaction.wait()
            out, _ = transaction.communicate()
            if(transaction.returncode != 0):
                print(out.decode())
            if(wait):
                input()
            self.assertTrue(transaction.returncode == 0)
        cprint('  OK', color='green')
        if verbose:
            print(out.decode())

    def failed_action(self, action_name, action_body, action_auth, action_text, errormsg='', wait=False):
        cprint(action_text + ' - Error expected', color='yellow')
        cleos_cmd = "cleos push action {} {} '{}' -p {}".format(
            self.config['deployer'], action_name, json.dumps(action_body), action_auth)
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
            errormsg = 'Error 3090004: Missing required authority'
        elif(errormsg == 'assert'):
            errormsg = 'Error 3050003: eosio_assert_message assertion failure'
        if(errormsg != ''):
            self.assertTrue(errormsg in out.decode())
        cprint('Get correct error', end='',  color='yellow')
        cprint('  OK', color='green')
        if verbose:
            print(out.decode())

    def setUp(self):
        pass

    def tearDown(self):
        self.action('resettables', {'user': self.config['deployer']}, self.config['deployer'], 'Reset all tables')
        self.wait(1)

    def wait(self, secs = None):
        if secs is None:
            secs = self.WAIT_FOR_NEW_BLOCK
        info('Wait {} sec until new block is generated'.format(secs))
        sleep(secs)

    def table(self, table, scope, limit=10):
        data = {'table': table, 'scope': scope, 'code': self.config['deployer'], 'limit': limit, 'json': True}
        with requests.post('http://127.0.0.1:8888/v1/chain/get_table_rows', json.dumps(data)) as t:
            if t.status_code == 200:
                if verbose:
                    cprint('Fetch from "{}" with scope "{}":\n{}'.format(table, scope, t.json()), color='yellow')
                tb = t.json()
                self.assertFalse(tb['more'])
                return tb['rows']
            else:
                cprint('Error fetching table data:\n' + str(t))
            self.assertTrue(t.status_code == 200)
                

    def get_non_registered_alice(self):
        return 'alice'

    def get_non_registered_bob(self):
        return 'bob'

    def get_non_registered_carol(self):
        return 'carol'

    def get_non_registered_ted(self):
        return 'ted'

    def get_non_registered_dan(self):
        return 'dan'

    def get_non_registered_frank(self):
        return 'frank'

    def register_alice_account(self, rating=None, moderation_points=None):
        return self._register_account('alice', rating, moderation_points)

    def register_bob_account(self, rating=None, moderation_points=None):
        return self._register_account('bob', rating, moderation_points)

    def register_carol_account(self, rating=None, moderation_points=None):
        return self._register_account('carol', rating, moderation_points)

    def register_ted_account(self, rating=None, moderation_points=None):
        return self._register_account('ted', rating, moderation_points)

    def register_dan_account(self, rating=None, moderation_points=None):
        return self._register_account('dan', rating, moderation_points)

    def register_frank_account(self, rating=None, moderation_points=None):
        return self._register_account('frank', rating, moderation_points)

    def _register_account(self, user, rating, moderation_points):
        self.action('registeracc', {'owner': str(user), 'display_name': str(
            user) + 'DispName', 'ipfs_profile': str(user) + '_IPFS'},
            user, 'Register {} account'.format(user))
        if rating is None:
            rating = self.DEFAULT_RATING
        if moderation_points is None:
            moderation_points = self.DEFAULT_MDP
        self.action('setaccrtmpc', {'user': str(user), 'rating': rating, 'moderation_points': moderation_points},
                    user, 'Set {} rating to {} and give {} moderation points'.format(str(user), rating, moderation_points))
        return user

def get_expected_account_body(owner):
    return {
        'owner': str(owner),
        'display_name': str(owner) + 'DispName',
        'ipfs_profile': str(owner) + '_IPFS',
        'registration_time': '#ignore',
        'moderation_points': '#var ' + str(owner) + '_mdp',
        'rating': '#var ' + str(owner) + '_rating',
        'string_properties': [],
        'integer_properties': []
    }


def load_defines(filepath):
    defs = {}
    with open(filepath, 'r') as ins:
        for line in ins:
            spl = line.split(' ')
            if len(spl) > 2 and spl[0] == '#define':
                try:
                    defs[spl[1]] = int(spl[2])
                except:
                    continue
    return defs


def info(text, data=None):
    cprint(text, color='yellow')
    if data != None:
        print(json.dumps(data, indent=2))


def begin(text, error_expected=False):
    cprint(text + ('- Error expected.' if error_expected else ''), color='cyan')


def end():
    cprint('Test ', end='', color='cyan')
    cprint('OK\n\n', color='green')


def hash_display_name(display_name):
    charmap = 'abcdefghijklmnopqrstuvwxyz'
    hash = ''
    for i in range(min(12, len(display_name))):
        hash += charmap[ord(display_name[i]) % 26]
    return hash
