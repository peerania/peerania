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

        global contract
        contract = eosf.Contract(sess.bob, "peerania")
        assert(not contract.error)
        deployment = contract.deploy()
        assert(not deployment.error)

        global contract_test_action
        print(sess.bob.active_key)

        global talice
        talice = eosf.account(sess.bob, "talice", permission=sess.bob)
        sess.wallet.import_key(talice)
        assert(not talice.error)
        print(talice.json)

        contract_test_action = eosf.Contract(talice, "testaction")
        assert(not contract_test_action.error)
        deployment_test_action = contract_test_action.deploy()
        assert(not deployment_test_action.error)

        #comm_permission = 'cleos set account permission alice active \'{"threshold":2,"keys":[],"accounts":[{"permission":{"actor":"bob","permission":"active"},"weight":1},{"permission":{"actor":"carol","permission":"active"},"weight":1}],"waits":[]}\' owner -p alice@owner'
        #print("execute command:\n" + comm_permission)
        #system(comm_permission)

    @classmethod
    def tearDownClass(cls):
        input("Press enter to close term")
        node.stop()

    def test_1_addaccount_new_user(self):
        global contract
        print("Test 1. Method addaccount - new user")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),
            sess.alice)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 1 OK\n\n')

    def test_2_addaccount__not_current_user(self):
        global contract
        print("Test 2. Method addaccount - call with user name of not current user")

        action = contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),
            sess.bob)

        self.assertTrue(action.error)
        #print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 2 OK\n\n')

    def test_3_addaccount__existing_user(self):
        global contract
        print("Test 3. Method addaccount - call action for existing user(Bob)")

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
        #print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 3 OK\n\n')

    def test_4_addaccount_structure(self):
        global contract
        print("Test 4. Method addaccount - structure with expanded table")

        action = contract.push_action(
            "taddaccs",
            '{"user": {"owner": "' + str(sess.carol) +
            '", "name": "' + sess.carol.name +
            '", "add_test_prop": ' + str(1005000) + '} }',
            sess.carol)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 4 OK\n\n')

    def test_5_delete_item_form_table(self):
        global contract
        print("Test 5. Method tremovedata - delete item from table")
        print('Table before action: \n', contract.table("account", "main"))

        action = contract.push_action(
            "tremovedata",
            '{"user": "' + str(sess.alice) + '"}',
            sess.alice)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 5 OK\n\n')

    def test_6_modify_table_item(self):
        global contract
        print("Test 6. Method tupdatedata - modify table item")
        print('Table before action: \n', contract.table("account", "main"))

        action = contract.push_action(
            "tupdatedata",
            '{"user": {"owner": "' + str(sess.carol) +
            '", "name": "' + str("Caroline(old carol) :)") +
            '", "add_test_prop": ' + str(6) + '} }',
            sess.carol)

        self.assertFalse(action.error)
        print(action)
        print('Table after acton:\n', contract.table("account", "main"))
        print('Test 6 OK\n\n')

    def test_7_test_action(self):
        global contract_test_action
        print('Test 7. Class:test_action, Method tactfunc - try to use second contract')
        action = contract_test_action.push_action(
            "tactfunc",
            '{"input": "test 07 input"}',
            sess.bob)
        self.assertFalse(action.error)
        print('Test 7 OK\n\n')

    def test_8_test_action_call(self):
        global contract
        print("Test 8. Method tcallcontr - call method from another contract")
        action = contract.push_action(
            "tcallcontr",
            '{"user": "' + str(sess.alice) +
            '", "input": "test 08 input"}',
            sess.alice)
        self.assertFalse(action.error)
        print('Test 8 OK\n\n')

    def tearDown(self):
        pass

    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()
