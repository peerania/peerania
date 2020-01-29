import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

defs = {**load_defines('./src/contracts/peeranha.main/economy.h'),
        **load_defines('./src/contracts/peeranha.main/question_container.hpp')}

class ForumreportforumTests(peeranhatest.peeranhaTest):
    def test_vote_delete_comment(self):
        begin('Test vote for question comment')
        (alice, bob, carol) = self._init_all_accounts()
        account_e = ['#ignoreorder',
                     {'user': 'alice', 'energy': '#var alice_energy',
                      'rating': '#var alice_rating'},
                     {'user': 'bob', 'energy': '#var bob_energy',
                      'rating': '#var bob_rating'},
                     {'user': 'carol', 'energy': '#var carol_energy',
                      'rating': '#var carol_rating'}]
        (e, var) = self._create_basic_hierarchy(alice, bob, carol)
        for key, value in var.items():
            if '_hst' in key or '_prop' in key:
                self.assertTrue(value == [])
        setvar(e, var)
        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa'], 'comment_id': var['aq_aa_bc2']},
                    alice, 'Alice vote for deletion Alice question->Alice answer->Bob comment')
        self.alice_energy -= defs['ENERGY_REPORT_COMMENT']
        find_by_field(
            e, 'ipfs_link', 'AQ->AA->BC2')['history'].append({'user': 'alice', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link', 'AQ->AA->BC2')['properties'].append({'key': defs['PROPERTY_REPORT_POINTS'], 'value': get_moderation_impact(self.alice_rating)})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_energy'] == self.alice_energy)
        info('Now {} has {} energy points'.format(
            alice, self.alice_energy))
        self.action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_aa'], 'comment_id': var['aq_aa_bc2']},
                    carol, 'Carol vote for deletion Alice question->Alice answer->Bob commnet')
        self.carol_energy -= defs['ENERGY_REPORT_COMMENT']
        self.bob_rating += defs['COMMENT_DELETED_REWARD']
        find_by_field(
            e, 'ipfs_link', 'AQ->AA->BC2')['history'].append({'user': 'carol', 'flag': '#ignore'})
        del(find_by_field(e, 'ipfs_link', 'AQ->AA')['comments'][2])
        info('Alice question->Alice answer->Bob commnet now removed by vote')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['carol_energy'] == self.carol_energy)
        info('Now {} has {} energy points'.format(
            carol, self.carol_energy))
        self.action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_cc']},
                    bob, 'Bob vote for deletion Alice question->Carrol comment')
        self.bob_energy -= defs['ENERGY_REPORT_COMMENT']
        find_by_field(
            e, 'ipfs_link',  'AQ->CC')['history'].append({'user': 'bob', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link',  'AQ->CC')['properties'].append({'key': defs['PROPERTY_REPORT_POINTS'], 'value': get_moderation_impact(self.bob_rating)})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['bob_energy'] == self.bob_energy)
        info('Now {} has {} energy points'.format(
            bob, self.bob_energy))
        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_cc']},
                    alice, 'Alice vote for deletion Alice question->Carol comment')
        self.alice_energy -= defs['ENERGY_REPORT_COMMENT']
        self.carol_rating += defs['COMMENT_DELETED_REWARD']
        del(find_by_field(e, 'ipfs_link',  'AQ')['comments'][0])
        info('Alice question->Carol comment now removed by vote')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_energy'] == self.alice_energy)
        info('Now {} has {} energy points'.format(
            alice, self.alice_energy))
        info('Now carol rating is {}'.format(self.carol_energy))
        self.action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_aa'], 'comment_id': var['aq_aa_bc1']},
                    carol, 'Carol vote for deletion Alice question->Alice answer->Bob comment1')
        self.carol_energy -= defs['ENERGY_REPORT_COMMENT']
        self.bob_rating += defs['COMMENT_DELETED_REWARD']
        del(find_by_field(e, 'ipfs_link',  'AQ->AA')['comments'][0])
        info('Alice question->Alice answer->Bob comment1 now removed by vote')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['carol_energy'] == self.carol_energy)
        info('Now {} has {} energy points'.format(
            carol, self.carol_energy))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_rating'] == self.alice_rating)
        self.assertTrue(var['bob_rating'] == self.bob_rating)
        self.assertTrue(var['carol_rating'] == self.carol_rating)
        end()

    def test_vote_delete_answer(self):
        begin('Test vote for answer deletion')
        (alice, bob, carol) = self._init_all_accounts()
        account_e = ['#ignoreorder',
                     {'user': 'alice', 'energy': '#var alice_energy',
                         'rating': '#var alice_rating'},
                     {'user': 'bob', 'energy': '#var bob_energy',
                         'rating': '#var bob_rating'},
                     {'user': 'carol', 'energy': '#var carol_energy', 'rating': '#var carol_rating'}]
        (e, var) = self._create_basic_hierarchy(alice, bob, carol)
        for key, value in var.items():
            if '_hst' in key or '_prop' in key:
                self.assertTrue(value == [])
        setvar(e, var)
        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    alice, 'Alice vote for deletion Alice question->Bob answer')
        self.alice_energy -= defs['ENERGY_REPORT_ANSWER']
        find_by_field(
            e, 'ipfs_link',  'AQ->BA')['history'].append({'user': 'alice', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link',  'AQ->BA')['properties'].append({'key': defs['PROPERTY_REPORT_POINTS'], 'value': get_moderation_impact(self.alice_rating)})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_energy'] == self.alice_energy)
        info('Now {} has {} energy points'.format(
            alice, self.alice_energy))

        self.action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    carol, 'Carol vote for deletion Alice question->Bob answer')
        self.carol_energy -= defs['ENERGY_REPORT_ANSWER']
        self.bob_rating += defs['ANSWER_DELETED_REWARD']
        del(find_by_field(e, 'ipfs_link',  'AQ')['answers'][1])
        info('Alice question->Bob answer now removed by vote')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['carol_energy'] == self.carol_energy)
        info('Now {} has {} energy points'.format(
            carol, self.carol_energy))
        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ca'], 'comment_id': 0},
                    alice, 'Alice vote for deletion Alice question->Carrol answer')
        self.alice_energy -= defs['ENERGY_REPORT_ANSWER']
        find_by_field(
            e, 'ipfs_link',  'AQ->CA')['history'].append({'user': 'alice', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link',  'AQ->CA')['properties'].append({'key': defs['PROPERTY_REPORT_POINTS'], 'value': get_moderation_impact(self.alice_rating)})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_energy'] == self.alice_energy)
        info('Now {} has {} energy points'.format(
            alice, self.alice_energy))
        self.action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ca'], 'comment_id': 0},
                    bob, 'Bob vote for deletion Alice question->Carrol answer')
        self.bob_energy -= defs['ENERGY_REPORT_ANSWER']
        find_by_field(
            e, 'ipfs_link',  'AQ->CA')['history'].append({'user': 'bob', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link',  'AQ->CA')['properties'][0]['value'] += get_moderation_impact(self.bob_rating)
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['bob_energy'] == self.bob_energy)
        info('Now {} has {} energy points'.format(
            bob, self.bob_energy))
        info('Not enought deletion rating to remove carol answer')
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_rating'] == self.alice_rating)
        self.assertTrue(var['bob_rating'] == self.bob_rating)
        self.assertTrue(var['carol_rating'] == self.carol_rating)
        end()

    def test_vote_delete_question(self):
        begin('Test vote for question comment')
        (alice, bob, carol) = self._init_all_accounts()
        account_e = ['#ignoreorder',
                     {'user': 'alice', 'energy': '#var alice_energy',
                         'rating': '#var alice_rating'},
                     {'user': 'bob', 'energy': '#var bob_energy',
                         'rating': '#var bob_rating'},
                     {'user': 'carol', 'energy': '#var carol_energy', 'rating': '#var carol_rating'}]
        (e, var) = self._create_basic_hierarchy(alice, bob, carol)
        for key, value in var.items():
            if '_hst' in key or '_prop' in key:
                self.assertTrue(value == [])
        setvar(e, var)
        self.action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    bob, 'Bob vote for deletion Alice question')
        self.bob_energy -= defs['ENERGY_REPORT_QUESTION']
        find_by_field(
            e, 'ipfs_link',  'AQ')['history'].append({'user': 'bob', 'flag': '#ignore'})
        find_by_field(
            e, 'ipfs_link',  'AQ')['properties'].append({'key': defs['PROPERTY_REPORT_POINTS'], 'value': get_moderation_impact(self.bob_rating)})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['bob_energy'] == self.bob_energy)
        info('Now {} has {} energy points'.format(
            bob, self.bob_energy))
        self.action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    carol, 'Carol vote for deletion Alice question-')
        self.carol_energy -= defs['ENERGY_REPORT_QUESTION']
        del(e[1])
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['carol_energy'] == self.carol_energy)
        info('Now {} has {} energy points'.format(
            carol, self.carol_energy))
        info('Alice question now removed by vote')
        self.alice_rating += defs['QUESTION_DELETED_REWARD']
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), var, ignore_excess=True))
        self.assertTrue(var['alice_rating'] == self.alice_rating)
        self.assertTrue(var['bob_rating'] == self.bob_rating)
        self.assertTrue(var['carol_rating'] == self.carol_rating)
        end()

    def test_vote_delete_answer_marked_as_correct(self):
        begin('Test delte correct answer(check rest correct answer id after action)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account(10000)
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, ignore_excess=True))
        self.assertTrue(var['aq_caid'] == var['aq_ba'])
        self.action('reportforum', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0}, alice, "Alice report bob answer")
        self.action('reportforum', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0}, carol, "Carol report bob answer")
        del(e[0]['answers'][0])
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, ignore_excess=True))
        self.assertTrue(var['aq_caid'] == 0)
        end()

    def test_vote_delete_upvoted_item(self):
        begin('Test upvote question and answer when upvoted')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                    carol, 'Carol upvote alice question')
        self.action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']},
                    carol, 'Carol upvote bob answer')
        self.failed_action('reportforum', {
            'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0}, carol, "Carol attempt to report alice question", 'assert')
        self.failed_action('reportforum', {
            'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0}, carol, "Carol attempt to report bob answer", 'assert')
        end()

    def test_vote_delete_twice_failed(self):
        begin('Test vote for deletion twice', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    bob, 'Bob vote for deletion Alice question')
        self.wait()
        self.failed_action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                           bob, 'Bob attempt to vote for deletion Alice question again', 'assert')

        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                    alice, 'Alice vote for deletion Alice question->Bob answer')
        self.wait()
        self.failed_action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                           alice, 'Alice attempt to vote for deletion  Alice question->Bob answer again', 'assert')

        self.action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_bc']},
                    alice, 'Alice vote for deletion Alice question->Bob comment')
        self.wait()
        self.failed_action('reportforum', {'user': 'alice', 'question_id': var['aq'],  'answer_id': 0, 'comment_id': var['aq_bc']},
                           alice, 'Alice attempt to vote for deletion  Alice question->Bob comment again', 'assert')

        self.action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var['aq_ba_ac']},
                    bob, 'Bob vote for deletion Alice question->Bob answer->Alice comment')
        self.wait()
        self.failed_action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var['aq_ba_ac']},
                           bob, 'Bob attempt to vote for deletion Alice question->Bob answer->Alice comment again', 'assert')
        end()

    def test_vote_from_non_existent_account_failed(self):
        begin('Test vote from non existent account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.get_non_registered_carol()
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                           carol, 'Carol attempt to vote for deletion Alice question', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                           carol, 'Carol attempt to vote for deletion Alice question->Bob answer', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var['aq_ba_ac']},
                           carol, 'Carol attempt to vote for deletion Alice question->Bob answer->Alice comment', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_bc']},
                           carol, 'Carol attempt to vote for deletion Alice question->Bob comment', 'assert')
        end()

    def test_vote_with_another_auth_failed(self):
        begin('Vote with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.failed_action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                           alice, 'Attempt tovote for deletion Alice question with another user auth', 'auth')
        self.failed_action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0},
                           bob, 'Attempt to vote for deletion Alice question->Bob answer with another user auth', 'auth')
        self.failed_action('reportforum', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_bc']},
                           bob, 'Attempt to vote for deletion Alice question->Bob comment with another user auth', 'auth')
        self.failed_action('reportforum', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var['aq_ba_ac']},
                           alice, 'Attempt to vote for deletion Alice question->Bob answer->Alice comment with another user auth', 'auth')
        end()

    def test_vote_non_existent_item(self):
        begin('Vote for non-existent question, answer or comment', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.failed_action('reportforum', {'user': 'carol', 'question_id': int(var['aq']) + 2, 'answer_id': 0, 'comment_id': 0},
                           carol, 'Carol attempt to vote for deletion non-existent question', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'] + 2, 'comment_id': 0},
                           carol, 'Carol attempt to vote for deletion Alice question->non-existent answer', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var['aq_ba_ac'] + 2},
                           carol, 'Carol attempt to vote for deletion Alice question->Bob answer->non-existent comment', 'assert')
        self.failed_action('reportforum', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': var['aq_bc'] + 2},
                           carol, 'Carol attempt to vote for deletion Alice question->non-existent comment', 'assert')
        end()

    def _create_basic_hierarchy(self, alice, bob, carol):
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'BQ', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                    'Register question from bob')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'post_time': '#ignore',
            'properties': '#var aq_prop',
            'history': '#var aq_hst',
            'answers': [],
            'comments': []
        }, {
            'id': '#var bq',
            'user': 'bob',
            'title': 'Title bob question',
            'ipfs_link': 'BQ',
            'post_time': '#ignore',
            'properties': '#var bq_prop',
            'history': '#var bq_hst',
            'answers': [],
            'comments': []
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'AQ->AA'},
                    alice, 'Register Alice answer to Alice')
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': var['aq'], 'ipfs_link': 'AQ->CA'},
                    carol, 'Register Carol answer to Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': var['bq'], 'ipfs_link': 'BQ->CA'},
                    carol, 'Register Carol answer to Bob')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'AQ->AA',
            'post_time': '#ignore',
            'properties': '#var aq_aa_prop',
            'history': '#var aq_aa_hst',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA',
            'post_time': '#ignore',
            'properties': '#var aq_ba_prop',
            'history': '#var aq_ba_hst',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'AQ->CA',
            'post_time': '#ignore',
            'properties': '#var aq_ca_prop',
            'history': '#var aq_ca_hst',
            'comments': []})
        e[2]['answers'].append({
            'id': '#var bq_ca',
            'user': 'carol',
            'ipfs_link': 'BQ->CA',
            'post_time': '#ignore',
            'properties': '#var bq_ca_prop',
            'history': '#var bq_ca_hst',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                    'ipfs_link': 'AQ->AA->BC1'}, bob, 'Register Bob 1 comment to Alice question->Alice answer')
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                    'ipfs_link': 'AQ->AA->AC'}, alice, 'Register Alice comment to Alice question->Alice answer')
        self.action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                    'ipfs_link': 'AQ->AA->BC2'}, bob, 'Register Bob 2 comment to Alice question->Alice answer')
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                    'ipfs_link': 'AQ->BA->AC'}, alice, 'Register Alice comment to Alice question->Bob answer')
        self.action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                    'ipfs_link': 'AQ->BA->BC'}, bob, 'Register Bob comment to Alice question->Bob answer')
        self.action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0,
                                    'ipfs_link': 'AQ->CC'}, carol, 'Register Carol comment to Alice question')
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0,
                                    'ipfs_link': 'AQ->AC'}, alice, 'Register Alice comment to Alice question')
        self.action('postcomment', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'AQ->BC'}, bob, 'Register Bob comment to Alice question')
        self.action('postcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                    'ipfs_link': 'BQ->CA->BC'}, bob, 'Register Bob comment to Bob question->Carol answer')
        self.action('postcomment', {'user': 'alice', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                    'ipfs_link': 'BQ->CA->AC'}, alice, 'Register Alice comment to Bob question->Carol answer')
        self.action('postcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                    'ipfs_link': 'BQ->CA->CC'}, carol, 'Register Carol comment to Bob question->Carol answer')
        self.action('postcomment', {
                    'user': 'carol', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->CC'}, carol, 'Register Carol comment to Bob question')
        self.action('postcomment', {
                    'user': 'alice', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->AC'}, alice, 'Register Alice comment to Bob question')
        self.action('postcomment', {
                    'user': 'bob', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->BC'}, bob, 'Register Bob comment to Bob question')

        e[1]['answers'][0]['comments'].append({'id': '#var aq_aa_bc1', 'post_time': '#ignore',
                                               'user': 'bob', 'ipfs_link': 'AQ->AA->BC1',
                                               'properties': '#var aq_aa_bc1_prop', 'history': '#var aq_aa_bc1_hst'})
        e[1]['answers'][0]['comments'].append({'id': '#var aq_aa_ac', 'post_time': '#ignore',
                                               'user': 'alice', 'ipfs_link': 'AQ->AA->AC',
                                               'properties': '#var aq_aa_ac_prop', 'history': '#var aq_aa_ac_hst'})
        e[1]['answers'][0]['comments'].append({'id': '#var aq_aa_bc2', 'post_time': '#ignore',
                                               'user': 'bob', 'ipfs_link': 'AQ->AA->BC2',
                                               'properties': '#var aq_aa_bc2_prop', 'history': '#var aq_aa_bc2_hst'})
        e[1]['answers'][1]['comments'].append({'id': '#var aq_ba_ac', 'post_time': '#ignore',
                                               'user': 'alice', 'ipfs_link': 'AQ->BA->AC',
                                               'properties': '#var aq_ba_ac_prop', 'history': '#var aq_ba_ac_hst'})
        e[1]['answers'][1]['comments'].append({'id': '#var aq_ba_bc', 'post_time': '#ignore',
                                               'user': 'bob', 'ipfs_link': 'AQ->BA->BC',
                                               'properties': '#var aq_ba_bc_prop', 'history': '#var aq_ba_bc_hst'})
        e[1]['comments'].append({'id': '#var aq_cc', 'post_time': '#ignore',
                                 'user': 'carol', 'ipfs_link': 'AQ->CC',
                                 'properties': '#var aq_cc_prop', 'history': '#var aq_cc_hst'})
        e[1]['comments'].append({'id': '#var aq_ac', 'post_time': '#ignore',
                                 'user': 'alice', 'ipfs_link': 'AQ->AC',
                                 'properties': '#var aq_ac_prop', 'history': '#var aq_ac_hst'})
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'AQ->BC',
                                 'properties': '#var aq_bc_prop', 'history': '#var aq_bc_hst'})
        e[2]['answers'][0]['comments'].append({'id': '#var bq_ca_bc', 'post_time': '#ignore',
                                               'user': 'bob', 'ipfs_link': 'BQ->CA->BC',
                                               'properties': '#var bq_ca_bc_prop', 'history': '#var bq_ca_bc_hst'})
        e[2]['answers'][0]['comments'].append({'id': '#var bq_ca_ac', 'post_time': '#ignore',
                                               'user': 'alice', 'ipfs_link': 'BQ->CA->AC',
                                               'properties': '#var bq_ca_ac_prop', 'history': '#var bq_ca_ac_hst'})
        e[2]['answers'][0]['comments'].append({'id': '#var bq_ca_cc', 'post_time': '#ignore',
                                               'user': 'carol', 'ipfs_link': 'BQ->CA->CC',
                                               'properties': '#var bq_ca_ac_prop', 'history': '#var bq_ca_ac_hst'})
        e[2]['comments'].append({'id': '#var bq_cc', 'post_time': '#ignore',
                                 'user': 'carol', 'ipfs_link': 'BQ->CC',
                                 'properties': '#var bq_cc_prop', 'history': '#var bq_cc_hst'})
        e[2]['comments'].append({'id': '#var bq_ac', 'post_time': '#ignore',
                                 'user': 'alice', 'ipfs_link': 'BQ->AC',
                                 'properties': '#var bq_ac_prop', 'history': '#var bq_ac_hst'})
        e[2]['comments'].append({'id': '#var bq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'BQ->BC',
                                 'properties': '#var bq_bc_prop', 'history': '#var bq_bc_hst'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('\nnow hierarchy look like')
        info('Alice question')
        info('  |-->Alice answer to herself')
        info('  |   |-->Bob comment')
        info('  |   |-->Alice comment')
        info('  |    `->Bob comment')
        info('  |-->Bob answer to Alice')
        info('  |   |-->Alice comment')
        info('  |    `->Bob comment')
        info('  |-->Carol answer to Alice')
        info('  |')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        info('\nBob question')
        info('  |-->Carol answer to Bob')
        info('  |   |-->Bob comment')
        info('  |   |-->Alice comment')
        info('  |    `->Carol comment')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        self.alice_energy -= defs['ENERGY_POST_QUESTION'] + \
            defs['ENERGY_POST_ANSWER'] + \
            5 * defs['ENERGY_POST_COMMENT']
        self.bob_energy -= defs['ENERGY_POST_QUESTION'] + \
            defs['ENERGY_POST_ANSWER'] + \
            6 * defs['ENERGY_POST_COMMENT']
        self.carol_energy -= 2 * defs['ENERGY_POST_ANSWER'] + \
            3 * defs['ENERGY_POST_COMMENT']
        return (e, var)

    def _create_simple_hierarchy(self, alice, bob):
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice')
        e = [{
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ',
            'properties': '#var aq_prop',
            'history': '#var aq_hst',
            'correct_answer_id': '#var aq_caid',
            'answers': [],
            'comments': []}]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice')
        e[0]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA',
            'properties': '#var aq_ba_prop',
            'history': '#var aq_ba_hst',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                    'ipfs_link': 'AQ->BA->AC'}, alice, 'Register Alice comment to Alice question->Bob answer')
        self.action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0,
                                    'ipfs_link': 'AQ->BC'}, bob, 'Register Bob comment to Alice question')
        e[0]['comments'].append({'id': '#var aq_bc', 'user': 'bob', 'ipfs_link': 'AQ->BC',
                                 'properties': '#var aq_bc_prop', 'history': '#var aq_bc_hst'})
        e[0]['answers'][0]['comments'].append({'id': '#var aq_ba_ac', 'user': 'alice', 'ipfs_link': 'AQ->BA->AC',
                                               'properties': '#var aq_ba_ac_prop', 'history': '#var aq_ba_ac_hst'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('Hierarchy look like')
        info('Alice question')
        info('  |-->Bob answer')
        info('  |     `->Alice comment')
        info('   `->Comments')
        info('        `->Bob comment')
        return (e, var)

    def _init_all_accounts(self):
        self.init_account_call = True
        self.alice_rating = 500
        self.bob_rating = 1000
        self.carol_rating = 7000
        self.alice_energy = 70
        self.bob_energy = 70
        self.carol_energy = 70

        alice = self.register_alice_account(
            self.alice_rating, self.alice_energy)
        bob = self.register_bob_account(
            self.bob_rating, self.bob_energy)
        carol = self.register_carol_account(
            self.carol_rating, self.carol_energy)
        return (alice, bob, carol)


if __name__ == '__main__':
    main()
