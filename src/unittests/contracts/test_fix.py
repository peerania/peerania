import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6
MODERATOR_FLG_ALL = 31

class TestFix(peeranhatest.peeranhaTest):  
    def test_delete_question(self):
        begin('test delete question')

        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        print('start')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '  aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '  bobRating')

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Register question from alice')

        e = [{
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Register Bob answer to Alice question')
        
        e[0]['answers'].append({'user': 'bob', 'id': '#var aq_ba'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('mrkascorrect', {'user': 'alice', 'question_id': var['aq'],
                                     'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')


        print('mrkascorrect ')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '   bobRating')

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        print('delete question')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '   bobRating')

        end()

    def test_delete_answer(self):
        begin('test delete answer')

        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        print('start')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '  aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '  bobRating')

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Register question from alice')

        e = [{
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Register Bob answer to Alice question')
        
        e[0]['answers'].append({'user': 'bob', 'id': '#var aq_ba'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('mrkascorrect', {'user': 'alice', 'question_id': var['aq'],
                                     'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')


        print('mrkascorrect ')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '   bobRating')

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        print('delete question')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')
        
        bobRating = self.table('account', 'allaccounts')[1]['rating']
        print(str(bobRating) + '   bobRating')

        end()

    def test_delete_question_2(self):
        begin('test delete question 2')

        alice = self.register_alice_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        print('start')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '  aliceRating')

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Register question from alice')

        e = [{
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    alice, 'Register Bob answer to Alice question')
                    
        
        e[0]['answers'].append({'user': 'alice', 'id': '#var aq_ba'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('mrkascorrect', {'user': 'alice', 'question_id': var['aq'],
                                     'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')


        print('mrkascorrect ')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')

        print('delete question')
        aliceRating = self.table('account', 'allaccounts')[0]['rating']
        print(str(aliceRating) + '   aliceRating')

        end()
    

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')


if __name__ == '__main__':
    main()