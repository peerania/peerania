import peeraniatest
from peeraniatest import *
from jsonutils import compare
from unittest import main


class ForumQuestionTests(peeraniatest.PeeraniaTest):

    def test_insert_question(self):
        begin('Testing registration of new question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1')]
        t = self.table("question", "allquestions")
        info('Table question: ', t)
        self.assertTrue(compare(e, t))
        end()

    def test_modify_question(self):
        begin('Test modify question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.action('modquestion', {
                    'user': 'alice', 'question_id': var['q1'], 'ipfs_link': 'updated IPFS'}, alice, 'Update IPFS link of Alice question')
        t = self.table("question", "allquestions")
        e[0]['ipfs_link'] = 'updated IPFS'
        self.assertTrue(compare(e, t))
        info('Table question: ', t)
        end()

    def test_delete_question(self):
        begin('Test modify question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.action('delquestion', {
                    'user': 'alice', 'question_id': var['q1']}, alice, 'Delete Alice question')
        t = self.table("question", "allquestions")
        e = []
        self.assertTrue(compare(e, t))
        info('Table question: ', t)
        end()

    def test_register_question_from_non_existent_account_failed(self):
        begin("Register question from non-regidtered account", True)
        alice = self.get_non_registered_alice()
        self.failed_action('regquestion', {'user': 'alice', 'ipfs_link': 'test'}, alice,
                           'Asking question from not registered Alice account', 'assert')
        end()

    def test_register_question_another_auth_failed(self):
        begin("Call register question with another owner auth", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('regquestion', {'user': 'alice', 'ipfs_link': 'test'}, bob,
                           'Attempt to register alice question with bob auth', 'auth')
        end()

    def test_modify_question_another_auth_failed(self):
        begin("Call modify question with another owner auth", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('modquestion', {
            'user': 'alice', 'question_id': var['q1'], 'ipfs_link': 'test'}, bob, 'Attempt to modify Alice question with bob auth', 'auth')
        end()

    def test_delete_question_another_auth_failed(self):
        begin("Call delete question with another owner auth", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': var['q1']}, bob, 'Attempt to delete Alice question with bob auth', 'auth')
        end()

    def test_modify_question_of_another_owner_failed(self):
        begin("Modify question of another owner", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('modquestion', {
            'user': 'bob', 'question_id': var['q1'], 'ipfs_link': 'test'}, bob, 'Attempt to modify alice question from bob account', 'assert')
        end()

    def test_delete_question_of_another_owner_failed(self):
        begin("Delete  question of another owner", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('delquestion', {
            'user': 'bob', 'question_id': var['q1']}, bob, 'Attempt to delete alice question from bob account', 'assert')
        end()

    def test_modify_non_existent_question_failed(self):
        begin("Modify non-existent question", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('modquestion', {
            'user': 'bob', 'question_id': var['q1'] + 1, 'ipfs_link': 'test'}, bob, 'Modify non-existent question', 'assert')
        end()

    def test_delete_non_existent_question_failed(self):
        begin("Delete non-existent question", True)
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table("question", "allquestions")
        var = {}
        self.assertTrue(compare(e, t, var))
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': var['q1'] + 1}, alice, 'Delete non-existent question', 'assert')
        end()

    def _register_question_action(self, owner, ipfs_link, id_var=''):
        self.action('regquestion', {'user': str(owner), 'ipfs_link': ipfs_link}, owner,
                    'Asking question from {} with text "{}"'.format(str(owner), ipfs_link))
        return {'id': '#ignore' if id_var == '' else '#var ' + id_var,
                'user': str(owner),
                'ipfs_link': ipfs_link,
                'registration_time': '#ignore',
                "answers": [],
                "comments": []}


if __name__ == "__main__":
    main()
