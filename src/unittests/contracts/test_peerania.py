import setup
import eosf
import node
import sess
import unittest
import time
from termcolor import cprint

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
        contract = eosf.Contract(sess.carol, "peerania")
        assert(not contract.error)

        deployment = contract.deploy()

        assert(not deployment.error)

    @classmethod
    def tearDownClass(cls):
        input("Press enter to close term")
        node.stop()

    def test_1_addaccount__new_user(self):
        global contract
        print("Test addaccount - new user")

        self.assertFalse(contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),
            sess.alice).error)

        t1 = contract.table("account", "main")
        print(t1)

    def test_2_addaccount__not_current_user(self):
        global contract
        print("Test addaccount - call with user name of not current user")

        self.assertTrue(contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.alice),
            sess.bob).error)

        t1 = contract.table("account", "main")
        print(str(t1))

    def test_3_addaccount__existing_user(self):
        global contract
        print("Test addaccount - call action for existing user")

        print("Register user")

        self.assertFalse(contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.bob),
            sess.bob).error)

        time.sleep(2)

        print("Attempt to register the same user twice. Error is expected.")

        self.assertTrue(contract.push_action(
            "addaccount",
            '["{0}"]'.format(sess.bob),
            sess.bob).error)

        t1 = contract.table("account", "main")
        print(str(t1))

    def tearDown(self):
        pass

    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()
