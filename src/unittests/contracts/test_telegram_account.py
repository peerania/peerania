import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6

class TestTopQuestion(peeranhatest.peeranhaTest):  
#     def test_add_telegram_account(self):
#         begin('test add telegram account')
#         alice = self.register_alice_account()
#         ted = self.register_ted_account()
#         bob = self.register_bob_account()

#         self.action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 503975561
#         }, ted, 'Alice add top question. Alice don t have permission')

#         self.wait(1)
#         self.failed_action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 503975561
#         }, ted, 'Alice add top question. Alice don t have permission') #повторное использование телеграм ид

#         self.failed_action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 1111111111
#         }, ted, 'Alice add top question. Alice don t have permission')  #повторное добавление в табл

#         self.failed_action('addtelacc', {
#         'bot_name': ted,
#         'user': bob,
#         'telegram_id': 503975561
#         }, ted, 'Alice add top question. Alice don t have permission')#повторное использование телеграм ид другим пользователем 

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)
#         end()

#     def test_appruve_telegram_account(self):
#         begin('test approve telegram account')
#         alice = self.register_alice_account()
#         ted = self.register_ted_account()
#         bob = self.register_bob_account()

#         self.action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 503975561
#         }, ted, 'Alice add top question. Alice don t have permission')

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

#         self.action('apprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')

#         self.wait(1)
#         self.failed_action('apprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission') #aprove again

#         self.failed_action('apprvacc', {
#         'user': bob
#         }, bob, 'Alice add top question. Alice don t have permission') #aprove nonexistent account 

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)
#         end()

#     def test_disappruve_telegram_account(self):
#         begin('test disapprove telegram account')
#         alice = self.register_alice_account()
#         ted = self.register_ted_account()
#         bob = self.register_bob_account()

#         self.action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 503975561
#         }, ted, 'Alice add top question. Alice don t have permission')

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)
        

#         self.action('dsapprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')

#         self.wait(1)
#         self.failed_action('dsapprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission') #aprove again

#         self.failed_action('dsapprvacc', {
#         'user': bob
#         }, bob, 'Alice add top question. Alice don t have permission') #aprove nonexistent account 

#         self.wait(2)
#         self.action('addtelacc', {
#         'bot_name': ted,
#         'user': alice,
#         'telegram_id': 503975562
#         }, ted, 'Alice add top question. Alice don t have permission')

#         self.action('apprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')

#         self.action('dsapprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)
#         end()


#     def test_post_question_telegram_account(self):
#         begin('test post question telegram account')
#         alice = self.register_alice_account()
#         bob = self.register_bob_account()

#         self.action('addtelacc', {
#         'bot_name': alice,
#         'user': alice,
#         'telegram_id': 503975561
#         }, alice, 'Alice add top question. Alice don t have permission')
#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

#         self.failed_action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
#                         'Register telegram question from alice')

#         self.action('apprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')
#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)
#         self.wait(1)
#         self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
#                         'Register telegram question from alice')

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

# # self.table('question', 'allquestions')[0]['id']
#         table_question = self.table('question', 'allquestions')
#         print(table_question)
#         end()

#     def test_post_answer_telegram_account(self):
#         begin('test post answer telegram account')
#         alice = self.register_alice_account()
#         bob = self.register_bob_account()

#         self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
#                     'Bob asking question')
#         id_question = self.table('question', 'allquestions')[0]['id']

#         self.action('addtelacc', {
#         'bot_name': alice,
#         'user': alice,
#         'telegram_id': 503975561
#         }, alice, 'Alice add top question. Alice don t have permission')
#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

#         self.failed_action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
#                         'Register telegram question from alice')
#         self.wait(1)

#         self.action('apprvacc', {
#         'user': alice
#         }, alice, 'Alice add top question. Alice don t have permission')
#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

#         self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
#                         'Register telegram question from alice')

#         table_telegram_account = self.table('telegramacc', 'alltelacc')
#         print(table_telegram_account)

