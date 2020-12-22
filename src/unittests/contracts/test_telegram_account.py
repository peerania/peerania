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
BASIC_RATING = 200

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
    
    def test_disappruve_telegram_account_through_telegram(self):
        begin('test disapprove telegram account through_telegram')
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

        self.action('dsapprvacctl', {
            'bot_name': ted,
            'user': alice
        }, ted, 'Alice disapprove telegram account')
        self.assertTrue(compare([], self.table('telegramacc', 'alltelacc'), ignore_excess=True))

        self.wait(1)
        self.failed_action('dsapprvacctl', {
            'bot_name': ted,
            'user': alice
        }, ted, 'Alice disapprove telegram account again')

        self.failed_action('dsapprvacctl', {
            'bot_name': ted,
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

        self.action('dsapprvacctl', {
            'bot_name': ted,
            'user': alice
        }, ted, 'Alice disapprove telegram account after approve')
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
        carol = self.register_carol_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        self.action('postquestion', {'user': 'carol', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, carol,
                    'carol asking question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
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

        example_question = [{'id': '68719476734', 'user': name_empty_account, 'title': 'telegram'}, {'id': '68719476735', 'user': carol}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_question, table_question, ignore_excess=True))
        example_answer = [{'id': 1, 'user': name_empty_account}]
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))

        example_usrquestions = [{'question_id': '68719476734'}]
        example_usranswers = [{'question_id': '68719476734', 'answer_id': 1}, {'question_id': '68719476735', 'answer_id': 1}]
        self.assertTrue(compare(example_usrquestions, self.table('usrquestions', name_empty_account), ignore_excess=True))
        self.assertTrue(compare(example_usranswers, self.table('usranswers', name_empty_account), ignore_excess=True))

        example_empty_account = [   {'user': name_empty_account, 'achievements_id': 10},
                                    {'user': name_empty_account, 'achievements_id': 30},
                                    {'user': name_empty_account, 'achievements_id': 40},
                                    {'user': name_empty_account, 'achievements_id': 50},
                                    {'user': name_empty_account, 'achievements_id': 60}]
        self.assertTrue(compare(example_empty_account, self.table('accachieve', name_empty_account), ignore_excess=True))
        example_alice = [   {'user': alice, 'achievements_id': 30},
                            {'user': alice, 'achievements_id': 40}]
        self.assertTrue(compare(example_alice, self.table('accachieve', alice), ignore_excess=True))
        example_achievement = [ {'id': 10, 'count': 1},
                                {'id': 30, 'count': 4}, # 4 // 5
                                {'id': 40, 'count': 4}, # 4 // 5
                                {'id': 50, 'count': 1},
                                {'id': 60, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        example_account = [{'user': 'alice', 'questions_asked': 0, 'answers_given': 0, 'correct_answers': 0}, 
                            {'user': 'carol'},
                            {'user': 'ted'}, 
                            {'user': name_empty_account, 'questions_asked': 1, 'answers_given': 2, 'correct_answers': 0}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        example_count_user = [{'version': 1, 'user_count': 5}]
        self.assertTrue(compare(example_count_user, self.table('globalstat', 'allstat'), ignore_excess=True))
        
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
        example_question = [{'id': '68719476734', 'user': 'alice', 'title': 'telegram'}, {'id': '68719476735', 'user': carol}]
        table_question = self.table('question', 'allquestions')
        self.assertTrue(compare(example_question, table_question, ignore_excess=True))
        example_answer = [{'id': 1, 'user': 'alice'}]
        self.assertTrue(compare(example_answer, table_question[0]["answers"], ignore_excess=True))

        example_usrquestions = [{'question_id': '68719476734'}]
        example_usranswers = [{'question_id': '68719476734', 'answer_id': 1}, {'question_id': '68719476735', 'answer_id': 1}]
        self.assertTrue(compare(example_usrquestions, self.table('usrquestions', alice), ignore_excess=True))
        self.assertTrue(compare(example_usranswers, self.table('usranswers', alice), ignore_excess=True))
        self.assertTrue(compare([], self.table('usrquestions', name_empty_account), ignore_excess=True))
        self.assertTrue(compare([], self.table('usranswers', name_empty_account), ignore_excess=True))
        example_alice = [   {'user': alice, 'achievements_id': 10},
                            {'user': alice, 'achievements_id': 30},
                            {'user': alice, 'achievements_id': 40},
                            {'user': alice, 'achievements_id': 50},
                            {'user': alice, 'achievements_id': 60}]
        self.assertTrue(compare(example_alice, self.table('accachieve', 'alice'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accachieve', name_empty_account), ignore_excess=True))
        example_achievement = [ {'id': 10, 'count': 1},
                                {'id': 30, 'count': 3}, # 3 // 4
                                {'id': 40, 'count': 3}, # 3 // 4
                                {'id': 50, 'count': 1},
                                {'id': 60, 'count': 1}]
        self.assertTrue(compare(example_achievement, self.table('achieve', 'allachieve'), ignore_excess=True))
        example_account = [{'user': 'alice', 'questions_asked': 1, 'answers_given': 2, 'correct_answers': 0}, {'user': 'carol'}, {'user': 'ted'}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        example_count_user = [{'version': 1, 'user_count': 4}]
        self.assertTrue(compare(example_count_user, self.table('globalstat', 'allstat'), ignore_excess=True))
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

        example_question = [{'id': id_question, 'answers': [{'id': 1, 'properties': [{'key': 16, 'value': 1}]}], 'properties': [{'key': 16, 'value': 1}]},
                            {'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}], 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}]
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

        example_question = [{'id': id_question, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}, {'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}], 'properties': []},
                            {'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 12, 'value': 1}, {'key': 13, 'value': 1}]}], 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_change_mark_value_empty_question_answer(self):
        begin('change the flag value of an empty question/answer (property: key = 15 value = 1 -> value = 0)')
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
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')

        example_question = [{'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}], 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        self.action('apprvacc', {
            'user': bob
        }, bob, 'Alice approve telegram account')

        example_question = [{'id': id_question_empty_acc, 'answers': [{'id': 1, 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 0}]}], 'properties': [{'key': 16, 'value': 1}, {'key': 15, 'value': 0}]}]
        self.assertTrue(compare(example_question, self.table('question', 'allquestions'), ignore_excess=True))
        end()
    
    def test_move_account_vote_answer_for_yourself(self):
        begin('user upvote answer  empty account and move his. Take away rating')
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        # general question
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')
        self.action('postanswer', {'user': 'ted', 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': False}, ted,
                    'Register bob answer')
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 1}, bob, "Bob upvote bob answer")
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 2}, bob, "Ted upvote bob answer")

        self.wait(3)
        # expert question
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                    'Bob asking question')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')
        self.action('postanswer', {'user': 'ted', 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': False}, ted,
                    'Register bob answer')
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 1}, bob, "Bob upvote bob answer")
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 2}, bob, "Ted upvote bob answer")           
        
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        example_account = [ {'user': 'bob', 'rating': 200}, 
                            {'user': 'ted', 'rating': 218},                 # (general) 15min + upvote + (expert)15min + upvote (1 + 2 + 5 + 10)
                            {'user': name_empty_account, 'rating': 34}]     # (general) 15min + first + upvote + (expert) 15min + first + upvote (1 + 1 + 2 + 5 + 5 + 10) = 24 + 10(start rating) 
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')
        example_account = [ {'user': 'bob', 'rating': 200},                     #move account -> take away rating empty account (vote yourself)
                            {'user': 'ted', 'rating': 218}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_move_account_mark_correct_answer_yourself(self):
        begin('user mark correct answer  empty account and move his. Take away rating')
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')

        # general question
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')
        self.action('postanswer', {'user': 'ted', 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': False}, ted,
                    'Register bob answer')
        self.action('mrkascorrect', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 1}, bob, "bob mark empty answer as correct")
        
        self.wait(3)
        # expert question
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                    'Bob asking question')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer from bob, telegram account don`t approve')
        self.action('postanswer', {'user': 'ted', 'question_id': id_question_empty_acc, 'ipfs_link': 'undefined', 'official_answer': False}, ted,
                    'Register bob answer')
        self.action('mrkascorrect', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 1}, bob, "bob mark empty answer as correct")

        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        example_account = [ {'user': 'bob', 'rating': 203},                 # (general) ACCEPT_ANSWER_AS_CORRECT_REWARD(1 rating) + (expert) ACCEPT_ANSWER_AS_CORRECT_REWARD (2 rating)
                            {'user': 'ted', 'rating': 206},                 # (general) 15min + (expert) 15min (1 + 5)
                            {'user': name_empty_account, 'rating': 40}]     # (general) 15min + first + ANSWER_ACCEPTED_AS_CORRECT_REWARD(3 rating) + (expert) 15min + first + ANSWER_ACCEPTED_AS_CORRECT_REWARD (15rating) (1 + 1 + 3 + 5 + 5 + 15) = 29 + 10(start rating)
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [ {'user': 'bob', 'rating': 200},                     #move account -> take away rating empty account (vote yourself)
                            {'user': 'ted', 'rating': 206}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_move_account_user_vote_mark_correct_answer(self):
        begin('user mark correct/vote answer -> move account. Check user rating ')
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'ted', 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': False}, ted,
                    'Register bob answer')
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question, 'answer_id': 1}, bob, "Bob upvote bob answer")
        self.action('mrkascorrect', {
                    'user': 'bob', 'question_id': id_question, 'answer_id': 1}, bob, "bob mark empty answer as correct")

        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        example_account = [ {'user': 'bob', 'rating': 201},                 # ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD(1 rating)
                            {'user': 'ted', 'rating': 207},                 # 15min + first + upvote + COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD (1 + 1 + 2 +3)
                            {'user': name_empty_account, 'rating': 10}]     
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')
        example_account = [ {'user': 'bob', 'rating': 201},                     
                            {'user': 'ted', 'rating': 207}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_move_account_vote_question_for_yourself(self):
        begin('user upvote question empty account and move his. Take away rating')
        ted = self.register_ted_account()
        bob = self.register_bob_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        # general question
        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                        'Register telegram question from alice, telegram account don`t approve')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 0}, bob, "Bob upvote bob answer")
        self.wait(3)
        # expert question
        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question from alice, telegram account don`t approve')
        id_question_empty_acc = self.table('question', 'allquestions')[0]['id']
        self.action('upvote', {
                    'user': 'bob', 'question_id': id_question_empty_acc, 'answer_id': 0}, bob, "Bob upvote bob answer")         
        
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        example_account = [ {'user': 'bob', 'rating': 200}, 
                            {'user': 'ted', 'rating': 200},
                            {'user': name_empty_account, 'rating': 16}]     # (general) upvote(5) + (expert) upvote (1)
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')
        example_account = [ {'user': 'bob', 'rating': 200},                     #move account -> take away rating empty account (vote yourself)
                            {'user': 'ted', 'rating': 200}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_change_display_name_empty_account(self):
        begin('change display name empty account')
        ted = self.register_ted_account()

        self.failed_action('updtdsplname', {'bot_name': 'ted', 'telegram_id': 111111111, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Сhange name emзty account, telegram account nonexistent')

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account')
        self.action('updtdsplname', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Сhange name emty account')

        name_empty_account = self.table('account', 'allaccounts')[1]['user']
        example_account = [ {'user': 'ted', 'display_name': 'tedDispName'},
                            {'user': name_empty_account, 'display_name': 'newName'}]  
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_change_display_name_connected_account(self):
        begin('change display name connected telegram account')
        bob = self.register_bob_account()
        ted = self.register_ted_account()
        
        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account')
        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')

        self.failed_action('updtdsplname', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Сhange display name, telegram account don`t approve')
        
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')
        example_account = [ {'user': 'bob', 'display_name': 'bobDispName'},
                            {'user': 'ted', 'display_name': 'tedDispName'}]  
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.wait(3)
        self.action('updtdsplname', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Сhange bob display name through telegram')
        example_account = [ {'user': 'bob', 'display_name': 'newName'},
                            {'user': 'ted', 'display_name': 'tedDispName'}]  
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_2_answer_from_1_user(self):
        begin('empty telegram account post question and post answer -> user1 post answer -> appruve telegram account with user1')
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        
        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer')
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_answer = [{'question_id': id_question, 'answer_id': 2}]
        self.assertTrue(compare(example_answer, self.table('usranswers', bob), ignore_excess=True))
        end()

    def test_2_answer_from_1_user_part2(self):
        begin('user1 post question and post answer -> empty tel acc post answer -> appruve telegram account with user1')
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        
        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')
        self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                        'Register telegram answer')
        

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_answer = [{'question_id': id_question, 'answer_id': 1}]
        self.assertTrue(compare(example_answer, self.table('usranswers', bob), ignore_excess=True))
        end()
    
    def test_take_away_rating_for_first_answer(self):
        begin('user1 post question and post answer -> empty tel acc post answer -> appruve telegram account with user1')
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        
        self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')

        example_account = [{'user': bob, 'rating': 210}, #first answer + 15 min
                            {'rating': 200},
                            {'rating': 10}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [{'user': bob, 'rating': 200},
                            {'rating': 200},]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_transfer_properties_telegram_account(self):
        begin('transfer properties of Telegram account on merge (first answer + 15 minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[3]['user']
        
        for w in range(5):
            self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))
            question_id = self.table('question', 'allquestions')[0]['id']
            self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                            'Register telegram answer')

        example_account = [{'user': alice, 'integer_properties': []},
                            { 'user': bob, 'integer_properties': []},
                            { 'user': ted, 'integer_properties': []},
                            { 'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}, {'key': 12, 'value': 5}, {'key': 13, 'value': 5}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [{'user': alice, 'integer_properties': []},
                            { 'user': bob, 'integer_properties': [ {'key': 13, 'value': 5}, {'key': 12, 'value': 5}]},
                            { 'user': ted, 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_transfer_properties_telegram_account_2(self):
        begin('keep account property on merge (first answer + 15 minutes)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[3]['user']
        
        for w in range(5):
            self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))
            question_id = self.table('question', 'allquestions')[0]['id']
            self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')

        example_account = [{'user': alice, 'integer_properties': []},
                            { 'user': bob, 'integer_properties': [{'key': 12, 'value': 5}, {'key': 13, 'value': 5}]},
                            { 'user': ted, 'integer_properties': []},
                            { 'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [{'user': alice, 'integer_properties': []},
                            { 'user': bob, 'integer_properties': [{'key': 12, 'value': 5}, {'key': 13, 'value': 5}]},
                            { 'user': ted, 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_take_away_properties_telegram_account_3(self):
        begin('take away properties telegram account on merge')
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        
        for w in range(5):
            self.register_question_action(bob, 'Alice question ' + str(68719476735 - w))
            question_id = self.table('question', 'allquestions')[0]['id']
            self.action('telpostansw', {'bot': 'ted', 'telegram_id': 503975561, 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': 0}, ted,
                            'Register telegram answer')

        example_account = [{ 'user': bob, 'integer_properties': []},
                            { 'user': ted, 'integer_properties': []},
                            { 'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}, {'key': 12, 'value': 5}, {'key': 13, 'value': 5}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [{ 'user': bob, 'integer_properties': [{'key': 13, 'value': 0}, {'key': 12, 'value': 0}]},
                            { 'user': ted, 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_take_away_properties_telegram_account_4(self):
        begin('take away properties account on merge')
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        name_empty_account = self.table('account', 'allaccounts')[2]['user']
        
        for w in range(5):
            self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
                        'Register telegram question')
            question_id = self.table('question', 'allquestions')[0]['id']
            self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    'Register bob answer')
            self.wait(1)

        example_account = [{ 'user': bob, 'integer_properties': [{'key': 12, 'value': 5}, {'key': 13, 'value': 5}]},
                            { 'user': ted, 'integer_properties': []},
                            { 'user': name_empty_account, 'integer_properties': [{'key': 15, 'value': 1}]}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))

        self.action('addtelacc', {
            'bot_name': ted,
            'user': bob,
            'telegram_id': 503975561
        }, ted, 'bob  add telegram account 503975561')
        self.action('apprvacc', {
            'user': bob
        }, bob, 'Bob approve telegram account')

        example_account = [{ 'user': bob, 'integer_properties': [{'key': 12, 'value': 0}, {'key': 13, 'value': 0}]},
                            { 'user': ted, 'integer_properties': []}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()

    def test_move_negative_rating(self):
        begin('move_negative_rating')
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('addemptelacc', {'bot_name': 'ted', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, ted,
                        'Add empty account through telegram')
        empty_account = self.table('account', 'allaccounts')[2]['user']
        self.action('chnguserrt', {'user': empty_account, 'rating_change': -5},
                            self.admin, 'decrease empty account rating')
        
        self.action('addtelacc', {
            'bot_name': ted,
            'user': alice,
            'telegram_id': 503975561
        }, ted, 'Alice add telegram account 503975561')
        self.action('apprvacc', {
            'user': alice
        }, alice, 'Alice approve telegram account, rating is not subtracted')
        
        example_account = [{'user': 'alice', 'rating': BASIC_RATING}, {'user': 'ted'}]
        self.assertTrue(compare(example_account, self.table('account', 'allaccounts'), ignore_excess=True))
        end()
        
if __name__ == '__main__':
    main()