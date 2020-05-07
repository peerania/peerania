import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

economy = load_defines('src/contracts/peeranha.main/economy.h')

class ForumAnswerTests(peeranhatest.peeranhaTest):

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
        account_e = ['#ignoreorder', get_expected_account_body(
            alice), get_expected_account_body(bob)]
        self._register_answer_action(
            bob, var['q1_id'], 'Bob answer 1 to Alice question 1', q)
        account_e[1]['energy'] -= economy['ENERGY_POST_QUESTION']
        account_e[2]['energy'] -= economy['ENERGY_POST_ANSWER']
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(q, t, ignore_excess=True))
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
        account_e = ['#ignoreorder', get_expected_account_body(
            alice), get_expected_account_body(bob)]
        self.action('modanswer', {'user': 'bob',
                                  'question_id': var['q1_id'],
                                  'answer_id': var['q1_a1_id'],
                                  'ipfs_link': 'updated IPFS'},
                    bob, 'Update Bob answer 1 to Alice question 1, set to "updated IPFS"')
        account_e[1]['energy'] -= economy['ENERGY_POST_QUESTION']
        account_e[2]['energy'] -= economy['ENERGY_POST_ANSWER']
        account_e[2]['energy'] -= economy['ENERGY_MODIFY_ANSWER']
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        setvar(q, var)
        t = self.table('question', 'allquestions')
        q[0]['answers'][0]['ipfs_link'] = 'updated IPFS'
        q[0]['answers'][0]['properties'] = [{'key': 3, 'value': '#ignore'}]
        self.assertTrue(compare(q, t, ignore_excess=True))
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
        account_e = ['#ignoreorder', get_expected_account_body(
            alice), get_expected_account_body(bob)]
        self.action('delanswer', {'user': 'bob',
                                  'question_id': var['q1_id'],
                                  'answer_id': var['q1_a1_id']},
                    bob, 'Delete Bob answer 1 to Alice question 1')
        account_e[1]['energy'] -= economy['ENERGY_POST_QUESTION']
        account_e[2]['energy'] -= economy['ENERGY_POST_ANSWER']
        account_e[2]['energy'] -= economy['ENERGY_DELETE_ANSWER']
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        t = self.table('question', 'allquestions')
        q[0]['answers'] = []
        self.assertTrue(compare(q, t, ignore_excess=True))
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
        self.failed_action('postanswer', {'user': 'bob', 'question_id': var['q1_id'], 'ipfs_link': 'test', 'official_answer': False}, bob,
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
        self.failed_action('postanswer', {'user': 'bob', 'question_id': var['q1_id'], 'ipfs_link': 'test', 'official_answer': False}, bob,
                           'Attempt to register answer from non-regidtered account', 'assert')
        end()

    def test_register_answer_another_auth_failed(self):
        begin('Register answer with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        q = [self._register_question_action(
            alice, 'Alice question 1', 'q1_id')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(q, t, var, True))
        self.failed_action('postanswer', {'user': 'carol', 'question_id': var['q1_id'], 'ipfs_link': 'test', 'official_answer': False}, bob,
                           'Attempt to register carol answer with bob auth', 'auth')
        end()

    def test_modify_answer_another_auth_failed(self):
        begin('Call modify answer with another user auth', True)
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
        begin('Call delete answer with another user auth', True)
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

    def test_modify_answer_of_another_user_failed(self):
        begin('Modify answer of another user', True)
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

    def test_delete_answer_of_another_user_failed(self):
        begin('Delete answer of another user', True)
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
        self.failed_action('postanswer', {'user': 'bob',
                                          'question_id': int(var['q1_id']) + 1,
                                          'ipfs_link': 'test', 'official_answer': False}, bob,
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
                                         'question_id': int(var['q1_id']) + 1,
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
                                         'question_id': int(var['q1_id']) + 1,
                                         'answer_id': var['q1_a1_id']},
                           bob, 'Attempt to delete answer of non-existent question', 'assert')
        end()

    def _register_question_action(self, user, ipfs_link, id_var=''):
        self.action('postquestion', {'user': str(user), 'title': 'title ' + ipfs_link, 'ipfs_link': ipfs_link, 'community_id': 1, 'tags': [1], 'type': 0}, user,
                    'Asking question from {} with text "{}"'.format(str(user), ipfs_link))
        return {'id': '#ignore' if id_var == '' else '#var ' + id_var,
                'user': str(user),
                'ipfs_link': ipfs_link,
                'title': 'title ' + ipfs_link,
                'post_time': '#ignore',
                'answers': [],
                'comments': []}

    def _register_answer_action(self, user, question_id, ipfs_link, question_table, id_var=''):
        self.action('postanswer', {'user': str(user), 'question_id': question_id, 'ipfs_link': ipfs_link, 'official_answer': False}, user,
                    '{} answer to question with id={}: "{}"'.format(str(user), question_id, ipfs_link))
        for question in question_table:
            if isinstance(question, str):
                continue
            if question['id'] == question_id:
                question['answers'].append({
                    'id': '#ignore' if id_var == '' else '#var ' + id_var,
                    'user': str(user),
                    'ipfs_link': ipfs_link,
                    'post_time': '#ignore',
                    'comments': []})


if __name__ == '__main__':
    main()
