import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION = 1 << 6
limit_question = 101

class TestTopQuestion(peeranhatest.peeranhaTest):  
    def test_add_to_top_community(self):
        begin('test add to top community')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        self.register_question_action(alice, 'Alice question 68719476735')
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']

        self.failed_action('addtotopcomm', {
        'user': alice,
        'community_id': community_id,
        'question_id': question_id
        }, alice, 'Alice add top question. Alice don t have permission')
        self.wait(1)
        
        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 2
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 2, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.failed_action('addtotopcomm', {
        'user': alice,
        'community_id': 2,
        'question_id': question_id
        }, alice, 'add a question from another community')

        self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 2, 'value': 64}, {'community': 1, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('addtotopcomm', {
        'user': alice,
        'community_id': community_id,
        'question_id': question_id
        }, alice, 'add community 1, question ' + str(question_id))
        example = [{'community_id': 1,'top_questions': ['68719476735']}]
        check_table(self, example)

        self.wait(2)
        self.failed_action('addtotopcomm', {
        'user': alice,
        'community_id': community_id,
        'question_id': question_id
        }, alice, 'again add community 1, question ' + str(question_id))

        self.failed_action('addtotopcomm', {
        'user': alice,
        'community_id': 1,
        'question_id': 11111
        }, alice, 'add a nonexistent question')
        end()

    def test_limit_top_questions(self):
        begin('test limit top questions')
        alice = self.register_alice_account()
        admin = self.get_contract_deployer(self.get_default_contract())

        self.action('givecommuflg', {
        'user': alice,
        'flags': 255,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 255}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        for w in range(limit_question):
            self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))

            question_id = self.table('question', 'allquestions')[0]['id']
            community_id = self.table('question', 'allquestions')[0]['community_id']
            self.action('addtotopcomm', {
                'user': alice,
                'community_id': community_id,
                'question_id': question_id
                }, alice, 'add community 1, question ' + str(community_id))

        self.register_question_action(alice, 'Alice question ' + str(68719476735 - limit_question -1))
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']
        self.failed_action('addtotopcomm', {
            'user': alice,
            'community_id': community_id,
            'question_id': question_id
            }, alice, 'add community 1, question ' + str(community_id))
        end()

    def test_remove_question_from_best_community(self):
        begin('test remove question from best community')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        install_table(self)
        
        self.failed_action('remfrmtopcom', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476735
            }, bob, 'remove a question without rights')
        self.wait(1)

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 64}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))
        
        self.action('remfrmtopcom', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476735
            }, bob, 'remove a first question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476733', '68719476732', '68719476731']}]
        check_table(self, example)

        self.action('remfrmtopcom', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476731
            }, bob, 'remove a last question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476733', '68719476732']}]
        check_table(self, example)

        self.failed_action('remfrmtopcom', {
            'user': bob,
            'community_id': 2,
            'question_id': 68719476731
            }, bob, 'remove a question from another community')

        self.failed_action('remfrmtopcom', {
            'user': bob,
            'community_id': 1,
            'question_id': 1111
            }, bob, 'remove a nonexistent question')
        end()

    def test_delete_top_question(self):
        begin('test delete top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()

        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
            'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')

        e = [self.register_question_action(bob, 'Alice question 1', 'q1')]
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addtotopcomm', {
            'user': bob,
            'community_id': 1,
            'question_id': question_id
        }, bob, 'add a question from another community')
        example = [{'community_id': 1, 'top_questions': [question_id]}]
        check_table(self, example)

        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('delquestion', {
                    'user': 'bob', 'question_id': var['q1']}, bob, 'Delete Alice question')

        example = [{'community_id': 1, 'top_questions': []}]
        check_table(self, example)
        end()

    def test_moderator_delete_top_question(self):
        begin('test moderator delete top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        alice = self.register_alice_account()

        self.action('givecommuflg', {
            'user': alice,
            'flags': 255,
            'community_id': 1
        }, admin, 'add a all community flag')

        e = [self.register_question_action(bob, 'Alice question 1', 'q1')]
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('addtotopcomm', {
            'user': alice,
            'community_id': 1,
            'question_id': question_id
        }, alice, 'add a top question')
        example = [{'community_id': 1, 'top_questions': [question_id]}]
        check_table(self, example)

        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('reportforum', {'user': 'alice', 'question_id': question_id, 'answer_id': 0, 'comment_id': 0},
                    alice, 'Alice delete bob question')

        example = [{'community_id': 1, 'top_questions': []}]
        check_table(self, example)
        end()

    def test_up_top_question(self):
        begin('test up top a question')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        install_table(self)
        
        self.failed_action('upquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733
            }, bob, 'up a question without rights')
        self.wait(1)

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 64}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))

        self.action('upquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733
            }, bob, 'up a question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476733', '68719476734', '68719476732', '68719476731']}]
        check_table(self, example)

        self.failed_action('upquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476735
            }, bob, 'up a first question')

        self.action('upquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476731
            }, bob, 'up a last question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476733', '68719476734', '68719476731', '68719476732']}]
        check_table(self, example)
       
        self.failed_action('upquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 1111
            }, bob, 'up a nonexistent question')

        self.failed_action('remfrmtopcom', {
            'user': bob,
            'community_id': 2,
            'question_id': 68719476731
            }, bob, 'up a question from another community')
        end()

    def test_down_top_question(self):
        begin('test down top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        install_table(self)
        
        self.failed_action('downquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733
            }, bob, 'down a question without rights')
        self.wait(1)

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 64}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))
        
        self.action('downquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733
            }, bob, 'down a question')
        example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476734', '68719476732', '68719476733', '68719476731']}]
        check_table(self, example)

        self.action('downquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476735
            }, bob, 'down a first question')
        example = [{'community_id': 1, 'top_questions': ['68719476734', '68719476735', '68719476732', '68719476733', '68719476731']}]
        check_table(self, example)

        self.failed_action('downquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476731
            }, bob, 'down a last question')

        self.failed_action('downquestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 1111
            }, bob, 'down a nonexistent question')

        self.failed_action('downquestion', {
            'user': bob,
            'community_id': 2,
            'question_id': 68719476732
            }, bob, 'down a question from another community')
        end()

    def test_move_top_question(self):
        begin('test move top question')
        admin = self.get_contract_deployer(self.get_default_contract())
        bob = self.register_bob_account()
        install_table(self)
        
        self.failed_action('movequestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733,
            'new_position': 1
            },bob, 'move question  without rights')
        self.wait(1)

        self.action('givecommuflg', {
        'user': bob,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
        table = self.table('propertycomm', 'allprprtcomm')
        example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 64}]}, {'user': 'bob', 'properties': [{'community': 1, 'value': 64}]}]
        self.assertTrue(compare(example, table, ignore_excess=True))
        
        self.action('movequestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476733,
            'new_position': 0
            },bob, 'move question on first position')
        example = [{'community_id': 1, 'top_questions': ['68719476733', '68719476735', '68719476734', '68719476732', '68719476731']}]
        check_table(self, example)

        self.failed_action('movequestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476734,
            'new_position': -1
            },bob, 'move a question on negative position')

        self.action('movequestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 68719476734,
            'new_position': 4
            },bob, 'move a question on last position')
        example = [{'community_id': 1, 'top_questions': ['68719476733', '68719476735', '68719476732', '68719476731', '68719476734']}]
        check_table(self, example)

        self.failed_action('movequestion', {
            'user': bob,
            'community_id': 1,
            'question_id': 1111,
            'new_position': 3
            },bob, 'move a nonexistent question')

        self.failed_action('movequestion', {
            'user': bob,
            'community_id': 2,
            'question_id': 68719476734,
            'new_position': 3
            },bob, 'move a question from another community')
        end()

