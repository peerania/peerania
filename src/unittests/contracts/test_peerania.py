import setup
import eosf
import node
import sess
import unittest
import json
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

    def test_register_user(self):
        cprint("\n\nTesting registration of new users Alice and Bob\n", color='cyan')
        self._init_accounts()
        cprint('Table account after acton:', color='blue')
        t = contract.table("account", "allaccounts")
        print(t.json['rows'], end='\n\n')
        self.assertFalse(t.json['more'])
        expectation = [{'owner': 'alice', 'display_name': 'aliceDisplName', 'ipfs_profile': 'aliceIpfs'},
                       {'owner': 'bob', 'display_name': 'bobDisplName', 'ipfs_profile': 'bobIpfs'}]
        reality = sorted(t.json['rows'], key=lambda acc: acc['owner'])
        self.assertTrue(len(expectation) == len(reality))
        for i in range(len(expectation)):
            self.assertTrue(expectation[i]['owner'] == reality[i]['owner'])
            self.assertTrue(expectation[i]['display_name']
                            == reality[i]['display_name'])
            self.assertTrue(expectation[i]['ipfs_profile']
                            == reality[i]['ipfs_profile'])
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
        self.assertTrue(
            'Error 3090004: missing required authority' in action.err_msg)
        if verbose:
            print(action)

    def test_register_account_twice_failed(self):
        self._init_accounts()
        cprint("Waiting 2 seconds until a new block is generated", color='yellow')
        sleep(2)
        cprint("Register Alice for the second time(error expected)", color='yellow')
        action = contract.push_action(
            "registeracc",
            '{{"owner":"{}", "display_name":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'DisplName', str(sess.alice) + 'Ipfs'),
            sess.alice)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3050003: eosio_assert_message assertion failure' in action.err_msg)
        if verbose:
            print(action)

    def test_user_property(self):
        cprint("\n\nTesting properties for accounts\n", color='cyan')
        self._init_accounts()
        for i in range(3):
            self._register_property_action(
                sess.alice, i + 1, str(sess.alice) + 'Property' + str(i + 1))
            self._register_property_action(
                sess.bob, i + 1, str(sess.bob) + 'Property' + str(i + 1))

        table_alice = contract.table("userprop", sess.alice)
        cprint('Table userprop after acton for Alice account:', color='blue')
        print(table_alice.json['rows'], end='\n\n')

        table_bob = contract.table("userprop", sess.bob)
        cprint('Table userprop after acton for Bob account:', color='blue')
        print(table_bob.json['rows'], end='\n\n')

        self.assertFalse(table_alice.json['more'])
        self.assertTrue(len(table_alice.json['rows']) == 3)
        self.assertFalse(table_bob.json['more'])
        self.assertTrue(len(table_bob.json['rows']) == 3)
        sorted_alice_table = sorted(
            table_alice.json['rows'], key=lambda prop: prop['key_value']['key'])
        sorted_bob_table = sorted(
            table_bob.json['rows'], key=lambda prop: prop['key_value']['key'])
        for i in range(3):
            self.assertTrue(sorted_alice_table[i]['owner'] == str(sess.alice))
            self.assertTrue(sorted_alice_table[i]['key_value']['key'] == i+1)
            self.assertTrue(sorted_alice_table[i]['key_value']['value'] == str(
                sess.alice) + 'Property' + str(i+1))
            self.assertTrue(sorted_bob_table[i]['owner'] == str(sess.bob))
            self.assertTrue(sorted_bob_table[i]['key_value']['key'] == i+1)
            self.assertTrue(sorted_bob_table[i]['key_value']['value'] == str(
                sess.bob) + 'Property' + str(i+1))

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

        table_bob = contract.table("userprop", sess.bob)
        cprint('Table userprop after acton for Bob account:', color='blue')
        print(table_bob.json['rows'], end='\n\n')

        self.assertFalse(table_bob.json['more'])
        self.assertTrue(len(table_bob.json['rows']) == 3)
        sorted_bob_table = sorted(
            table_bob.json['rows'], key=lambda prop: prop['key_value']['key'])
        for i in range(3):
            self.assertTrue(sorted_bob_table[i]['owner'] == str(sess.bob))
            self.assertTrue(sorted_bob_table[i]['key_value']['key'] == i+1)
            if i != 0:
                self.assertTrue(sorted_bob_table[i]['key_value']['value'] == str(
                    sess.bob) + 'Property' + str(i+1))
            else:
                self.assertTrue(sorted_bob_table[i]['key_value']['value'] == str(
                    sess.bob) + 'updatedProperty 1')
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_account_management(self):
        cprint(
            "\n\nTesting functions for changing ipfs profile and display_name\n", color='cyan')
        self._init_accounts()
        cprint("Changing Alice ipfs profile", end='', color='yellow')
        action = contract.push_action(
            "setipfspro",
            '{{"owner":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'updated IPFS profile'),
            sess.alice)
        self.assertFalse(action.error)
        if verbose:
            print(action)

        t = contract.table("account", "allaccounts")
        self.assertFalse(t.json['more'])
        expectation = [{'owner': 'alice', 'display_name': 'aliceDisplName', 'ipfs_profile': str(sess.alice) + 'updated IPFS profile'},
                       {'owner': 'bob', 'display_name': 'bobDisplName', 'ipfs_profile': 'bobIpfs'}]
        reality = sorted(t.json['rows'], key=lambda acc: acc['owner'])
        self.assertTrue(len(expectation) == len(reality))
        for i in range(len(expectation)):
            self.assertTrue(expectation[i]['owner'] == reality[i]['owner'])
            self.assertTrue(expectation[i]['display_name']
                            == reality[i]['display_name'])
            self.assertTrue(expectation[i]['ipfs_profile']
                            == reality[i]['ipfs_profile'])
        cprint("  OK", color='green')

        cprint("Changing Alice display_name to 'aliceUbpdeateddisplay_name'",
               end='', color='yellow')
        action = contract.push_action(
            "setdispname",
            '{{"owner":"{}", "display_name":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'Ubpdeateddisplay_name'),
            sess.alice)
        self.assertFalse(action.error)
        if verbose:
            print(action)

        t = contract.table("account", "allaccounts")
        self.assertFalse(t.json['more'])
        expectation[0]['display_name'] = str(
            sess.alice) + 'Ubpdeateddisplay_name'
        reality = sorted(t.json['rows'], key=lambda acc: acc['owner'])
        self.assertTrue(len(expectation) == len(reality))
        for i in range(len(expectation)):
            self.assertTrue(expectation[i]['owner'] == reality[i]['owner'])
            self.assertTrue(expectation[i]['display_name']
                            == reality[i]['display_name'])
            self.assertTrue(expectation[i]['ipfs_profile']
                            == reality[i]['ipfs_profile'])
        cprint("  OK", color='green')
        cprint('Table account after actons:', color='blue')
        print(t.json['rows'], end='\n\n')
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_display_name_mapper(self):
        cprint("\n\nTesting display_name mapper functionality\n", color='cyan')
        self._init_accounts()
        display_names = ['aliceDisplName', 'bobDisplName', 'nonexistent']
        expectation = [[{'owner': 'alice', 'display_name': 'aliceDisplName'}],
                       [{'owner': 'bob', 'display_name': 'bobDisplName'}], []]
        reality = []
        for display_name in display_names:
            cprint('Table of users with display_name={}'.format(
                display_name), color='blue')
            reality.append(contract.table("disptoacc",
                                          hash_display_name(display_name)))
            print(reality[-1].json['rows'], end='\n\n')

        self.assertTrue(len(expectation) == len(reality))
        for i in range(len(expectation)):
            self.assertFalse(reality[i].json['more'])
            self.assertTrue(reality[i].json['rows'] == expectation[i])
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
        if verbose:
            print(action)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3050003: eosio_assert_message assertion failure' in action.err_msg)
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
        if verbose:
            print(action)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3050003: eosio_assert_message assertion failure' in action.err_msg)

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
        self._init_accounts()
        cprint("\n\nTesting registration of the property with another account(errors expected)\n", color='cyan')
        cprint(
            'Register new Alice property 1 with bob auth(error expected)', color='yellow')
        action = contract.push_action(
            "setaccparam",
            '{{"owner":"{}", "property":{{"key":{}, "value":"{}"}} }}'.format(
                str(sess.alice), 1, 'property 1'),
            sess.bob)
        if verbose:
            print(action)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3090004: missing required authority' in action.err_msg)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    def test_management_another_owner_failed(self):
        cprint("\n\nTesting account changing IPFS profile and display_name with another account(errors expected)\n", color='cyan')
        cprint(
            "Changing Alice ipfs profile with bob auth(error expected)", color='yellow')
        action = contract.push_action(
            "setipfspro",
            '{{"owner":"{}", "ipfs_profile":"{}"}}'.format(
                str(sess.alice), str(sess.alice) + 'updated IPFS profile'),
            sess.bob)
        if verbose:
            print(action)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3090004: missing required authority' in action.err_msg)

        cprint(
            "Changing Alice display_name with bob auth(error expected)", color='yellow')
        action = contract.push_action(
            "setdispname",
            '{{"owner":"{}", "display_name":"{}"}}'.format(
                str(sess.alice), 'aliceUbpdeateddisplay_name'),
            sess.bob)
        if verbose:
            print(action)
        self.assertTrue(action.error)
        self.assertTrue(
            'Error 3090004: missing required authority' in action.err_msg)
        cprint("Test ", end='', color='cyan')
        cprint("OK\n\n", color='green')

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        node.stop()

    def _init_accounts(self):
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

    def _register_property_action(self, owner, key, value):
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


if __name__ == "__main__":
    unittest.main()
