import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

MODERATOR_FLG_ALL = 63

economy = load_defines('./src/contracts/peeranha.main/economy.h')

class TestWithin15Minutes(peeranhatest.peeranhaTest):  
    def test_account_properties(self):
        begin('test account properties (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self._create_basic_hierarchy(alice, bob, carol)       

        example_account = [{'user': 'alice', 'integer_properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}, 
                            {'user': 'bob', 'integer_properties': []},
                            {'user': 'carol', 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_account_properties_mod_delete_answer(self):
        begin('test account properties moderator delete answer(first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL) 

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, alice,
                    'Asking question from alice with text "Alice question"')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'Bob answer to Alice', 'official_answer': False},
                    bob, ' |-->Answer to alice from alice: "Alice answer to herself"')

        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': id_question, 'answer_id': 1, 'comment_id': 0},
                    ted, 'Ted vote for Alice question deletion')
        
        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}, {'key': 12, 'value': 0}, {'key': 13, 'value': 0}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_account_properties_mod_delete_question(self):
        begin('test account properties moderator delete question(first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL) 

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, alice,
                    'Asking question from alice with text "Alice question"')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'Bob answer to Alice', 'official_answer': False},
                    bob, ' |-->Answer to alice from alice: "Alice answer to herself"')

        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
       
        self.action('reportforum', {'user': 'ted', 'question_id': id_question, 'answer_id': 0, 'comment_id': 0},
                    ted, 'Ted vote for Alice question deletion')
        
        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_account_properties_delete_answer(self):
        begin('test account properties moderator delete answer(first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL) 

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, alice,
                    'Asking question from alice with text "Alice question"')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'Bob answer to Alice', 'official_answer': False},
                    bob, ' |-->Answer to alice from alice: "Alice answer to herself"')

        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        
        self.action('delanswer', {'user': 'bob', 'question_id': id_question, 'answer_id': 1}, bob, 'Delete Alice answer to Carol question')
        
        example_account = [{'user': 'alice', 'integer_properties': []}, 
                            {'user': 'bob', 'integer_properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]},
                            {'user': 'ted', 'integer_properties': [{'key': 48, 'value': 63}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_delete_answers(self):
        begin('test delete answers (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)

       
        self.action('delanswer', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 1}, alice, 'Delete Alice answer to Carol question')
        self.action('delanswer', {'user': 'bob', 'question_id': var['aq'], 'answer_id': 2}, bob, 'Delete Bob answer to Carol question')

        example_rating = [{'user': 'alice', 'rating': 199}, {'user': 'bob', 'rating': 199}, {'user': 'carol', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_report_answers(self):
        begin('test delete answers (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL) 
       
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 1, 'comment_id': 0},
                    ted, 'Ted vote for Alice question deletion')
        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 2, 'comment_id': 0},
                    ted, 'Ted vote for Bob question deletion')

        example_rating = [{'user': 'alice', 'rating': 198}, {'user': 'bob', 'rating': 198}, {'user': 'carol', 'rating': 200}, {'user': 'ted', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_report_question(self):
        begin('test report question (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)

        self.action('reportforum', {'user': 'ted', 'question_id': var['aq'], 'answer_id': 0, 'comment_id': 0},
                    ted, 'Ted vote for Bob question deletion')

        example_rating = [{'user': 'alice', 'rating': 200}, {'user': 'bob', 'rating': 200}, {'user': 'carol', 'rating': 198}, {'user': 'ted', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_downvote_answer(self):
        begin('test downvote answer (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)

        
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 1}, carol, 'Carol downvote for Alice question->Bob answer rating')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 2}, carol, 'Carol downvote for Bob question->Bob answer rating')
        
        example_rating = [{'user': 'alice', 'rating': 198}, {'user': 'bob', 'rating': 198}, {'user': 'carol', 'rating': 198}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))

        example_question = [{'id': '68719476735', 'user': 'carol', 'answers': [{'id': 1, 'user': 'alice', 'properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]}, {'id': 2, 'user': 'bob', 'properties': []}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_downvote_and_upvote_answer(self):
        begin('test downvote and upvote answer (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)       

        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 1}, carol, 'Carol downvote for Alice question->Bob answer rating')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 2}, carol, 'Carol downvote for Bob question->Bob answer rating')
        
        example_rating = [{'user': 'alice', 'rating': 198}, {'user': 'bob', 'rating': 198}, {'user': 'carol', 'rating': 198}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        example_question = [{'id': '68719476735', 'user': 'carol', 'answers': [{'id': 1, 'user': 'alice', 'properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]}, {'id': 2, 'user': 'bob', 'properties': []}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))

        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 1}, carol, 'Carol upvote for Alice question->Bob answer rating')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 2}, carol, 'Carol upvote for Bob question->Bob answer rating')
        
        example_rating = [{'user': 'alice', 'rating': 220}, {'user': 'bob', 'rating': 210}, {'user': 'carol', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))

        example_question = [{'id': '68719476735', 'user': 'carol', 'answers': [{'id': 1, 'user': 'alice', 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}, {'id': 2, 'user': 'bob', 'properties': []}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()
    
    def test_upvote_and_downvote_answer(self):
        begin('test upvote and downvote answer (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        var = self._create_basic_hierarchy(alice, bob, carol)       

        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 1}, carol, 'Carol upvote for Alice question->Bob answer rating')
        self.action('upvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 2}, carol, 'Carol upvote for Bob question->Bob answer rating')
        
        example_rating = [{'user': 'alice', 'rating': 220}, {'user': 'bob', 'rating': 210}, {'user': 'carol', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 1}, carol, 'Carol downvote for Alice question->Bob answer rating')
        self.action('downvote', {
                    'user': 'carol', 'question_id': var['aq'], 'answer_id': 2}, carol, 'Carol downvote for Bob question->Bob answer rating')
        
        example_rating = [{'user': 'alice', 'rating': 198}, {'user': 'bob', 'rating': 198}, {'user': 'carol', 'rating': 198}]
        end()
    
    def test_change_type_quesion(self):
        begin('test change type question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
        
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, alice,
                    'Asking question from alice with text')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))

        example_rating = [  {'user': 'alice', 'rating': 200}, 
                            {'user': 'bob', 'rating': 210}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 1, 'restore_rating': True}, alice, "Change question type to general")
        example_rating = [  {'user': 'alice', 'rating': 200}, 
                            {'user': 'bob', 'rating': 202}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('chgqsttype', {
                    'user': 'alice', 'question_id': question_id, 'type': 0, 'restore_rating': True}, alice, "Change question type to expert")
        example_rating = [  {'user': 'alice', 'rating': 200}, 
                            {'user': 'bob', 'rating': 210}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_upvote_answer(self):
        begin('test account properties (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()  

        for w in range(3):
            self.register_question_action(bob, 'Alice question ' + str(68719476735 - w))
            question_id = self.table('question', 'allquestions')[0]['id']
            self.action('postanswer', {'user': 'alice', 'question_id': question_id, 'ipfs_link': 'Alice post answer', 'official_answer': False},
                    alice, ' |-->Answer to alice from bob: "Alice post answer"')

        self.action('upvote', {'user': 'bob', 'question_id': question_id, 'answer_id': 1},
                    bob, 'Bob upvote Alice answer')

        example_account = [{'user': 'alice', 'integer_properties': [{'key': 12, 'value': 3}, {'key': 13, 'value': 3}]}, 
                            {'user': 'bob', 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
   
    def _create_basic_hierarchy(self, alice, bob, carol):
        self.action('postquestion', {'user': 'carol', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, carol,
                    'Asking question from alice with text "Alice question"')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'user': 'carol',
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
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'Alice answer to herself', 'official_answer': False},
                    alice, ' |-->Answer to alice from alice: "Alice answer to herself"')
        self.wait(7)
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'Bob answer to alice', 'official_answer': False},
                    bob, '  `->Answer to alice from bob: "Bob answer to alice"')
        
        example_question = [{'id': '68719476735', 'user': 'carol', 'answers': [{'id': 1, 'user': 'alice', 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}, {'id': 2, 'user': 'bob', 'properties': []}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        example_rating = [{'user': 'alice', 'rating': 210}, 
                            {'user': 'bob', 'rating': 200}, 
                            {'user': 'carol', 'rating': 200}]
        self.assertTrue(compare(example_rating, self.table('account', 'allaccounts'), ignore_excess=True))
        return var

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()