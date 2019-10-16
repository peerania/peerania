import peeranhatest
from peeranhatest import *
from jsonutils import compare
from time import sleep
from unittest import main

economy = load_defines('src/contracts/peeranha.main/economy.h')

class AccountManagementTests(peeranhatest.peeranhaTest):

    def test_register_user(self):
        begin('Testing registration of new user Alice')
        alice = self.get_non_registered_alice()
        self.action('registeracc', {
            'user': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS',
            'ipfs_avatar': 'alice_avatar'},
            alice, 'Register Alice account')
        t = self.table('account', 'allaccounts')
        self.assertTrue(compare(['#ignoreorder',
                                 get_expected_account_body(alice)], t, ignore_excess=True))
        end()

    def test_register_user_another_user_failed(self):
        begin('Register Alice with bob auth', True)
        bob = self.get_non_registered_bob()
        self.failed_action('registeracc', {
            'user': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS',
            'ipfs_avatar': 'alice_avatar'},
            bob, 'Register Alice account', 'auth')
        end()

    def test_register_account_twice_failed(self):
        begin('Register alice account twice', True)
        alice = self.register_alice_account()
        self.wait()
        self.failed_action('registeracc', {
            'user': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS',
            'ipfs_avatar': 'alice_avatar'},
            alice, 'Register Alice account again', 'assert')
        end()

    def test_account_management(self):
        begin('Testing functions for changing ipfs profile and display_name')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = ['#ignoreorder',
             get_expected_account_body(alice),
             get_expected_account_body(bob)]
        self.action('setaccprof', {'user': 'alice', 'ipfs_profile': 'updated IPFS', 'display_name': 'updated display name', 'ipfs_avatar': 'updated_avatar'},
                    alice, 'Set Alice IPFS profile to \'updated IPFS\'')
        
        t = self.table('account', 'allaccounts')
        e[1]['ipfs_profile'] = 'updated IPFS'
        e[1]['display_name'] = 'updated display name'
        e[1]['ipfs_avatar'] = 'updated_avatar'
        e[1]['energy'] -= economy['ENERGY_UPDATE_PROFILE']
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_change_display_name_and_ipfs_profile_for_non_existent_account_failed(self):
        begin('Testing changing account IPFS profile and display_name for non-existing account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('setaccprof', {
                           'user': 'alice', 'ipfs_profile': 'test', 'display_name': 'test', 'ipfs_avatar': 'updated_avatar'}, alice, 'Changing Alice ipfs profile', 'assert')
        end()

    def test_change_display_name_and_ipfs_profile_another_user_failed(self):
        begin('Testing changing account IPFS profile and display_name with another account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('setaccprof',  {
                           'user': 'alice', 'ipfs_profile': 'test', 'display_name': 'test', 'ipfs_avatar': 'updated_avatar'}, bob, 'Changing Alice ipfs profile with bob auth', 'auth')
        end()


if __name__ == '__main__':
    main()
