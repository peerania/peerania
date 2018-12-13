import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main

class UserQuestionsAndAnswersTablesTests(peeraniatest.PeeraniaTest):

    def test_delete_own_item(self):
        begin('Test user questions and answers tables when delete own item')
        (alice, bob, e, var) = self._create_simple_hierarchy()
        self.action('delanswer', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, bob, 'Bob delete own answer')
        self.assertTrue(compare([], self.table('usranswers', bob)))
        self.action('delanswer', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa']}, alice, 'Alice delete own answer')
        self.assertTrue(compare([], self.table('usranswers', alice)))
        self.action('delquestion', {'user': 'alice', 'question_id': var['aq']}, alice, 'Alice delete own question')
        self.assertTrue(compare([], self.table('usrquestions', alice)))
        end()
    
    def test_delete_question_by_vote(self):
        begin('Test user questions and answers tables when question deleted by vote')
        carol = self.register_carol_account(30000, 10)
        (alice, bob, e, var) = self._create_simple_hierarchy()
        self.action('votedelete', {'user': carol, 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0}, carol, 'Carol delete alice question')
        self.assertTrue(compare([], self.table('usranswers', bob)))
        self.assertTrue(compare([], self.table('usranswers', alice)))
        self.assertTrue(compare([], self.table('usrquestions', alice)))
        end()

    def test_delete_answer_by_vote(self):
        begin('Test user answers tables when answer deleted by vote')
        carol = self.register_carol_account(30000, 10)
        (alice, bob, e, var) = self._create_simple_hierarchy()
        self.action('votedelete', {'user': carol, 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0}, carol, 'Carol delete bob answer')
        self.assertTrue(compare([], self.table('usranswers', bob)))
        self.action('votedelete', {'user': carol, 'question_id': var['aq'], 'answer_id': var['aq_aa'], 'comment_id': 0}, carol, 'Carol delete alice answer')
        self.assertTrue(compare([], self.table('usranswers', alice)))
        end()

    def _create_simple_hierarchy(self):
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags':[1]}, alice,
                    'Register question from alice')
        e = [{'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        } ]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(compare([{'question_id': var['aq']}], self.table('usrquestions', alice)))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'AQ->AA'},
                    alice, 'Register Alice answer to Alice')
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice')
        e[0]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'AQ->AA'})
        e[0]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(compare([{'question_id': var['aq'], 'answer_id': var['aq_aa']}], self.table('usranswers', alice)))
        self.assertTrue(compare([{'question_id': var['aq'], 'answer_id': var['aq_ba']}], self.table('usranswers', bob)))
        info('Hierarchy look like')
        info('Alice question')
        info(' |-->Alice answer')
        info('  `->Bob answer')
        return alice, bob, e, var


if __name__ == '__main__':
    main()
