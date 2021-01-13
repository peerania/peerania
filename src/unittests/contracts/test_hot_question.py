import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

class TestTopQuestion(peeranhatest.peeranhaTest):  
    # def test_add_telegram_account(self):
    #     begin('test add telegram account')
    #     alice = self.register_alice_account()

    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     print(self.table('accounts', 'alice', contract='token') )
    #     self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
    #                 'Bob asking question')
    #     question_id = self.table('question', 'allquestions')[0]['id']


    #     self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
    #                 'Bob asking question', contract='token')
    #     print(self.table('accounts', 'alice', contract='token') )
    #     print(self.table('promquestion', 1, contract='token'))

    #     self.wait(5)
    #     self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
    #                 'Bob asking question')
    #     question_id = self.table('question', 'allquestions')[0]['id']

    #     self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
    #                 'Bob asking question', contract='token')
    #     print(self.table('accounts', 'alice', contract='token') )
    #     print(self.table('promquestion', 1, contract='token'))
    #     end()
    
    # def test_add_promoted_question(self):
    #     begin('test add promoted question')
    #     alice = self.register_alice_account()

    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
    #                 'Bob asking question')
    #     question_id = self.table('question', 'allquestions')[0]['id']

    #     self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
    #                 'Bob asking question', contract='token')
    #     print(self.table('accounts', 'alice', contract='token') )
    #     print(self.table('promquestion', 1, contract='token'))

    #     example_promoted_question = [{'question_id': question_id}]
    #     self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
    #     end()
    
    # def test_auto_delete_promoted_question(self):
    #     begin('auto delete promoted question')
    #     alice = self.register_alice_account()

    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
    #                 'Bob asking question')
    #     question_id = self.table('question', 'allquestions')[0]['id']

    #     self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
    #                 'Bob asking question', contract='token')
    #     print(self.table('accounts', 'alice', contract='token') )
    #     print(self.table('promquestion', 1, contract='token'))

    #     example_promoted_question = [{'question_id': question_id}]
    #     self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
    #     self.wait(5)

    #     self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
    #                 'Bob asking question')
    #     question_id = self.table('question', 'allquestions')[0]['id']
    #     self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
    #                 'Bob asking question', contract='token')
    #     example_promoted_question = [{'question_id': question_id}]
    #     self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
    #     end()
    
    def test_add_promoted_question(self):
        begin('test add promoted question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        give_ratings(self, bob, 2)      # 0 period 
        give_ratings(self, alice, 2)
        self.wait(2)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # boost
        self.wait(4)

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 2 period
        self.wait(4)

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Bob asking question', contract='token')
        # print(self.table('accounts', 'alice', contract='token') )
        print(self.table('tokenawards', 'allawards', contract='token'))

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 2 period
        self.wait(4)


        

        # self.wait(4)
        

        give_ratings(self, alice, 2)
        give_ratings(self, bob, 2)      # 2 period
        self.wait(4)



        # example_promoted_question = [{'question_id': question_id}]
        # self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodrating', 'bob'))
        print("--------------")
        print(self.table('periodrating', 'alice'))
        

        self.action('pickupreward', {'user': bob, 'period': 3},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')    

        print(self.table('periodreward', 'bob', contract='token'))

        self.action('pickupreward', {'user': bob, 'period': 5},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')    

        print(self.table('periodreward', 'bob', contract='token'))
        end()


def give_tokens(self, user, tokens):
    begin('to give tokens ')
    self.action('issue', {'to': user, 'quantity': tokens, 'memo': "13" },
                    'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)

def give_ratings(self, user, rating):
    begin('to give rating ')
    self.action('chnguserrt', {'user': user, 'rating_change': rating},
                            self.admin, 'Update alice rating')


if __name__ == '__main__':
    main()