def check_table(self, examplee):
    table = self.table('topquestion', 'alltopquest')
    self.assertTrue(compare(examplee, table, ignore_excess=True))

def install_table(self):
    begin('install table')
    admin = self.get_contract_deployer(self.get_default_contract())
    alice = self.register_alice_account()
    self.action('givecommuflg', {
        'user': alice,
        'flags': COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION,
        'community_id': 1
        }, admin, 'add a flag COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION')
    table = self.table('propertycomm', 'allprprtcomm')
    example = [{'user': 'alice', 'properties': [{'community': 1, 'value': 64}]}]
    self.assertTrue(compare(example, table, ignore_excess=True))

    for w in range(5):
        self.register_question_action(alice, 'Alice question ' + str(68719476735 - w))
        question_id = self.table('question', 'allquestions')[0]['id']
        community_id = self.table('question', 'allquestions')[0]['community_id']
        self.action('addtotopcomm', {
            'user': alice,
            'community_id': community_id,
            'question_id': question_id
            }, alice, 'add community 1, question ' + str(community_id))

    top = self.table('topquestion', 'alltopquest')
    example = [{'community_id': 1, 'top_questions': ['68719476735', '68719476734', '68719476733', '68719476732', '68719476731']}]
    print("intall table")
    self.assertTrue(compare(example, top, ignore_excess=True))

if __name__ == '__main__':
    main()