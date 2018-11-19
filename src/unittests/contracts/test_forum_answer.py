import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class ForumAnswerTests(peeraniatest.PeeraniaTest):

    def test_register_answer(self):
        begin('Test register new answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q)
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, ignore_excess=True))
        info('Table question after question registration', t)
        end()

    def test_modify_answer(self):
        begin('Test modify answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.action('modanswer', {'user': 'bob',
                                  'question_id': var['q1_id'],
                                  'answer_id': var['q1_a1_id'],
                                  'ipfs_link': 'updated IPFS'},
                    bob, 'Update Bob answer 1 to Alice question 1, set to "updated IPFS"')
        setvar(q, var)
        t = self.table('question', 'allquestions')
        q[0]['answers'][0]['ipfs_link'] = 'updated IPFS'
        self.assertTrue(compare(q, t, ignore_excess=True))
        info('Table question after actions', t)
        end()

    def test_delete_answer(self):
        begin('Test delete answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.action('delanswer', {'user': 'bob',
                                  'question_id': var['q1_id'],
                                  'answer_id': var['q1_a1_id']},
                    bob, 'Delete Bob answer 1 to Alice question 1')
        t = self.table('question', 'allquestions')
        q[0]['answers'] = []
        self.assertTrue(compare(q, t, ignore_excess=True))
        info('Table question after actions', t)
        end()

    def test_register_answer_twice_failed(self):
        begin('Test register answer twice')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q)
        self.failed_action('postanswer', {'user': 'bob', 'question_id': var['q1_id'], 'ipfs_link': 'test'}, bob,
                           'Attempt to register answer for the second time', 'assert')
        end()

    def test_register_answer_from_non_existent_account_failed(self):
        begin('Register answer from non-regidtered account', True)
        alice = self.register_alice_account()
        bob = self.get_non_registered_bob()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('postanswer', {'user': 'bob', 'question_id': var['q1_id'], 'ipfs_link': 'test'}, bob,
                           'Attempt to register answer from non-regidtered account', 'assert')
        end()

    def test_register_answer_another_auth_failed(self):
        begin('Register answer with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('postanswer', {'user': 'carol', 'question_id': var['q1_id'], 'ipfs_link': 'test'}, bob,
                           'Attempt to register carol answer with bob auth', 'auth')
        end()

    def test_modify_answer_another_auth_failed(self):
        begin('Call modify answer with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('modanswer', {'user': 'bob',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id'],
                                         'ipfs_link': 'test'},
                           carol, 'Attempt to modify bob answer with carol auth', 'auth')
        end()

    def test_delete_answer_another_auth_failed(self):
        begin('Call delete answer with another owner auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('delanswer', {'user': 'bob',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id']},
                           carol, 'Attempt to delete bob answer with carol auth', 'auth')
        end()

    def test_modify_answer_of_another_owner_failed(self):
        begin('Modify answer of another owner', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('modanswer', {'user': 'carol',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id'],
                                         'ipfs_link': 'test'},
                           carol, 'Attempt to modify bob answer with carol account', 'assert')
        end()

    def test_delete_answer_of_another_owner_failed(self):
        begin('Delete answer of another owner', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('delanswer', {'user': 'carol',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id']},
                           carol, 'Attempt to delete bob answer from carol account', 'assert')
        end()

    def test_modify_non_existent_answer_failed(self):
        begin('Test modify non existent answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('modanswer', {'user': 'bob',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id'] + 1,
                                         'ipfs_link': 'updated IPFS'},
                           bob, 'Attempt to update non-existent answer', 'assert')
        end()

    def test_delete_non_existent_answer_failed(self):
        begin('Test delete non existent answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('delanswer', {'user': 'bob',
                                         'question_id': var['q1_id'],
                                         'answer_id': var['q1_a1_id'] + 1},
                           bob, 'Attempt to delete non-existent answer', 'assert')
        end()

    def test_register_answer_to_non_existent_question_failed(self):
        begin('Register answer to non-existent question', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('postanswer', {'user': 'bob', 'question_id': var['q1_id'] + 1, 'ipfs_link': 'test'}, bob,
                           'Attempt to register answer to non existent question', 'assert')
        end()

    def test_modify_answer_of_non_existent_question_failed(self):
        begin('Test modify answer of non-existent question', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('modanswer', {'user': 'bob',
                                         'question_id': var['q1_id'] + 1,
                                         'answer_id': var['q1_a1_id'],
                                         'ipfs_link': 'updated IPFS'},
                           bob, 'Attempt to modify answer of non-existent question', 'assert')
        end()

    def test_delete_answer_of_non_existent_question_failed(self):
        begin('Test delete answer of non-existent question', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        setvar(q, var)
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q, 'q1_a1_id')
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('delanswer', {'user': 'bob',
                                         'question_id': var['q1_id'] + 1,
                                         'answer_id': var['q1_a1_id']},
                           bob, 'Attempt to delete answer of non-existent question', 'assert')
        end()

    def _register_question_action(self, owner, ipfs_link, id_var=''):
        self.action('postquestion', {'user': str(owner), 'title': 'title ' + ipfs_link, 'ipfs_link': ipfs_link}, owner,
                    'Asking question from {} with text "{}"'.format(str(owner), ipfs_link))
        return {'id': '#ignore' if id_var == '' else '#var ' + id_var,
                'user': str(owner),
                'ipfs_link': ipfs_link,
                'title': 'title ' + ipfs_link,
                'post_time': '#ignore',
                'answers': [],
                'comments': []}

    def _register_answer_action(self, owner, question_id, ipfs_link, question_table, id_var=''):
        self.action('postanswer', {'user': str(owner), 'question_id': question_id, 'ipfs_link': ipfs_link}, owner,
                    '{} answer to question with id={}: "{}"'.format(str(owner), question_id, ipfs_link))
        for question in question_table:
            if isinstance(question, str):
                continue
            if question['id'] == question_id:
                question['answers'].append({
                    'id': '#ignore' if id_var == '' else '#var ' + id_var,
                    'user': str(owner),
                    'ipfs_link': ipfs_link,
                    'post_time': '#ignore',
                    'comments': []})


if __name__ == '__main__':
    main()
