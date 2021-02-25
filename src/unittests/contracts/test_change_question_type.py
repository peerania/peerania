import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

FIRST_ANSWER_COMMON = 1
FIRST_ANSWER_EXPERT = 5
ANSWER_15_COMMON = 1
ANSWER_15_EXPERT = 5
MARK_AS_CORRECT_EXPERT = 15
MARK_AS_CORRECT_COMMON = 3
COMMON_ANSWER_UPVOTED_REWARD = 2
EXPERT_ANSWER_UPVOTED_REWARD = 10
COMMON_ANSWER_DOWNVOTED_REWARD = -4
EXPERT_ANSWER_DOWNVOTED_REWARD = -12

class RatingRewardsTestsGeneralQuestion(peeranhatest.peeranhaTest):
    def test_change_question_type(self):
        begin("Test change question type")
        (alice, bob, carol, dan) = self._create_basic_hierarchy(0)
        self.action('mrkascorrect', {
            'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']}, alice, "Alice upvote Carol answer") 
        self.action('downvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice downvote Bob answer")
        bob_rating_expert = 200 + FIRST_ANSWER_EXPERT + ANSWER_15_EXPERT + MARK_AS_CORRECT_EXPERT + EXPERT_ANSWER_DOWNVOTED_REWARD
        carol_rating_expert = 200 + FIRST_ANSWER_EXPERT + 2 * ANSWER_15_EXPERT + EXPERT_ANSWER_UPVOTED_REWARD
        self.assertTrue(bob_rating_expert == self.table('account', 'allaccounts')[1]['rating'])
        self.assertTrue(carol_rating_expert == self.table('account', 'allaccounts')[2]['rating'])
        self.action('modquestion', {'user': 'dan', 'question_id': self.var['aq'], 'community_id': 1, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 1, "restore_rating": True}, dan,
                    'Dan modify alice question type')
        self.action('modquestion', {'user': 'dan', 'question_id': self.var['bq'], 'community_id': 1, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 1, "restore_rating": True}, dan,
                    'Dan modify bob question type')
        bob_rating = 200 + FIRST_ANSWER_COMMON + ANSWER_15_COMMON + MARK_AS_CORRECT_COMMON + COMMON_ANSWER_DOWNVOTED_REWARD
        carol_rating = 200 + FIRST_ANSWER_COMMON + 2 * ANSWER_15_COMMON + COMMON_ANSWER_UPVOTED_REWARD
        self.assertTrue(bob_rating == self.table('account', 'allaccounts')[1]['rating'])
        self.assertTrue(carol_rating == self.table('account', 'allaccounts')[2]['rating'])
        end()


    def _create_basic_hierarchy(self, tp=0):
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        dan = self.register_dan_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': tp}, alice,
                    'Alice asking question')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'BQ', 'community_id': 1, 'tags': [1], 'type': tp}, bob,
                    'Bob asking question')
        self.forum_e = ['#ignoreorder',
                        {
                            'id': '#var aq',
                            'user': 'alice',
                            'title': 'Title alice question',
                            'ipfs_link': 'AQ',
                            'correct_answer_id': '#var aq_caid',
                            'rating': '#var aq_rating',
                            'answers': [],
                            'comments':[]
                        }, {
                            'id': '#var bq',
                            'user': 'bob',
                            'title': 'Title bob question',
                            'ipfs_link': 'BQ',
                            'correct_answer_id': '#var bq_caid',
                            'rating': '#var bq_rating',
                            'answers': [],
                            'comments':[]
                        }]
        t = self.table('question', 'allquestions')
        self.var = {}
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->CA', 'official_answer': False},
                    carol, 'Carol answering Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': self.var['bq'], 'ipfs_link': 'BQ->CA', 'official_answer': False},
                    carol, 'Carol answering Bob')
        self.forum_e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA',
            'rating': '#var aq_aa_rating',
            'comments': []})
        self.forum_e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'AQ->CA',
            'rating': '#var aq_ca_rating',
            'comments': []})
        self.forum_e[2]['answers'].append({
            'id': '#var bq_ca',
            'user': 'carol',
            'ipfs_link': 'BQ->CA',
            'rating': '#var bq_ca_rating',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(self.forum_e, t, self.var, True))
     
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(self.forum_e, t, self.var, True))

        self.defs = {**load_defines('./src/contracts/peeranha.main/economy.h'),
                     **load_defines('./src/contracts/peeranha.main/question_container.hpp')}
        self.account_e = ['#ignoreorder',
                          {'user': 'alice', 'energy': '#var alice_energy',
                           'rating': '#var alice_rating'},
                          {'user': 'bob', 'energy': '#var bob_energy',
                              'rating': '#var bob_rating'},
                          {'user': 'carol', 'energy': '#var carol_energy',
                              'rating': '#var carol_rating'},
                          {'user': 'dan', 'energy': '#var dan_energy', 
                              'rating': '#var dan_rating'}]
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': 'dan', 'flags': 32}, admin, "Give moderator flags to dan")   
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        return alice, bob, carol, dan

    def _verify_acc(self):
        buf_var = {}
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), buf_var, ignore_excess=True))
        for key, value in buf_var.items():
            # print(key, self.var[key], value)
            self.assertTrue(self.var[key] == value)

    def get_stub_suggested_tags(self):
        tags = []
        for i in range(0, 10):
            tags.append({
                'name': f'Tag {i}',
                'ipfs_description': f'IPFS of tag {i}'
            })
        return tags


if __name__ == '__main__':
    main()