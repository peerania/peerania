import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from time import time
from enum import Enum

MODERATOR_FLG_ALL = 31


# questions_asked = 1
# answers_given = 2
# correct_answers = 3
# first_10k_registered = 4
# stranger = 5

# newbie = 6
# junior = 7
# resident = 8
# resident = 8
# resident = 8

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
        begin('test post and delete question, answer, mark correct ansewer')
       
        # admin = self.get_contract_deployer(self.get_default_contract())

        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_ALL)       

        # self.action('intallaccach', {}, admin, 'Alice add top question. Alice don t have permission')

        table_achive = self.table('accachieve', 'allaccachieve')
        print(table_achive)

        self.register_question_action(alice, 'Alice question ' + str(68719476735));

        self.action('postanswer', {'user': str(bob), 'question_id': 68719476735, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(bob), 68719476735, 'Register Alice answer'))
        
        
        self.action('mrkascorrect', {'user': alice, 'question_id': 68719476735,
                                     'answer_id': 1}, str(alice), 'Alice mark bob answer as correct')

        table_achive = self.table('accachieve', 'allaccachieve')
        print(table_achive)

        print('==============================================')

        table_acc_achive = self.table('accachieve', 'allaccachieve')
        
        example = [{'user': 'alice', 'user_achievements': [{'achievements_id': 1, 'value': 1}]}, 
                {'user': 'bob', 'user_achievements': [{'achievements_id': 2, 'value': 1}, {'achievements_id': 3, 'value': 1}]}]
        
        print(table_acc_achive)

        print(self.table('account', 'allaccounts'))
        # print(example)
        # self.assertTrue(compare(example, table_acc_achive, ignore_excess=True))

        

        # self.action('reportforum', {'user': 'ted', 'question_id': 68719476735, 'answer_id': 1, 'comment_id': 0},
        #             ted, 'Bob vote for Alice question deletion')
        
        # table_acc_achive = self.table('accachieve', 'allaccachieve')
        # example = [{'user': 'alice', 'user_achievements': [{'achievements_id': 1, 'value': 1, 'date': 1597752813}]}, 
        #             {'user': 'bob', 'user_achievements': [
        #                 {'achievements_id': 2, 'value': 0, 'date': 1597752813}, 
        #                 {'achievements_id': 3, 'value': 0, 'date': 1597752813}, 
        #                 {'achievements_id': 1, 'value': 0, 'date': 1597752813}]}]
        # self.assertTrue(compare(example, table_acc_achive, ignore_excess=True))


        # table_achive = self.table('accachieve', 'allaccachieve')
        # print(table_achive)

        # print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
        # self.action('intachregusr', {}, admin, 'Alice add top question. Alice don t have permission')

        # table_achive = self.table('accachieve', 'allaccachieve')
        # print(table_achive)

        table_squeezed_achievement = self.table('achieve', 'allachieve')
        print(table_squeezed_achievement)

        # table_squeezed_achievement = self.table('achieve', 'allachieve')
        # example = [{'id': 1, 'count': 1}, {'id': 2, 'count': 1}, {'id': 3, 'count': 1}]
        # self.assertTrue(compare(example, table_squeezed_achievement, ignore_excess=True))
        end()
    
    def test_achievement_register_account(self):
        begin('test achievement register first 10 000 accounts')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        example = [ {'user': 'alice', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}, 
                    {'user': 'peeranhamain', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}, 
                    {'user': 'ted', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}] 
        table_account_achive = self.table('accachieve', 'allaccachieve')
        self.assertTrue(compare(example, table_account_achive, ignore_excess=True))

        example = [{'id': Achievents.first_10k_registered.value, 'count': 3}]
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

        self.action('intachrating', {}, admin, 'Alice add top question. Alice don t have permission')   

        example = [ {'user': 'alice', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'achievements_id': Achievents.stranger.value, 'value': 1}, {'achievements_id': Achievents.newbie.value, 'value': 1}, {'achievements_id': Achievents.junior.value, 'value': 1}, {'achievements_id': Achievents.resident.value, 'value': 1}, {'achievements_id': Achievents.senior.value, 'value': 1}]}, 
                    {'user': 'bob', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}, 
                    {'user': 'peeranhamain', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}, 
                    {'user': 'ted', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'achievements_id': Achievents.stranger.value, 'value': 1}, {'achievements_id': Achievents.newbie.value, 'value': 1}, {'achievements_id': Achievents.junior.value, 'value': 1}, {'achievements_id': Achievents.resident.value, 'value': 1}, {'achievements_id': Achievents.senior.value, 'value': 1}, {'achievements_id': Achievents.hero.value, 'value': 1}, {'achievements_id': Achievents.superhero.value, 'value': 1}]}]
        table_account_achive = self.table('accachieve', 'allaccachieve')
        self.assertTrue(compare(example, table_account_achive, ignore_excess=True))

        example = [{'id': Achievents.first_10k_registered.value, 'count': 4}, {'id': Achievents.stranger.value, 'count': 2}, {'id': Achievents.newbie.value, 'count': 2}, {'id': Achievents.junior.value, 'count': 2}, {'id': Achievents.resident.value, 'count': 2}, {'id': Achievents.senior.value, 'count': 2}, {'id': Achievents.hero.value, 'count': 1}, {'id': Achievents.superhero.value, 'count': 1}]
        table_achievement = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achievement, ignore_excess=True))
        end()

    def test_init_achievement(self):
        begin('init achievement: questions_asked, answers_given, correct_answers')

        alice = self.register_alice_account(5000)
        admin = self.get_contract_deployer(self.get_default_contract())

        self.action('intallaccach', {}, admin, 'Alice add top question. Alice don t have permission')
        
        example = [ {'user': 'alice', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'achievements_id': Achievents.questions_asked.value, 'value': 0}, {'achievements_id': Achievents.answers_given.value, 'value': 0}, {'achievements_id': Achievents.correct_answers.value, 'value': 0}]}, 
                    {'user': 'peeranhamain', 'user_achievements': [{'achievements_id': Achievents.first_10k_registered.value, 'value': 1}]}]
        table_account_achive = self.table('accachieve', 'allaccachieve')
        self.assertTrue(compare(example, table_account_achive, ignore_excess=True))


        example = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.correct_answers.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 2}]
        table_achieve = self.table('achieve', 'allachieve')
        self.assertTrue(compare(example, table_achieve, ignore_excess=True))
        end()



    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()