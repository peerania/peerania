import peeranhatest
import requests
from termcolor import cprint
from peeranhatest import *
from jsonutils import *
from unittest import main
from random import randint
from time import sleep

economy = load_defines('src/contracts/peeranha/economy.h')

class FrumStatusLimitsTests(peeranhatest.peeranhaTest):

    def test_energy_timer(self):
        begin('Test energy restore')
        alice = self.register_alice_account(499, 0)
        info('Wait untill period ends')
        sleep(3)
        info('All stats restored')
        var = {}
        self.action('followcomm', {'user': alice, 'community_id': 1}, alice, 'Call stub action')
        e = [{'user': 'alice', 'energy': economy['STATUS1_ENERGY'] - economy['ENERGY_FOLLOW_COMMUNITY']}]
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))
        self.action('setaccrten', {'user': alice, 'rating': 999, 'energy': 0}, alice, 'Took all moderation points, give 999 rating')
        info('Wait until period ends')
        sleep(3)
        info('All stats restored')
        self.action('followcomm', {'user': alice, 'community_id': 2}, alice, 'Call stub action')
        e[0]['energy'] = economy['STATUS2_ENERGY'] - economy['ENERGY_FOLLOW_COMMUNITY']
        print(self.table('account', 'allaccounts'))
        self.assertTrue(compare(e, self.table('account', 'allaccounts'), var, True))


if __name__ == '__main__':
    main()
