import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from enum import Enum

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # #       STAGE == 2
# # # START_POOL 40 -> START_POOL 10000
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class TestBoost(peeranhatest.peeranhaTest):  
    # def test_add_boost(self):
    #     begin('add boost')
    #     alice = self.register_alice_account()
    #     bob = self.register_bob_account()
    #     # carol = self.register_carol_account()

    #     # self.action('issue', {'to': 'peeranhatken', 'maximum_supply': '100.000000 PEER', 'memo': "test"},
    #     #             'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)
    #     self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')
    #     # self.action('addboost', {'user': 'bob', 'tokens': '12.000000 PEER'}, bob,
    #     #             'Asking question from alice with text "Alice question"', contract='token')

    #     print("alice +10")
    #     print(self.table('boost', 'alice', contract='token'))
    #     # print(self.table('boost', 'bob', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))

    #     self.wait(3)

    #     # self.action('addboost', {'user': 'bob', 'tokens': '13.000000 PEER'}, bob,
    #     #             'Asking question from alice with text "Alice question"', contract='token')
        
    #     self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')

    #     print("alice +2")
    #     print(self.table('boost', 'alice', contract='token'))
    #     # print(self.table('boost', 'bob', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))

    #     self.wait(3)
    #     self.action('addboost', {'user': 'alice', 'tokens': '-2.000000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')
    #     print("alice -2")
    #     print(self.table('boost', 'alice', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))
    #     self.action('addboost', {'user': 'alice', 'tokens': '-0.500000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')
    #     print("alice -0.5 the same period")
    #     print(self.table('boost', 'alice', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))

    #     self.wait(3)

    #     self.action('addboost', {'user': 'alice', 'tokens': '-3.000000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')
    #     print("alice -3")
    #     print(self.table('boost', 'alice', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))

    #     self.wait(3)
        
        
    #     self.action('addboost', {'user': 'alice', 'tokens': '-4.000000 PEER'}, alice,
    #                 'Asking question from alice with text "Alice question"', contract='token')
    #     print("alice -4")
    #     print(self.table('boost', 'alice', contract='token'))
    #     print(self.table('statboost', 'allboost', contract='token'))
    #     end()




    def test_get_boost_x4(self): 
        begin('get boost X4')
        bob = self.register_bob_account()
        give_tokens(self, 'bob', '20.000000 PEER')
        self.action('addboost', {'user': 'bob', 'tokens': '5.00000 PEER'}, bob,
                    'Bob add boost 5 peer, x4 boost', contract='token')
        
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 4000}] # 1 rating * 4 boost * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '32.000000 PEER'}] # 8 token * 4 boost
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '32.000000 PEER'}] # 8 token * 4 boost
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        end()

    def test_get_boost_x3(self): 
        begin('get boost X3')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        give_tokens(self, 'bob', '20.000000 PEER')
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
                    'Bob add boost 10 peer, x4 boost', contract='token')
        self.action('addboost', {'user': 'bob', 'tokens': '7.00000 PEER'}, bob,
                    'Bob add boost 7 peer, x3 boost', contract='token')
        
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 3000}] # 1 rating * 3 boost * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '24.000000 PEER'}] # 8 token * 3 boost
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '24.000000 PEER'}] # 8 token * 3 boost
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        end()

    def test_get_boost_x2(self): 
        begin('get boost X2')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        give_tokens(self, 'bob', '20.000000 PEER')
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
                    'Bob add boost 10 peer, x4 boost', contract='token')
        self.action('addboost', {'user': 'bob', 'tokens': '5.00000 PEER'}, bob,
                    'Bob add boost 7 peer, x3 boost', contract='token')
        
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 2000}] # 1 rating * 2 boost * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '16.000000 PEER'}] # 8 token * 2 boost
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '16.000000 PEER'}] # 8 token * 2 boost
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        end()

    # def test_get_boost_x1_25(self): 
    #     begin('get boost X1.25')
    #     bob = self.register_bob_account()
    #     alice = self.register_alice_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
    #     give_tokens(self, 'alice', '20.000000 PEER')
    #     self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
    #                 'Bob add boost 10 peer, x4 boost', contract='token')
    #     self.action('addboost', {'user': 'bob', 'tokens': '3.00000 PEER'}, bob,
    #                 'Bob add boost 7 peer, x3 boost', contract='token')
        
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')

    #     print(self.table('totalrating', 'allperiods'))
    #     print(self.table('periodreward', 'bob', contract='token'))
    #     print(self.table('periodrating', 'bob'))
    #     print(self.table('totalreward', 'allperiods', contract='token'))      
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1250}] # 1 rating * 1.25 boost * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '10.000000 PEER'}] # 8 token * 1.25 boost
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '10.000000 PEER'}] # 8 token * 1.25 boost
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
    #     end()

    def test_get_boost_x1(self): 
        begin('get boost X1')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        give_tokens(self, 'bob', '20.000000 PEER')
        give_tokens(self, 'alice', '20.000000 PEER')
        self.action('addboost', {'user': 'alice', 'tokens': '10.00000 PEER'}, alice,
                    'Bob add boost 10 peer, x4 boost', contract='token')
        self.action('addboost', {'user': 'bob', 'tokens': '1.00000 PEER'}, bob,
                    'Bob add boost 7 peer, x3 boost', contract='token')
        
        
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1 boost * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}] # 8 token * 1 boost
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}] # 8 token * 1 boost
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        end()

    def test_without_boost(self): 
        begin('without_boost')
        bob = self.register_bob_account()
                
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}]
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}]
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        end()


    def test_add_boost_after_accruals_rating(self): 
        begin('add boost after accruals rating')
        bob = self.register_bob_account()
        give_tokens(self, 'bob', '20.000000 PEER')
        
        give_ratings(self, bob, 1)      # 0 period
        self.wait(3)

        give_ratings(self, bob, 1)      # boost
        self.wait(4)

        self.action('addboost', {'user': 'bob', 'tokens': '1.00000 PEER'}, bob,
                    'Bob add boost 1 peer, x4 boost', contract='token')
        give_ratings(self, bob, 1)      # 2 period
        self.wait(4)

        self.action('pickupreward', {'user': bob, 'period': 2},
                    bob, bob + ' pick up her reward for 2 preiod', contract='token')

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodrating', 'bob'))
        print(self.table('totalreward', 'allperiods', contract='token'))      
        
        example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1000
        self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
        example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}] # 8 token
        self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

        example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
        self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

        example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}] # 8 token
        self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        
        print(self.table('boost', 'bob', contract='token'))
        example_boost = [{'streaked_tokens': '1.00000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 3}]
        self.assertTrue(compare(example_boost, self.table('boost', 'bob', contract='token'), ignore_excess=True))
        
        print(self.table('statboost', 'allboost', contract='token'))
        example_statistics = [{'sum_tokens': '1.00000 PEER', 'max_stake': '1.00000 PEER', 'user_max_stake': 'bob', 'period': 3}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

    # def test_take_away_all_boost(self): 
    #     begin('add boost after accruals rating')
    #     bob = self.register_bob_account()
    #     give_tokens(self, 'bob', '20.000000 PEER')
        
        
    #     give_ratings(self, bob, 1)      # 0 period
    #     self.wait(3)

    #     self.action('addboost', {'user': 'bob', 'tokens': '-3.00000 PEER'}, bob,
    #                 'Bob add boost 1 peer, x4 boost', contract='token')
    #     self.wait(4)                    # 1 period

    #     give_ratings(self, bob, 1)      # boost
    #     self.wait(4)

        
    #     give_ratings(self, bob, 1)      # 2 period
    #     self.wait(4)

    #     self.action('pickupreward', {'user': bob, 'period': 2},
    #                 bob, bob + ' pick up her reward for 2 preiod', contract='token')

    #     print(self.table('totalrating', 'allperiods'))
    #     print(self.table('periodreward', 'bob', contract='token'))
    #     print(self.table('periodrating', 'bob'))
    #     print(self.table('totalreward', 'allperiods', contract='token'))      
        
    #     example_totalrating = [{'period': 1}, {'period': 2, 'total_rating_to_reward': 1000}] # 1 rating * 1000
    #     self.assertTrue(compare(example_totalrating, self.table('totalrating', 'allperiods'), ignore_excess=True))
        
    #     example_bob_tokens = [{'period': 2, 'reward': '8.000000 PEER'}] # 8 token
    #     self.assertTrue(compare(example_bob_tokens, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))

    #     example_user_rating = [{'period': 0}, {'period': 1}, {'period': 2, 'rating': 203, 'rating_to_award': 1}]
    #     self.assertTrue(compare(example_user_rating, self.table('periodrating', 'bob'), ignore_excess=True))

    #     example_total_reward = [{'period': 2, 'total_reward': '8.000000 PEER'}] # 8 token
    #     self.assertTrue(compare(example_total_reward, self.table('totalreward', 'allperiods', contract='token'), ignore_excess=True))
        
    #     print(self.table('boost', 'bob', contract='token'))
    #     example_boost = [{'streaked_tokens': '1.00000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 3}]
    #     self.assertTrue(compare(example_boost, self.table('boost', 'bob', contract='token'), ignore_excess=True))
        
    #     print(self.table('statboost', 'allboost', contract='token'))
    #     example_statistics = [{'sum_tokens': '1.00000 PEER', 'max_stake': '1.00000 PEER', 'user_max_stake': 'bob', 'period': 3}]
    #     self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
    #     end()

    



    def test_add_boost(self):
        begin('add boost')
        alice = self.register_alice_account()
        give_tokens(self, 'alice', '20.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        print(self.table('statboost', 'allboost', contract='token'))
        example_boost = [{'streaked_tokens': '10.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}]
        self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

        self.wait(3)
        self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        print(self.table('statboost', 'allboost', contract='token'))
        example_boost = [{'streaked_tokens': '10.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}, 
                        {'streaked_tokens': '12.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 2}]
        self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}, 
                            {'sum_tokens': '12.000000 PEER', 'max_stake': '12.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()
    
    def test_add_boost_without_tokens(self):
        begin('add boost, balance = 0')
        alice = self.register_alice_account()

        self.failed_action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')

        self.wait(3)
        self.failed_action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        end()

    def test_pick_up_stake(self):
        begin('add boost 2 user')
        alice = self.register_alice_account()
        give_tokens(self, 'alice', '25.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '20.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_boost = [{'streaked_tokens': '20.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}]
        self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_statistics = [{'sum_tokens': '20.000000 PEER', 'max_stake': '20.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
        self.action('addboost', {'user': 'alice', 'tokens': '-2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_boost = [{'streaked_tokens': '18.000000 PEER', 'conclusion_tokens': '-2.000000 PEER', 'period': 1}]
        print(self.table('boost', 'alice', contract='token'))
        self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '18.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

        self.wait(3)
        self.action('addboost', {'user': 'alice', 'tokens': '-5.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_boost = [{'streaked_tokens': '18.000000 PEER', 'conclusion_tokens': '-2.000000 PEER', 'period': 1},
                        {'streaked_tokens': '13.000000 PEER', 'conclusion_tokens': '-5.000000 PEER', 'period': 2}]
        self.assertTrue(compare(example_boost, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '18.000000 PEER', 'user_max_stake': 'alice', 'period': 1},
                                {'sum_tokens': '13.000000 PEER', 'max_stake': '13.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

    def test_add_boost_2user(self):
        begin('add boost 2 user')
        alice = self.register_alice_account()
        carol = self.register_carol_account()
        give_tokens(self, 'alice', '20.000000 PEER')
        give_tokens(self, 'carol', '20.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        self.action('addboost', {'user': 'carol', 'tokens': '5.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        print(self.table('statboost', 'allboost', contract='token'))
        example_boost_alice = [{'streaked_tokens': '10.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}]
        self.assertTrue(compare(example_boost_alice, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_boost_carol = [{'streaked_tokens': '5.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}]
        self.assertTrue(compare(example_boost_carol, self.table('boost', 'carol', contract='token'), ignore_excess=True))

        example_statistics = [{'sum_tokens': '15.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

        self.wait(3)
        self.action('addboost', {'user': 'alice', 'tokens': '2.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        self.action('addboost', {'user': 'carol', 'tokens': '1.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')

        print(self.table('boost', 'alice', contract='token'))
        print(self.table('boost', 'carol', contract='token'))
        print(self.table('statboost', 'allboost', contract='token'))
        example_boost_alice = [{'streaked_tokens': '10.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}, 
                        {'streaked_tokens': '12.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 2}]
        self.assertTrue(compare(example_boost_alice, self.table('boost', 'alice', contract='token'), ignore_excess=True))
        example_boost_carol = [{'streaked_tokens': '5.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 1}, 
                        {'streaked_tokens': '6.000000 PEER', 'conclusion_tokens': '0.000000 PEER', 'period': 2}]
        self.assertTrue(compare(example_boost_carol, self.table('boost', 'carol', contract='token'), ignore_excess=True))

        example_statistics = [{'sum_tokens': '15.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}, 
                            {'sum_tokens': '18.000000 PEER', 'max_stake': '12.000000 PEER', 'user_max_stake': 'alice', 'period': 2}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

    def test_max_stake_change_user(self):
        begin('add boost 2 user')
        alice = self.register_alice_account()
        carol = self.register_carol_account()
        give_tokens(self, 'alice', '20.000000 PEER')
        give_tokens(self, 'carol', '20.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
        self.action('addboost', {'user': 'carol', 'tokens': '15.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '25.000000 PEER', 'max_stake': '15.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

    def test_max_stake_change_user_add_stake(self):
        begin('add boost 2 user')
        alice = self.register_alice_account()
        carol = self.register_carol_account()
        give_tokens(self, 'alice', '20.000000 PEER')
        give_tokens(self, 'carol', '20.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
        self.action('addboost', {'user': 'carol', 'tokens': '8.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

        self.action('addboost', {'user': 'carol', 'tokens': '5.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '23.000000 PEER', 'max_stake': '13.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
        print(self.table('statboost', 'allboost', contract='token'))
        print(self.table('boost', 'carol', contract='token'))
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

    def test_max_stake_change_user_pick_up_stake(self):
        begin('add boost 2 user')
        alice = self.register_alice_account()
        carol = self.register_carol_account()
        give_tokens(self, 'alice', '20.000000 PEER')
        give_tokens(self, 'carol', '20.000000 PEER')

        self.action('addboost', {'user': 'alice', 'tokens': '10.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '10.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        
        self.action('addboost', {'user': 'carol', 'tokens': '8.000000 PEER'}, carol,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '18.000000 PEER', 'max_stake': '10.000000 PEER', 'user_max_stake': 'alice', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))

        self.action('addboost', {'user': 'alice', 'tokens': '-5.000000 PEER'}, alice,
                    'Asking question from alice with text "Alice question"', contract='token')
        example_statistics = [{'sum_tokens': '13.000000 PEER', 'max_stake': '8.000000 PEER', 'user_max_stake': 'carol', 'period': 1}]
        self.assertTrue(compare(example_statistics, self.table('statboost', 'allboost', contract='token'), ignore_excess=True))
        end()

def give_tokens(self, user, tokens):
    begin('to give tokens ')
    self.action('issue', {'to': user, 'quantity': tokens, 'memo': "13" },
                    'peeranhatken', 'Create token PEER', contract='token', suppress_output=True)

def give_ratings(self, user, rating):
    begin('to give rating ')
    self.action('chnguserrt', {'user': user, 'rating_change': rating},
                            self.admin, 'Update alice rating')

    print('+{} rating'.format(rating))
    print(self.table('totalrating', 'allperiods'))
    print(self.table('periodrating', user) )


if __name__ == '__main__':
    main()