import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

MODERATOR_FLG_ALL = 63

economy = load_defines('./src/contracts/peeranha.main/economy.h')

class TestBoost(peeranhatest.peeranhaTest):  
    def test_add_boost(self):
        begin('add boost')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        # carol = self.register_carol_account()

        # self.action('issue', {'to': 'peeranhatken', 'maximum_supply': '100.000000 PEER', 'memo': "test"},
        #             'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)
        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        # self.action('addboost', {'user': 'bob', 'tokens': '12.000000 PEER'}, bob,
        #             'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        # print(self.table('boost', 'bob', contract='token'))
        # print(self.table('statboost', 'allboost', contract='token'))

        self.wait(3)

        # self.action('addboost', {'user': 'bob', 'tokens': '13.000000 PEER'}, bob,
        #             'Asking question from alice with text "Alice question"', contract='token')
        
        self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        # print(self.table('boost', 'bob', contract='token'))
        # print(self.table('statboost', 'allboost', contract='token'))

        self.wait(3)
        self.action('addboost', {'user': 'alice', 'tokens': '-2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        print(self.table('boost', 'alice', contract='token'))

        self.wait(3)

        self.action('addboost', {'user': 'alice', 'tokens': '-3.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        print(self.table('boost', 'alice', contract='token'))

        self.wait(3)
        
        
        self.action('addboost', {'user': 'alice', 'tokens': '-4.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        print(self.table('boost', 'alice', contract='token'))

        self.wait(3)

        end()
    
    

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()