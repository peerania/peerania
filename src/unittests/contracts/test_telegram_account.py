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
        self.assertTrue(compare(example, self.table('telegramacc', 'alltelacc'), ignore_excess=True))

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
        self.assertTrue(compare(example, self.table('telegramacc', 'alltelacc'), ignore_excess=True))

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
        self.assertTrue(compare(example, self.table('telegramacc', 'alltelacc'), ignore_excess=True))
        

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice disapprove telegram account')
        self.assertTrue(compare([], self.table('telegramacc', 'alltelacc'), ignore_excess=True))

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
        self.assertTrue(compare(example, self.table('telegramacc', 'alltelacc'), ignore_excess=True))

        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Alice disapprove telegram account after approve')
        self.assertTrue(compare([], self.table('telegramacc', 'alltelacc'), ignore_excess=True))
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
        self.assertTrue(compare(example, self.table('question', 'allquestions'), ignore_excess=True))
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

    def test_add_empty_account_through_telegram(self):
        begin('test add empty account through telegram')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.failed_action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice, account not add')

        self.action('addtelacc', {
            'bot_name': alice,
            'user': alice,
            'telegram_id': 503975561
        }, alice, 'Alice add telegram account 503975561')

        self.failed_action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Add empty account through telegram, telegram id already added')
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': ted,
            'telegram_id': 503975562
        }, ted, 'Ted add telegram account 503975561')

        self.action('apprvacc', {
            'user': ted
        }, ted, 'Ted approve telegram account')
        
        self.failed_action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Add empty account through telegram, telegram id already added')

        self.action('dsapprvacc', {
            'user': ted
        }, ted, 'Ted approve telegram account')
        self.action('dsapprvacc', {
            'user': alice
        }, alice, 'Ted approve telegram account')

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975562, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Add empty account through telegram')

        example = [{'telegram_id': 503975562, 'confirmed': 2}]
        self.assertTrue(compare(example, self.table('telegramacc', 'alltelacc'), ignore_excess=True))
        end()
    
    def test_post_question_empty_telegram_account(self):
        begin('test post question empty telegram account')
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Add empty account through telegram')
        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': '68719476735', 'user': name_empty_account, 'title': 'telegram'}]
        self.assertTrue(compare(example, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_post_answer_empty_telegram_account(self):
        begin('test post answer empty telegram account')
        bob = self.register_bob_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('addemptelacc', {'bot_name': 'bob', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, bob,
                        'Add empty account through telegram')
        
        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram answer from alice')

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
                        'Add empty account through telegram')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')

        example = [{'telegram_id': 503975561, 'confirmed': 2}]
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        self.assertTrue(compare(example, table_telegram_account, ignore_excess=True))
        name_empty_account = table_telegram_account[0]['user']

        example = [{'id': '68719476735', 'user': name_empty_account, 'title': 'telegram'}]
        self.assertTrue(compare(example, self.table('question', 'allquestions'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')

        example = [{'id': '68719476735', 'user': 'alice', 'title': 'telegram'}]
        self.assertTrue(compare(example, self.table('question', 'allquestions'), ignore_excess=True))
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
                        'Add empty account through telegram')
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
                        'Add empty account through telegram')
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
        example_alice = [{'user': name_empty_account, 'achievements_id': Achievents.questions_asked.value, 'value': 1}, 
                        {'user': name_empty_account, 'achievements_id': Achievents.answers_given.value, 'value': 1}, 
                        {'user': name_empty_account, 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, 
                        {'user': name_empty_account, 'achievements_id': Achievents.answer_15_minutes.value, 'value': 1}, 
                        {'user': name_empty_account, 'achievements_id': Achievents.first_answer.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', name_empty_account), ignore_excess=True))
        example_achive_amount = [{'id': Achievents.questions_asked.value, 'count': 1}, 
                                {'id': Achievents.answers_given.value, 'count': 1}, 
                                {'id': Achievents.first_10k_registered.value, 'count': 3}, # first_10k_registered = 3 || 4
                                {'id': Achievents.answer_15_minutes.value, 'count': 1}, 
                                {'id': Achievents.first_answer.value, 'count': 1}]
        self.assertTrue(compare(example_achive_amount, self.table('achieve', 'allachieve'), ignore_excess=True))
        example_account = [{'user': 'alice', 'questions_asked': 0, 'answers_given': 0, 'correct_answers': 0}, 
                            {'user': 'ted'}, 
                            {'user': name_empty_account, 'questions_asked': 1, 'answers_given': 1, 'correct_answers': 0}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        
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
        example_alice = [{'user': 'alice', 'achievements_id': Achievents.questions_asked.value, 'value': 1}, 
                        {'user': 'alice', 'achievements_id': Achievents.answers_given.value, 'value': 1}, 
                        {'user': 'alice', 'achievements_id': Achievents.first_10k_registered.value, 'value': 1}, 
                        {'user': 'alice', 'achievements_id': Achievents.answer_15_minutes.value, 'value': 1}, 
                        {'user': 'alice', 'achievements_id': Achievents.first_answer.value, 'value': 1}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accachieve', name_empty_account), ignore_excess=True))
        example_achive_amount = [{'id': Achievents.questions_asked.value, 'count': 1}, 
                                {'id': Achievents.answers_given.value, 'count': 1}, 
                                {'id': Achievents.first_10k_registered.value, 'count': 2}, #first_10k_registered = 2 || 3
                                {'id': Achievents.answer_15_minutes.value, 'count': 1}, 
                                {'id': Achievents.first_answer.value, 'count': 1}]
        self.assertTrue(compare(example_achive_amount, self.table('achieve', 'allachieve'), ignore_excess=True))
        example_account = [{'user': 'alice', 'questions_asked': 1, 'answers_given': 1, 'correct_answers': 0}, {'user': 'ted'}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_clear_table_telegram_account(self):
        begin('test clear table telegram account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')        

        example_tel_account = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 0}, {'user': name_empty_account, 'telegram_id': 503975561, 'confirmed': 2}]
        self.assertTrue(compare(example_tel_account, self.table('telegramacc', 'alltelacc'), ignore_excess=True))        

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
        example_tel_account = [{'user': 'alice', 'telegram_id': 503975561, 'confirmed': 1}]
        self.assertTrue(compare(example_tel_account, self.table('telegramacc', 'alltelacc'), ignore_excess=True))
        end()

    def test_clear_table_property_community(self):
        begin('test clear_table_property_community')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        self.action('givecommuflg', {
        'user': name_empty_account,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        'community_id': 1
        }, admin, 'add a flag in wrong community')
        self.action('givecommuflg', {
        'user': name_empty_account,
        'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        'community_id': 2
        }, admin, 'add a flag in wrong community')

        example_property_community = [{'user': name_empty_account, 'properties': [{'community': 1, 'value': 2}, {'community': 2, 'value': 2}]}]
        self.assertTrue(compare(example_property_community, self.table('propertycomm', 'allprprtcomm')))
        
        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
        self.assertTrue(compare([], self.table('propertycomm', 'allprprtcomm')))
        end()

    def test_clear_table_account(self):
        begin('test clear_table_account')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        name_empty_account = self.table('telegramacc', 'alltelacc')[0]['user']
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        example_account = [{'user': 'alice'}, {'user': 'ted'}, {'user': name_empty_account}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account')
        example_account = [{'user': 'alice'}, {'user': 'ted'}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_mark_empty_user_answer_question(self):
        begin('test mark empty user, empty user post answer and question (property: key = 15)')
        ted = self.register_ted_account()
        bob = self.register_bob_account()
        
        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975562
        }, ted, 'bob add telegram account 503975562')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'bob approve telegram account')
        
        example_account = [{'user': 'bob', 'integer_properties': [],}, 
                            {'user': 'ted', 'integer_properties': [],}, 
                            {'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from alice, telegram account don`t approve')

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975562, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from bob')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975562, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')

        example_question = [{'id': id_question, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}], 'properties': []},
                            {'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}, {'key': 15, 'value': 1}]}], 'properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_mark_empty_answer_question(self):
        begin('test mark, empty user post answer and question (property: key = 15)')
        ted = self.register_ted_account()
        bob = self.register_bob_account()
        
        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        
        example_account = [{'user': 'bob', 'integer_properties': [],}, 
                            {'user': 'ted', 'integer_properties': [],}, 
                            {'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
                        'Register telegram question from alice')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                    'Asking question from alice with text "Alice question"')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from alice, telegram account don`t approve')

        example_question = [{'id': id_question, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}, {'key': 15, 'value': 1}]}], 'properties': []},
                            {'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}], 'properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()
        
if __name__ == '__main__':
    main()