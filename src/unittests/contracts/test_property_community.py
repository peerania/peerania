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
COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6    #64
COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER  = 1 << 7

class TestPropertyCommunity(peeranhatest.peeranhaTest):
    def test_add_flags(self):
        begin('Test add flags')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.failed_action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 666
        }, admin, 'add a flag in wrong community')

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 2}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
            'community_id': 1
        }, admin, 'alice add a flag COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_ENERGY,
            'community_id': 2
        }, admin, 'alice add a flag COMMUNITY_ADMIN_FLG_CREATE_COMMUNITY')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 1}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
            'community_id': 1
        }, admin, 'bob add a flag COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 32}, {'community': 2, 'value': 1}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 32}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))
        end()
    
    def test_pick_up_flag(self):
        begin('Test pick up flag')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        
        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 2}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': 0,
            'community_id': 1
        }, admin, 'pick_up flag for community 1')
        example = []
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.wait(2)
        self.action('givecommuflg', {
            'user': alice,
            'flags': 5,
            'community_id': 1
        }, admin, 'add a flag 5 for community 1')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 5}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': 10,
            'community_id': 2
        }, admin, 'add a flag 10 for community 2')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 5}, {'community': 2, 'value': 10}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': 0,
            'community_id': 2
        }, admin, 'pick_up flag for community 1')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 5}]}]
        self.assertTrue(compare(example, self.table('propertycomm', 'allprprtcomm'), ignore_excess=True))
        end()

    def test_add_flag_ignore_rating_create_tag(self):
        begin('Test add flag ignore rating')
        alice = self.register_alice_account(0, 100)
        admin = self.get_contract_deployer(self.get_default_contract())

        self.failed_action('crtag', {'user': alice, 'name': 'Alice create tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag, Alice don t have rating')
        self.wait(1)
        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_IGNORE_RATING,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_IGNORE_RATING')
        self.action('crtag', {'user': alice, 'name': 'Alice create tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag, with flag ignore rating')

        bob = self.register_bob_account(0, 200)
        t = self.table('crtagtb', get_tag_scope(1))
        self.failed_action('vtcrtag', {'user': bob, 'community_id': 1,
                                'tag_id': t[0]['id']}, bob, 'Bob vote create tag, Bob don t have rating')
        self.failed_action('vtdeltag', {'user': bob, 'community_id': 1,
                                 'tag_id': t[0]['id']}, bob, 'Bob vote delete tag, Bob don t have rating')
        self.wait(1)

        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_IGNORE_RATING,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_IGNORE_RATING')
        self.action('vtcrtag', {'user': bob, 'community_id': 1,
                                'tag_id': t[0]['id']}, bob, 'Bob vote create tag, with flag ignore rating')
        self.action('vtdeltag', {'user': bob, 'community_id': 1,
                                 'tag_id': t[0]['id']}, bob, 'Bob vote delete tag, with flag ignore rating')
        end()

    
    def test_add_flag_ignore_rating_upvote_downvote(self):
        begin('Test add flag ignore rating for upvote/downvote answer/question')
        alice = self.register_alice_account(0, 200)
        bob = self.register_bob_account(0, 200)
        admin = self.get_contract_deployer(self.get_default_contract())

        self._register_question_action(alice, 'Alice question 1', 'q1')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'answer without flag "official_answer", variable official_answer = False'))

        self.failed_action('upvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 0}, bob, 'bob upvote Alice question without rating')
        self.failed_action('upvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 1}, bob, 'bob upvote Alice answer without rating')
        self.failed_action('downvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 1}, bob, 'bob downvote Alice question without rating')
        self.failed_action('downvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 0}, bob, 'bob downvote Alice answer without rating')

        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_IGNORE_RATING,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_IGNORE_RATING')

        self.wait(2)
        self.action('upvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 0}, bob, 'bob upvote Alice question without rating')
        self.action('upvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 1}, bob, 'bob upvote Alice answer without rating')
        self.action('downvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 1}, bob, 'bob downvote Alice question without rating')
        self.action('downvote', {
                    'user': 'bob', 'question_id': question_id, 'answer_id': 0}, bob, 'bob downvote Alice answer without rating')
        end()


    def test_add_flag_energy(self):
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

        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        energy = self.table('account', 'allaccounts')[0]['energy']
        self.assertTrue(compare(energy, self.DEFAULT_ENERGY, ignore_excess=True))
        end()


    def test_add_flag_change_status(self):
        begin('Test add flag change question status')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        self._register_question_action(alice, 'Alice question 1', 'q1')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.failed_action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 1, 'restore_rating': True}, alice, "Change question type to general, don't have permission") 
        self.failed_action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 0, 'restore_rating': True}, alice, "Change question type to expert, don't have permission")  

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS')

        self.action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 1, 'restore_rating': True}, alice, "Change question type to general")
        self.action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 0, 'restore_rating': True}, alice, "Change question type to expert")
        end()


    def test_create_tags(self):
        begin('Test add flag "create tag"')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        old_table = self.table('tags', get_tag_scope(1))
        self.action('crtag', {'user': alice, 'name': 'Alice create tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag, Alice don t have permission')
        self.assertTrue(compare(old_table, self.table('tags', get_tag_scope(1)), ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_CREATE_TAG,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CREATE_TAG')
        
        self.wait(1)
        self.action('crtag', {'user': alice, 'name': 'Alice create tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag')
        example = {
            'id': 7, 
            'name': 'Alice create tag', 
            'ipfs_description': 'undefined', 
            'questions_asked': 0
        }
        self.assertTrue(compare(example, self.table('tags', get_tag_scope(1))[6], ignore_excess=True))
        end()

    def test_official_answer(self):
        begin('Test post answeradd with "official_answer" (flag 10)')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        self._register_question_action(alice, 'Alice question 1', 'q1')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer" (properties official answer don`t give)'))
        answers = self.table('question', 'allquestions')[0]['answers'][0]['properties']
        example = [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]
        self.assertTrue(compare(example, answers, ignore_excess=True))

        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER')

        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'answer with flag "official_answer"'))
        answers = self.table('question', 'allquestions')[0]['answers'][1]['properties']
        example = [{'key': 10, 'value': 1}]
        self.assertTrue(compare(example, answers, ignore_excess=True))
        end()

    def test_modify_official_answer(self):
        begin('Test modify_answer with "official_answer"')
        alice = self.register_alice_account(100,100)
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        self._register_question_action(alice, 'Alice question 1', 'q1')
        question_id = self.table('question', 'allquestions')[0]['id']

        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer", variable official_answer = False'))
        answers_id = self.table('question', 'allquestions')[0]['answers'][0]['id']
        self.action('modanswer', {'user': str(bob), 'question_id': question_id, 'answer_id': answers_id,
                                  'ipfs_link': 'undefined123', 'official_answer': True}, bob, 'modify answer without flag "official_answer", variable official_answer = True')
        properties = self.table('question', 'allquestions')[0]['answers'][0]['properties']
        example = {'key': 10, 'value': 1}
        self.assertFalse(compare(example, properties[0], ignore_excess=True))


        self.action('givecommuflg', {
            'user': alice,
            'flags': COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER')

        self.action('postanswer', {'user': str(alice), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'answer with flag "official_answer", variable official_answer = False'))

        answers_id = self.table('question', 'allquestions')[0]['answers'][1]['id']
        self.action('modanswer', {'user': str(alice), 'question_id': question_id, 'answer_id': answers_id,
                                  'ipfs_link': 'undefined123', 'official_answer': True}, alice, 'modify answer with flag "official_answer", variable official_answer = True')
        properties = self.table('question', 'allquestions')[0]['answers'][1]['properties']
        example = [{'key': 3}, {'key': 10, 'value': 1}]
        self.assertTrue(compare(example, properties, ignore_excess=True))

        self.action('modanswer', {'user': str(alice), 'question_id': question_id, 'answer_id': answers_id,
                                  'ipfs_link': 'undefined123', 'official_answer': False}, alice, 'modify answer with flag "official_answer", variable official_answer = false')
        properties = self.table('question', 'allquestions')[0]['answers'][1]['properties']
        example = {'key': 10, 'value': 1}
        self.assertFalse(compare(example, properties[0], ignore_excess=True))
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
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False},
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