import peeranhatest
from peeranhatest import *
from jsonutils import compare
from unittest import main

economy = load_defines('src/contracts/peeranha.main/economy.h')

class ForumQuestionTests(peeranhatest.peeranhaTest):

    def test_insert_question(self):
        begin('Testing registration of new question')
        alice = self.register_alice_account()
        account_e = [get_expected_account_body(alice)]
        e = [self.register_question_action(alice, 'Alice question 1')]
        t = self.table('question', 'allquestions')
        account_e[0]['energy'] -= economy['ENERGY_POST_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_modify_question(self):
        begin('Test modify question')
        alice = self.register_alice_account()
        account_e = [get_expected_account_body(alice)]
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('modquestion', {
                    'user': 'alice', 'question_id': var['q1'], 'title': 'updated Title', 'ipfs_link': 'updated IPFS', 'community_id': 2, 'tags':[1]}, alice, 'Update Alice question')
        account_e[0]['energy'] -= economy['ENERGY_MODIFY_QUESTION']
        account_e[0]['energy'] -= economy['ENERGY_POST_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        e[0]['ipfs_link'] = 'updated IPFS'
        e[0]['title'] = 'updated Title'
        e[0]['properties'] = [{'key': 3, 'value': '#ignore'}]
        e[0]['community_id'] = 2
        e[0]['tags'] = [1]
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_delete_question(self):
        begin('Test delete question')
        alice = self.register_alice_account()
        account_e = [get_expected_account_body(alice)]
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('delquestion', {
                    'user': 'alice', 'question_id': var['q1']}, alice, 'Delete Alice question')
        account_e[0]['energy'] -= economy['ENERGY_POST_QUESTION']
        account_e[0]['energy'] -= economy['ENERGY_DELETE_QUESTION']
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        e = []
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_register_question_from_non_existent_account_failed(self):
        begin('Register question from non-regidtered account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'test', 'community_id': 1, 'tags':[1], 'type': 0}, alice,
                           'Asking question from not registered Alice account', 'assert')
        end()

    def test_register_question_another_auth_failed(self):
        begin('Call register question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'test', 'community_id': 1, 'tags':[1], 'type': 0}, bob,
                           'Attempt to register alice question with bob auth', 'auth')
        end()

    def test_modify_question_another_auth_failed(self):
        begin('Call modify question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {
            'user': 'alice', 'question_id': var['q1'], 'title': 'test', 'ipfs_link': 'test', 'community_id': 2, 'tags':[1]}, bob, 'Attempt to modify Alice question with bob auth', 'auth')
        end()

    def test_title_length_assert_failed(self):
        begin('Test register and modify title length assert ', True)
        alice = self.register_alice_account()
        self.failed_action('postquestion', {'user': alice, 'title': 'T', 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1], 'type': 0}, alice,
                           'Register question with title len=1', 'assert')
        self.failed_action('postquestion', {'user': alice, 'title':  "".join('a' for x in range(257)), 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1], 'type': 0}, alice,
                           'Register question with title len=129', 'assert')
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {'user': alice, 'question_id': var['q1'], 'title': 'T', 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Modify question, set title with len=1', 'assert')
        self.failed_action('modquestion', {'user': alice, 'question_id': var['q1'], 'title':  "".join('a' for x in range(257)), 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Modify question, set title with len=257', 'assert')
        end()

    def test_delete_question_another_auth_failed(self):
        begin('Call delete question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': var['q1']}, bob, 'Attempt to delete Alice question with bob auth', 'auth')
        end()

    def test_modify_question_of_another_user_failed(self):
        begin('Modify question of another user', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {
            'user': 'bob', 'question_id': var['q1'], 'title': 'test', 'ipfs_link': 'test', 'community_id': 2, 'tags':[1]}, bob, 'Attempt to modify alice question from bob account', 'assert')
        end()

    def test_delete_question_of_another_user_failed(self):
        begin('Delete  question of another user', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delquestion', {
            'user': 'bob', 'question_id': var['q1']}, bob, 'Attempt to delete alice question from bob account', 'assert')
        end()

    def test_modify_non_existent_question_failed(self):
        begin('Modify non-existent question', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {
            'user': 'bob', 'question_id': int(var['q1']) + 1, 'title': 'test', 'ipfs_link': 'test', 'community_id': 2, 'tags':[1]}, bob, 'Modify non-existent question', 'assert')
        end()

    def test_delete_non_existent_question_failed(self):
        begin('Delete non-existent question', True)
        alice = self.register_alice_account()
        e = [self.register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': int(var['q1']) + 1}, alice, 'Delete non-existent question', 'assert')
        end()


if __name__ == '__main__':
    main()
