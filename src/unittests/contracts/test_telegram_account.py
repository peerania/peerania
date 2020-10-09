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

COMMUNITY_ADMIN_FLG_INFINITE_IMPACT = 1 << 1        # 2

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
        }, ted, 'Alice add telegram account 503975561')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975562
        }, ted, 'Alice telegram account 503975562, Alice is already have telegram account') #повторное использование телеграм ид

        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 1111111111
        }, ted, 'Alice add telegram account 503975561 again')  #повторное добавление в табл

        self.failed_action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'Bob add telegram account 503975561, telegram id is already added')#повторное использование телеграм ид другим пользователем 
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
        }, ted, 'Alice add telegram account 503975561')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 1}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account again')

        self.failed_action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram nonexistent account')
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
        }, ted, 'Alice add telegram account 503975561')
        example = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice disapprove telegram account')
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare([], table_telegram_account, ignore_excess=True))

        self.wait(1)
        self.failed_action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice disapprove telegram account again')

        self.failed_action('dsapprvacc', {
            'user': bob
        }, bob, 'Bob disapprove nonexistent telegram account')

        self.wait(2)
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975562
        }, ted, 'Alice add telegram account 503975562')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
        example = [{'user': 'alice', 'telegram_id': 503975562, 'confirmed': 1}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice disapprove telegram account after approve')
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
        }, alice, 'Alice add telegram account 503975561')

        self.failed_action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice, telegram account don`t approve')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
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
        }, alice, 'Alice add telegram account 503975561')

        self.failed_action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram answer from alice, telegram account don`t approve')
        self.wait(1)

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')

        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram answer from alice')
        example_answer = [{'id': 1, 'user': 'alice'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))
        end()

    def test_post_question_empty_telegram_account(self):
        begin('test post question empty telegram account')
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Register telegram answer from alice')
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

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Register telegram answer from alice')
        
        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram answer from alice')
        
        print(self.table('telegramacc', 'alltelacc'))
        print(self.table('account', 'allaccounts'))

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

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Register telegram answer from alice')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')

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
        }, ted, 'Alice add telegram account 503975561')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')

        example = [{'id': '68719476735', 'user': 'alice', 'title': 'telegram'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question, ignore_excess=True))
        end()


    def test_post_answer_empty_telegram_account_move_account(self):
        begin('test post answer empty telegram account move author answer')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Register telegram answer from alice')
        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram answer from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': 1, 'user': name_empty_account}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question[0]["answers"], ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')

        example = [{'id': 1, 'user': 'alice'}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example, table_question[0]["answers"], ignore_excess=True))
        end()


    def test_post_question_answer_empty_account_move_data(self):
        begin('test post question empty telegram account move author question')
        ted = self.register_ted_account()
        alice = self.register_alice_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Register telegram answer from alice')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from alice')

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
        example_achive_amount = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 3}, {'id': Achievents.answer_15_minutes.value, 'count': 1}, {'id': Achievents.first_answer.value, 'count': 1}]
        self.assertTrue(compare(example_achive_amount, self.table('achieve', 'allachieve'), ignore_excess=True))
        # ____________________________________________________________before_______________________________________________________

        self.action('addtelacc', {
        'bot_name': ted,
        'user': alice,
        'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')
        self.action('apprvacc', {
        'user': alice
        }, alice, 'Alice approve telegram account')
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
        example_achive_amount = [{'id': Achievents.questions_asked.value, 'count': 1}, {'id': Achievents.answers_given.value, 'count': 1}, {'id': Achievents.first_10k_registered.value, 'count': 2}, {'id': Achievents.answer_15_minutes.value, 'count': 1}, {'id': Achievents.first_answer.value, 'count': 1}]
        self.assertTrue(compare(example_achive_amount, self.table('achieve', 'allachieve'), ignore_excess=True))
        end()

    # def test_clear_table_telegram_account(self):
    #     begin('test clear table telegram account')
    #     alice = self.register_alice_account()
    #     ted = self.register_ted_account()

        # self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
        #                 'Register telegram answer from alice')
    #     self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
    #                     'Register telegram question from alice')
    #     name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
    #     print(self.table('telegramacc', 'alltelacc'))
        
    #     self.action('addtelacc', {
    #         'bot_name': ted,
    #         'user': alice,
    #         'telegram_id': 503975561
    #     }, ted, 'Alice add telegram account 503975561')        

    #     example_tel_account = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}, {'user': name_empty_account, 'telegram_id': 503975561, 'confirmed': 2}]
    #     print(self.table('telegramacc', 'alltelacc'))
    #     self.assertTrue(compare(example_tel_account, print(self.table('telegramacc', 'alltelacc')), ignore_excess=True))
        

    #     self.action('apprvacc', {
    #         'user': alice
    #     }, alice, 'Alice approve telegram account')
    #     example_tel_account = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}, {'user': name_empty_account, 'telegram_id': 503975561, 'confirmed': 2}]
    #     self.assertTrue(compare(example_tel_account, print(self.table('telegramacc', 'alltelacc')), ignore_excess=True))
    #     end()

    # def test_clear_table_telegram_account(self):
    #     begin('test clear_table_telegram_account')
    #     admin = self.get_contract_deployer(self.get_default_contract())
    #     alice = self.register_alice_account()
    #     ted = self.register_ted_account()

        # self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
        #                 'Register telegram answer from alice')
    #     self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
    #                     'Register telegram question from alice')
    #     name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
    #     print(self.table('telegramacc', 'alltelacc'))
        
    #     self.action('addtelacc', {
    #         'bot_name': ted,
    #         'user': alice,
    #         'telegram_id': 503975561
    #     }, ted, 'Alice add telegram account 503975561')


        
    #     self.wait(2)

    #     self.action('givecommuflg', {
    #     'user': name_empty_account,
    #     'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
    #     'community_id': 1
    #     }, admin, 'add a flag in wrong community')

    #     print(self.table('propertycomm', 'allprprtcomm'))
    #     print(self.table('periodrating', name_empty_account))
        

    #     # print(self.table('telegramacc', 'alltelacc'))
    #     # print(self.table('account', 'allaccounts'))

    #     self.action('apprvacc', {
    #         'user': alice
    #     }, alice, 'Alice approve telegram account')
    #     # print(self.table('telegramacc', 'alltelacc'))
    #     # print(self.table('account', 'allaccounts'))
    #     print(self.table('propertycomm', 'allprprtcomm'))
    #     end()

    # def test_clear_table_telegram_account(self):
    #     begin('test clear_table_telegram_account')
    #     admin = self.get_contract_deployer(self.get_default_contract())
    #     alice = self.register_alice_account()
    #     ted = self.register_ted_account()

        # self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
        #                 'Register telegram answer from alice')
    #     self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
    #                     'Register telegram question from alice')
    #     name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
    #     print(self.table('telegramacc', 'alltelacc'))
        
    #     self.action('addtelacc', {
    #         'bot_name': ted,
    #         'user': alice,
    #         'telegram_id': 503975561
    #     }, ted, 'Alice add telegram account 503975561')


        
    #     self.wait(2)

    #     self.action('givecommuflg', {
    #     'user': name_empty_account,
    #     'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
    #     'community_id': 1
    #     }, admin, 'add a flag in wrong community')

    #     print(self.table('propertycomm', 'allprprtcomm'))
    #     print(self.table('periodrating', name_empty_account))
        

    #     # print(self.table('telegramacc', 'alltelacc'))
    #     # print(self.table('account', 'allaccounts'))

    #     self.action('apprvacc', {
    #         'user': alice
    #     }, alice, 'Alice approve telegram account')
    #     # print(self.table('telegramacc', 'alltelacc'))
    #     # print(self.table('account', 'allaccounts'))
    #     print(self.table('propertycomm', 'allprprtcomm'))
    #     end()


    # def test_communities(self):
    #     begin('test communities')
    #     alice = self.register_alice_account()
    #     ted = self.register_ted_account()
    #     # admin = self.get_contract_deployer(self.get_default_contract())
    #     self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
    #     # editcomm(eosio::name user, uint16_t community_id, std::string name, IpfsHash ipfs_link)

    #     print(self.table('communities', 'allcomm'))
        
    #     self.action('editcomm', {
    #         'user': alice,
    #         'community_id': 1,
    #         'name': 'testtesttest',
    #         'ipfs_link': 'alice_IPFS'
    #     }, alice, 'Alice add top question. Alice don t have permission')
    #     print(self.table('communities', 'allcomm'))
        
    #     end()
    
    # def _give_moderator_flag(self, acc, flg):
    #     admin = self.get_contract_deployer(self.get_default_contract())
    #     self.action('givemoderflg', {
    #             'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

    

if __name__ == '__main__':
    main()