import peeraniatest
import requests
from termcolor import cprint
from peeraniatest import *
from jsonutils import *
from unittest import main
from random import randint
from time import sleep


class FrumStatusLimitsTests(peeraniatest.PeeraniaTest):

    def test_moderation_point_and_question_limit_timer(self):
        begin('Test question limit and moderation poit restore')
        alice = self.register_alice_account(499,0)
        info('Wait untill period ends')
        sleep(3)
        info('All stats restored')
        var = {}
        e = [{'owner': 'alice', 'moderation_points': '#var alice_mdp'}]
        self._test_question_limit(alice, 499, 5)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.assertTrue(var['alice_mdp'] == 1)
        self.action('setaccrtmpc', {'user': alice, 'rating': 999, 'moderation_points': 0}, alice, 'Took all moderation points, give 999 rating')
        info('Wait until period ends')
        sleep(3)
        info('All stats restored')
        self._test_question_limit(alice, 999, 6)
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.assertTrue(var['alice_mdp'] == 5)


        info('Wait til period ends')
        sleep(3)


    def test_comment_to_question_limit_failed_st1(self):
        self._test_comment_to_question_limit_failed(99, 2)

    def test_comment_to_question_limit_failed_st2(self):
        self._test_comment_to_question_limit_failed(499, 3)
    
    def test_comment_to_own_answer_limit_st1(self):
        self._test_comment_to_own_answer_limit(99, 2)

    def test_comment_to_own_answer_limit_st2(self):
        self._test_comment_to_own_answer_limit(499, 3)

    def test_comment_inside_own_question_limit_st1(self):
        self._test_comment_inside_own_question_limit(99, 2)

    def test_comment_inside_own_question_limit_st2(self):
        self._test_comment_inside_own_question_limit(499, 3)

    def _test_comment_to_question_limit_failed(self, user_rating, comment_count):
        begin('The queston has answer, answer owner has limit to comment question', True)
        (_, carol, _, var) = self._create_simple_hierarchy(user_rating)
        for i in range(comment_count):
            self.action('postcomment', {'user': carol, 'question_id': var['aq'], 'answer_id': 0,
                                        'ipfs_link': f'AQ-CA({i})'}, carol, f'Register carol comment to alice question{i}')
        self.failed_action('postcomment', {'user': carol, 'question_id': var['aq'], 'answer_id': 0,
                                           'ipfs_link': 'AQ-CC'}, carol, 'Register carol comment to alice question(limit reached)')
        end()

    def _test_comment_to_own_answer_limit(self, user_rating, comment_count):
        begin('Test comment to own answer no limit')
        (alice, carol, bob, var) = self._create_simple_hierarchy(user_rating)
        for i in range(comment_count + 1):
            self.action('postcomment', {'user': carol, 'question_id': var['aq'], 'answer_id': var['aq_ca'],
                                        'ipfs_link': f'AQ-CA({i})'}, carol, f'Register carol comment to own answer({i})')
        end()

    def _test_comment_inside_own_question_limit(self, user_rating, comment_count):
        begin('Test comment inside own question has no limit')
        (alice, carol, bob, var) = self._create_simple_hierarchy(user_rating)
        for i in range(comment_count + 1):
            self.action('postcomment', {'user': alice, 'question_id': var['aq'], 'answer_id': 0,
                                        'ipfs_link': f'AQ-AC({i})'}, alice, f'Register alice comment to own question({i})')
        for i in range(comment_count + 1):
            self.action('postcomment', {'user': alice, 'question_id': var['aq'], 'answer_id': var['aq_ca'],
                                        'ipfs_link': f'AQ-AA({i})'}, alice, f'Register alice comment to carolanswer answer, but own question({i})')
        end()

    def _test_question_limit(self, user, user_rating, question_count):
        for i in range(question_count):
            self.action('postquestion', {'user': user, 'title': 'Hey you' + str(
                i), 'ipfs_link': 'IPFS ' + str(i)}, user, 'Reg question ' + str(i))
        self.failed_action('postquestion', {'user': user, 'title': 'Hey you',
                                            'ipfs_link': 'IPFS '}, user, 'Reg alice question, after limit reached', 'assert')
        end()
 
    def _create_simple_hierarchy(self, user_rating):
        alice = self.register_alice_account(user_rating, 0)
        bob = self.register_bob_account(user_rating, 0)
        carol = self.register_carol_account(user_rating, 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
                    'Register question from alice')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'BQ'}, bob,
                    'Register question from bob')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'answers': [],
            'comments': []
        }, {
            'id': '#var bq',
            'user': 'bob',
            'title': 'Title bob question',
            'ipfs_link': 'BQ',
            'answers': [],
            'comments': []
        }, ]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'carol', 'question_id': var['aq'], 'ipfs_link': 'AQ->CA'},
                    carol, 'Register Carol answer to Alice')
        self.action('postanswer', {'user': 'alice', 'question_id': var['bq'], 'ipfs_link': 'BQ->AA'},
                    alice, 'Register Alice answer to Bob')
        e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'AQ->CA',
            'comments': []})
        e[2]['answers'].append({
            'id': '#var bq_aa',
            'user': 'alice',
            'ipfs_link': 'BQ->AA',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('Hierarchy look like')
        info('Alice question')
        info('  `-->Carol answer')
        info('Bob question')
        info('  `-->Alice answer')
        return (alice, carol, bob, var)


if __name__ == '__main__':
    main()
