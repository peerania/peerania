import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main


class ForumGlobalTests(peeranhatest.peeranhaTest):
    def test_forum_global(self):
        begin('This is a large positive test that verifies the correctness of the contract algorithms.')
        alice = self.register_alice_account()
        bob = self.register_bob_account(100, 100)
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question','ipfs_link': 'Alice question',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question','ipfs_link': 'Bob question',  'community_id': 1, 'tags': [1], 'type': 0}, bob,
                    'Register question from bob')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'Alice question',
            'post_time': '#ignore',
            'answers': [],
            'comments': []
        }, {
            'id': '#var bq',
            'user': 'bob',
            'title': 'Title bob question',
            'ipfs_link': 'Bob question',
            'post_time': '#ignore',
            'answers': [],
            'comments': []
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself'},
                    alice, 'Register Alice answer to Alice')
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'Bob answer to Alice'},
                    bob, 'Register Bob answer to Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': var['aq'], 'ipfs_link': 'Carol answer to Alice'},
                    carol, 'Register Carol answer to Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': var['bq'], 'ipfs_link': 'Carol answer to Bob'},
                    carol, 'Register Carol answer to Bob')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself',
            'post_time': '#ignore',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'Bob answer to Alice',
            'post_time': '#ignore',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'Carol answer to Alice',
            'post_time': '#ignore',
            'comments': []})
        e[2]['answers'].append({
            'id': '#var bq_ca',
            'user': 'carol',
            'ipfs_link': 'Carol answer to Bob',
            'post_time': '#ignore',
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

        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc1', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->AA->BC1'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->AA->AC'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc2', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->AA->BC2'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->BA->AC'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->BA->BC'})
        e[1]['comments'].append(
            {'id': '#var aq_cc', 'post_time': '#ignore', 'user': 'carol', 'ipfs_link': 'AQ->CC'})
        e[1]['comments'].append(
            {'id': '#var aq_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->AC'})
        e[1]['comments'].append(
            {'id': '#var aq_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->BC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->CA->BC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'BQ->CA->AC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_cc', 'post_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CA->CC'})
        e[2]['comments'].append(
            {'id': '#var bq_cc', 'post_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CC'})
        e[2]['comments'].append(
            {'id': '#var bq_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'BQ->AC'})
        e[2]['comments'].append(
            {'id': '#var bq_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->BC'})
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
        self.action('modcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': var[
                    'aq_ba_bc'], 'ipfs_link': 'AQ->BA->BC updated'}, bob, 'Update Bob comment to Alice question->Bob answer')
        self.action('modcomment', {
                    'user': 'bob', 'question_id': var['bq'], 'answer_id': 0, 'comment_id': var['bq_bc'], 'ipfs_link': 'BQ->BC updated'}, bob, 'Update Bob comment to Bob question')
        e[1]['answers'][1]['comments'][1]['ipfs_link'] = 'AQ->BA->BC updated'
        e[2]['comments'][2]['ipfs_link'] = 'BQ->BC updated'
        self.action('delcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'comment_id': var['bq_ca_bc']}, bob, 'Delete Bob comment to Bob question->Carol answer')
        self.action('delcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'comment_id': var['bq_ca_cc']}, carol, 'Delete Carol comment to Bob question->Carol answer')
        del e[2]['answers'][0]['comments'][2]
        del e[2]['answers'][0]['comments'][0]
        self.action('postcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                    'ipfs_link': 'BQ->CA->BC new'}, bob, 'Register new Bob comment to Bob question->Carol answer')
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->CA->BC new'})
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
        info('  |    `->Bob comment(updated)')
        info('  |-->Carol answer to Alice')
        info('  |')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        info('\nBob question')
        info('  |-->Carol answer to Bob')
        info('  |    |-->Alice comment')
        info('  |     `->Bob comment(new)')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment(updated)')
        self.action('delcomment', {'user': 'alice', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'comment_id': var['bq_ca_ac']}, alice, 'Dlete Alice comment to Bob question->Carol answer')
        del e[2]['answers'][0]['comments'][0]

        self.action('postcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                    'ipfs_link': 'BQ->CA->CC new'}, carol, 'Register Carol comment to Bob question->Carol answer')
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_cc', 'post_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CA->CC new'})
        self.action('delanswer', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa']}, alice, 'Delete Alice answer to Alice(cascade operation)')
        self.action('delanswer', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ca']}, carol, 'Delete Carol answer to Alice(cascade operation)')
        del e[1]['answers'][2]
        del e[1]['answers'][0]
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('\nnow hierarchy look like')
        info('Alice question')
        info('  |-->Bob answer to Alice')
        info('  |   |-->Alice comment')
        info('  |    `->Bob comment')
        info('  |')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        info('\nBob question')
        info('  |-->Carol answer to Bob')
        info('  |    |-->Bob comment')
        info('  |     `->Carol comment(new)')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself new'},
                    alice, 'Register Alice answer to Alice')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself new',
            'post_time': '#ignore',
            'comments': []})
        self.action('delanswer', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca']},
                    carol, 'Delete carol answer(only questions without answer could be deleted)')
        self.action('delquestion', {
                    'user': 'bob', 'question_id': var['bq']}, bob, 'Delete bob question(cascade operation)')
        del e[2]
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('\nnow hierarchy look like')
        info('Alice question')
        info('  |-->Bob answer to Alice')
        info('  |   |-->Alice comment')
        info('  |    `->Bob comment')
        info('  |-->Alice answer to Alice(new)')
        info('  |')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        self.action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                    'ipfs_link': 'AQ->AA->CC'}, carol, 'Register Carol comment to Alice question->Alice answer')
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_aa_cc', 'post_time': '#ignore', 'user': 'carol', 'ipfs_link': 'AQ->AA->CC'})
        self.action('modanswer', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                  'ipfs_link': 'AQ->BA updated'}, bob, 'Update Bob answer to Alice question')
        e[1]['answers'][0]['ipfs_link'] = 'AQ->BA updated'
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('\nnow hierarchy look like')
        info('Alice question')
        info('  |-->Bob answer to Alice(updated)')
        info('  |   |-->Alice comment')
        info('  |    `->Bob comment')
        info('  |-->Alice answer to Alice')
        info('  |    `->Carol comment(new)')
        info('  |')
        info('   `->Comments')
        info('      |-->Carol comment')
        info('      |-->Alice comment')
        info('       `->Bob comment')
        end()

    def test_delete_question_with_answer_failed(self):
        begin('Delete own question with answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
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
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'title': 'Title bob question','ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice question')
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': var['aq']}, alice, 'Attempt to delete Alice question', 'assert')
        end()

    def test_delete_answer_marked_as_correct_failed(self):
        begin('Delete own answer marked as correct', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
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
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice question')
        e[0]['answers'].append({'user': 'bob', 'id': '#var aq_ba'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('mrkascorrect', {'user': 'alice', 'question_id': var['aq'],
                                     'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')
        self.failed_action('delanswer', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba']},
                           bob, 'Bob attempt to delete his answer to Alice question', 'assert')
        end()


if __name__ == '__main__':
    main()
