import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class AccountModerationTests(peeraniatest.PeeraniaTest):
    def test_report_user(self):
        begin('Test report user')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        account_e = [{
            'user': alice,
            'reports': [],
            'report_power': 0,
            'is_freezed': False
        }, {
            'user': bob,
            'reports': [],
            'report_power': 0,
            'is_freezed': False
        }]
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        account_e[0]['reports'].append({
            'user': 'bob',
            'report_points': 1
        })
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

    def test_clear_report(self):
        begin('Test clear reports')
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        account_e = [{
            'user': alice,
            'reports': [],
            'report_power': 0,
            'is_freezed': False
        }, {
            'user': bob,
            'reports': [],
            'report_power': 0,
            'is_freezed': False
        }]
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.wait(2)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        account_e[0]['reports'].append({
            'user': 'bob',
            'report_points': 6
        })
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

    def test_report_twice_failed(self):
        begin('Test call report twice', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.wait()
        self.failed_action('reportprof', {
            'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account', 'assert')
        end()

    def test_report_own_failed(self):
        begin('Test call report to own', True)
        alice = self.register_alice_account()
        self.failed_action('reportprof', {
            'user': alice, 'user_to_report': 'alice'}, alice, 'alice report own account', 'assert')
        end()

    def test_freze_profile(self):
        begin('Freze profile')
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        carol = self.register_carol_account(10000, 5)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.action('reportprof', {
                    'user': carol, 'user_to_report': 'alice'}, carol, 'Carol report alice account')
        account_e = [{
            'user': alice,
            'reports': [{
                'user': 'bob',
                'report_points': 6
            }, {
                'user': 'carol',
                'report_points': 6
            }],
            'report_power': 1,
            'is_freezed': 1
        }, {'user': bob}, {'user': carol}]
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

    def test_report_when_frezed_failed(self):
        begin('Call report, when account already freezed', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        carol = self.register_carol_account(10000, 5)
        ted = self.register_ted_account()
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.action('reportprof', {
                    'user': carol, 'user_to_report': 'alice'}, carol, 'Carol report alice account')
        self.failed_action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice account', 'assert')
        end()

    def test_autounfreze(self):
        begin('Unfreezing profile in some period')
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        carol = self.register_carol_account(10000, 5)
        ted = self.register_ted_account(500, 2)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.action('reportprof', {
                    'user': carol, 'user_to_report': 'alice'}, carol, 'Carol report alice account')
        info("Wait untill freeze stoppeed")
        self.wait(2)
        self.failed_action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice, it freezed yet', 'assert')
        self.wait(1)
        self.action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice account')
        account_e = [{
            'user': alice,
            'reports': [{
                'user': 'ted',
                'report_points': 2
            }],
            'report_power': 1,
            'is_freezed': False
        }, {'user': bob}, {'user': carol}, {'user': 'ted'}]
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.action('reportprof', {
                    'user': carol, 'user_to_report': 'alice'}, carol, 'Carol report alice account')
        info("Wait untill freeze stoppeed")
        self.wait(5)
        self.failed_action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice, it freezed yet', 'assert')
        self.wait(1)
        self.action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice account')
        account_e[0]['report_power'] = 2
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

    def test_report_power_reset(self):
        begin('Unfreezing profile in some period')
        alice = self.register_alice_account()
        bob = self.register_bob_account(10000, 5)
        carol = self.register_carol_account(10000, 5)
        ted = self.register_ted_account(500, 2)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        self.action('reportprof', {
                    'user': carol, 'user_to_report': 'alice'}, carol, 'Carol report alice account')
        self.wait(3)
        self.action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice account')
        account_e = [{
            'user': alice,
            'reports': [{
                'user': 'ted',
                'report_points': 2
            }],
            'report_power': 1,
            'is_freezed': False
        }, {'user': bob}, {'user': carol}, {'user': 'ted'}]
        self.wait(4)
        self.action('reportprof', {
                    'user': ted, 'user_to_report': 'alice'}, ted, 'Ted attempt to report alice account')
        account_e[0]['report_power'] = 0
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

if __name__ == '__main__':
    main()
