import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


def cbody(user, question_id, a_id=0, ipfs='', c_id=-1):
    ret = {'user': str(user),
           'question_id': question_id,
           'answer_id': a_id}
    if ipfs != '':
        ret['ipfs_link'] = ipfs
    if c_id != -1:
        ret['comment_id'] = c_id
    return ret


class ForumCommentTests(peeraniatest.PeeraniaTest):

    def test_register_comment(self):
        begin('Register comment')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            alice, var['aq'], ipfs='Comment to Alice question'), alice, 'Register alice comment to Alice question')
        self.action('postcomment', cbody(
            alice, var['aq'], var['aq_aa'], 'Alice comment to Alice answer'), alice, 'Register alice comment to Alice question->Alice answer')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        self.action('postcomment', cbody(
            alice, var['aq'], var['aq_ba'], 'Alice comment to Bob answer'), alice, 'Register alice comment to Alice question->Bob answer')
        e[1]['comments'].append({'id': '#var aq_ac', 'post_time': '#ignore',
                                 'user': 'alice', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'Alice comment to Alice answer'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'Alice comment to Bob answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, ignore_excess=True))
        info('Table after action', t)
        end()

    def test_modify_comment(self):
        begin('Modify comment')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('modcomment', cbody(
            bob, var['aq'], ipfs='updated Bob comment to Alice question', c_id=var['aq_bc']), bob, 'Update bob comment to Alice question')
        self.action('modcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'updated Bob comment to Alice answer', c_id=var['aq_aa_bc']), bob, 'Update bob comment to Alice question->Alice answer')
        e[1]['comments'][0]['ipfs_link'] = 'updated Bob comment to Alice question'
        e[1]['comments'][0]['properties'] = [{'key': 3, 'value': '#ignore'}]
        e[1]['answers'][0]['comments'][0]['ipfs_link'] = 'updated Bob comment to Alice answer'
        e[1]['answers'][0]['comments'][0]['properties'] = [{'key': 3, 'value': '#ignore'}]
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('Table after action', t)
        end()

    def test_delete_comment(self):
        begin('Delete comment')
        begin('Register comment')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment: Alice question')
        self.action('postcomment', cbody(
            alice, var['aq'], var['aq_aa'], 'Alice comment to Alice answer'), alice, 'Register alice comment: Alice question->Alice answer')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment: Alice question->Alice answer')
        self.action('postcomment', cbody(
            alice, var['aq'], var['aq_ba'], 'Alice comment to Bob answer'), alice, 'Register alice comment to Alice question->Bob answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'Alice comment to Alice answer'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        e[1]['answers'][1]['comments'].append(
            {'id': '#var aq_ba_ac', 'post_time': '#ignore', 'user': 'alice', 'ipfs_link': 'Alice comment to Bob answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        setvar(e, var)
        self.action('delcomment', cbody(
            bob, var['aq'], c_id=var['aq_bc']), bob, 'Delete bob comment to Alice question')
        self.action('delcomment', cbody(
            bob, var['aq'], var['aq_aa'], c_id=var['aq_aa_bc']), bob, 'Dlete bob comment to Alice question->Alice answer')
        e[1]['comments'] = []
        del e[1]['answers'][0]['comments'][1]
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('Table after action', t)
        end()

    def test_register_comment_from_non_existent_account_failed(self):
        begin('Register comment from non-regidtered account', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.get_non_registered_carol()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('postcomment', cbody(carol, var['aq'], ipfs='test'), carol,
                           'Attempt to register comment to question from non-registered account', 'assert')
        self.failed_action('postcomment', cbody(carol, var['aq'], var['aq_ba'], 'test'), carol,
                           'Attempt to register comment to answer from non-registered account' 'assert')
        end()

    def test_register_comment_another_auth_failed(self):
        begin('Register comment using another auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('postcomment', cbody(bob, var['aq'], ipfs='test'), alice,
                           'Attempt to register comment to question with another user auth', 'auth')
        self.failed_action('postcomment', cbody(bob, var['aq'], var['aq_ba'], 'test'), alice,
                           'Attempt to register comment to answer with another user auth' 'auth')
        end()

    def test_modify_comment_another_auth_failed(self):
        begin('Call modify comment with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modcomment', cbody(
            bob, var['aq'], ipfs='test', c_id=var['aq_bc']), alice,
            'Attempt to modify comment to question with another user auth', 'auth')
        self.failed_action('modcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'test', c_id=var['aq_aa_bc']),  alice,
            'Attempt to modify comment to answer with another user auth' 'auth')
        end()

    def test_delete_comment_another_auth_failed(self):
        begin('Call modify comment with another user auth', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delcomment', cbody(
            bob, var['aq'], c_id=var['aq_bc']), alice,
            'Attempt to delete comment to question with another user auth', 'auth')
        self.failed_action('delcomment', cbody(
            bob, var['aq'], var['aq_aa'], c_id=var['aq_aa_bc']),  alice,
            'Attempt to delete comment to answer with another user auth' 'auth')
        end()

    def test_modify_comment_of_another_user_failed(self):
        begin('Modify comment of another user', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modcomment', cbody(
            carol, var['aq'], ipfs='test', c_id=var['aq_bc']), carol,
            'Attempt to modify comment to question from another account', 'assert')
        self.failed_action('modcomment', cbody(
            carol, var['aq'], var['aq_aa'], 'test', c_id=var['aq_aa_bc']),  carol,
            'Attempt to modify comment to answer from another account' 'assert')
        end()


    def test_delete_comment_of_another_user_failed(self):
        begin('Delete comment of another user', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delcomment', cbody(
            carol, var['aq'], c_id=var['aq_bc']), carol,
            'Attempt to delete comment to question from another account', 'assert')
        self.failed_action('delcomment', cbody(
            carol, var['aq'], var['aq_aa'], c_id=var['aq_aa_bc']),  carol,
            'Attempt to delete comment to answer from another account' 'assert')
        end()

    def test_modify_non_existent_comment_failed(self):
        begin('Test modify non existent comment', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modcomment', cbody(
                            bob, var['aq'], ipfs = 'test', c_id=var['aq_bc'] + 1), bob,
                            'Attempt to modify non-existent comment to question', 'assert')
        self.failed_action('modcomment', cbody(
                            bob, var['aq'], var['aq_aa'], ipfs = 'test', c_id=var['aq_aa_bc'] + 1),  bob,
                            'Attempt to modify non-existent comment to answer' 'assert')
        end()


    def test_delete_non_existent_comment_failed(self):
        begin('Test delete non existent comment', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delcomment', cbody(
            bob, var['aq'], c_id=var['aq_bc'] + 1), bob,
            'Attempt to delete non-existent comment to question', 'assert')
        self.failed_action('delcomment', cbody(
            bob, var['aq'], var['aq_aa'], c_id=var['aq_aa_bc'] + 1),  bob,
            'Attempt to delete non-existent comment to answer' 'assert')
        end()

    def test_register_comment_to_non_existent_question_and_answer_failed(self):
        begin('Register comment to non existent question and answer failed', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.get_non_registered_carol()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.failed_action('postcomment', cbody(carol, int(var['aq']) + 10, ipfs='test'), carol,
                           'Attempt to register comment to non-existent question', 'assert')
        self.failed_action('postcomment', cbody(carol, var['aq'], int(var['aq_ba']) + 10, 'test'), carol,
                           'Attempt to register comment to non-existent answer' 'assert')
        end()


    def test_modify_comment_to_non_existent_question_and_answer_failed(self):
        begin('Test modify comment to non-existent question or answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('modcomment', cbody(
                            bob, int(var['aq']) + 10, ipfs = 'test', c_id=var['aq_bc']), bob,
                            'Attempt to modify comment to non-existent question', 'assert')
        self.failed_action('modcomment', cbody(
                            bob, var['aq'], int(var['aq_aa']) + 10, ipfs = 'test', c_id=var['aq_aa_bc']),  bob,
                            'Attempt to modify comment to non-existent answer' 'assert')
        end()

    def test_delete_comment_to_non_existent_question_and_answer_failed(self):
        begin('Test delete comment to non-existent question or answer', True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        (e, var) = self._create_basic_hierarchy(alice, bob)
        self.action('postcomment', cbody(
            bob, var['aq'], ipfs='Comment to Alice question'), bob, 'Register bob comment to Alice question')
        self.action('postcomment', cbody(
            bob, var['aq'], var['aq_aa'], 'Bob comment to Alice answer'), bob, 'Register bob comment to Alice question->Alice answer')
        e[1]['comments'].append({'id': '#var aq_bc', 'post_time': '#ignore',
                                 'user': 'bob', 'ipfs_link': 'Comment to Alice question'})
        e[1]['answers'][0]['comments'].append(
            {'id': '#var aq_aa_bc', 'post_time': '#ignore', 'user': 'bob', 'ipfs_link': 'Bob comment to Alice answer'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.failed_action('delcomment', cbody(
                            bob, int(var['aq']) + 10, c_id=var['aq_bc']), bob,
                            'Attempt to delete comment to non-existent question', 'assert')
        self.failed_action('delcomment', cbody(
                            bob, var['aq'], int(var['aq_aa']) + 10, c_id=var['aq_aa_bc']),  bob,
                            'Attempt to delte comment to non-existent answer' 'assert')
        end()

    def _create_basic_hierarchy(self, alice, bob):
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question','ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1]}, alice,
                    'Asking question from alice with text "Alice question"')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'alice',
                    'ipfs_link': 'Alice question',
                    'title': 'Title alice question',
                    'post_time': '#ignore',
                    'answers': [],
                    'comments': []
        }]

        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself'},
                    alice, '  |-->Answer to alice from alice: "Alice answer to herself"')
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'Bob answer to alice'},
                    bob, '  `->Answer to alice from bob: "Bob answer to alice"')
        e[1]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to herself',
            'post_time': '#ignore',
            'comments': []})
        e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'Bob answer to alice',
            'post_time': '#ignore',
            'comments': []})
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'Bob question',  'community_id': 1, 'tags': [2]}, bob,
                    'Asking question from bob with text "Bob question"')
        e.append({
            'id': '#var bq',
            'user': 'bob',
            'title': 'Title bob question',
            'ipfs_link': 'Bob question',
            'post_time': '#ignore',
            'answers': [],
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': var['bq'], 'ipfs_link': 'Alice answer to bob'},
                    alice, '  `->Answer to bob from alice: "Alice answer to bob"')
        e[2]['answers'].append({
            'id': '#var bq_aa',
            'user': 'alice',
            'ipfs_link': 'Alice answer to bob',
            'post_time': '#ignore',
            'comments': []})
        t = self.table('question', 'allquestions')
        setvar(e, var)
        self.assertTrue(compare(e, t, var, True))
        return e, var


if __name__ == '__main__':
    main()
