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
    
    def test_add_promoted_question(self):
        begin('test add promoted question')
        alice = self.register_alice_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Bob asking question', contract='token')
        print(self.table('accounts', 'alice', contract='token') )
        print(self.table('promquestion', 1, contract='token'))

        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        end()
    
    def test_auto_delete_promoted_question(self):
        begin('auto delete promoted question')
        alice = self.register_alice_account()

        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Bob asking question', contract='token')
        print(self.table('accounts', 'alice', contract='token') )
        print(self.table('promquestion', 1, contract='token'))

        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        self.wait(5)

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Bob asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addhotquestn', {'user': 'alice', 'question_id': question_id, 'hours': 1}, alice,
                    'Bob asking question', contract='token')
        example_promoted_question = [{'question_id': question_id}]
        self.assertTrue(compare(example_promoted_question, self.table('promquestion', 1, contract='token'), ignore_excess=True))
        end()


def give_tokens(self, user, tokens):
    begin('to give tokens ')
    self.action('issue', {'to': user, 'quantity': tokens, 'memo': "13" },
                    'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)


if __name__ == '__main__':
    main()