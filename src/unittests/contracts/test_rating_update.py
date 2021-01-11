import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

economy = load_defines('./src/contracts/peeranha.main/economy.h')

class TestRatingUpdate(peeranhatest.peeranhaTest):

    def test_rating_update(self):
        begin("Testing of update rating periodicity")
        alice = self.register_alice_account()
        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        rating = self.DEFAULT_RATING
        self.assertTrue(alice_rating == rating)
       
        self.wait(3)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        rating += 1
        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(alice_rating == rating)

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in less than 3 days')
        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(alice_rating == rating)
        
        self.wait(3)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        rating += 1
        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        self.assertTrue(alice_rating == rating)
        end()

if __name__ == '__main__':
    main()