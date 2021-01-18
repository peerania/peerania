import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
 

class TestBoost(peeranhatest.peeranhaTest):  
    def test_get_all_rewards(self): 
        begin('tets get all rewards')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        
        give_ratings(self, bob, 1)      # 0 period 
        give_ratings(self, alice, 1)      # 0 period 
        give_ratings(self, ted, 1)      # 0 period 
        self.wait(3)

        give_ratings(self, bob, 2)      # boost
        give_ratings(self, alice, 2)      # boost
        give_ratings(self, ted, 2)      # boost
        self.wait(4)

        give_ratings(self, bob, 3)      # 2 period
        give_ratings(self, alice, 3)      # 2 period
        give_ratings(self, ted, 3)      # 2 period
        self.wait(4)

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodrating', 'bob'))
        
        self.action('pickupallrew', {},
                    'peeranhatken', ' pick up her reward for 2 preiod', contract='token')

        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodreward', 'alice', contract='token'))
        print(self.table('periodreward', 'ted', contract='token'))
        example_period_reward = [{'period': 1}, {'period': 2}]
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'ted', contract='token'), ignore_excess=True))
        end()

    def test_get_rewards(self): 
        begin('tets get rewards for all users')
        bob = self.register_bob_account()
        alice = self.register_alice_account()
        ted = self.register_ted_account()
        
        give_ratings(self, bob, 1)      # 0 period 
        give_ratings(self, alice, 1)      # 0 period 
        give_ratings(self, ted, 1)      # 0 period 
        self.wait(3)

        give_ratings(self, bob, 2)      # boost
        give_ratings(self, alice, 2)      # boost
        give_ratings(self, ted, 2)      # boost
        self.wait(4)

        give_ratings(self, bob, 3)      # 2 period
        give_ratings(self, alice, 3)      # 2 period
        give_ratings(self, ted, 3)      # 2 period
        self.wait(4)


        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodrating', 'bob'))
        
        self.action('pickupallrew', {},
                    'peeranhatken', ' pick up her reward for 2 preiod', contract='token')

        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodreward', 'alice', contract='token'))
        print(self.table('periodreward', 'ted', contract='token'))
        example_period_reward = [{'period': 1}, {'period': 2}]
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'ted', contract='token'), ignore_excess=True))
        # //////////////////////////////////////

        give_ratings(self, bob, 4)      # 2 period
        give_ratings(self, alice, 4)      # 2 period
        give_ratings(self, ted, 4)      # 2 period
        self.wait(4)

        give_ratings(self, bob, 4)      # 2 period
        give_ratings(self, alice, 4)      # 2 period
        give_ratings(self, ted, 4)      # 2 period
        self.wait(4)

        print(self.table('totalrating', 'allperiods'))
        print(self.table('periodrating', 'bob'))
        
        self.action('pickuprew', {'user': alice},
                    'alice', ' pick up her reward for 2 preiod', contract='token')

        print(self.table('periodreward', 'bob', contract='token'))
        print(self.table('periodreward', 'alice', contract='token'))
        print(self.table('periodreward', 'ted', contract='token'))
        example_period_reward = [{'period': 1}, 
                                {'period': 2}, 
                                {'period': 4}, 
                                {'period': 5}]
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'bob', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'alice', contract='token'), ignore_excess=True))
        self.assertTrue(compare(example_period_reward, self.table('periodreward', 'ted', contract='token'), ignore_excess=True))
        end()
    
    

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