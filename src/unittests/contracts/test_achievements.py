import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

MODERATOR_FLG_ALL = 31

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
    superhero = 11

class TestAchievents(peeranhatest.peeranhaTest):  
    def test_post_question_answer_mark_correct_ansewer(self):
        begin('test post question, answer, mark correct answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()      

        self.register_question_action(alice, 'Alice question ' + str(68719476735))

        self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), 68719476735, 'Register Alice answer'))
        self.action('mrkascorrect', {'user': alice, 'question_id': 68719476735,
                                     'answer_id': 1}, str(alice), 'Alice mark bob answer as correct')

        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        example_bob = [{'user': 'bob', 'achievements_id': Achievents.answers_given.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.correct_answers.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.newbie.value, 'value': 1}]

        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))

        table_achieve = self.table('achieve', 'allachieve')
        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.correct_answers.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 2}, {'id': Achievents.newbie.value, 'count': 2}]
        self.assertTrue(compare(example, table_achieve, ignore_excess=True))
        end()
    

    def test_moderator_delete_question(self):
        begin('moderator delete question with correct answer')

        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)       

        self.register_question_action(alice, 'Alice question ' + str(68719476735))

        self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), 68719476735, 'Register Bob answer'))
        self.action('mrkascorrect', {'user': alice, 'question_id': 68719476735,
                                     'answer_id': 1}, str(alice), 'Alice mark bob answer as correct')
        self.action('reportforum', {'user': 'ted', 'question_id': 68719476735, 'answer_id': 0, 'comment_id': 0},
                    ted, 'Bob vote for Alice question deletion')
        
        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.correct_answers.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        example_bob = [{'user': 'bob', 'achievements_id': Achievents.answers_given.value, 'value': 0}, {'user': 'bob', 'achievements_id': Achievents.correct_answers.value, 'value': 0}, {'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]

        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))
        self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

        table_achive = self.table('achieve', 'allachieve')
        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 2}, {'id': Achievents.correct_answers.value, 'count': 2}, {'id': Achievents.first_10k_registered.value, 'count': 3}, {'id': Achievents.newbie.value, 'count': 2}]
        self.assertTrue(compare(example, table_achive, ignore_excess=True))
        end()


    def test_delete_question(self):
        begin('delete question')
        alice = self.register_alice_account()    

        self.register_question_action(alice, 'Alice question ' + str(68719476735))
        self.action('delquestion', {
                    'user': 'alice', 'question_id': 68719476735}, alice, "Delete alice question")

        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        table_achive = self.table('achieve', 'allachieve')
        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 1}, {'id': Achievents.newbie.value, 'count': 1}]
        self.assertTrue(compare(example, table_achive, ignore_excess=True))
        end()


    def test_moderator_delete_answer(self):
        begin('moderator delete answer with correct answer')
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)       

        self.register_question_action(alice, 'Alice question ' + str(68719476735));
        self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), 68719476735, 'Register Bob answer')) 
        self.action('mrkascorrect', {'user': alice, 'question_id': 68719476735,
                                     'answer_id': 1}, str(alice), 'Alice mark bob answer as correct')
        self.action('reportforum', {'user': 'ted', 'question_id': 68719476735, 'answer_id': 1, 'comment_id': 0},
                    ted, 'Ted deleted Bob answer')
        
        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        example_bob = [{'user': 'bob', 'achievements_id': Achievents.questions_asked.value, 'value': 0}, {'user': 'bob', 'achievements_id': Achievents.answers_given.value, 'value': 0}, {'user': 'bob', 'achievements_id': Achievents.correct_answers.value, 'value': 0}, {'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'bob', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]

        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))
        self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

        table_achive = self.table('achieve', 'allachieve')
        example = [{'id': Achievents.questions_asked.value, 'count': 2}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.correct_answers.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 3}, {'id': Achievents.newbie.value, 'count': 2}]
        self.assertTrue(compare(example, table_achive, ignore_excess=True))
        end()

    def test_delete_answer(self):
        begin('delete answer')
        alice = self.register_alice_account()    

        self.register_question_action(alice, 'Alice question ' + str(68719476735));
        self.action('postanswer', {'user': str(alice), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), 68719476735, 'Register Alice answer'))
        self.action('delanswer', {'user': 'alice', 'question_id': 68719476735, 'answer_id': 1}, alice, 'Delete Alice answer to Alice question')

        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        table_achive = self.table('achieve', 'allachieve')
        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 1}, {'id': Achievents.newbie.value, 'count': 1}]
        self.assertTrue(compare(example, table_achive, ignore_excess=True))
        end()


    def test_achievement_register_account(self):
        begin('test achievement register first 10 000 accounts')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        example_alice = [{'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
        example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]

        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

        example = [{'id': Achievents.first_10k_registered.value, 'count': 2}]
        table_achive = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achive, ignore_excess=True))
        end()


    def test_achievement_rating(self):
        begin('test init achievement rating')
        alice = self.register_alice_account(4999)
        ted = self.register_ted_account(11000)
        bob = self.register_bob_account(-5)
        admin = self.get_contract_deployer(self.get_default_contract())
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)    

        self.action('intachrating', {}, admin, 'init achievements rating in all accounts')   

        example_alice = [{'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.stranger.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.newbie.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.junior.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.resident.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.senior.value, 'value': 1}]
        example_bob = [{'user': 'bob', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
        example_ted = [{'user': 'ted', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.stranger.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.newbie.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.junior.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.resident.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.senior.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.hero.value, 'value': 1}, {'user': 'ted', 'achievements_id': Achievents.superhero.value, 'value': 1}]

        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare(example_bob, self.table('accachieve', 'bob'), ignore_excess=True))
        self.assertTrue(compare(example_ted, self.table('accachieve', 'ted'), ignore_excess=True))

        example = [{'id': Achievents.first_10k_registered.value, 'count': 4}, {'id': Achievents.stranger.value, 'count': 2}, {'id': Achievents.newbie.value, 'count': 2}, {'id': Achievents.junior.value, 'count': 2}, {'id': Achievents.resident.value, 'count': 2}, {'id': Achievents.senior.value, 'count': 2}, {'id': Achievents.hero.value, 'count': 1}, {'id': Achievents.superhero.value, 'count': 1}]
        table_achievement = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achievement, ignore_excess=True))
        end()


    def test_init_achievement(self):
        begin('init achievements: questions_asked, answers_given, correct_answers')
        alice = self.register_alice_account(5000)
        admin = self.get_contract_deployer(self.get_default_contract())

        self.action('intallaccach', {}, admin, 'init achievements: questions_asked, answers_given, correct_answers in all accounts')
        
        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.correct_answers.value, 'value': 0}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))

        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.correct_answers.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 1}]
        table_achieve = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achieve, ignore_excess=True))
        end()

    def test_limit_achievement(self):
        begin('test limit question ask (limit 2)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        ted = self.register_ted_account()

        self.register_question_action(alice, 'Alice question ' + str(68719476735))
        self.register_question_action(bob, 'bob question ' + str(68719476734))
        self.register_question_action(carol, 'carol question ' + str(68719476733))
        self.register_question_action(ted, 'ted question ' + str(68719476732)) 
        
        example = [{'id': Achievents.questions_asked.value, 'count': 2}, {'id': Achievents.first_10k_registered.value, 'count': 4}]
        table_achieve = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achieve, ignore_excess=True))
        end()

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()