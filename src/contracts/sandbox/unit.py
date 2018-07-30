import setup
import eosf
import node
import sess
import unittest
import time
from termcolor import cprint

from os import system

setup.set_verbose(False)
setup.set_json(False)
setup.use_keosd(False)


class PeeraniaTests(unittest.TestCase):
    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        testnet = node.reset()
        assert(not testnet.error)

        sess.init()

        global global_scope_name
        global_scope_name = "main"

        global contract
        contract = eosf.Contract(sess.bob, "peerania")
        assert(not contract.error)
        deployment = contract.deploy()
        assert(not deployment.error)

        global contract_test_action
        print(sess.bob.active_key)

        global talice
        talice = eosf.account(sess.bob, "talice")#, permission='bob@eosid.code', owner_key=sess.bob.active_key)
        sess.wallet.import_key(talice)
        assert(not talice.error)
        print(talice.json)

        contract_test_action = eosf.Contract(talice, "testaction")
        assert(not contract_test_action.error)
        deployment_test_action = contract_test_action.deploy()
        assert(not deployment_test_action.error)

        # comm_permission = 'cleos set account permission alice active \'{"threshold":2,"keys":[],"accounts":[{"permission":{"actor":"bob","permission":"active"},"weight":1},{"permission":{"actor":"carol","permission":"active"},"weight":1}],"waits":[]}\' owner -p alice@owner'
        # print("execute command:\n" + comm_permission)
        # system(comm_permission)

    @classmethod
    def tearDownClass(cls):
        input("Press enter to close term")
        node.stop()

    def test_01_addaccount_new_user(self):
        global contract
        print("Test 01. Method addaccount - new user")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 01 OK\n\n')

    def test_02_addaccount__not_current_user(self):
        global contract
        print("Test 02. Method addaccount - call with user name of not current user")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),
            sess.bob)

        self.assertTrue(action.error)
        # print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 02 OK\n\n')

    def test_03_addaccount__existing_user(self):
        global contract
        print("Test 03. Method addaccount - call action for existing user(Bob)")

        print("Register user")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.bob),
            sess.bob)

        self.assertFalse(action.error)
        print(action)
        print('Wait 1 sec utill new block generated')
        time.sleep(1)

        print("Attempt to register the same user twice. Error is expected.")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.bob),
            sess.bob)

        self.assertTrue(action.error)
        # print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 03 OK\n\n')

    def test_04_addaccount_structure(self):
        global contract
        print("Test 04. Method addaccount - structure with expanded table")

        action = contract.push_action(
            "taddaccs",
            '{"user": {"owner": "' + str(sess.carol) +
            '", "name": "' + sess.carol.name +
            '", "add_test_prop": ' + str(1005000) + '} }',
            sess.carol)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 04 OK\n\n')

    def test_05_delete_item_form_table(self):
        global contract
        print("Test 05. Method tremovedata - delete item from table")
        print('Table before action: \n', contract.table(
            "account", global_scope_name))

        action = contract.push_action(
            "tremovedata",
            '{"user": "' + str(sess.alice) + '"}',
            sess.alice)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 05 OK\n\n')

    def test_06_modify_table_item(self):
        global contract
        print("Test 06. Method tupdatedata - modify table item")
        print('Table before action: \n', contract.table(
            "account", global_scope_name))

        action = contract.push_action(
            "tupdatedata",
            '{"user": {"owner": "' + str(sess.carol) +
            '", "name": "' + str("Caroline(old carol) :)") +
            '", "add_test_prop": ' + str(6) + '} }',
            sess.carol)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table(
            "account", global_scope_name))
        print('Test 06 OK\n\n')

    def test_07_test_action(self):
        global contract_test_action
        print('Test 07. Class:test_action, Method tactfunc - try to use second contract')
        action = contract_test_action.push_action(
            "tactfunc",
            '{"input": "test 07 input"}',
            sess.bob)
        self.assertFalse(action.error)
        print('Test 07 OK\n\n')

    def test_08_test_read_from_another_contract(self):
        global contract_test_action
        print('Test 08. Class:test_action, Method trdanother - try to read from table of another contract')
        action = contract_test_action.push_action(
            "trdanother",
            '{"table": "'+str(contract.account) +
            '","scope":"' + global_scope_name + '"}',
            sess.bob)
        self.assertFalse(action.error)
        print('Test 08 OK\n\n')

    def test_09_test_modify_table_of_another_contract(self):
        global contract_test_action
        print("Test 09. Class:test_action, Method trdanother - try to read from table of another contract. Error is expected.")
        action = contract_test_action.push_action(
            "taddanother",
            '{"table": "'+str(contract.account) +
            '","scope":"' + global_scope_name +
            '", "user": {"owner": "' + str(sess.carol) +
            '", "name": "' + str("Caroline(old carol) :)") +
            '", "add_test_prop": ' + str(9) + '} }',
            sess.carol)

        self.assertTrue(action.error)
        print('Test 09 OK\n\n')
    
    """
    def test_10_test_action_call(self):
        global contract
        print("Test 10. Method tcallcontr - call method from another contract")
        action = contract.push_action(
            "tcallcontr",
            '{"user": "' + str(sess.alice) +
            '", "input": "test 10 input"}',
            sess.alice)
        self.assertFalse(action.error)
        print('Test 10 OK\n\n')
    """    
    def tearDown(self):
        pass

    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()
