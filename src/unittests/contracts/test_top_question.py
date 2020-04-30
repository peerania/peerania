import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

class TestTopQuestion(peeranhatest.peeranhaTest):  
    def test_add_to_top_community(self):
        begin('test add to top community')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        self.register_question_action(alice, 'Alice question 68719476735')
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']

        self.failed_action('addtotopcomm', {
        'user': 'peeranhamain',
        'community_id': 2,
        'question_id': question_id
        }, admin, 'add a question from another community')

        self.action('addtotopcomm', {
        'user': 'peeranhamain',
        'community_id': community_id,
        'question_id': question_id
        }, admin, 'add community 1, question ' + str(question_id))
        example = [{'community_id': 1,'top_questions': ['68719476735']}]
        check_table(self, example)

        self.wait(2)
        self.failed_action('addtotopcomm', {
        'user': 'peeranhamain',
        'community_id': community_id,
        'question_id': question_id
        }, admin, 'again add community 1, question ' + str(question_id))

        self.failed_action('addtotopcomm', {
        'user': 'peeranhamain',
        'community_id': 1,
        'question_id': 11111
        }, admin, 'add a nonexistent question')
        end()

    def test_limit_top_questions(self):
        begin('test limit top questions')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        max_size = 26
        for w in range(max_size):
            self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))

            question_id = self.table('question', 'allquestions')[0]['id']
            community_id = self.table('question', 'allquestions')[0]['community_id']
            self.action('addtotopcomm', {
                'user': 'peeranhamain',
                'community_id': community_id,
                'question_id': question_id
                }, admin, 'add community 1, question ' + str(community_id))

        self.register_question_action(alice, 'Alice question ' + str(68719476735 - max_size -1))
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']
        self.failed_action('addtotopcomm', {
            'user': 'peeranhamain',
            'community_id': community_id,
            'question_id': question_id
            }, admin, 'add community 1, question ' + str(community_id))
        end()

    def test_remove_question_from_best_community(self):
        begin('test remove question from best community')
        admin = self.get_contract_deployer(self.get_default_contract())
        install_table(self)
        
        self.action('remfrmtopcom', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476735
            }, admin, 'remove a first question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476733', '68719476732', '68719476731']}]
        check_table(self, example)

        self.action('remfrmtopcom', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476731
            }, admin, 'remove a last question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476733', '68719476732']}]
        check_table(self, example)

        self.action('remfrmtopcom', {
            'user': 'peeranhamain',
            'community_id': 2,
            'question_id': 68719476731
            }, admin, 'remove a question from another community')
        check_table(self, example)

        self.failed_action('remfrmtopcom', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 1111
            }, admin, 'remove a nonexistent question')
        end()

    def test_up_top_question(self):
        begin('test up top a question')
        admin = self.get_contract_deployer(self.get_default_contract())
        install_table(self)
        
        self.action('upquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476733
            }, admin, 'up a question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476733', '68719476734', '68719476732', '68719476731']}]
        check_table(self, example)

        self.failed_action('upquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476735
            }, admin, 'up a first question')

        self.action('upquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476731
            }, admin, 'up a last question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476733', '68719476734', '68719476731', '68719476732']}]
        check_table(self, example)
       
        self.failed_action('upquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 1111
            }, admin, 'up a nonexistent question')

        self.action('remfrmtopcom', {
            'user': 'peeranhamain',
            'community_id': 2,
            'question_id': 68719476731
            }, admin, 'up a question from another community')
        check_table(self, example)
        end()

    def test_down_top_question(self):
        begin('test down top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        install_table(self)
        
        self.action('downquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476733
            }, admin, 'down a question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476734', '68719476732', '68719476733', '68719476731']}]
        check_table(self, example)

        self.action('downquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476735
            }, admin, 'down a first question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476735', '68719476732', '68719476733', '68719476731']}]
        check_table(self, example)

        self.failed_action('downquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476731
            }, admin, 'down a last question')

        self.failed_action('downquestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 1111
            }, admin, 'down a nonexistent question')

        self.action('downquestion', {
            'user': 'peeranhamain',
            'community_id': 2,
            'question_id': 68719476732
            }, admin, 'down a question from another community')
        check_table(self, example)
        end()

    def test_move_top_question(self):
        begin('test move top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        install_table(self)
        
        self.action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476733,
            'new_position': 1
            },admin, 'move question on first position')
        example = [{'community_id': 1, 'top_questions': ['68719476733', '68719476735', '68719476734', '68719476732', '68719476731']}]
        check_table(self, example)

        self.failed_action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476734,
            'new_position': -1
            },admin, 'move a question on negative position')

        self.failed_action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476734,
            'new_position': 0
            },admin, 'move a question on zero position')

        self.action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 68719476734,
            'new_position': 5
            },admin, 'move a question on last position')
        example = [{'community_id': 1, 'top_questions': ['68719476733', '68719476735', '68719476732', '68719476731', '68719476734']}]
        check_table(self, example)

        self.failed_action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 1,
            'question_id': 1111,
            'new_position': 3
            },admin, 'move a nonexistent question')

        self.action('movequestion', {
            'user': 'peeranhamain',
            'community_id': 2,
            'question_id': 68719476734,
            'new_position': 3
            },admin, 'move a question from another community')
        check_table(self, example)
        end()

def check_table(self, examplee):
    table = self.table('topquestion', 'alltopquest')
    self.assertTrue(compare(examplee, table, ignore_excess=True))

def install_table(self):
    begin('install table')
    admin = self.get_contract_deployer(self.get_default_contract())
    alice = self.register_alice_account()

    for w in range(5):
        self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']
        self.action('addtotopcomm', {
            'user': 'peeranhamain',
            'community_id': community_id,
            'question_id': question_id
            }, admin, 'add community 1, question ' + str(community_id))

    top = self.table('topquestion', 'alltopquest')
    example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476734', '68719476733', '68719476732', '68719476731']}]
    print("test intall table")
    self.assertTrue(compare(example, top, ignore_excess=True))

if __name__ == '__main__':
    main()