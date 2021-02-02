import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # #       STAGE == 2
# # # START_POOL 40 -> START_POOL 10000
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class TestTopQuestion(peeranhatest.peeranhaTest):  
    def test_wrong_hours(self):
        begin('Test test wrong hours')
        alice = self.register_alice_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1.4}, alice,
                    'Mark question as promoted (wrong hours)', contract='token')
        end()
    
    def test_wrong_question_id(self):
        begin('Test wrong question id')
        alice = self.register_alice_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.failed_action('addhotquestn', {'user': 'alice', 'question_id': 666, 'hours': 1}, alice,
                    'Mark question as promoted (wrong question id)', contract='token')
        end()

    def test_zero_token(self):
        begin('Test zero token')
        alice = self.register_alice_account()

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted (zero token)', contract='token')
        end()

    def test_wrong_user(self):
        begin('Test alice post question, bob add to hot question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('addhotquestn', {'user': 'bob', 'question_id': question_id, 'hours': 1}, bob,
                    'Mark question as promoted (alice post question bob add to hot question)', contract='token')
        end()

    def test_add_promoted_question(self):
        begin('test add promoted question')
        alice = self.register_alice_account()
        self.register_frank_account()
        self.register_dan_account()
        self.assertTrue(compare([], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'dan', contract='token'), ignore_excess=True))

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted', contract='token')

        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        end()

    def test_add_promoted_question_again(self):
        begin('test add promoted question again (question already mark as promoted)')
        alice = self.register_alice_account()
        self.register_frank_account()
        self.register_dan_account()

        give_tokens(self, 'alice', '40.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 2}, alice,
                    'Mark question as promoted', contract='token')

        example_promoted_question = [{'question_id': question_id}]
        print(self.table('promquestion', 1, contract='token'))
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))

        self.failed_action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted, again', contract='token')
        end()

    def test_add_promoted_question_again2(self):
        begin('test add promoted question again (was question mark as promoted)')
        alice = self.register_alice_account()
        self.register_frank_account()
        self.register_dan_account()

        give_tokens(self, 'alice', '40.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted', contract='token')
        self.wait(5)
        example_promoted_question = [{'question_id': question_id}]
        print(self.table('promquestion', 1, contract='token'))
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted', contract='token')
        end()
    
    def test_auto_delete_promoted_question(self):
        begin('auto delete promoted question')
        alice = self.register_alice_account()
        self.register_frank_account()
        self.register_dan_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark first question as promoted', contract='token')

        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        self.wait(5)

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark second question as promoted (delete first promoted question(promoted table))', contract='token')
        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        end()
    
    def test_get_award(self):
        begin('test get award')
        bob = self.register_bob_account()
        self.register_frank_account()
        self.register_dan_account()
        self.assertTrue(compare([], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'frank', contract='token'), ignore_excess=True))

        give_ratings(self, bob, 2)      # 1 period
        self.wait(2)

        give_ratings(self, bob, 2)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 2)      # 3 period
        self.wait(4)

        give_tokens(self, 'bob', '20.000000 PEER')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'bob', 'question_id': question_id, 'hours': 1}, bob,
                    'Mark question as promoted', contract='token')
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))

        give_ratings(self, bob, 2)      # 4 period
        self.wait(4)      

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 3 preiod', contract='token')

        example_reward = [{'period': 3, 'reward': '17.000000 PEER'}]    # 16 + 1(promoted)
        print(self.table('periodreward', 'bob', contract='token'))
        self.assertTrue(compare(example_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '0.000000 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        end()

    def test_get_award_divided(self):
        begin('test get award divided')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.register_frank_account()
        self.register_dan_account()

        give_ratings(self, alice, 2)      # 1 period 
        give_ratings(self, bob, 1)
        self.wait(2)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 1)      # 2 period 
        self.wait(4)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 1)      # 3 period 
        self.wait(4)

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark question as promoted', contract='token')

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 1)      # 4 period 
        self.wait(4)      

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 3 preiod', contract='token')

        example_reward = [{'period': 3, 'reward': '8.333330 PEER'}]    # 8 + 0.333330(promoted)
        print(self.table('periodreward', 'bob', contract='token'))
        self.assertTrue(compare(example_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '1.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '0.666670 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        end()

    def test_get_award_without_promoted(self):
        begin('test get award without_promoted question')
        bob = self.register_bob_account()
        self.register_frank_account()
        self.register_dan_account()

        give_ratings(self, bob, 1)      # 1 period 
        self.wait(2)

        give_ratings(self, bob, 1)      # 2 period 
        self.wait(4)

        give_ratings(self, bob, 1)      # 3 period 
        self.wait(4)

        give_ratings(self, bob, 1)      # 4 period 
        self.wait(4)      

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 3 preiod', contract='token')

        example_reward = [{'period': 3, 'reward': '8.000000 PEER'}]    # 8 + 0(promoted)
        self.assertTrue(compare(example_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        end()

    def test_get_double_award(self):
        begin('test get double award 2 user')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.register_frank_account()
        self.register_dan_account()

        give_ratings(self, alice, 2)      # 1 period 
        give_ratings(self, bob, 2)
        self.wait(2)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 2 period 
        self.wait(4)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 3 period 
        self.wait(3)

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark first question as promoted', contract='token')

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question2', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Mark second question as promoted', contract='token')

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 4 period 
        self.wait(4)      

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 3 preiod', contract='token')

        example_reward = [{'period': 3, 'reward': '17.000000 PEER'}]    # 16 + 1(promoted)
        self.assertTrue(compare(example_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        end()

    def test_get_award_2_hours(self):
        begin('test get double award 2 user')
        bob = self.register_bob_account()
        self.register_frank_account()
        self.register_dan_account()
        self.assertTrue(compare([], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'dan', contract='token'), ignore_excess=True))

        give_ratings(self, bob, 2)      # 1 period 
        self.wait(2)

        give_ratings(self, bob, 2)      # 2 period 
        self.wait(4)

        give_ratings(self, bob, 2)      # 3 period 
        self.wait(3)

        give_tokens(self, 'bob', '20.000000 PEER')
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addhotquestn', {'user': 'bob', 'question_id': question_id, 'hours': 2}, bob,
                    'Mark question as promoted at 2 hours', contract='token')
        self.assertTrue(compare([{'balance': '2.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '2.000000 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))

        give_ratings(self, bob, 2)      # 4 period 
        self.wait(4)      

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 3 preiod', contract='token')

        example_reward = [{'period': 3, 'reward': '18.000000 PEER'}]    # 16 + 2(promoted)
        print(self.table('periodreward', 'bob', contract='token'))
        self.assertTrue(compare(example_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '2.000000 PEER'}], self.table('accounts', 'frank', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '0.000000 PEER'}], self.table('accounts', 'dan', contract='token'), ignore_excess=True))
        end()

    

def give_tokens(self, user, tokens):
    begin('to give tokens ')
    self.action('issue', {'to': user, 'quantity': tokens, 'memo': "13" },
                    'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)

def give_ratings(self, user, rating):
    begin('to give rating ')
    self.action('chnguserrt', {'user': user, 'rating_change': rating},
                            self.admin, 'Update rating')


if __name__ == '__main__':
    main()