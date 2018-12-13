import peeraniatest
from peeraniatest import *
from jsonutils import compare
from time import sleep
from unittest import main


class AccountManagementTests(peeraniatest.PeeraniaTest):

    def test_register_user(self):
        begin('Testing registration of new user Alice')
        alice = self.get_non_registered_alice()
        self.action('registeracc', {
            'owner': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS'},
            alice, 'Register Alice account')
        t = self.table('account', 'allaccounts')
        self.assertTrue(compare(['#ignoreorder',
                                 get_expected_account_body(alice)], t, ignore_excess=True))
        end()

    def test_register_user_another_owner_failed(self):
        begin('Register Alice with bob auth', True)
        bob = self.get_non_registered_bob()
        self.failed_action('registeracc', {
            'owner': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS'},
            bob, 'Register Alice account', 'auth')
        end()

    def test_register_account_twice_failed(self):
        begin('Register alice account twice', True)
        alice = self.register_alice_account()
        self.wait()
        self.failed_action('registeracc', {
            'owner': 'alice',
            'display_name': 'aliceDispName',
            'ipfs_profile': 'alice_IPFS'},
            alice, 'Register Alice account again', 'assert')
        end()

    def test_user_property(self):
        begin('Testing properties for accounts')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        def regInt(owner, key, value):
            self.action('setaccintprp',
                        {'owner': str(
                            owner), 'key': key, 'value': value}, owner,
                        'Set {} integer property, {{key = {}, value = {} }}'.format(str(owner),
                                                                                    key, value))

        def regStr(owner, key, value):
            self.action('setaccstrprp',
                        {'owner': str(
                            owner), 'key': key, 'value': value}, owner,
                        'Set {} string property, {{key = {}, value = "{}" }}'.format(str(owner),
                                                                                     key, value))
        e = ['#ignoreorder',
             get_expected_account_body(alice),
             get_expected_account_body(bob)]
        for i in range(3):
            regInt(alice, i + 5, i * i * i)
            e[1]['integer_properties'].append(
                {'key': i + 5, 'value': i * i * i})
            regInt(bob, i + 1, i * i)
            e[2]['integer_properties'].append({'key': i + 1, 'value': i * i})
            regStr(alice, i + 10, 'alice' + str(i + 2))
            e[1]['string_properties'].append(
                {'key': i + 10, 'value': 'alice'+str(i + 2)})
            regStr(bob, i + 20, 'bob' + str(i + 10))
            e[2]['string_properties'].append(
                {'key': i + 20, 'value': 'bob' + str(i + 10)})

        t = self.table('account', 'allaccounts')
        self.assertTrue(compare(e, t, ignore_excess=True))
        info('Table accounts after operation: ', t)
        info('Test update property\n')
        regInt(alice, 6, 48)
        e[1]['integer_properties'][1] = {'key': 6, 'value': 48}
        regStr(alice, 11, 'updated')
        e[1]['string_properties'][1] = {'key': 11, 'value': 'updated'}
        t = self.table('account', 'allaccounts')
        self.assertTrue(compare(e, t, ignore_excess=True))
        info('Table account after opertion: ', t)
        end()

    def test_account_management(self):
        begin('Testing functions for changing ipfs profile and display_name')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = ['#ignoreorder',
             get_expected_account_body(alice),
             get_expected_account_body(bob)]
        self.action('setaccprof', {'owner': 'alice', 'ipfs_profile': 'updated IPFS', 'display_name': 'updated display name'},
                    alice, 'Set Alice IPFS profile to \'updated IPFS\'')
        t = self.table('account', 'allaccounts')
        e[1]['ipfs_profile'] = 'updated IPFS'
        e[1]['display_name'] = 'updated display name'
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_properties_for_non_existent_account_failed(self):
        begin('Testing register property for non-existing account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('setaccintprp',
                           {'owner': str(
                               alice), 'key': 1, 'value': 1}, alice,
                           'Set Alice(not registered) integer property', 'assert')
        self.failed_action('setaccstrprp',
                           {'owner': str(
                               alice), 'key': 1, 'value': '1'}, alice,
                           'Set Alice(not registered) integer property', 'assert')
        end()
    
    def test_change_display_name_and_ipfs_profile_for_non_existent_account_failed(self):
        begin('Testing changing account IPFS profile and display_name for non-existing account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('setaccprof', {
                           'owner': 'alice', 'ipfs_profile': 'test', 'display_name': 'test'}, alice, 'Changing Alice ipfs profile', 'assert')
        end()

    def test_properties_another_owner_failed(self):
        begin('Testing registration of the integer and string property with another account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('setaccstrprp',  {
                           'owner': 'alice', 'key': 1, 'value': 1}, bob, 'Register new Alice string property with bob auth', 'auth')
        self.failed_action('setaccintprp',  {
                           'owner': 'alice', 'key': 1, 'value': '1'}, bob, 'Register new Alice integer property with bob auth', 'auth')
        end()

    def test_change_display_name_and_ipfs_profile_another_owner_failed(self):
        begin('Testing changing account IPFS profile and display_name with another account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('setaccprof',  {
                           'owner': 'alice', 'ipfs_profile': 'test', 'display_name': 'test'}, bob, 'Changing Alice ipfs profile with bob auth', 'auth')
        end()


if __name__ == '__main__':
    main()
