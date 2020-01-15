import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main


REFERAL_REWARD = '10.000000 PEER'

class TokenReferal(peeranhatest.peeranhaTest):

    def test_referal_not_registret_failed(self):
        begin('Referal not registred', True)
        bob = self.get_non_registered_bob()
        alice = self.get_non_registered_alice()
        self.failed_action('inviteuser', {
            'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob attempt to invite alice, but he hasn\'t peeranha account', 'assert', contract='token')
        end()

    def test_invite_already_registred_failed(self):
        begin('Ivite already registred account', True)
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        self.failed_action('inviteuser', {
            'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob attempt to invite alice, but alice already have peeranha account', 'assert', contract='token')
        end()

    def test_invite_referal_twice_failed(self):
        begin('Test invite referal twice', True)
        bob = self.register_bob_account()
        alice = self.get_non_registered_alice()
        self.action('inviteuser', {
                    'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', contract='token')
        self.wait()
        self.failed_action('inviteuser', {
            'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', 'assert', contract='token')
        end()

    def test_invite_self_failed(self):
        begin('Test invite self', True)
        alice = self.get_non_registered_alice()
        bob = self.register_bob_account()
        self.failed_action('inviteuser', {
            'inviter': 'alice', 'invited_user': 'alice'}, alice, 'Alice invite himself', 'assert', contract='token')
        self.failed_action('inviteuser', {
            'inviter': 'bob', 'invited_user': 'bob'}, bob, 'Bob invite himself', 'assert', contract='token')
        end()

    def test_pickup_referal_reward_without_rating_failed(self):
        begin('Test pickup referal reward without reach required rating', True)
        bob = self.register_bob_account()
        alice = self.get_non_registered_alice()
        self.action('inviteuser', {
                    'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', contract='token')
        self.register_alice_account()
        self.failed_action('rewardrefer', {'invited_user': 'alice'}, alice, 'Alice attempt to pickup reward', 'assert', contract='token')
        end()

    def test_pickup_referal_reward_without_rating2_failed(self):
        begin('Test pickup referal reward without reach required rating 35(34 only reached)', True)
        bob = self.register_bob_account()
        alice = self.get_non_registered_alice()
        self.action('inviteuser', {
                    'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', contract='token')
        self.register_alice_account(10)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 24},
                            self.admin, 'Change alice rating to 34')
        info('Wait until period ends')
        sleep(3)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 1},
                            self.admin, 'Update alice rating')
        self.failed_action('rewardrefer', {'invited_user': 'alice'}, alice, 'Alice attempt to pickup reward', 'assert', contract='token')
        end()

    def test_pickup_referal_reward(self):
        zero_asset = '0.000000 PEER'
        begin('Test pickup referal reward')
        bob = self.register_bob_account()
        alice = self.get_non_registered_alice()
        self.action('inviteuser', {
                    'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', contract='token')
        e = {'invited_user': 'alice',
             'inviter': 'bob',
             'common_reward': zero_asset}
        self.assertTrue(compare([e], self.table('invited', 'allinvited', contract='token')))
        self.register_alice_account(10)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 25},
                            self.admin, 'Change alice rating to 35')
        info('Wait until period ends')
        sleep(3)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 1},
                            self.admin, 'Update alice rating')
        self.action('rewardrefer', {'invited_user': 'alice'}, alice, 'Alice attempt to pickup reward', contract='token')
        
        e['common_reward'] = REFERAL_REWARD
        self.assertTrue(compare([e], self.table('invited', 'allinvited', contract='token')))

        stat_e = {
            'user_supply': REFERAL_REWARD,
            'supply': REFERAL_REWARD,
            'funding_supply': zero_asset,
        }
        stat = self.table('stat', '......2mcp2p', contract='token')[0]
        self.assertTrue(compare(stat_e, stat, ignore_excess = True))

        alice_reward = self.table('accounts', 'alice', contract='token')[0]["balance"]
        bob_reward = self.table('accounts', 'bob', contract='token')[0]["balance"]

        #spilt coef
        self.assertTrue(alice_reward == '5.000000 PEER')
        self.assertTrue(bob_reward == '5.000000 PEER')
        end()

    def test_pickup_referal_reward_twice_failed(self):
        begin('Test pickup referal reward twice')
        bob = self.register_bob_account()
        alice = self.get_non_registered_alice()
        self.action('inviteuser', {
                    'inviter': 'bob', 'invited_user': 'alice'}, alice, 'Bob invite alice', contract='token')
        self.register_alice_account(10)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 25},
                            self.admin, 'Change alice rating to 35')
        info('Wait until period ends')
        sleep(3)
        self.action('chnguserrt', {'user': 'alice', 'rating_change': 1},
                            self.admin, 'Update alice rating')
        self.action('rewardrefer', {'invited_user': 'alice'}, alice, 'Alice attempt to pickup reward', contract='token')
        self.wait()
        self.failed_action('rewardrefer', {'invited_user': 'alice'}, alice, 'Alice attempt to pickup reward again', 'assert', contract='token')
        end()

if __name__ == '__main__':
    main()
