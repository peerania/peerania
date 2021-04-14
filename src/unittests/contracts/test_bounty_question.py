import peeranhatest
from peeranhatest import *
from jsonutils import *
from time import time
from unittest import main

BOUNTY_STATUS_ACTIVE = 1    #enum
BOUNTY_STATUS_PAID = 2
BOUNTY_STATUS_PENDING = 3
BOUNTY_STATUS_DELETED = 4

COMMUNITY_ADMIN_FLG_INFINITE_IMPACT = 1 << 1        # 2

class TestTopQuestion(peeranhatest.peeranhaTest): 
    def test_wrong_value_bounty(self):
        begin('Test wrong value bounty')
        alice = self.register_alice_account()
        time = time_sec()
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('setbounty', {'user': 'alice', 'bounty': '-10.000000 PEER', 'question_id': question_id, 'end_timestamp': time + 1000}, alice,
                    'Alice set bounty. Bad value bounty', contract='token')
        end()

    def test_wrong_format_bounty(self):
        begin('Test wrong format bounty')
        alice = self.register_alice_account()
        time = time_sec()
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('setbounty', {'user': 'alice', 'bounty': '10.000000', 'question_id': question_id, 'end_timestamp': time + 1000}, alice,
                    'Alice set bounty. Bad format bounty', contract='token')
        end()
    
    def test_bad_end_timestamp(self):
        begin('Test wrong end_timestamp')
        alice = self.register_alice_account()
        time = time_sec()
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.failed_action('setbounty', {'user': 'alice', 'bounty': '10.000000 PEER', 'question_id': question_id, 'end_timestamp': time - 1000}, alice,
                    'Alice set bounty. Bad end_timestamp', contract='token')
        end()
    
    def test_wrong_question_id(self):
        begin('Test wrong value bounty')
        alice = self.register_alice_account()
        time = time_sec()
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Alice asking question')
        self.failed_action('setbounty', {'user': 'alice', 'bounty': '10.000000 PEER', 'question_id': 666, 'end_timestamp': time + 1000}, alice,
                    'Alice set bounty. Wrong question id', contract='token')
        end()

    def test_set_bounty(self):
        begin('Test set bounty')
        alice = self.register_alice_account()
        time = time_sec()
        set_bounty_time = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('setbounty', {'user': 'alice', 'bounty': '10.000000 PEER', 'question_id': question_id, 'end_timestamp': set_bounty_time}, alice,
                    'Alice set 10 bounty.', contract='token')

        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': set_bounty_time}] 
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_set_bounty_again(self):
        begin('Test set double bounty on the one question')
        alice = self.register_alice_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('setbounty', {'user': 'alice', 'bounty': '2.000000 PEER', 'question_id': question_id, 'end_timestamp': time_set_bounty}, alice,
                    'Alice set 2 bounty. question already has bounty', contract='token')
        end()

    def test_edit_bounty_to_less_without_answer(self):
        begin('Test edit bounty to less without answer 10 -> 2')
        alice = self.register_alice_account()
        time = time_sec()
        time_set_bounty = time + 1000
        time_edit_bounty = time + 2000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        
        self.action('editbounty', {'user': 'alice', 'bounty': '2.000000 PEER', 'question_id': question_id, 'end_timestamp': time_edit_bounty}, alice,
                    'Alice edit bounty. 10 -> 2', contract='token')
        self.assertTrue(compare([{'balance': '18.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '2.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_edit_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()

    def test_edit_bounty_to_less_with_answer(self):
        begin('Test edit bounty to less with answer 10 -> 2')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        time_edit_bounty = time + 2000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        
        self.failed_action('editbounty', {'user': 'alice', 'bounty': '2.000000 PEER', 'question_id': question_id, 'end_timestamp': time_edit_bounty}, alice,
                    'Alice edit bounty. 10 -> 2, question has answers', contract='token')
        end()


    def test_edit_bounty_to_more_without_answer(self):
        begin('Test edit bounty to more without answer 10 -> 15')
        alice = self.register_alice_account()
        time = time_sec()
        time_set_bounty = time + 1000
        time_edit_bounty = time + 2000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        
        self.action('editbounty', {'user': 'alice', 'bounty': '15.000000 PEER', 'question_id': question_id, 'end_timestamp': time_edit_bounty}, alice,
                    'Alice edit bounty. 10 -> 15', contract='token')
        self.assertTrue(compare([{'balance': '5.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '15.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_edit_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()

    def test_edit_bounty_to_more_with_answer(self):
        begin('Test edit bounty to more with answer 10 -> 15')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        time_edit_bounty = time + 2000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        
        self.action('editbounty', {'user': 'alice', 'bounty': '15.000000 PEER', 'question_id': question_id, 'end_timestamp': time_edit_bounty}, alice,
                    'Alice edit bounty. 10 -> 15', contract='token')
        self.assertTrue(compare([{'balance': '5.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '15.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_edit_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()

    def test_autor_delede_question_without_answer(self):
        begin('Test autor "delete" question without answer')
        alice = self.register_alice_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'alice', 'question_id': question_id, 'on_delete': 1}, alice,
                    'Alice delete her answer', contract='token')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_DELETED, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_autor_delede_question_with_answer(self):
        begin('Test autor "delete" question with answer (answer must not delete -> nothing happens)')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('paybounty', {'user': 'alice', 'question_id': question_id, 'on_delete': 1}, alice,
                    'Alice tries delete her question with answers', contract='token')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_random_user_calls_paybounty(self):
        begin('Test random user call paybounty')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'random user calls paybounty', contract='token')
        end()
    
    def test_community_moderator_delete_question_without_answer(self):
        begin('Test moderator_delete_question_without_answer')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 1
        }, admin, 'add a COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'Community moderator "delete" question', contract='token')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_DELETED, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_another_community_moderator_delete_question_without_answer(self):
        begin('Test community moderator from 2 community delete question without answer from 1 community')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 2
        }, admin, 'add a COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'Community moderator from 2 community "delete" question from 1 community', contract='token')
        end()

    def test_community_moderator_delete_question_with_answer(self):
        begin('Test community moderator delete question with answer')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('givecommuflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
            'community_id': 1
        }, admin, 'add a COMMUNITY_ADMIN_FLG_INFINITE_IMPACT')
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'Community moderator "delete" question with answer', contract='token')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_DELETED, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()

    def test_moderator_delete_question_with_answer(self):
        begin('Test moderator delete question with answer')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('givemoderflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        }, admin, 'add a ADMIN_FLG_INFINITE_IMPACT')
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'moderator "delete" question with answer', contract='token')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_DELETED, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_moderator_delete_question_without_answer(self):
        begin('Test moderator delete question without answer')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('givemoderflg', {
            'user': bob,
            'flags': COMMUNITY_ADMIN_FLG_INFINITE_IMPACT,
        }, admin, 'add a ADMIN_FLG_INFINITE_IMPACT')
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 1}, bob,
                    'moderator "delete" question without answer', contract='token')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_DELETED, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_pay_bounty(self):
        begin('Test pay bounty')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'bob', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark bob answer as correct")
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 0}, bob,
                    'pay bounty', contract='token')
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'bob', contract='token'), ignore_excess=True))
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_PAID, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))
        end()
    
    def test_pay_bounty_2_times(self):
        begin('Test pay bounty 2 times')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'bob', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark bob answer as correct")
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 0}, bob,
                    'pay bounty', contract='token')
        self.wait(3)
        self.failed_action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 0}, bob,
                    'pay bounty again', contract='token')
        end()

    def test_pay_bounty_without_best_answer(self):
        begin('Test pay bounty without best answer')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'bob', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('paybounty', {'user': 'bob', 'question_id': question_id, 'on_delete': 0}, bob,
                    'pay bounty', contract='token')
        end()

    def test_pay_itself_bounty(self):
        begin('Test pay bounty 2 times')
        alice = self.register_alice_account()
        time = time_sec()
        time_set_bounty = time + 1000
        give_tokens(self, 'alice', '20.000000 PEER')
        self.assertTrue(compare([{'balance': '20.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare([], self.table('accounts', 'bob', contract='token'), ignore_excess=True))

        question_id = user_ask_question_and_setbounty(self, alice, time_set_bounty, '10.000000 PEER')
        self.action('postanswer', {'user': 'alice', 'question_id': question_id, 'ipfs_link': 'undefined123', 'official_answer': False}, alice,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Bob post answer'))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question_id, 'answer_id': 1}, alice, "Alice mark her self answer as correct")
        self.assertTrue(compare([{'balance': '10.000000 PEER'}], self.table('accounts', 'alice', contract='token'), ignore_excess=True))       
        example_bounty = [{'user': 'alice', 'amount': '10.000000 PEER', 'question_id': question_id, 'status': BOUNTY_STATUS_ACTIVE, 'end_timestamp': time_set_bounty}] 
        self.assertTrue(compare(example_bounty, self.table('bounty', 'allbounties', contract='token'), ignore_excess=True))

        self.failed_action('paybounty', {'user': 'alice', 'question_id': question_id, 'on_delete': 0}, alice,
                    'Alice tries to pay bounty herself', contract='token')
        end()


def user_ask_question_and_setbounty(self, user, time_set_bounty , bounty):
    self.action('postquestion', {'user': user, 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 1}, user,
                'Alice asking question')
    question_id = self.table('question', 'allquestions')[0]['id']
    self.action('setbounty', {'user': user, 'bounty': bounty, 'question_id': question_id, 'end_timestamp': time_set_bounty}, user,
                '{user} set 10 bounty.', contract='token')
    return question_id
if __name__ == '__main__':
    main()