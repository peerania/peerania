import peeranhatest
from test_forum_comment import cbody
from peeranhatest import *
from jsonutils import *
from unittest import main

CONFIGURATION_KEY_QUESTION = 1
CONFIGURATION_KEY_TELEGRAM = 2
ALICE_VALUE = '3773036822876127232'


class TestPropertyCommunity(peeranhatest.peeranhaTest):
    def test_add_configuration(self):
        begin('Test add configuration')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.action('addconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '500'}, admin,
                    'Add configuration Question')
        self.failed_action('addconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '1'}, admin,
                    'Add configuration Question again')
        example_config = [{'key': 1, 'value': 500}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))
        
        self.action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'Add configuration Telegram')
        self.failed_action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': '1234'}, admin,
                    'Add configuration Telegram again')
        example_config = [{'key': 1, 'value': 500}, {'key': 2, 'value': ALICE_VALUE}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))
        end()

    def test_update_configuration(self):
        begin('Test add configuration')
        admin = self.get_contract_deployer(self.get_default_contract())

        self.failed_action('updateconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '400'}, admin,
                    'updateconfig configuration, configuration not added')

        self.action('addconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '500'}, admin,
                    'Add configuration Question')
        
        self.wait(4)
        self.action('updateconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '400'}, admin,
                    'updateconfig configuration  use value')
        example_config = [{'key': 1, 'value': 400}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))

        self.action('upuserconfig', {'key': CONFIGURATION_KEY_QUESTION, 'user': 'alice'}, admin,
                    'updateconfig configuration use user name')
        example_config = [{'key': 1, 'value': ALICE_VALUE}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))
        end()
    
    def test_post_question(self):
        begin('post question')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.failed_action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice, configuration not added')

        self.action('addconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '500'}, admin,
                    'Add configuration Question')
        example_config = [{'key': 1, 'value': 500}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))

        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice (id 500)')
        example_answer = [{'id': 500}]
        self.assertTrue(compare(example_answer, self.table('question', 'allquestions'), ignore_excess=True))
        self.wait(4)

        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice (id 499)')
        example_answer = [{'id': 499}, {'id': 500}]
        self.assertTrue(compare(example_answer, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_delete_question(self):
        begin('delete question')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.action('addconfig', {'key': CONFIGURATION_KEY_QUESTION, 'value': '500'}, admin,
                    'Add configuration Question')
        example_config = [{'key': 1, 'value': 500}]
        self.assertTrue(compare(example_config, self.table('config', 'allconfig'), ignore_excess=True))        

        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice (id 500)')
        example_answer = [{'id': 500}]
        self.assertTrue(compare(example_answer, self.table('question', 'allquestions'), ignore_excess=True))
        
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('delquestion', {
                    'user': 'alice', 'question_id': question_id}, alice, 'Delete Alice question')
        self.wait(4)

        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice (id 499)')
        example_answer = [{'id': 499}]
        self.assertTrue(compare(example_answer, self.table('question', 'allquestions'), ignore_excess=True))
        end()

    def test_add_telegram_account(self):
        begin('add telegram account')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.failed_action('addtelacc', {
            'bot_name': alice,
            'user': bob,
            'telegram_id': 503975561
        }, alice, 'bob add telegram account 503975561, configuration not added')

        self.action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'Add configuration Telegram')
        
        self.wait(4)
        self.action('addtelacc', {
            'bot_name': alice,
            'user': bob,
            'telegram_id': 503975561
        }, alice, 'bob add telegram account 503975561')
        end()

    def test_disaprove_telegram_account(self):
        begin('disaprove telegram account')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()
        bob = self.register_bob_account()

        self.action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'Add configuration Telegram')
        
        self.wait(4)
        self.action('addtelacc', {
            'bot_name': alice,
            'user': bob,
            'telegram_id': 503975561
        }, alice, 'bob add telegram account 503975561')

        self.action('updateconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'value': '132456'}, admin,
                    'updateconfig configuration (wrong config)')
        self.failed_action('dsapprvacctl', {'bot_name': alice, 'user': 'bob'}, admin,
                    'disaprove telegram account. wrong telegram config')

        self.action('upuserconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'updateconfig configuration (right config)')
        self.action('dsapprvacctl', {'bot_name': alice, 'user': 'bob'}, alice,
                    'disaprove telegram account')
        end()

    def test_addemptelacc_telegram_account(self):
        begin('addemptelacc telegram account')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.failed_action('addemptelacc', {'bot_name': 'alice', 'telegram_id': 503975562, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, alice,
                        'Add empty account through telegram, configuration not added')
        self.action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'Add configuration Telegram')
        
        self.wait(4)
        self.action('addemptelacc', {'bot_name': 'alice', 'telegram_id': 503975562, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, alice,
                        'Add empty account through telegram')
        end()

    def test_update_display_name_telegram_account(self):
        begin('update display name')
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account()

        self.action('addusrconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'Add configuration Telegram')
        self.action('addemptelacc', {'bot_name': 'alice', 'telegram_id': 503975561, 'display_name': 'testNAme', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, alice,
                        'Add empty account through telegram')
        
        self.action('upuserconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'qwerty'}, admin,
                    'updateconfig configuration')
        self.failed_action('updtdsplname', {'bot_name': 'alice', 'telegram_id': 503975561, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, alice,
                        'Сhange name emty account, configuration not added')
        
        self.wait(4)
        self.action('upuserconfig', {'key': CONFIGURATION_KEY_TELEGRAM, 'user': 'alice'}, admin,
                    'updateconfig configuration')
        self.action('updtdsplname', {'bot_name': 'alice', 'telegram_id': 503975561, 'display_name': 'newName', 'ipfs_profile': 'qwe', 'ipfs_avatar': 'rty'}, alice,
                        'Сhange name emty account')
        end()

if __name__ == '__main__':
    main()