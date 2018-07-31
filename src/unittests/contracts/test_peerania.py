import setup
import eosf
import node
import sess
import unittest
from time import sleep
from termcolor import cprint
setup.set_verbose(False)
setup.set_json(False)
setup.use_keosd(False)


def hash_display_name(display_name):
    charmap = "abcdefghijklmnopqrstuvwxyz"
    hash = ''
    for i in range(min(12, len(display_name))):
        hash += charmap[ord(display_name[i]) % 26]
    return hash


class PeeraniaTests(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        global verbose
        verbose = False

    def setUp(self):
        testnet = node.reset()
        assert(not testnet.error)
        sess.init()
        global contract
        contract = eosf.Contract(sess.alice, "peerania")
        assert(not contract.error)
        deployment = contract.deploy()
        assert(not deployment.error)

    def init_accounts(self):
        cprint("Register Alice", end='', color='yellow')
        action = contract.push_action(
            "registeracc",
            '{{"owner":"{}", "display_name":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'DisplName', str(sess.alice) + 'Ipfs'),
            sess.alice)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')
        cprint("Register Bob", end='', color='yellow')
        action = contract.push_action(
            "registeracc",
            '{{"owner":"{}", "display_name":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.bob), str(sess.bob) + 'DisplName', str(sess.bob) + 'Ipfs'),
            sess.bob)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')

    def register_property_action(self, owner, key, value):
        cprint('Register new {} property {}'.format(
            str(owner), key), end='', color='yellow')
        action = contract.push_action(
            "setaccparam",
            '{{"owner":"{}", "property":{{"key":{}, "value":"{}"}} }}'.format(
                str(owner), key, value),
            owner)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')

    def test_register_user(self):
        cprint("\n\nTesting registration of new users Alice and Bob\n", color='cyan')
        self.init_accounts()
        cprint('Table account after acton:', color='blue')
        print(contract.table(
            "account", "allaccounts").json['rows'], end='\n\n')
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_register_user_another_owner_failed(self):
        cprint("Register Alice with bob auth(error expected)", color='yellow')
        action = contract.push_action(
            "registeracc",
            '{{"owner":"{}", "display_name":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'DisplName', str(sess.alice) + 'Ipfs'),
            sess.bob)
        self.assertTrue(action.error)
        if verbose:
            print(action)

    def test_register_account_twice_failed(self):
        self.init_accounts()
        cprint("Waiting 2 seconds until a new block is generated", color='yellow')
        sleep(2)
        cprint("Register Alice for the second time(error expected)", color='yellow')
        action = contract.push_action(
            "registeracc",
            '{{"owner":"{}", "display_name":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'DisplName', str(sess.alice) + 'Ipfs'),
            sess.alice)
        self.assertTrue(action.error)
        if verbose:
            print(action)

    def test_user_property(self):
        cprint("\n\nTesting properties for accounts\n", color='cyan')
        self.init_accounts()
        self.register_property_action(
            sess.alice, 1, str(sess.alice) + 'Property1')
        self.register_property_action(
            sess.alice, 2, str(sess.alice) + 'Property2')
        self.register_property_action(
            sess.alice, 3, str(sess.alice) + 'Property3')
        self.register_property_action(
            sess.bob, 1, str(sess.bob) + 'Property1')
        self.register_property_action(
            sess.bob, 2, str(sess.bob) + 'Property2')
        self.register_property_action(
            sess.bob, 3, str(sess.bob) + 'Property3')
        cprint('Table userprop after acton for Alice account:', color='blue')
        print(contract.table("userprop",
                             sess.alice).json['rows'], end='\n\n')
        cprint('Table userprop after acton for Bob account:', color='blue')
        print(contract.table("userprop",
                             sess.bob).json['rows'], end='\n\n')

        cprint("\nUpdate Bob property 1", end='', color='yellow')
        action = contract.push_action(
            "setaccparam",
            '{{"owner":"{}", "property":{{"key":{}, "value":"{}"}} }}'.format(
                str(sess.bob), 1, str(sess.bob) + 'updatedProperty 1'),
            sess.bob)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')
        cprint('Table userprop after acton for Bob account:', color='blue')
        print(contract.table("userprop",
                             sess.bob).json['rows'], end='\n\n')

        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_account_management(self):
        cprint(
            "\n\nTesting functions for changing ipfs profile and display_name\n", color='cyan')
        self.init_accounts()
        cprint("Changing Alice ipfs profile", end='', color='yellow')
        action = contract.push_action(
            "setipfspro",
            '{{"owner":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'updated IPFS profile'),
            sess.alice)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')
        cprint("Changing Alice display_name to 'aliceUbpdeateddisplay_name'",
               end='', color='yellow')
        action = contract.push_action(
            "setdispname",
            '{{"owner":"{}", "display_name":"{}"}}'.format(
                str(sess.alice), 'aliceUbpdeateddisplay_name'),
            sess.alice)
        self.assertFalse(action.error)
        if verbose:
            print(action)
        cprint("  OK", color='green')
        cprint('Table account after acton:', color='blue')
        print(contract.table(
            "account", "allaccounts").json['rows'], end='\n\n')
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_display_name_mapper(self):
        cprint("\n\nTesting display_name mapper functionality\n", color='cyan')
        self.init_accounts()
        display_names = ['aliceDisplName', 'bobDisplName', 'nonexistent']
        for display_name in display_names:
            cprint('Table of users with display_name={}'.format(
                display_name), color='blue')
            print(contract.table("dnametoacc",
                                 hash_display_name(display_name)), end='\n\n')
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_properties_for_non_existent_account_failed(self):
        cprint("\n\nTesting registration of the property for non-existing account(errors expected)\n", color='cyan')
        cprint('Register new Alice property 1(error expected)', color='yellow')
        action = contract.push_action(
            "setaccparam",
            '{{"owner":"{}", "property":{{"key":{}, "value":"{}"}} }}'.format(
                str(sess.alice), 1, 'property 1'),
            sess.alice)
        self.assertTrue(action.error)
        if verbose:
            print(action)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_management_for_non_existent_account_failed(self):
        cprint("\n\nTesting account changing IPFS profile and display_name for non-existing account(errors expected)\n", color='cyan')
        cprint("Changing Alice ipfs profile(error expected)", color='yellow')
        action = contract.push_action(
            "setipfspro",
            '{{"owner":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'updated IPFS profile'),
            sess.alice)
        self.assertTrue(action.error)
        if verbose:
            print(action)

        cprint("Changing Alice display_name(error expected)", color='yellow')
        action = contract.push_action(
            "setdispname",
            '{{"owner":"{}", "display_name":"{}"}}'.format(
                str(sess.alice), 'aliceUbpdeateddisplay_name'),
            sess.alice)
        self.assertTrue(action.error)
        if verbose:
            print(action)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_properties_another_owner_failed(self):
        self.init_accounts()
        cprint("\n\nTesting registration of the property with another account(errors expected)\n", color='cyan')
        cprint('Register new Alice property 1 with bob auth(error expected)', color='yellow')
        action = contract.push_action(
            "setaccparam",
            '{{"owner":"{}", "property":{{"key":{}, "value":"{}"}} }}'.format(
                str(sess.alice), 1, 'property 1'),
            sess.bob)
        self.assertTrue(action.error)
        if verbose:
            print(action)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_management_another_owner_failed(self):
        cprint("\n\nTesting account changing IPFS profile and display_name with another account(errors expected)\n", color='cyan')
        cprint("Changing Alice ipfs profile with bob auth(error expected)", color='yellow')
        action = contract.push_action(
            "setipfspro",
            '{{"owner":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'updated IPFS profile'),
            sess.bob)
        self.assertTrue(action.error)
        if verbose:
            print(action)

        cprint("Changing Alice display_name with bob auth(error expected)", color='yellow')
        action = contract.push_action(
            "setdispname",
            '{{"owner":"{}", "display_name":"{}"}}'.format(
                str(sess.alice), 'aliceUbpdeateddisplay_name'),
            sess.bob)
        self.assertTrue(action.error)
        if verbose:
            print(action)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')
        
    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        node.stop()

if __name__ == "__main__":
    unittest.main()
