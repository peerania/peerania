
import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class ForumGlobalTests(peeraniatest.PeeraniaTest):
    def test_forum_global(self):
        begin('This is a large positive test that verifies the correctness of the contract algorithms.')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self.action('regquestion', {'user': 'alice', 'ipfs_link': 'Alice question'}, alice,
                    'Register question from alice')
        self.action('regquestion', {'user': 'bob', 'ipfs_link': 'Bob question'}, bob,
                    'Register question from bob')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
            'ipfs_link': 'Alice question',
            'registration_time': '#ignore',
            'answers': [],
            'comments': []
        }, {
            'id': '#var bq',
            'user': 'bob',
            'ipfs_link': 'Bob question',
            'registration_time': '#ignore',
            'answers': [],
            'comments': []
        }]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))

        self.action('reganswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself'},
                    alice, 'Register Alice answer to Alice')
        self.action('reganswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'Bob answer to Alice'},
                    bob, 'Register Bob answer to Alice')
        self.action('reganswer', {'user': 'carol', 'question_id': var['aq'], 'ipfs_link': 'Carol answer to Alice'},
                    carol, 'Register Carol answer to Alice')
        self.action('reganswer', {'user': 'carol', 'question_id': var['bq'], 'ipfs_link': 'Carol answer to Bob'},
                    carol, 'Register Carol answer to Bob')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself',
            'registration_time': '#ignore',
            "comments": []})
        e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'Bob answer to Alice',
            'registration_time': '#ignore',
            "comments": []})
        e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'Carol answer to Alice',
            'registration_time': '#ignore',
            "comments": []})
        e[2]['answers'].append({
            'id': '#var bq_ca',
            'user': 'carol',
            'ipfs_link': 'Carol answer to Bob',
            'registration_time': '#ignore',
            "comments": []})
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
        self.action('regcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                   'ipfs_link': 'AQ->AA->BC1'}, bob, 'Register Bob 1 comment to Alice question->Alice answer')
        self.action('regcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                   'ipfs_link': 'AQ->AA->AC'}, alice, 'Register Alice comment to Alice question->Alice answer')
        self.action('regcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                   'ipfs_link': 'AQ->AA->BC2'}, bob, 'Register Bob 2 comment to Alice question->Alice answer')
        self.action('regcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                   'ipfs_link': 'AQ->BA->AC'}, alice, 'Register Alice comment to Alice question->Bob answer')
        self.action('regcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                                   'ipfs_link': 'AQ->BA->BC'}, bob, 'Register Bob comment to Alice question->Bob answer')
        self.action('regcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0,
                                   'ipfs_link': 'AQ->CC'}, carol, 'Register Carol comment to Alice question')
        self.action('regcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0,
                                   'ipfs_link': 'AQ->AC'}, alice, 'Register Alice comment to Alice question')
        self.action('regcomment', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'AQ->BC'}, bob, 'Register Bob comment to Alice question')
        self.action('regcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'ipfs_link': 'BQ->CA->BC'}, bob, 'Register Bob comment to Bob question->Carol answer')
        self.action('regcomment', {'user': 'alice', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'ipfs_link': 'BQ->CA->AC'}, alice, 'Register Alice comment to Bob question->Carol answer')
        self.action('regcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'ipfs_link': 'BQ->CA->CC'}, carol, 'Register Carol comment to Bob question->Carol answer')
        self.action('regcomment', {
                    'user': 'carol', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->CC'}, carol, 'Register Carol comment to Bob question')
        self.action('regcomment', {
                    'user': 'alice', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->AC'}, alice, 'Register Alice comment to Bob question')
        self.action('regcomment', {
                    'user': 'bob', 'question_id': var['bq'], 'answer_id': 0, 'ipfs_link': 'BQ->BC'}, bob, 'Register Bob comment to Bob question')

        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc1', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->AA->BC1'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_ac', 'registration_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->AA->AC'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc2', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->AA->BC2'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_ac', 'registration_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->BA->AC'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_bc', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->BA->BC'})
        e[1]['comments'].append(
            {'id': '#var aq_cc', 'registration_time': '#ignore', 'user': 'carol', 'ipfs_link': 'AQ->CC'})
        e[1]['comments'].append(
            {'id': '#var aq_ac', 'registration_time': '#ignore', 'user': 'alice', 'ipfs_link': 'AQ->AC'})
        e[1]['comments'].append(
            {'id': '#var aq_bc', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'AQ->BC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_bc', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->CA->BC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_ac', 'registration_time': '#ignore', 'user': 'alice', 'ipfs_link': 'BQ->CA->AC'})
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_cc', 'registration_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CA->CC'})
        e[2]['comments'].append(
            {'id': '#var bq_cc', 'registration_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CC'})
        e[2]['comments'].append(
            {'id': '#var bq_ac', 'registration_time': '#ignore', 'user': 'alice', 'ipfs_link': 'BQ->AC'})
        e[2]['comments'].append(
            {'id': '#var bq_bc', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->BC'})
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
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
                    'user': 'bob', 'question_id': var['bq'], 'answer_id': 0, 'comment_id': var['bq_bc'],'ipfs_link': 'BQ->BC updated'}, bob, 'Update Bob comment to Bob question')
        e[1]['answers'][1]['comments'][1]['ipfs_link'] = 'AQ->BA->BC updated'
        e[2]['comments'][2]['ipfs_link'] = 'BQ->BC updated'
        self.action('delcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'comment_id': var['bq_ca_bc']}, bob, 'Delete Bob comment to Bob question->Carol answer')
        self.action('delcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'comment_id': var['bq_ca_cc']}, carol, 'Delete Carol comment to Bob question->Carol answer')
        del e[2]['answers'][0]['comments'][2]
        del e[2]['answers'][0]['comments'][0]
        self.action('regcomment', {'user': 'bob', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                                   'ipfs_link': 'BQ->CA->BC new'}, bob, 'Register new Bob comment to Bob question->Carol answer')
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_bc', 'registration_time': '#ignore', 'user': 'bob', 'ipfs_link': 'BQ->CA->BC new'})
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
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
        
        self.action('regcomment', {'user': 'carol', 'question_id': var['bq'], 'answer_id': var['bq_ca'],
                            'ipfs_link': 'BQ->CA->CC new'}, carol, 'Register Carol comment to Bob question->Carol answer')
        e[2]['answers'][0]['comments'].append(
            {'id': '#var bq_ca_cc', 'registration_time': '#ignore', 'user': 'carol', 'ipfs_link': 'BQ->CA->CC new'})
        self.action('delanswer', {'user':'alice', 'question_id':var['aq'], 'answer_id':var['aq_aa']}, alice, 'Delete Alice answer to Alice(cascade operation)')
        self.action('delanswer', {'user':'carol', 'question_id':var['aq'], 'answer_id':var['aq_ca']}, carol, 'Delete Carol answer to Alice(cascade operation)')
        del e[1]['answers'][2]
        del e[1]['answers'][0]
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
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
        self.action('reganswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself new'},
                    alice, 'Register Alice answer to Alice')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself new',
            'registration_time': '#ignore',
            "comments": []})
        self.action('delquestion', {'user':'bob', 'question_id':var['bq']}, bob, 'Delete bob question(cascade operation)')
        del e[2]
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
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
        self.action('regcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_aa'],
                                   'ipfs_link': 'AQ->AA->CC'}, carol, 'Register Carol comment to Alice question->Alice answer')
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_aa_cc', 'registration_time': '#ignore', 'user': 'carol', 'ipfs_link': 'AQ->AA->CC'})

        self.action('modanswer', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'],
                            'ipfs_link': 'AQ->BA updated'}, bob, 'Update Bob answer to Alice question')
        e[1]['answers'][0]['ipfs_link'] = 'AQ->BA updated'
        t = self.table("question", "allquestions")
        self.assertTrue(compare(e, t, var))
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

        
if __name__ == "__main__":
    main()
