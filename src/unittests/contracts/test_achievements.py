import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

MODERATOR_FLG_ALL = 63

class Achievents(int, Enum): 
    questions_asked = 1, 
    answers_given = 2, 
    correct_answers = 3, 
    first_10k_registered = 4, 
    stranger = 5, 
    newbie = 6, 
    junior = 7, 
    resident = 8, 
    senior = 9, 
    hero = 10, 
    superhero = 11,
    answer_15_minutes = 12,
    first_answer = 13

class TestAchievents(peeranhatest.peeranhaTest):  
    def test_post_question(self):
        begin('test post question (bronze, silver, gold) ahievements')
        alice = self.register_alice_account()     

        self.register_question_action(alice, 'Alice question ' + str(68719476735))
        example_alice = [{'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476734))
        example_alice = [{'user': 'alice', 'achievements_id': 1}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476733))
        self.register_question_action(alice, 'Alice question ' + str(68719476732))
        self.register_question_action(alice, 'Alice question ' + str(68719476731))
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 2}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476730))
        self.register_question_action(alice, 'Alice question ' + str(68719476729))
        self.register_question_action(alice, 'Alice question ' + str(68719476728))
        self.register_question_action(alice, 'Alice question ' + str(68719476727))
        self.register_question_action(alice, 'Alice question ' + str(68719476726))
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 2},
                        {'user': 'alice', 'achievements_id': 3}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 2, 'count': 1},
                                {'id': 3, 'count': 1},
                                {'id': 30, 'count': 1},
                                {'id': 40, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()

    
    def test_post_answer(self):
        begin('test post answer (bronze, silver, gold) ahievements')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.register_question_action(alice, 'Alice question ' + str(68719476735))

        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))

        example_alice = [{'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        example_bob = [ {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50}, 
                        {'user': 'bob', 'achievements_id': 60}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476734))

        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        example_alice = [{'user': 'alice', 'achievements_id': 1}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50}, 
                        {'user': 'bob', 'achievements_id': 60}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476733))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476732))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476731))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 2}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 11},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 51},
                        {'user': 'bob', 'achievements_id': 52}, 
                        {'user': 'bob', 'achievements_id': 60},
                        {'user': 'bob', 'achievements_id': 61},
                        {'user': 'bob', 'achievements_id': 62}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476730))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476729))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476728))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476727))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.register_question_action(alice, 'Alice question ' + str(68719476726))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 2},
                        {'user': 'alice', 'achievements_id': 3}, 
                        {'user': 'alice', 'achievements_id': 30}, 
                        {'user': 'alice', 'achievements_id': 40}]
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 11},
                        {'user': 'bob', 'achievements_id': 12},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 51},
                        {'user': 'bob', 'achievements_id': 52}, 
                        {'user': 'bob', 'achievements_id': 60},
                        {'user': 'bob', 'achievements_id': 61},
                        {'user': 'bob', 'achievements_id': 62}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 2, 'count': 1},
                                {'id': 3, 'count': 1},
                                {'id': 10, 'count': 1},
                                {'id': 11, 'count': 1},
                                {'id': 12, 'count': 1},
                                {'id': 30, 'count': 2},
                                {'id': 31, 'count': 1},
                                {'id': 40, 'count': 2},
                                {'id': 41, 'count': 1},
                                {'id': 50, 'count': 1},
                                {'id': 51, 'count': 1},
                                {'id': 52, 'count': 1},
                                {'id': 60, 'count': 1},
                                {'id': 61, 'count': 1},
                                {'id': 62, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()

    def test_mark_correct_answer(self):
        begin('test mark correct answer (bronze, silver, gold) ahievements')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.register_question_action(alice, 'Alice question ' + str(68719476735))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark Carol answer as correct")

        example_alice = [{'user': 'alice', 'achievements_id': 30},
                        {'user': 'alice', 'achievements_id': 31}, 
                        {'user': 'alice', 'achievements_id': 40},
                        {'user': 'alice', 'achievements_id': 41}]
        example_bob = [ {'user': 'bob', 'achievements_id': 20},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50}, 
                        {'user': 'bob', 'achievements_id': 60}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476734))

        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark Carol answer as correct")
        

        self.register_question_action(alice, 'Alice question ' + str(68719476733))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark Carol answer as correct")
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 30},
                        {'user': 'alice', 'achievements_id': 31}, 
                        {'user': 'alice', 'achievements_id': 40},
                        {'user': 'alice', 'achievements_id': 41}]
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 20},
                        {'user': 'bob', 'achievements_id': 21},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 51}, 
                        {'user': 'bob', 'achievements_id': 60},
                        {'user': 'bob', 'achievements_id': 61}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))
        
        
        self.register_question_action(alice, 'Alice question ' + str(68719476732))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark Carol answer as correct")

        self.register_question_action(alice, 'Alice question ' + str(68719476731))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': True}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), question_id, 'answer without flag "official_answer"'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark Carol answer as correct")
        example_alice = [{'user': 'alice', 'achievements_id': 1},
                        {'user': 'alice', 'achievements_id': 2}, 
                        {'user': 'alice', 'achievements_id': 30},
                        {'user': 'alice', 'achievements_id': 31}, 
                        {'user': 'alice', 'achievements_id': 40},
                        {'user': 'alice', 'achievements_id': 41},]
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 11},
                        {'user': 'bob', 'achievements_id': 20},
                        {'user': 'bob', 'achievements_id': 21},
                        {'user': 'bob', 'achievements_id': 22},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 51},
                        {'user': 'bob', 'achievements_id': 52}, 
                        {'user': 'bob', 'achievements_id': 60},
                        {'user': 'bob', 'achievements_id': 61},
                        {'user': 'bob', 'achievements_id': 62}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 2, 'count': 1},
                                {'id': 10, 'count': 1},
                                {'id': 11, 'count': 1},
                                {'id': 20, 'count': 1},
                                {'id': 21, 'count': 1},
                                {'id': 22, 'count': 1},
                                {'id': 30, 'count': 2},
                                {'id': 31, 'count': 2},
                                {'id': 40, 'count': 2},
                                {'id': 41, 'count': 2},
                                {'id': 50, 'count': 1},
                                {'id': 51, 'count': 1},
                                {'id': 52, 'count': 1},
                                {'id': 60, 'count': 1},
                                {'id': 61, 'count': 1},
                                {'id': 62, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()


    
    def test_downvote_answer(self):
        begin('downvote answer (first answer + answer within_15_minutes) post answer and right away downvote x3. Max 1 first answer and answer within_15_minutes in moment')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.register_question_action(alice, 'Alice question ' + str(68719476735));
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        self.action('downvote', {'user': 'ted', 'question_id': question_id, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        
        self.register_question_action(alice, 'Alice question ' + str(68719476734));
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        self.action('downvote', {'user': 'ted', 'question_id': question_id, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        
        self.register_question_action(alice, 'Alice question ' + str(68719476733));
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        self.action('downvote', {'user': 'ted', 'question_id': question_id, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')

        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 60}]
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 10, 'count': 1},
                                {'id': 30, 'count': 4},
                                {'id': 31, 'count': 2},
                                {'id': 40, 'count': 4},
                                {'id': 41, 'count': 2},
                                {'id': 50, 'count': 1},
                                {'id': 60, 'count': 1}]
        print(self.table('achieve', 'allachieve'))
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()

    def test_downvote_upvote_answer(self):
        begin('downvote and upvote answer (first answer + answer within_15_minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()   

        self.register_question_action(alice, 'Alice question ' + str(68719476735));
        question_id_1 = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id_1, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id_1, 'Register Alice answer'))
        self.action('downvote', {'user': 'ted', 'question_id': question_id_1, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        
        self.register_question_action(alice, 'Alice question ' + str(68719476734));
        question_id_2 = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id_2, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id_2, 'Register Alice answer'))
        self.action('downvote', {'user': 'ted', 'question_id': question_id_2, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        self.action('upvote', {'user': 'ted', 'question_id': question_id_1, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        self.action('upvote', {'user': 'ted', 'question_id': question_id_2, 'answer_id': 1}, ted, 'ted downvote for Alice question->Bob answer rating')
        
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 60}]
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 10, 'count': 1},
                                {'id': 30, 'count': 3},
                                {'id': 31, 'count': 2},
                                {'id': 40, 'count': 3},
                                {'id': 41, 'count': 2},
                                {'id': 50, 'count': 1},
                                {'id': 60, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))

        self.register_question_action(alice, 'Alice question ' + str(68719476733));
        question_id_3 = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': str(bob), 'question_id': question_id_3, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id_3, 'Register Alice answer'))
        
        example_bob = [ {'user': 'bob', 'achievements_id': 10},
                        {'user': 'bob', 'achievements_id': 30}, 
                        {'user': 'bob', 'achievements_id': 31}, 
                        {'user': 'bob', 'achievements_id': 40}, 
                        {'user': 'bob', 'achievements_id': 41}, 
                        {'user': 'bob', 'achievements_id': 50},
                        {'user': 'bob', 'achievements_id': 51},
                        {'user': 'bob', 'achievements_id': 60},
                        {'user': 'bob', 'achievements_id': 61},]
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        example_achievement = [{'id': 1, 'count': 1},
                                {'id': 10, 'count': 1},
                                {'id': 30, 'count': 3},
                                {'id': 31, 'count': 2},
                                {'id': 40, 'count': 3},
                                {'id': 41, 'count': 2},
                                {'id': 50, 'count': 1},
                                {'id': 51, 'count': 1},
                                {'id': 60, 'count': 1},
                                {'id': 61, 'count': 1},]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()

    # def test_post_2questions_and_2answers(self):
    #     begin('post 2 questions and alice post 2 answers  (first answer + answer within_15_minutes)')
    #     alice = self.register_alice_account()
    #     bob = self.register_bob_account()

    #     self.register_question_action(alice, 'Alice question ' + str(68719476735))
    #     self.register_question_action(alice, 'Alice question ' + str(68719476734))
    #     self.action('postanswer', {'user': str(alice), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, alice,
    #                 '{} answer to question with id={}: "{}"'.format(str(alice), 68719476735, 'Register Alice answer'))
    #     self.action('postanswer', {'user': str(alice), 'question_id': 68719476734, 'ipfs_link': 'undefined', 'official_answer': False}, alice,
    #                 '{} answer to question with id={}: "{}"'.format(str(alice), 68719476734, 'Register Alice answer'))

    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1},
    #                     {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1},
    #                     {'user': 'alice', 'achievements_id': Achievents.answer_15_minutes.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.first_answer.value, 'value': 2}]
    #     print(self.table('accachieve', 'alice'))
    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1},
    #                     {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1},
    #                     {'user': 'alice', 'achievements_id': Achievents.answer_15_minutes.value, 'value': 2},
    #                     {'user': 'alice', 'achievements_id': Achievents.first_answer.value, 'value': 2}]
    #     print(self.table('accachieve', 'alice'))
    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

    #     table_achive = self.table('achieve', 'allachieve')
    #     example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 1}, {'id': Achievents.newbie.value, 'count': 1}, {'id': Achievents.answer_15_minutes.value, 'count': 1}, {'id': Achievents.first_answer.value, 'count': 1}]
    #     self.assertTrue(compare(example, table_achive, ignore_excess=True))
    #     end()

    # def test_post_questions_and_answers_2user(self):
    #     begin('post question and post answers 2 user (first answer + answer within_15_minutes)')
    #     bob = self.register_bob_account() 
    #     alice = self.register_alice_account()
       

    #     self.register_question_action(alice, 'Alice question ' + str(68719476735))
    #     self.action('postanswer', {'user': str(alice), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, alice,
    #                 '{} answer to question with id={}: "{}"'.format(str(alice), 68719476735, 'Register Alice answer'))
    #     self.wait(7)
    #     self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
    #                 '{} answer to question with id={}: "{}"'.format(str(bob), 68719476735, 'Register Alice answer'))

    #     print(self.table('accachieve', 'alice'))
    #     print(self.table('accachieve', 'bob'))
    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.answer_15_minutes.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_answer.value, 'value': 1}]
    #     example_bob = [{'user': 'bob', 'achievements_id': Achievents.answers_given.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
    #     self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

    #     table_achive = self.table('achieve', 'allachieve')
    #     print(self.table('achieve', 'allachieve'))
    #     example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 2}, {'id': Achievents.first_10k_registered.value, 'count': 2}, {'id': Achievents.newbie.value, 'count': 1}, {'id': Achievents.answer_15_minutes.value, 'count': 1}, {'id': Achievents.first_answer.value, 'count': 1}]
    #     self.assertTrue(compare(example, table_achive, ignore_excess=True))
    #     end()

    # def test_achievement_register_account(self):
    #     begin('test achievement register first 10 000 accounts')
    #     alice = self.register_alice_account()
    #     ted = self.register_ted_account()

    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
    #     example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]

    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
    #     self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

    #     example = [{'id': Achievents.first_10k_registered.value, 'count': 2}]
    #     table_achive = self.table('achieve', 'allachieve')
    #     self.assertTrue(compare(example, table_achive, ignore_excess=True))
    #     end()


    # def test_achievement_rating(self):
    #     begin('test init achievement rating')
    #     alice = self.register_alice_account(4999)
    #     ted = self.register_ted_account(11000)
    #     bob = self.register_bob_account(-5)
    #     admin = self.get_contract_deployer(self.get_default_contract())
    #     self._give_moderator_flag(ted, MODERATOR_FLG_ALL)    

    #     self.action('intachrating', {}, admin, 'init achievements rating in all accounts')   

    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.stranger.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.junior.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.resident.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.senior.value, 'value': 1}]
    #     example_bob = [{'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
    #     example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.stranger.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.newbie.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.junior.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.resident.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.senior.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.hero.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.superhero.value, 'value': 1}]

    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
    #     self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))
    #     self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

    #     example = [{'id': Achievents.first_10k_registered.value, 'count': 4}, {'id': Achievents.stranger.value, 'count': 2}, {'id': Achievents.newbie.value, 'count': 2}, {'id': Achievents.junior.value, 'count': 2}, {'id': Achievents.resident.value, 'count': 2}, {'id': Achievents.senior.value, 'count': 2}, {'id': Achievents.hero.value, 'count': 1}, {'id': Achievents.superhero.value, 'count': 1}]
    #     table_achievement = self.table('achieve', 'allachieve')
    #     self.assertTrue(compare(example, table_achievement, ignore_excess=True))
    #     end()


    # def test_init_achievement(self):
    #     begin('init achievements: questions_asked, answers_given, correct_answers')
    #     alice = self.register_alice_account(5000)
    #     admin = self.get_contract_deployer(self.get_default_contract())

    #     self.action('intallaccach', {}, admin, 'init achievements: questions_asked, answers_given, correct_answers in all accounts')
        
    #     example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 0},
    #                     {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 0},
    #                     {'user': 'alice', 'achievements_id': Achievents.correct_answers.value, 'value': 0},
    #                     {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
    #     self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

    #     example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.correct_answers.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 1}]
    #     table_achieve = self.table('achieve', 'allachieve')
    #     self.assertTrue(compare(example, table_achieve, ignore_excess=True))
    #     end()

    # def test_limit_achievement(self):
    #     begin('test limit question ask (limit 2)')
    #     alice = self.register_alice_account()
    #     bob = self.register_bob_account()
    #     carol = self.register_carol_account()
    #     ted = self.register_ted_account()

    #     self.register_question_action(alice, 'Alice question ' + str(68719476735))
    #     self.register_question_action(bob, 'bob question ' + str(68719476734))
    #     self.register_question_action(carol, 'carol question ' + str(68719476733))
    #     self.register_question_action(ted, 'ted question ' + str(68719476732)) 
        
    #     example = [{'id': Achievents.questions_asked.value, 'count': 2}, {'id': Achievents.first_10k_registered.value, 'count': 4}]
    #     table_achieve = self.table('achieve', 'allachieve')
    #     self.assertTrue(compare(example, table_achieve, ignore_excess=True))
    #     end()

    # def test_change_type_quesion(self):
    #     begin('test change type question')
    #     alice = self.register_alice_account()
    #     bob = self.register_bob_account()
    #     self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
        
        
    #     self.register_question_action(alice, 'ted question ' + str(68719476732))
    #     self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
    #                 '{} answer to question with id={}: "{}"'.format(str(alice), 68719476735, 'Register Alice answer'))

    #     print(self.table('accachieve', 'bob'))
    #     print(self.table('account', 'allaccounts'))

    #     question_id = self.table('question', 'allquestions')[0]['id']

    #     self.action('chgqsttype', {
    #                 'user': 'alice', 'question_id': question_id, 'type': 1, 'restore_rating': True}, alice, "Change question type to general")
        
    #     print("change type")
    #     print(self.table('account', 'allaccounts'))

    #     self.action('chgqsttype', {
    #                 'user': 'alice', 'question_id': question_id, 'type': 0, 'restore_rating': True}, alice, "Change question type to general")
        
    #     print("change type")
    #     print(self.table('account', 'allaccounts'))
        # example = [{'id': Achievents.questions_asked.value, 'count': 2}, {'id': Achievents.first_10k_registered.value, 'count': 4}]
        # table_achieve = self.table('achieve', 'allachieve')
        # self.assertTrue(compare(example, table_achieve, ignore_excess=True))
        # end()

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()