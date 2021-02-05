import peeranhatest
from test_forum_comment import cbody
from peeranhatest import *
from jsonutils import *
from unittest import main

MODERATION_IMPACT_INFINITE = 255
PROPERTY_MODERATOR_FLAGS = 48
MODERATOR_FLG_ALL = 31

class TestEditCommunity(peeranhatest.peeranhaTest):
    
    
    def test_edit_community_by_user(self):
        begin('Test editing community by user')
        bob = self.register_bob_account(100000, 400)
        self._give_moderator_flag(bob, MODERATOR_FLG_ALL)
        alice = self.register_alice_account(100000, 400)
        self.action('crcommunity', {'user': bob, 'name': 'admin community1', 'type': 2,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, bob, 'Bob create community')
        self.failed_action('editcomm', {'user': alice, 'community_id': 4, 'name': 'alice community1', 'tags': [1], 'title': 'Title alice question2', 'ipfs_description': 'ACM1', 'type': 2}, alice,
                           'Alice try to edit community without permissions', 'assert')                            
        end()

    def test_edit_community_by_admin(self):
        begin('Test editing community by community admin')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account(100000, 400)
        bob = self.register_bob_account(100000, 400)
        self._give_moderator_flag(bob, MODERATOR_FLG_ALL)
        self.action('crcommunity', {'user': bob, 'name': 'admin community1', 'type': 2,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, bob, 'Bob create community')

        self.action('givecommuflg', {
            'user': alice,
            'flags': MODERATION_IMPACT_INFINITE,
            'community_id': 4
        }, admin, 'add a flag MODERATION_IMPACT_INFINITE')

        self.action('editcomm', {'user': alice, 'community_id': 4, 'name': 'alice community1', 'tags': [1], 'title': 'Title alice question2', 'ipfs_description': 'ACM1', 'type': 2}, alice,
                           'Alice edit community with community admin permission')

        end()

    def test_edit_community_by_moderator(self):
        bob = self.register_bob_account(100000, 400)
        self._give_moderator_flag(bob, MODERATOR_FLG_ALL)
        self.action('crcommunity', {'user': bob, 'name': 'admin community1', 'type': 2,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, bob, 'Bob create community')
        self.action('editcomm', {'user': bob, 'community_id': 4, 'name': 'alice community1', 'tags': [1], 'title': 'Title alice question2', 'ipfs_description': 'ACM1', 'type': 2}, bob,
                           'Bob edit community with moderator permission')
        end()

    def get_stub_suggested_tags(self):
        tags = []
        for i in range(0, 10):
            tags.append({
                'name': f'Tag {i}',
                'ipfs_description': f'IPFS of tag {i}'
            })
        return tags

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()