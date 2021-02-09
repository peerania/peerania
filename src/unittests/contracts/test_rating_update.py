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
        
        bob = self.register_bob_account()
        ted = self.register_ted_account()

        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.register_question_action(alice, 'Alice question ' + str(68719476735))
        question_id = self.table('question', 'allquestions')[0]['id']
        self.wait(2)
        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.action('postanswer', {'user': str(bob), 'question_id': question_id, 'ipfs_link': 'undefined', 'official_answer': False}, bob,
                    '{} answer to question with id={}: "{}"'.format(str(alice), question_id, 'Register Alice answer'))
        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.action('downvote', {'user': 'ted', 'question_id': question_id, 'answer_id': 0}, ted, 'ted downvote for Alice question')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.wait(1)
        self.action('downvote', {'user': 'ted', 'question_id': question_id, 'answer_id': 0}, ted, 'ted downvote for Alice question')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        alice_rating = self.table('account', 'allaccounts')[0]['rating']

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        alice_rating = self.table('account', 'allaccounts')[0]['rating']

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])

        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])
        alice_rating = self.table('account', 'allaccounts')[0]['rating']

        self.wait(1)
        
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in less than 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])


        self.wait(2)
        
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in less than 3 days')
        # print(self.table('account', 'allaccounts')[0]['rating'])


        alice_rating = self.table('account', 'allaccounts')[0]['rating']
      
        self.wait(2)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')

        # print(self.table('account', 'allaccounts')[0]['rating'])
        
        self.wait(1)
        self.action('updateacc', {'user': 'alice'},
                            alice, 'Update alice rating in 3 days')

        # print(self.table('account', 'allaccounts')[0]['rating'])

        rating += 3
        alice_rating = self.table('account', 'allaccounts')[0]['rating']
        # self.assertTrue(alice_rating == rating)
        end()

if __name__ == '__main__':
    main()