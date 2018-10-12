import peeraniatest
from peeraniatest import *
from jsonutils import *
from time import sleep
from unittest import main


class AccountManagementTests(peeraniatest.PeeraniaTest):
    def test_timer_basic(self):
        begin('Test account timer 1 tick for different account')
        alice = self.register_alice_account(1, 0)
        bob = self.register_bob_account(1, 1)
        e = ['#ignoreorder',
             get_expected_account_body(alice),
             get_expected_account_body(bob)
            ]
        var = {}
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.wait()
        info('Wait 6 second untill the timer tick')
        sleep(6)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.assertTrue(var['alice_mdp'] == 3)
        self.assertTrue(var['bob_mdp'] == 4)
        info('Now alice have 3 moderation points, bob 4')
        info('Wait 6 second untill the timer tick')
        sleep(6)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.assertTrue(var['alice_mdp'] == 6)
        self.assertTrue(var['bob_mdp'] == 7)
        info('Now alice have 6 moderation points, bob 7')
        end()

    def test_broke_timer_failed(self):
        begin('Attempt to broke timer(DDOS)')
        alice = self.register_alice_account()
        e = [get_expected_account_body(alice)]
        var = {}
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        info('Call update acc in all possible blocks')
        for i in range(12):
            self.action('updateacc', {'user': 'alice'}, alice, 'Call system func update_account')
            self.wait()
        self.action('updateacc', {'user': 'alice'}, alice, 'Call system func update_account')
        var['alice_mdp'] += 3
        setvar(e, var)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        end()

    def test_call_system_func_another_auth_failed(self):
        begin('Test account timer 1 tick for different account')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('updateacc', {'user': 'bob'}, alice, 'Call system func update_account')
        end()

    def test_no_rating_no_moderation_points(self):
        begin('Test rating equal zero timer do nothing')
        alice = self.register_alice_account(0, 0)
        e = [get_expected_account_body(alice)]
        var = {}
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        info('Wait 6 second untill the timer tick')
        sleep(6)
        self.wait()
        setvar(e, var)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        info('The number of alice moderation points isn\'t changed')
        end()
        
if __name__ == '__main__':
    main()
