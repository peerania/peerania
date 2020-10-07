import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

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

COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6

class TestTopQuestion(peeranhatest.peeranhaTest):  
    def test_add_telegram_account(self):
        begin('test add telegram account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission') #повторное использование телеграм ид

        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 1111111111
        }, ted, 'Alice add top question. Alice don t have permission')  #повторное добавление в табл

        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')#повторное использование телеграм ид другим пользователем 
        end()

    def test_appruve_telegram_account(self):
        begin('test approve telegram account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 1}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission') #aprove again

        self.failed_action('apprvacc', {
            'user': bob
        }, bob, 'Alice add top question. Alice don t have permission') #aprove nonexistent account 
        end()

    def test_disappruve_telegram_account(self):
        begin('test disapprove telegram account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare([], table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission') #aprove again

        self.failed_action('dsapprvacc', {
            'user': bob
        }, bob, 'Alice add top question. Alice don t have permission') #aprove nonexistent account 

        self.wait(2)
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975562
        }, ted, 'Alice add top question. Alice don t have permission')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        example = [{'user': 'alice', 'telegram_id': 503975562, 'confirmed': 1}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare([], table_telegram_account, ignore_excess=True))
        end()

    def test_post_question_telegram_account(self):
        begin('test post question telegram account')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.action('addtelacc', {
            'bot_name': alice,
            'user': alice,
            'telegram_id': 503975561
        }, alice, 'Alice add top question. Alice don t have permission')

        self.failed_action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        self.wait(1)

        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice')
        example = [{'id': '68719476735', 'user': 'alice', 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question, ignore_excess=True))
        end()

    def test_post_answer_telegram_account(self):
        begin('test post answer telegram account')
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('addtelacc', {
            'bot_name': alice,
            'user': alice,
            'telegram_id': 503975561
        }, alice, 'Alice add top question. Alice don t have permission')

        self.failed_action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram question from alice')
        self.wait(1)

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')

        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram question from alice')
        example_answer = [{'id': 1, 'user': 'alice'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))
        end()

    def test_post_question_empty_telegram_account(self):
        begin('test post question empty telegram account')
        bob = self.register_bob_account()

        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': '68719476735', 'user': name_empty_account, 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question, ignore_excess=True))
        end()

    def test_post_answer_empty_telegram_account(self):
        begin('test post answer empty telegram account')
        bob = self.register_bob_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram question from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': 1, 'user': name_empty_account}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question[0]["answers"], ignore_excess=True))
        end()
    
    def test_post_question_empty_telegram_account_move_account(self):
        begin('test post question empty telegram account move author question')
        ted = self.register_ted_account()
        alice = self.register_alice_account()

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')

        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)
        # table_question = self.table('question', 'allquestions')
        # print(table_question)
        # t = self.table('account', 'allaccounts')
        # print(t)
        # print("+=====================----------------------------------------===========")

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': '68719476735', 'user': name_empty_account, 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question, ignore_excess=True))

        self.action('addtelacc', {
        'bot_name': ted,
        'user': alice,
        'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')

        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)

        self.action('apprvacc', {
        'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')

        example = [{'id': '68719476735', 'user': 'alice', 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question, ignore_excess=True))

        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)
        # table_question = self.table('question', 'allquestions')
        # print(table_question)
        # t = self.table('account', 'allaccounts')
        # print(t)
        end()


    def test_post_answer_empty_telegram_account_move_account(self):
        begin('test post answer empty telegram account move author answer')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram question from alice')

        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': 1, 'user': name_empty_account}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question[0]["answers"], ignore_excess=True))

        table_question = self.table('question', 'allquestions')
        # print(table_question)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.action('addtelacc', {
        'bot_name': ted,
        'user': alice,
        'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        
        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)

        self.action('apprvacc', {
        'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')

        example = [{'id': 1, 'user': 'alice'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question[0]["answers"], ignore_excess=True))

        # table_telegram_account = self.table('telegramacc', 'alltelacc')
        # print(table_telegram_account)
        # table_question = self.table('question', 'allquestions')
        # print(table_question)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # t = self.table('account', 'allaccounts')
        # print(t)
        end()


    def test_post_question_answer_empty_account_move_data(self):
        begin('test post question empty telegram account move author question')
        ted = self.register_ted_account()
        alice = self.register_alice_account()

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram question from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example_question = [{'id': '68719476735', 'user': name_empty_account, 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_question, table_question, ignore_excess=True))
        example_answer = [{'id': 1, 'user': name_empty_account}]
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))

        example_usrquestions = [{'question_id': '68719476735'}]
        example_usranswers = [{'question_id': '68719476735', 'answer_id': 1}]
        self.assertTrue(compare(example_usrquestions, self.table('usrquestions', name_empty_account), ignore_excess=True))
        self.assertTrue(compare(example_usranswers, self.table('usranswers', name_empty_account), ignore_excess=True))
        example_alice = [{'user': name_empty_account, 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': name_empty_account, 'achievements_id': Achievents.answers_given.value, 'value': 1}, {'user': name_empty_account, 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': name_empty_account, 'achievements_id': Achievents.answer_15_minutes.value, 'value': 1}, {'user': name_empty_account, 'achievements_id': Achievents.first_answer.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', name_empty_account), ignore_excess=True))
        # ____________________________________________________________before_______________________________________________________

        self.action('addtelacc', {
        'bot_name': ted,
        'user': alice,
        'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        self.action('apprvacc', {
        'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')
        # ____________________________________________________________after_______________________________________________________
        example_question = [{'id': '68719476735', 'user': 'alice', 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_question, table_question, ignore_excess=True))
        example_answer = [{'id': 1, 'user': 'alice'}]
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))

        example_usrquestions = [{'question_id': '68719476735'}]
        example_usranswers = [{'question_id': '68719476735', 'answer_id': 1}]
        self.assertTrue(compare(example_usrquestions, self.table('usrquestions', alice), ignore_excess=True))
        self.assertTrue(compare(example_usranswers, self.table('usranswers', alice), ignore_excess=True))
        self.assertTrue(compare([], self.table('usrquestions', name_empty_account), ignore_excess=True))
        self.assertTrue(compare([], self.table('usranswers', name_empty_account), ignore_excess=True))
        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.answer_15_minutes.value, 'value': 1}, {'user': 'alice', 'achievements_id': Achievents.first_answer.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accachieve', name_empty_account), ignore_excess=True))
        end()










    def test_clear_table_telegram_account(self):
        begin('test clear_table_telegram_account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')

        
        # table_telegram_account = self.table('account', 'allaccounts')
        # print(table_telegram_account)
        print(self.table('telegramacc', 'alltelacc'))
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        
        # table_telegram_account = self.table('account', 'allaccounts')
        # print(table_telegram_account)
        print(self.table('telegramacc', 'alltelacc'))

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')

        # table_telegram_account = self.table('account', 'allaccounts')
        # print(table_telegram_account)
        print(self.table('telegramacc', 'alltelacc'))
        end()

    

if __name__ == '__main__':
    main()