import peeraniatest
from peeraniatest import *
from jsonutils import compare
from unittest import main


class ForumQuestionTests(peeraniatest.PeeraniaTest):

    def test_insert_question(self):
        begin('Testing registration of new question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1')]
        t = self.table('question', 'allquestions')
        info('Table question: ', t)
        self.assertTrue(compare(e, t, ignore_excess=True))
        end()

    def test_modify_question(self):
        begin('Test modify question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('modquestion', {
                    'user': 'alice', 'question_id': var['q1'], 'title': 'updated Title', 'ipfs_link': 'updated IPFS', 'community_id': 2, 'tags':[1]}, alice, 'Update Alice question')
        t = self.table('question', 'allquestions')
        e[0]['ipfs_link'] = 'updated IPFS'
        e[0]['title'] = 'updated Title'
        e[0]['properties'] = [{'key': 3, 'value': '#ignore'}]
        e[0]['community_id'] = 2
        e[0]['tags'] = [1]
        self.assertTrue(compare(e, t, ignore_excess=True))
        info('Table question: ', t)
        end()

    def test_delete_question(self):
        begin('Test delete question')
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('delquestion', {
                    'user': 'alice', 'question_id': var['q1']}, alice, 'Delete Alice question')
        t = self.table('question', 'allquestions')
        e = []
        self.assertTrue(compare(e, t, ignore_excess=True))
        info('Table question: ', t)
        end()

    def test_register_question_from_non_existent_account_failed(self):
        begin('Register question from non-regidtered account', True)
        alice = self.get_non_registered_alice()
        self.failed_action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'test', 'community_id': 1, 'tags':[1]}, alice,
                           'Asking question from not registered Alice account', 'assert')
        end()

    def test_register_question_another_auth_failed(self):
        begin('Call register question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.failed_action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'test', 'community_id': 1, 'tags':[1]}, bob,
                           'Attempt to register alice question with bob auth', 'auth')
        end()

    def test_modify_question_another_auth_failed(self):
        begin('Call modify question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {
            'user': 'alice', 'question_id': var['q1'], 'title': 'test', 'ipfs_link': 'test', 'community_id': 2, 'tags':[1]}, bob, 'Attempt to modify Alice question with bob auth', 'auth')
        end()

    def test_title_length_assert_failed(self):
        begin('Test register and modify title length assert ', True)
        alice = self.register_alice_account()
        self.failed_action('postquestion', {'user': alice, 'title': 'Te', 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Register question with title len=2', 'assert')
        self.failed_action('postquestion', {'user': alice, 'title':  "".join('a' for x in range(129)), 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Register question with title len=129', 'assert')
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {'user': alice, 'question_id': var['q1'], 'title': 'Te', 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Modify question, set title with len=2', 'assert')
        self.failed_action('modquestion', {'user': alice, 'question_id': var['q1'], 'title':  "".join('a' for x in range(129)), 'ipfs_link': 'Alice ipfs', 'community_id': 1, 'tags':[1]}, alice,
                           'Modify question, set title with len=129', 'assert')
        end()

    def test_delete_question_another_auth_failed(self):
        begin('Call delete question with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
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
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
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
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
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
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modquestion', {
            'user': 'bob', 'question_id': int(var['q1']) + 1, 'title': 'test', 'ipfs_link': 'test', 'community_id': 2, 'tags':[1]}, bob, 'Modify non-existent question', 'assert')
        end()

    def test_delete_non_existent_question_failed(self):
        begin('Delete non-existent question', True)
        alice = self.register_alice_account()
        e = [self._register_question_action(alice, 'Alice question 1', 'q1')]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delquestion', {
            'user': 'alice', 'question_id': int(var['q1']) + 1}, alice, 'Delete non-existent question', 'assert')
        end()

    def _register_question_action(self, user, ipfs_link, id_var=''):
        tags = [1, 2, 3] if str(user) == 'alice' else [2, 3, 4]
        self.action('postquestion', {'user': str(user), 'title': 'Title ' + ipfs_link, 'ipfs_link': ipfs_link, 'community_id': 1, 'tags': tags}, user,
                    'Asking question from {} with text "{}"'.format(str(user), ipfs_link))
        return {'id': '#ignore' if id_var == '' else '#var ' + id_var,
                'user': str(user),
                'title': 'Title ' + ipfs_link,
                'ipfs_link': ipfs_link,
                'post_time': '#ignore',
                'community_id': 1,
                'tags': tags,
                'answers': [],
                'comments': []}


if __name__ == '__main__':
    main()
