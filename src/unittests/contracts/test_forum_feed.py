import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class ForumFeedTests(peeraniatest.PeeraniaTest):
    def test_un_follow_community(self):
        begin('Test follow community, unfollow community')
        alice = self.register_alice_account()
        account_e = [{
            'user': alice,
            'followed_communities': []
        }]
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Alice now following community 1')
        account_e[0]['followed_communities'].append(1)
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('followcomm', {'user': alice, 'community_id': 2}, alice, 'Alice now following community 2')
        account_e[0]['followed_communities'].append(2)
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('unfollowcomm', {'user': alice, 'community_id': 1}, alice, 'Alice no longer follows 1 community.')
        del account_e[0]['followed_communities'][0]
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('unfollowcomm', {'user': alice, 'community_id': 2}, alice, 'Alice no longer follows 2 community.')
        del account_e[0]['followed_communities'][0]
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_un_follow_community_another_auth_failed(self):
        begin('Test follow community, unfollow community with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Alice now followin community 1')
        self.failed_action('unfollowcomm', {'user': alice, 'community_id': 1}, bob, 'Bob attempt to call unfollow for alice account', 'auth')
        self.failed_action('followcomm', {'user': bob, 'community_id': 2}, alice, 'Alice attempt to call follow for bob account', 'auth')
        end()


    def test_un_follow_not_registered_failed(self):
        begin('Test follow community, unfollow community without peerania account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('unfollowcomm', {'user': alice, 'community_id': 1}, alice, 'Alice attempt to call unfollow without account', 'assert')
        self.failed_action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Alice attempt to call follow without account', 'assert')
        end()

    def test_un_follow_non_existent_communities_failed(self):
        begin('Test follow community, unfollow non-existent community', True)
        alice = self.register_alice_account()
        self.failed_action('followcomm', {'user': alice, 'community_id': 10}, alice, 'Alice attempt to follow not existent community', 'assert')
        self.failed_action('unfollowcomm', {'user': alice, 'community_id': 10}, alice, 'Alice attempt to unfollow not existent community', 'assert')
        end()

    def test_un_follow_twice_failed(self):
        begin('Test follow community, unfollow community twice', True)
        alice = self.register_alice_account()
        self.action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Alice now followin community 1')
        self.wait()
        self.failed_action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Alice attempt to follow 1 community again', 'assert')
        self.action('unfollowcomm', {'user': alice, 'community_id': 1}, alice, 'Alice no longer follows 1 community.')
        self.wait()
        self.failed_action('unfollowcomm', {'user': alice, 'community_id': 1}, alice, 'Alice attempt to unfollow 1 community again', 'assert')
        end()

if __name__ == '__main__':
    main()
