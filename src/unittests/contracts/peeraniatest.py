import unittest
import setup
import eosf
import node
import json
from jsonutils import compare
from termcolor import cprint
from time import sleep


class PeeraniaTest(unittest.TestCase):
    DEFAULT_RATING = 200
    DEFAULT_MDP = 2
    WAIT_FOR_NEW_BLOCK = 1.5

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        setup.set_verbose(False)
        setup.set_json(False)
        setup.use_keosd(False)

    def setUp(self):
        self.verbose = False
        testnet = node.reset()
        assert(not testnet.error)

        wallet = eosf.Wallet()

        eosio = eosf.AccountMaster()
        wallet.import_key(eosio)

        deployer = eosf.account(eosio, "deployer")
        wallet.import_key(deployer)

        self.alice = eosf.account(eosio, "alice")
        wallet.import_key(self.alice)

        self.bob = eosf.account(eosio, "bob")
        wallet.import_key(self.bob)

        self.carol = eosf.account(eosio, "carol")
        wallet.import_key(self.carol)

        self.ted = eosf.account(eosio, "ted")
        wallet.import_key(self.ted)

        self.dan = eosf.account(eosio, "dan")
        wallet.import_key(self.dan)

        self.frank = eosf.account(eosio, "frank")
        wallet.import_key(self.frank)

        eosf.Contract(eosio, "eosio.bios").deploy()

        self.contract = eosf.Contract(deployer, 'peerania')
        assert(not self.contract.error)
        deployment = self.contract.deploy()
        assert(not deployment.error)

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        node.stop()

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

    def register_alice_account(self, rating=None, moderation_points=None):
        return self._register_account(self.alice, rating, moderation_points)

    def register_bob_account(self, rating=None, moderation_points=None):
        return self._register_account(self.bob, rating, moderation_points)

    def register_carol_account(self, rating=None, moderation_points=None):
        return self._register_account(self.carol, rating, moderation_points)

    def register_ted_account(self, rating=None, moderation_points=None):
        return self._register_account(self.ted, rating, moderation_points)

    def register_dan_account(self, rating=None, moderation_points=None):
        return self._register_account(self.dan, rating, moderation_points)

    def register_frank_account(self, rating=None, moderation_points=None):
        return self._register_account(self.frank, rating, moderation_points)

    def action(self, action_name, action_body, action_auth, action_text, wait=False):
        cprint(action_text, end='', color='yellow')
        action = self.contract.push_action(
            action_name, json.dumps(action_body), action_auth)
        if(wait):
            input()
        self.assertFalse(action.error)
        if self.verbose:
            print(action)
        cprint('  OK', color='green')

    def failed_action(self, action_name, action_body, action_auth, action_text, errormsg='', wait=False):
        cprint(action_text + ' - Error expected', color='yellow')
        action = self.contract.push_action(
            action_name, json.dumps(action_body), action_auth)
        if(wait):
            input()
        self.assertTrue(action.error)
        if self.verbose:
            print(action)
        if(errormsg == 'auth'):
            errormsg = 'Error 3090004: missing required authority'
        elif(errormsg == 'assert'):
            errormsg = 'Error 3050003: eosio_assert_message assertion failure'
        if(errormsg != ''):
            self.assertTrue(errormsg in action.err_msg)
        cprint('Get correct error', end='',  color='yellow')
        cprint('  OK', color='green')

    def table(self, tablename, scope):
        t = self.contract.table(tablename, scope)
        self.assertFalse(t.error)
        self.assertFalse(t.json['more'])
        return t.json['rows']

    def wait(self):
        info('Wait {} sec until new block is generated'.format(self.WAIT_FOR_NEW_BLOCK))
        sleep(self.WAIT_FOR_NEW_BLOCK)

    def get_non_registered_alice(self):
        return self.alice

    def get_non_registered_bob(self):
        return self.bob

    def get_non_registered_carol(self):
        return self.carol

    def get_non_registered_ted(self):
        return self.ted

    def get_non_registered_dan(self):
        return self.dan

    def get_non_registered_frank(self):
        return self.frank

    @staticmethod
    def get_expected_account_body(owner):
        return {
            'owner': str(owner),
            'display_name': str(owner) + 'DispName',
            'ipfs_profile': str(owner) + '_IPFS',
            'registration_time': '#ignore',
            'string_properties': [],
            'integer_properties': []
        }

    @staticmethod
    def load_defines(filepath):
        defs = {}
        with open(filepath, 'r') as ins:
            for line in ins:
                spl = line.split(' ')
                if len(spl) > 2 and spl[0]=='#define':
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
