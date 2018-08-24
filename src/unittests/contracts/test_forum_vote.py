import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class ForumVoteTests(peeraniatest.PeeraniaTest):
    def test_vote_question(self):
        begin('Test vote question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_rating')
        self.action('upvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': 0}, alice, 'Alice upvote for Alice question')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol upvote for Alice question')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 2)
        info('Now Alice question rating is 2')
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': 0}, alice, 'Alice downvote for Alice question')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol downvote for Alice question')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == -2)
        info('Now Alice question rating is -2')

    def test_vote_answer(self):
        begin('Test vote answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_ba_rating')
        self.action('upvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice upvote for Alice question->Bob answer rating')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol upvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 2)
        info('Now Alice question->Bob answer rating is 2')
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol downvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == -2)
        info('Now Alice question->Bob answer rating is -2')

    def test_remove_vote_answer(self):
        begin('Test remove vote answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_ba_rating')
        self.action('upvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice upvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 1)
        info('Now Alice question->Bob answer rating is 1')
        self.wait()
        self.action('upvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']},
                    alice, 'Alice remove upvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == -1)
        info('Now Alice question->Bob answer rating is -1')
        self.wait()
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')

    def test_remove_vote_question(self):
        begin('Test remove vote question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_rating')
        self.action('upvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob upvote for Alice question rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 1)
        info('Now Alice question rating is 1')
        self.wait()
        self.action('upvote', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0},
                    bob, 'Bob remove upvote for Alice question rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')
        self.action('downvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob downvote for Alice question rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == -1)
        info('Now Alice question rating is -1')
        self.wait()
        self.action('downvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob downvote for Alice question rating')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')

    def test_mark_answer_as_correct(self):
        begin('Test mark answer as correct')
        begin('Test vote answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        setvar(e, var, 'caid')
        for key, value in var.items():
            if 'caid' in key:
                self.assertTrue(value == 0)
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == var['aq_ba'])
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa']}, alice, 'Alice mark herself answer as correct')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == var['aq_aa'])
        self.wait()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa']}, alice, 'Alice unmark herself answer as correct')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == 0)
        end()

    def test_vote_from_non_existent_account_failed(self):
        begin('Vote from non-regidtered account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.get_non_registered_carol()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                           carol, 'Attempt to upvote question from non-existent account', 'assert')
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                           carol, 'Attempt to downvote question from non-existent account', 'assert')
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, carol, 'Attempt to upvote answer from non-existent account', 'assert')
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, carol, 'Attempt to downvote answer from non-existent account', 'assert')
        end()

    def test_vote_with_another_auth_failed(self):
        begin('Vote with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                           alice, 'Attempt to upvote question from non-existent account', 'auth')
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                           alice, 'Attempt to downvote question from non-existent account', 'auth')
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, alice, 'Attempt to upvote answer from non-existent account', 'auth')
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, alice, 'Attempt to downvote answer from non-existent account', 'auth')
        end()

    def test_mark_answer_as_correct_for_question_of_another_owner_failed(self):
        begin('Mark answer as correct for question of another owner', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('mrkascorrect', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, bob, 'Bob attempt to mark bob answer as correct for Alice question', 'assert')
        end()

    def test_mark_answer_as_correct_another_auth(self):
        begin('Mark answer as correct for question with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, bob, 'Attempt to mark bob answer as correct for Alice question with bob auth', 'auth')
        end()

    def test_vote_non_existent_item(self):
        begin('Vote for non-existent question or answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('upvote', {'user': 'alice', 'question_id': var['aq'] + 5, 'answer_id': 0},
                           alice, 'Attempt to upvote non-existent  question', 'assert')
        self.failed_action('downvote', {'user': 'alice', 'question_id': var['aq'] + 5, 'answer_id': 0},
                           alice, 'Attempt to downvote non-existent  question', 'assert')
        self.failed_action('upvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba'] + 5}, alice, 'Attempt to upvote non-existent answer', 'assert')
        self.failed_action('downvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba'] + 5}, alice, 'Attempt to downvote non-existent answer', 'assert')
        end()

    def test_mark_non_existent_answer_as_correct(self):
        begin('Mark non-existent answer as correct', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'] + 10}, alice, 'Attempt to mark non-existent answer as correct', 'assert')
        end()

    def _create_basic_hierarchy(self, alice, bob):
        self.action('postquestion', {'user': 'alice', 'ipfs_link': 'Alice question'}, alice,
                    'Asking question from alice with text "Alice question"')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
                    'ipfs_link': 'Alice question',
                    'post_time': '#ignore',
                    'answers': [],
                    'comments': [],
                    'correct_answer_id':'#var aq_caid',
                    'rating':'#var aq_rating'
        }]

        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself'},
                    alice, ' |-->Answer to alice from alice: "Alice answer to herself"')
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'Bob answer to alice'},
                    bob, '  `->Answer to alice from bob: "Bob answer to alice"')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself',
            'post_time': '#ignore',
            'rating': '#var aq_aa_rating',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'Bob answer to alice',
            'post_time': '#ignore',
            'rating': '#var aq_ba_rating',
            'comments': []})
        self.action('postquestion', {'user': 'bob', 'ipfs_link': 'Bob question'}, bob,
                    'Asking question from bob with text "Bob question"')
        e.append({
            'id': '#var bq',
            'user': 'bob',
            'ipfs_link': 'Bob question',
            'post_time': '#ignore',
            'answers': [],
            'comments': [],
            'correct_answer_id': '#var bq_caid',
            'rating': '#var bq_rating'
        })
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['bq'], 'ipfs_link': 'Alice answer to bob'},
                    alice, '  `->Answer to bob from alice: "Alice answer to bob"')
        e[2]['answers'].append({
            'id': '#var bq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to bob',
            'post_time': '#ignore',
            'rating': '#var bq_aa_rating',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        return e, var

if __name__ == '__main__':
    main()