# # self.table('question', 'allquestions')[0]['id']
#         table_question = self.table('question', 'allquestions')
#         print(table_question)
#         end()


    # def test_post_question_empty_telegram_account(self):
    #     begin('test post question empty telegram account')
    #     bob = self.register_bob_account()

    #     self.action('telpostqstn', {'bot': 'bob', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, bob,
    #                     'Register telegram question from alice')

    #     table_telegram_account = self.table('telegramacc', 'alltelacc')
    #     print(table_telegram_account)

    #     table_question = self.table('question', 'allquestions')
    #     print(table_question)

    #     print("+================================")
    #     t = self.table('account', 'allaccounts')
    #     print(t)
    #     end()

    # def test_post_answer_empty_telegram_account(self):
    #     begin('test post answer empty telegram account')
    #     bob = self.register_bob_account()

    #     self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
    #                 'Bob asking question')
    #     id_question = self.table('question', 'allquestions')[0]['id']

    #     self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
    #                     'Register telegram question from alice')

    #     table_telegram_account = self.table('telegramacc', 'alltelacc')
    #     print(table_telegram_account)

    #     table_question = self.table('question', 'allquestions')
    #     print(table_question)

    #     print("+================================")
    #     t = self.table('account', 'allaccounts')
    #     print(t)
    #     end()
    
    # def test_post_question_empty_telegram_account_move_account(self):
    #     begin('test post question empty telegram account')
    #     ted = self.register_ted_account()
    #     alice = self.register_alice_account()

    #     self.action('telpostqstn', {'bot': 'ted', 'telegram_id': 503975561, 'title': 'telegram', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, ted,
    #                     'Register telegram question from alice')

    #     table_telegram_account = self.table('telegramacc', 'alltelacc')
    #     print(table_telegram_account)

    #     table_question = self.table('question', 'allquestions')
    #     print(table_question)

    #     t = self.table('account', 'allaccounts')
    #     print(t)
    #     print("+=====================----------------------------------------===========")

    #     self.action('addtelacc', {
    #     'bot_name': ted,
    #     'user': alice,
    #     'telegram_id': 503975561
    #     }, ted, 'Alice add top question. Alice don t have permission')

    #     table_telegram_account = self.table('telegramacc', 'alltelacc')
    #     print(table_telegram_account)

    #     self.action('apprvacc', {
    #     'user': alice
    #     }, alice, 'Alice add top question. Alice don t have permission')

    #     table_telegram_account = self.table('telegramacc', 'alltelacc')
    #     print(table_telegram_account)

    #     table_question = self.table('question', 'allquestions')
    #     print(table_question)

    #     t = self.table('account', 'allaccounts')
    #     print(t)
    #     end()


    def test_post_answer_empty_telegram_account(self):
        begin('test post answer empty telegram account')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()

        self.action('postquestion', {'user': 'bob', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, bob,
                    'Bob asking question')
        id_question = self.table('question', 'allquestions')[0]['id']

        self.action('telpostansw', {'bot': 'bob', 'telegram_id': 503975561, 'question_id': id_question, 'ipfs_link': 'undefined', 'official_answer': 0}, bob,
                        'Register telegram question from alice')

        table_telegram_account = self.table('telegramacc', 'alltelacc')
        print(table_telegram_account)

        table_question = self.table('question', 'allquestions')
        print(table_question)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.action('addtelacc', {
        'bot_name': ted,
        'user': alice,
        'telegram_id': 503975561
        }, ted, 'Alice add top question. Alice don t have permission')
        
        table_telegram_account = self.table('telegramacc', 'alltelacc')
        print(table_telegram_account)

        self.action('apprvacc', {
        'user': alice
        }, alice, 'Alice add top question. Alice don t have permission')

        table_telegram_account = self.table('telegramacc', 'alltelacc')
        print(table_telegram_account)

        table_question = self.table('question', 'allquestions')
        print(table_question)

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        t = self.table('account', 'allaccounts')
        print(t)
        end()

    

if __name__ == '__main__':
    main()