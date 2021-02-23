import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

MODERATOR_FLG_ALL = 31

defs = load_defines('./src/contracts/peeranha.main/economy.h')


class CommunityQuestionsTypeTest(peeranhatest.peeranhaTest):

    def test_ask_and_modify_questions(self):
        begin("Testing work of asking and modifying questionst in community with general/expert/any type")
        alice = self.register_alice_account(100000, 400)
        self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
        self.action('crcommunity', {'user': alice, 'name': 'alice community1', 'type': 0,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with EXPERT type')
        self.action('crcommunity', {'user': alice, 'name': 'alice community2', 'type': 1,
                                    'ipfs_description': 'ACM2', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with GENERAL type')
        self.action('crcommunity', {'user': alice, 'name': 'alice community3', 'type': 2,
                                    'ipfs_description': 'ACM3', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with ANY type')
        self.failed_action('crcommunity', {'user': alice, 'name': 'alice community3', 'type': 3,
                                    'ipfs_description': 'ACM4', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice attempt to create community with non-existent type', 'assert')
        self.action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ1', 'type': 0}, alice,
                           'Alice ask EXPERT question in EXPERT_TYPE community')
        self.failed_action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ12', 'type': 1}, alice,
                           'Alice attempt to ask GENERAL question in EXPERT_TYPE community', 'assert')
        self.action('postquestion', {'user': alice, 'community_id': 5, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ2', 'type': 1}, alice,
                           'Alice ask GENERAL question in GENERAL_TYPE community')
        self.failed_action('postquestion', {'user': alice, 'community_id': 5, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ22', 'type': 0}, alice,
                           'Alice attempt to ask EXPERT question in GENERAL_TYPE community', 'assert')
        self.action('postquestion', {'user': alice, 'community_id': 6, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ3', 'type': 0}, alice,
                           'Alice ask EXPERT question in ANY_TYPE community')
        self.action('postquestion', {'user': alice, 'community_id': 6, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ4', 'type': 1}, alice,
                           'Alice ask GENERAL question in ANY_TYPE community')
        # AQ_id = self.table('question', 'allquestions')[0]['id']
        questions = self.table('question', 'allquestions')
        self.failed_action('modquestion', {'user': alice, 'question_id': questions[2]['id'], 'title': 'Title alice question1', 'ipfs_link': 'AQ2', 'community_id': 5, 'tags':[1], 'type': 0, 'restore_rating': True}, alice,
                            'Alice attempt to modify question type in community with only GENERAL questions', 'assert')
        self.failed_action('modquestion', {'user': alice, 'question_id': questions[3]['id'], 'title': 'Title alice question1', 'ipfs_link': 'AQ1', 'community_id': 4, 'tags':[1], 'type': 1, 'restore_rating': True}, alice,
                            'Alice attempt to modify question type in community with only EXPERT questions', 'assert')
        end()

    def test_change_community_questions_type(self):
        begin("Testing work of changing community questions type")
        alice = self.register_alice_account(100000, 400)
        self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
        self.action('crcommunity', {'user': alice, 'name': 'alice community1', 'type': 2,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with ANY type')
        self.action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ3', 'type': 0}, alice,
                           'Alice ask EXPERT question in ANY_TYPE community')
        self.action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ4', 'type': 1}, alice,
                           'Alice ask GENERAL question in ANY_TYPE community')
        self.action('editcomm', {'user': alice, 'community_id': 4, 'name': 'alice community1', 'tags': [1], 'title': 'Title alice question1', 'ipfs_description': 'ACM1', 'type': 0}, alice,
                           'Alice edit community question type to EXPERT')
        self.action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ1', 'type': 0}, alice,
                           'Alice ask EXPERT question in EXPERT_TYPE community')
        self.failed_action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ12', 'type': 1}, alice,
                           'Alice attempt to ask GENERAL question in EXPERT_TYPE community', 'assert')
        self.action('editcomm', {'user': alice, 'community_id': 4, 'name': 'alice community1', 'tags': [1], 'title': 'Title alice question1', 'ipfs_description': 'ACM1', 'type': 1}, alice,
                           'Alice edit community question type to GENERAL')
        self.action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question1', 'ipfs_link': 'AQ2', 'type': 1}, alice,
                           'Alice ask GENERAL question in GENERAL_TYPE community')
        self.failed_action('postquestion', {'user': alice, 'community_id': 4, 'tags': [1], 'title': 'Title alice question2', 'ipfs_link': 'AQ22', 'type': 0}, alice,
                           'Alice attempt to ask EXPERT question in GENERAL_TYPE community', 'assert')
        end()

    def test_create_specific_type_community_allowed(self):
        begin("Testing work of changing community questions type")
        alice = self.register_alice_account(100000, 400)
        self.failed_action('crcommunity', {'user': alice, 'name': 'alice community1', 'type': 0,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with ANY type', 'assert')
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