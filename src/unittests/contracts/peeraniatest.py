import unittest
import setup
import eosf
import node
import sess
import json
from jsonutils import compare
from termcolor import cprint

class PeeraniaTest(unittest.TestCase):
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
        sess.init()
        self.contract = eosf.Contract(sess.alice, "peerania")
        assert(not self.contract.error)
        deployment = self.contract.deploy()
        assert(not deployment.error)

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        node.stop()

    def register_alice_account(self):
        self.action('registeracc', {'owner': str(sess.alice), 'display_name': str(
            sess.alice) + 'DispName', 'ipfs_profile': str(sess.alice) + '_IPFS'}, 
            sess.alice, 'Register Alice account')
        return sess.alice

    def register_bob_account(self):
        self.action('registeracc', {'owner': str(sess.bob), 'display_name': str(
            sess.bob) + 'DispName', 'ipfs_profile': str(sess.bob) + '_IPFS'}, 
            sess.bob, 'Register Bob account')
        return sess.bob

    def register_carol_account(self):
        self.action('registeracc', {'owner': str(sess.carol), 'display_name': str(
            sess.carol) + 'DispName', 'ipfs_profile': str(sess.carol) + '_IPFS'}, 
            sess.carol, 'Register Carol account')
        return sess.carol

    def action(self, action_name, action_body, action_auth, action_text, wait = False):
        cprint(action_text, end='', color='yellow')
        action = self.contract.push_action(
            action_name, json.dumps(action_body), action_auth)
        if(wait):
            input()
        self.assertFalse(action.error)
        if self.verbose:
            print(action)
        cprint("  OK", color='green')

    def failed_action(self, action_name, action_body, action_auth, action_text, errormsg='', wait = False):
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
        cprint('Get correct error', end = '',  color='yellow')
        cprint("  OK", color='green')

    def table(self, tablename, scope):
        t = self.contract.table(tablename, scope)
        self.assertFalse(t.error)
        self.assertFalse(t.json['more'])
        return t.json['rows']

    @staticmethod
    def get_non_registered_alice():
        return sess.alice

    @staticmethod
    def get_non_registered_bob():
        return sess.bob

    @staticmethod
    def get_non_registered_carol():
        return sess.carol

    @staticmethod
    def get_expected_account_body(owner):
        return {
            'owner': str(owner),
            'display_name': str(owner)+'DispName',
            'ipfs_profile': str(owner)+'_IPFS',
            'registration_time': '#ignore',
            'string_properties': [],
            'integer_properties':[]
        }
        

def info(text, data = None):
    cprint(text, color='yellow')
    if data != None:
        print(json.dumps(data, indent = 2))

def begin(text, error_expected=False):
    cprint(text + ('- Error expected.' if error_expected else ''), color='cyan')

def end():
    cprint("Test ", end='', color='cyan')
    cprint("OK\n\n", color='green')
    
def hash_display_name(display_name):
    charmap = "abcdefghijklmnopqrstuvwxyz"
    hash = ''
    for i in range(min(12, len(display_name))):
        hash += charmap[ord(display_name[i]) % 26]
    return hash