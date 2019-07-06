import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main

economy = load_defines('./src/contracts/peerania/economy.h')

class ForumVoteTests(peeraniatest.PeeraniaTest):
    def test_vote_question(self):
        begin('Test vote question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        account_e = [
            '#ignoreorder',
            get_expected_account_body(alice),
            get_expected_account_body(bob),
            get_expected_account_body(carol)
        ]
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_rating')
        self.action('upvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob upvote Alice question')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol upvote Alice question')
        account_e[1]['energy'] -= self.alice_energy_reduce
        account_e[2]['energy'] -= self.bob_energy_reduce + economy['ENERGY_UPVOTE_QUESTION']
        account_e[3]['energy'] -= economy['ENERGY_UPVOTE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 2)
        info('Now Alice question rating is 2')
        self.action('downvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob downvote Alice question')
        account_e[2]['energy'] -= economy['ENERGY_DOWNVOTE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol downvote Alice question')
        account_e[3]['energy'] -= economy['ENERGY_DOWNVOTE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == -2)
        info('Now Alice question rating is -2')
        end()

    def test_vote_answer(self):
        begin('Test vote answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        account_e = [
            '#ignoreorder',
            get_expected_account_body(alice),
            get_expected_account_body(bob),
            get_expected_account_body(carol)
        ]
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_ba_rating')
        self.action('upvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice upvote for Alice question->Bob answer rating')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol upvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -= self.alice_energy_reduce + economy['ENERGY_UPVOTE_ANSWER']
        account_e[2]['energy'] -= self.bob_energy_reduce
        account_e[3]['energy'] -= economy['ENERGY_UPVOTE_ANSWER']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 2)
        info('Now Alice question->Bob answer rating is 2')
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -= economy['ENERGY_DOWNVOTE_ANSWER']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol downvote for Alice question->Bob answer rating')
        t = self.table('question', 'allquestions')
        account_e[3]['energy'] -= economy['ENERGY_DOWNVOTE_ANSWER']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == -2)
        info('Now Alice question->Bob answer rating is -2')
        end()

    def test_remove_vote_question(self):
        begin('Test remove vote question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        account_e = [
            '#ignoreorder',
            get_expected_account_body(alice),
            get_expected_account_body(bob),
        ]
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_rating')
        self.action('upvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob upvote for Alice question rating')
        account_e[1]['energy'] -= self.alice_energy_reduce
        account_e[2]['energy'] -= self.bob_energy_reduce + economy['ENERGY_UPVOTE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 1)
        info('Now Alice question rating is 1')
        self.wait()
        self.action('upvote', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 0},
                    bob, 'Bob remove upvote for Alice question rating')
        account_e[2]['energy'] -= economy['ENERGY_FORUM_VOTE_CHANGE']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')
        self.action('downvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob downvote for Alice question rating')
        account_e[2]['energy'] -= economy['ENERGY_DOWNVOTE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == -1)
        info('Now Alice question rating is -1')
        self.wait()
        self.action('downvote', {
                    'user': 'bob', 'question_id': var['aq'], 'answer_id': 0}, bob, 'Bob downvote for Alice question rating')
        account_e[2]['energy'] -= economy['ENERGY_FORUM_VOTE_CHANGE']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_rating'] == 0)
        info('Now Alice question rating is 0')
        end()

    def test_remove_vote_answer(self):
        begin('Test remove vote answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        account_e = [
            '#ignoreorder',
            get_expected_account_body(alice),
            get_expected_account_body(bob),
        ]
        t = self.table('question', 'allquestions')
        for key, value in var.items():
            if 'rating' in key:
                self.assertTrue(value == 0)
        setvar(e, var, 'aq_ba_rating')
        self.action('upvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice upvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -= self.alice_energy_reduce + economy['ENERGY_UPVOTE_ANSWER']
        account_e[2]['energy'] -= self.bob_energy_reduce
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 1)
        info('Now Alice question->Bob answer rating is 1')
        self.wait()
        self.action('upvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']},
                    alice, 'Alice remove upvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -= economy['ENERGY_FORUM_VOTE_CHANGE']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -=  economy['ENERGY_DOWNVOTE_ANSWER']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == -1)
        info('Now Alice question->Bob answer rating is -1')
        self.wait()
        self.action('downvote', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice downvote for Alice question->Bob answer rating')
        account_e[1]['energy'] -= economy['ENERGY_FORUM_VOTE_CHANGE']     
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))   
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_ba_rating'] == 0)
        info('Now Alice question->Bob answer rating is 0')
        end()

    def test_upvote_voted_for_deletion_failed(self):
        begin('Test upvote reported question')
        begin('Test upvote question and answer when downwoted')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('votedelete', {
            'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0}, carol, "Carol report alice question")
        self.action('votedelete', {
            'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'comment_id': 0}, carol, "Carol report bob answer")

        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0},
                           carol, 'Carol attempt to upvote alice question', 'assert')
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']},
                           carol, 'Carol attempt to upvote bob answer', 'assert')
        end()

    def test_mark_answer_as_correct(self):
        begin('Test mark answer as correct')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        account_e = [
            '#ignoreorder',
            get_expected_account_body(alice),
            get_expected_account_body(bob),
        ]
        setvar(e, var, 'caid')
        for key, value in var.items():
            if 'caid' in key:
                self.assertTrue(value == 0)
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, alice, 'Alice mark bob answer as correct')
        account_e[1]['energy'] -= self.alice_energy_reduce + economy['ENERGY_MARK_ANSWER_AS_CORRECT']
        account_e[2]['energy'] -= self.bob_energy_reduce
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == var['aq_ba'])
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_aa']}, alice, 'Alice mark herself answer as correct')
        account_e[1]['energy'] -= economy['ENERGY_MARK_ANSWER_AS_CORRECT']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == var['aq_aa'])
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': var['aq'], 'answer_id': 0}, alice, 'Alice remove correct answer mark')
        t = self.table('question', 'allquestions')
        account_e[1]['energy'] -= economy['ENERGY_MARK_ANSWER_AS_CORRECT']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.assertTrue(compare(e, t, var, True))
        self.assertTrue(var['aq_caid'] == 0)
        end()

    def vote_for_own_item_failed(self):
        begin("Vote for own item", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('upvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0},
                           alice, 'Attempt to upvote own question', 'assert')
        self.failed_action('downvote', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0},
                           alice, 'Attempt to downvote own question', 'assert')
        self.failed_action('upvote', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, bob, 'Attempt to upvote own answer', 'assert')
        self.failed_action('downvote', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var[
                           'aq_ba']}, bob, 'Attempt to downvote own answer', 'assert')
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
        begin('Vote with another user auth', True)
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

    def test_mark_answer_as_correct_for_question_of_another_user_failed(self):
        begin('Mark answer as correct for question of another user', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('mrkascorrect', {
            'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, bob, 'Bob attempt to mark bob answer as correct for Alice question', 'assert')
        end()

    def test_mark_answer_as_correct_another_auth(self):
        begin('Mark answer as correct for question with another user auth', True)
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
        self.failed_action('upvote', {'user': 'alice', 'question_id': int(var['aq']) + 5, 'answer_id': 0},
                           alice, 'Attempt to upvote non-existent  question', 'assert')
        self.failed_action('downvote', {'user': 'alice', 'question_id': int(var['aq']) + 5, 'answer_id': 0},
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
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3]}, alice,
                    'Asking question from alice with text "Alice question"')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
                    'title': 'Title alice question',
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
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'Bob question', 'community_id': 1, 'tags': [1, 2, 3]}, bob,
                    'Asking question from bob with text "Bob question"')
        e.append({
            'id': '#var bq',
            'title': 'Title bob question',
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
        self.alice_energy_reduce = economy['ENERGY_POST_QUESTION'] + \
            2 * economy['ENERGY_POST_ANSWER'] 
        self.bob_energy_reduce = economy['ENERGY_POST_QUESTION'] + \
            economy['ENERGY_POST_ANSWER']
        return e, var


if __name__ == '__main__':
    main()
