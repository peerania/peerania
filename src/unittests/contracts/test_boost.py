import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # #       STAGE == 2
# # # START_POOL 40 -> START_POOL 10000
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class TestBoost(peeranhatest.peeranhaTest):  
    def test_init_boost(self): 
        begin('test init boost (total rating * 1000)')
        bob = self.register_bob_account()
    
        
        give_ratings(self, bob, 1)      # 0 period 
        self.wait(4)

        give_ratings(self, bob, 2)      # boost
        self.wait(4)

        give_ratings(self, bob, 3)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 4)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 5)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 6)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 7)      # 2 period
        self.wait(4)


        print(self.table('totalrating', 'allperiods'))
        print(self.table('totalratingg', 'allperiods'))
        print("///////////////////")

        admin = self.get_contract_deployer(self.get_default_contract())
        self.failed_action('intboost', {'period': 50},
                    admin, ' pick up her reward for 2 preiod')
        self.action('intboost', {'period': 5},
                    admin, ' pick up her reward for 2 preiod')
        print(self.table('totalrating', 'allperiods'))
        print(self.table('totalratingg', 'allperiods'))
        end()
    
    # def test_get_boost_x4(self): 
    #     begin('get boost X4')
    #     bob = self.register_bob_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
    #     self.action('addboost', {'user': 'bob', 'tokens': '5.00000 PEER'}, bob,
    #                 'Bob add boost 5 peer, x4 boost', contract='token')
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')

    #     # print(self.table('totalrating', 'allperiods'))
    #     # print(self.table('periodreward', 'bob', contract='token'))
    #     # print(self.table('periodrating', 'bob'))
    #     # print(self.table('totalreward', 'allperiods', contract='token'))    
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 4000}] # 1 rating * 4 boost * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     print(self.table('periodreward', 'bob', contract='token'))
    #     example_bob_tokens = [{'period': 2, 'reward': '32.000000 PEER'}] # 8 token * 4 boost
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '32.000000 PEER'}] # 8 token * 4 boost
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
    #     end()

    # def test_get_boost_x2_5(self): 
    #     begin('get boost X2.5')
    #     bob = self.register_bob_account()
    #     alice = self.register_alice_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
    #                 'Alice add boost 10 peer, x4 boost', contract='token')
    #     self.action('addboost', {'user': 'bob', 'tokens': '5.00000 PEER'}, bob,
    #                 'Bob add boost 7 peer, x3 boost', contract='token')
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')    
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 2500}] # 1 rating * 2,5 boost * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '20.000000 PEER'}] # 8 token * 2 boost
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '20.000000 PEER'}] # 8 token * 2 boost
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
    #     end()

    # def test_get_boost_x1_3(self): 
    #     begin('get boost X1,3')
    #     bob = self.register_bob_account()
    #     alice = self.register_alice_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
    #                 'Bob add boost', contract='token')
    #     self.action('addboost', {'user': 'bob', 'tokens': '1.00000 PEER'}, bob,
    #                 'Bob add boost', contract='token')
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')      
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1300}] # 1 rating * 1.3 boost * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '10.400000 PEER'}] # 8 token * 1.3 boost
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '10.400000 PEER'}] # 8 token * 1,3 boost
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
    #     end()

    # def test_without_boost(self): 
    #     begin('without_boost')
    #     bob = self.register_bob_account()
                
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')     
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}]
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}]
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
    #     end()


    # def test_add_boost_after_accruals_rating(self): 
    #     begin('add boost after accruals rating')
    #     bob = self.register_bob_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     self.action('addboost', {'user': 'bob', 'tokens': '1.00000 PEER'}, bob,
    #                 'Bob add boost 1 peer, x4 boost', contract='token')
    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')      
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}] # 8 token
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}] # 8 token
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))

    #     example_boost = [{'staked_tokens': '1.00000 PEER', 'period': 3}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'bob', contract='token'), ignore_excess=True))

    #     example_statistics = [{'sum_tokens': '1.00000 PEER', 'max_stake': '1.00000 PEER', 'user_max_stake': 'bob', 'period': 3}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_take_away_all_boost(self): 
    #     begin('take away all boost')
    #     bob = self.register_bob_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.action('addboost', {'user': 'bob', 'tokens': '3.00000 PEER'}, bob,
    #                 'Bob add boost 3 peer, x4 boost', contract='token')
        
    #     self.wait(3)                    # 1 period

    #     self.action('addboost', {'user': 'bob', 'tokens': '0.00000 PEER'}, bob,
    #                 'pick up boost', contract='token')
    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')   

    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 4000}] # 1 rating * 1000 * 4 boost
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '32.000000 PEER'}] # 8 token * 4 boost
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '32.000000 PEER'}] # 8 token * 4 boost
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))

    #     example_boost = [{'staked_tokens': '3.00000 PEER', 'period': 1}, {'staked_tokens': '0.00000 PEER', 'period': 2}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'bob', contract='token'), ignore_excess=True))

    #     example_statistics = [{'sum_tokens': '3.00000 PEER', 'max_stake': '3.00000 PEER', 'user_max_stake': 'bob', 'period': 1}, 
    #                         {'sum_tokens': '0.00000 PEER', 'max_stake': '0.000000 PEER', 'user_max_stake': 'bob', 'period': 2}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_add_boost(self):
    #     begin('add boost')
    #     alice = self.register_alice_account()
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost', contract='token')

    #     example_boost = [{'staked_tokens': '10.000000 PEER', 'period': 1}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

    #     self.wait(3)
    #     self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
    #                 'Alice add boost', contract='token')

    #     example_boost = [{'staked_tokens': '10.000000 PEER', 'period': 1}, 
    #                     {'staked_tokens': '2.000000 PEER', 'period': 2}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}, 
    #                         {'sum_tokens': '2.000000 PEER', 'max_stake': '2.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()
    
    # def test_add_boost_without_tokens(self):
    #     begin('add boost, balance = 0')
    #     alice = self.register_alice_account()

    #     self.failed_action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost 10 token', contract='token')

    #     self.wait(3)
    #     self.failed_action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
    #                 'Alice add boost 2 token', contract='token')
    #     end()

    # def test_pick_up_stake(self):
    #     begin('pick up stake')
    #     alice = self.register_alice_account()
    #     give_tokens(self, 'alice', '25.000000 PEER')

    #     self.action('addboost', {'user': 'alice', 'tokens': '20.000000 PEER'}, alice,
    #                 'Alice add boost 20 token', contract='token')
    #     example_boost = [{'staked_tokens': '20.000000 PEER', 'period': 1}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_statistics = [{'sum_tokens': '20.000000 PEER', 'max_stake': '20.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
    #     self.action('addboost', {'user': 'alice', 'tokens': '18.000000 PEER'}, alice,
    #                 'Alice add boost 18 token', contract='token')
    #     example_boost = [{'staked_tokens': '18.000000 PEER', 'period': 1}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '18.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

    #     self.wait(3)
    #     self.action('addboost', {'user': 'alice', 'tokens': '13.000000 PEER'}, alice,
    #                 'Alice add boost 13 token', contract='token')
    #     example_boost = [{'staked_tokens': '18.000000 PEER', 'period': 1},
    #                     {'staked_tokens': '13.000000 PEER', 'period': 2}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '18.000000 PEER', 'user_max_stake': 'alice', 'period': 1},
    #                             {'sum_tokens': '13.000000 PEER', 'max_stake': '13.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_add_boost_2user(self):
    #     begin('add boost 2 user')
    #     alice = self.register_alice_account()
    #     carol = self.register_carol_account()
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     give_tokens(self, 'carol', '20.000000 PEER')

    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost 10 token', contract='token')
    #     self.action('addboost', {'user': 'carol', 'tokens': '5.000000 PEER'}, carol,
    #                 'Carol add boost 5 token', contract='token')

    #     example_boost_alice = [{'staked_tokens': '10.000000 PEER', 'period': 1}]
    #     self.assertTrue(compare(example_boost_alice, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_boost_carol = [{'staked_tokens': '5.000000 PEER', 'period': 1}]
    #     self.assertTrue(compare(example_boost_carol, self.table('boost', 'carol', contract='token'), ignore_excess=True))

    #     example_statistics = [{'sum_tokens': '15.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

    #     self.wait(3)
    #     self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
    #                 'Alice add boost 2 token', contract='token')
    #     self.action('addboost', {'user': 'carol', 'tokens': '1.000000 PEER'}, carol,
    #                 'Carol add boost 1 token', contract='token')

    #     example_boost_alice = [{'staked_tokens': '10.000000 PEER', 'period': 1}, 
    #                     {'staked_tokens': '2.000000 PEER', 'period': 2}]
    #     self.assertTrue(compare(example_boost_alice, self.table('boost', 'alice', contract='token'), ignore_excess=True))
    #     example_boost_carol = [{'staked_tokens': '5.000000 PEER', 'period': 1}, 
    #                     {'staked_tokens': '1.000000 PEER', 'period': 2}]
    #     self.assertTrue(compare(example_boost_carol, self.table('boost', 'carol', contract='token'), ignore_excess=True))

    #     example_statistics = [{'sum_tokens': '15.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}, 
    #                         {'sum_tokens': '3.000000 PEER', 'max_stake': '2.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_max_stake_change_user(self):
    #     begin('add boost 2 user')
    #     alice = self.register_alice_account()
    #     carol = self.register_carol_account()
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     give_tokens(self, 'carol', '20.000000 PEER')

    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost 10 token', contract='token')
    #     example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
    #     self.action('addboost', {'user': 'carol', 'tokens': '15.000000 PEER'}, carol,
    #                 'Carol add boost 15 token', contract='token')
    #     example_statistics = [{'sum_tokens': '25.000000 PEER', 'max_stake': '15.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_max_stake_change_user_add_stake(self):
    #     begin('max_stake_change_user_add_stake')
    #     alice = self.register_alice_account()
    #     carol = self.register_carol_account()
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     give_tokens(self, 'carol', '20.000000 PEER')

    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost 10 token', contract='token')
    #     example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
    #     self.action('addboost', {'user': 'carol', 'tokens': '8.000000 PEER'}, carol,
    #                 'Carol add boost 8 token', contract='token')
    #     example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

    #     self.action('addboost', {'user': 'carol', 'tokens': '13.000000 PEER'}, carol,
    #                 'Carol add boost 13 token', contract='token')
    #     example_statistics = [{'sum_tokens': '23.000000 PEER', 'max_stake': '13.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    # def test_max_stake_change_user_pick_up_stake(self):
    #     begin('max_stake_change_user_pick_up_stake')
    #     alice = self.register_alice_account()
    #     carol = self.register_carol_account()
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     give_tokens(self, 'carol', '20.000000 PEER')

    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Alice add boost 10 token', contract='token')
    #     example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
    #     self.action('addboost', {'user': 'carol', 'tokens': '8.000000 PEER'}, carol,
    #                 'Carol add boost 8 token', contract='token')
    #     example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

    #     self.action('addboost', {'user': 'alice', 'tokens': '5.000000 PEER'}, alice,
    #                 'Alice add boost 5 token', contract='token')
    #     example_statistics = [{'sum_tokens': '13.000000 PEER', 'max_stake': '8.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

def give_tokens(self, user, tokens):
    begin('to give tokens ')
    self.action('issue', {'to': user, 'quantity': tokens, 'memo': "13" },
                    'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)

def give_ratings(self, user, rating):
    begin('to give rating ')
    self.action('chnguserrt', {'user': user, 'rating_change': rating},
                            self.admin, 'Update alice rating')
    # print('+{} rating'.format(rating))
    # print(self.table('totalrating', 'allperiods'))
    # print(self.table('periodrating', user) )


if __name__ == '__main__':
    main()