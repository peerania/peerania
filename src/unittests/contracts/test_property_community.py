import peeranhatest
from test_forum_comment import cbody
from peeranhatest import *
from jsonutils import *
from unittest import main


COMMUNITY_ADMIN_FLG_INFINITE_ENERGY = 1 << 0        # 1
COMMUNITY_ADMIN_FLG_INFINITE_IMPACT = 1 << 1        # 2
COMMUNITY_ADMIN_FLG_IGNORE_RATING = 1 << 2          # 4
COMMUNITY_ADMIN_FLG_CREATE_TAG = 1 << 4             # 16
COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS = 1 << 5 #32
COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6
COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER  = 1 << 7

class TestPropertyCommunity(peeranhatest.peeranhaTest):
    def test_add_user(self):
        begin('Test add flags')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 2}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
        'community_id': 1
        }, admin, 'alice add a flag COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_ENERGY,
        'community_id': 2
        }, admin, 'alice add a flag COMMUNITY_ADMIN_FLG_CREATE_COMMUNITY')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 1}]}]
        
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
        'community_id': 1
        }, admin, 'bob add a flag COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 1}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))
        end()

    def test_create_question(self):
        begin('Test add flag energy')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_ENERGY,
        'community_id': 1
        }, admin, 'alice add a flag COMMUNITY_ADMIN_FLG_INFINITE_ENERGY')

        self._register_question_action(alice, 'Alice question 1', 'q1')
        energy = self.table('account', 'allaccounts')[0]['energy']
        self.assertTrue(compare(energy, self.DEFAULT_ENERGY, ignore_excess=True))

        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postcomment', cbody(
            alice, question_id, ipfs='Comment to Alice question'), alice, 'Register alice comment')
        energy = self.table('account', 'allaccounts')[0]['energy']
        self.assertTrue(compare(energy, self.DEFAULT_ENERGY, ignore_excess=True))

        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined'}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        energy = self.table('account', 'allaccounts')[0]['energy']
        self.assertTrue(compare(energy, self.DEFAULT_ENERGY, ignore_excess=True))
        end()


    def test_create_tags(self):
        begin('Test add flag "create tag"')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        old_table = self.table('tags', get_tag_scope(1))
        self.action('crtag', {'user': alice, 'name': 'Alice tag, Alice has no rights',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag, Alice has no rights')
        table = self.table('tags', get_tag_scope(1))
        self.assertTrue(compare(old_table, table, ignore_excess=True))

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CREATE_TAG,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CREATE_TAG')
        
        self.action('crtag', {'user': alice, 'name': 'Alice tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag')
        table = self.table('tags', get_tag_scope(1))
        example = {
            'name': 'Alice tag',
            'ipfs_description': 'undefined',
        }
        self.assertTrue(compare(example, table[6], ignore_excess=True))
        end()

    def test_official_answer(self):
        begin('Test add flag "official_answer"')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        
        self._register_question_action(alice, 'Alice question 1', 'q1')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CREATE_TAG')

        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined'}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Bob answer to Alice'))
        answers = self.table('question', 'allquestions')[0]['answers'][0]['properties']
        print(answers)
        example = {
            'key': 10,
            'value': 1,
        }
        print(example)

        self.assertTrue(compare(example, answers[0], ignore_excess=True))
        end()

    def test_delete(self):
        begin('Test delete')

        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        ted = self.register_ted_account()

        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined'},
                    bob, 'Register Bob answer to Alice')
        answer_id = self.table('question', 'allquestions')[0]['answers'][0]['id']
        self.action('postcomment', {'user': 'carol', 'question_id': question_id, 'answer_id': answer_id,
                                    'ipfs_link': 'undefined'}, carol, 'Register Carol comment to Bob answer')
        comment_id = self.table('question', 'allquestions')[0]['answers'][0]['comments'][0]['id']

        self.action('givecommuflg', {
            'user': ted,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        example = []
        
        self.action('reportforum', {'user': 'ted', 'question_id': question_id, 'answer_id': answer_id, 'comment_id': comment_id},
                    ted, 'Ted delete comment')
        comment = self.table('question', 'allquestions')[0]['answers'][0]['comments']
        self.assertTrue(compare(example, comment, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': question_id, 'answer_id': answer_id, 'comment_id': 0},
                    ted, 'Ted delete answer')
        answer = self.table('question', 'allquestions')[0]['answers']
        self.assertTrue(compare(example, answer, ignore_excess=True))

        self.action('reportforum', {'user': 'ted', 'question_id': question_id, 'answer_id': 0, 'comment_id': 0},
                    ted, 'Ted delete question')
        question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, question, ignore_excess=True))
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

if __name__ == '__main__':
    main()