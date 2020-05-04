import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

COMMUNITY_ADMIN_FLG_INFINITE_ENERGY = 1 << 0        # 1
COMMUNITY_ADMIN_FLG_INFINITE_IMPACT = 1 << 1        # 2
COMMUNITY_ADMIN_FLG_IGNORE_RATING = 1 << 2          # 4
COMMUNITY_ADMIN_FLG_CREATE_COMMUNITY = 1 << 3       # 8
COMMUNITY_ADMIN_FLG_CREATE_TAG = 1 << 4             # 16
COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS = 1 << 5 #32

class TestPropertyCommunity(peeranhatest.peeranhaTest):
    def test_Add_user(self):
        begin('Test add user')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        'community_id': 1
        }, admin, 'add a question from another community')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 2}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
        'community_id': 1
        }, admin, 'add a question from another community')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CREATE_COMMUNITY,
        'community_id': 2
        }, admin, 'add a question from another community')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 8}]}]
        
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
        'community_id': 1
        }, admin, 'add a question from another community')
        table = self.table('propertycomm', 'allprprtcomm')
        print(table)
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 8}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))


        end()
if __name__ == '__main__':
    main()