import peeraniatest
import requests
from termcolor import cprint
from peeraniatest import *
from jsonutils import *
from unittest import main
from random import randint
class TT(peeraniatest.PeeraniaTest):
    def key_func(self, str):
        key = 0
        i = 0
        for c in str:
            key += ord(c) << (120 - i)
            i += 8
        return key

    def test_ok(self):
        alice = self.get_non_registered_alice()
        bob = self.get_non_registered_bob()
        carol = self.get_non_registered_carol()
        
        self.action('registeracc', {'owner': alice, 'display_name': 'aaaaa', 'ipfs_profile': 'ofrjfjfnfrjnljnfpljk'}, alice, 'reg alice')
        self.action('registeracc', {'owner': bob, 'display_name': 'aab', 'ipfs_profile': 'ofrjfjfnfrjnljnfpljk'}, bob, 'reg alice')
        self.action('registeracc', {'owner': carol, 'display_name': 'aaaaa', 'ipfs_profile': 'ofrjfjfnfrjnljnfpljk'}, carol, 'reg alice')

        self.table('account', 'allaccounts', upperBound=self.key_func('aaaaa'), indexPosition = 3, keyType = 'i128')

if __name__ == '__main__':
    main()
