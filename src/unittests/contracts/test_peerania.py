import setup
import eosf
import node
import unittest
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

        wallet = eosf.Wallet()
        assert(not wallet.error)

        global account_master
        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)
        assert(not account_master.error)

        global account_alice
        account_alice = eosf.account(account_master)
        wallet.import_key(account_alice)
        assert(not account_alice.error)

        global account_bob
        account_bob = eosf.account(account_master)
        wallet.import_key(account_bob)
        assert(not account_bob.error)

        global account_carol
        account_carol = eosf.account(account_master)
        wallet.import_key(account_carol)
        assert(not account_carol.error)

        account_deploy = eosf.account(account_master)
        wallet.import_key(account_deploy)
        assert(not account_deploy.error)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()
        assert(not contract_eosio_bios.error)

        global contract
        contract = eosf.Contract(account_deploy, "peerania")
        assert(not contract.error)

        deployment = contract.deploy()

        assert(not deployment.error)


    def setUp(self):
        pass


    def test_addaccount__new_user(self):
        print("Test addaccount - new user")

        self.assertFalse(contract.push_action(
            "addaccount",
            '["{0}"]'.format(account_alice), 
            account_alice).error)

        t1 = contract.table("account", account_bob)
        print(str(t1))

    def test_addaccount__not_current_user(self):
        print("Test addaccount - call with user name of not current user")

        self.assertTrue(contract.push_action(
            "addaccount",
            '["{0}"]'.format(account_alice), 
            account_bob).error)

    def test_addaccount__existing_user(self):
        print("Test addaccount - call action for existing user")

        print("Register user")

        self.assertFalse(contract.push_action(
            "addaccount",
            '["{0}"]'.format(account_bob), 
            account_bob).error)

        print("Attempt to register the same user twice. Error is expected.")

        self.assertTrue(contract.push_action(
            "addaccount",
            '["{0}"]'.format(account_bob), 
            account_bob).error)
    
    def tearDown(self):
        pass

    
    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()