import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6
MODERATOR_FLG_ALL = 31

DEFAULT_RATING = 200

ANSWER_ACCEPTED_AS_CORRECT_REWARD = 15        #answer
COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD = 3

ACCEPT_ANSWER_AS_CORRECT_REWARD = 2           #question
ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD = 1

QUESTION_DELETED_REWARD = 2
ANSWER_DELETED_REWARD = 2

class TestFix(peeranhatest.peeranhaTest):  
    def test_delete_question(self):
        begin('test delete expert question with correct answer')
        var = {}
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        create_question(self, alice, bob, 0, var)

        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        bob_rating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING + ACCEPT_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(bob_rating, DEFAULT_RATING + ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')
        
        newAliceRating = self.table('account', 'allaccounts')[0]['rating']
        newBobRating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(newAliceRating, alice_rating - ACCEPT_ANSWER_AS_CORRECT_REWARD - QUESTION_DELETED_REWARD, ignore_excess=True))
        self.assertTrue(compare(newBobRating, bob_rating - ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        end()
    
    def test_delete_common_question(self):
        begin('test delete common question with correct answer')
        var = {}
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        create_question(self, alice, bob, 1, var)

        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        bob_rating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING + ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(bob_rating, DEFAULT_RATING + COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')
        
        newAliceRating = self.table('account', 'allaccounts')[0]['rating']
        newBobRating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(newAliceRating, alice_rating - ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD - QUESTION_DELETED_REWARD, ignore_excess=True))
        self.assertTrue(compare(newBobRating, bob_rating - COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        end()

    def test_delete_correct_answer_in_expert_question(self):
        begin('test delete correct answer in expert question')

        var = {}
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        create_question(self, alice, bob, 0, var)

        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        bob_rating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING + ACCEPT_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(bob_rating, DEFAULT_RATING + ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')
        
        newAliceRating = self.table('account', 'allaccounts')[0]['rating']
        newBobRating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(newAliceRating, alice_rating - ACCEPT_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(newBobRating, bob_rating - ANSWER_ACCEPTED_AS_CORRECT_REWARD - ANSWER_DELETED_REWARD, ignore_excess=True))

        end()
    
    def test_delete_correct_answer_in_common_question(self):
        begin('test delete correct answer in common question')

        var = {}
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        create_question(self, alice, bob, 1, var)

        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        bob_rating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING + ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(bob_rating, DEFAULT_RATING + COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')
        
        newAliceRating = self.table('account', 'allaccounts')[0]['rating']
        newBobRating = self.table('account', 'allaccounts')[1]['rating']
        self.assertTrue(compare(newAliceRating, alice_rating - ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD, ignore_excess=True))
        self.assertTrue(compare(newBobRating, bob_rating - COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD - ANSWER_DELETED_REWARD, ignore_excess=True))

        end()

    def test_delete_answer_1(self):
        begin('test delete correct answer in common question(question and correct answer from alice)')

        alice = self.register_alice_account()
        var = {}
        create_question(self, alice, alice, 1, var)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING, ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        new_alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(new_alice_rating, alice_rating - ANSWER_DELETED_REWARD, ignore_excess=True))

        end()
    
    def test_delete_answer_2(self):
        begin('test delete correct answer in expert question(question and correct answer from alice)')

        alice = self.register_alice_account()
        var = {}
        create_question(self, alice, alice, 0, var)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING, ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        new_alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(new_alice_rating, alice_rating - ANSWER_DELETED_REWARD, ignore_excess=True))

        end()

    def test_delete_question_1(self):
        begin('test delete common question with correct answer(question and correct answer from alice)')

        alice = self.register_alice_account()
        var = {}
        create_question(self, alice, alice, 1, var)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING, ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        new_alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(new_alice_rating, alice_rating - QUESTION_DELETED_REWARD, ignore_excess=True))

        end()
    
    def test_delete_question_2(self):
        begin('test delete expert question with correct answer(question and correct answer from alice)')

        alice = self.register_alice_account()
        var = {}
        create_question(self, alice, alice, 0, var)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(alice_rating, DEFAULT_RATING, ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        new_alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(compare(new_alice_rating, alice_rating - QUESTION_DELETED_REWARD, ignore_excess=True))

        end()
    

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')


def create_question(self, user_post_question, user_post_answer, typeQuestion, var):
    begin('Create question and answer')

    self.action('postquestion', {'user': user_post_question, 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': typeQuestion}, user_post_question,
                'Register question from alice')

    e = [{
            'id': '#var aq',
            'user': user_post_question,
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        }]
    t = self.table('question', 'allquestions')
    
    self.assertTrue(compare(e, t, var, True))
    self.action('postanswer', {'user': user_post_answer, 'question_id': var['aq'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                user_post_answer, 'Register Bob answer to Alice question')
        
    e[0]['answers'].append({'user': user_post_answer, 'id': '#var aq_ba'})
    t = self.table('question', 'allquestions')

    self.assertTrue(compare(e, t, var, True))
    self.action('mrkascorrect', {'user': user_post_question, 'question_id': var['aq'],
                                     'answer_id': var['aq_ba']}, user_post_question, 'Alice mark bob answer as correct')

if __name__ == '__main__':
    main()