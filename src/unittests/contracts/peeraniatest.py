import json
from termcolor import cprint
from eostest import *
from time import time


PERIOD = 604800 
monday_1_october_2018 = 1538341200

class PeeraniaTest(EOSTest):
    DEFAULT_RATING = 200
    DEFAULT_MDP = 2
    WAIT_FOR_NEW_BLOCK = 0.51
    contracts = {}

    def setUp(self):
        self.action('create', {'issuer': 'peerania.tkn', 'maximum_supply':'100000000.000000 PEER'}, 'peerania.tkn', 'Create token PEER', contract='token')

    def tearDown(self):
        self.action('resettables', {}, self.get_contract_deployer('token'), 'Reset all token tables', contract='token')
        self.action('resettables', {}, self.get_contract_deployer(self.get_default_contract()),'Reset all tables')
        self.wait(1)

    def get_non_registered_alice(self):
        return 'alice'

    def get_non_registered_bob(self):
        return 'bob'

    def get_non_registered_carol(self):
        return 'carol'

    def get_non_registered_ted(self):
        return 'ted'

    def get_non_registered_dan(self):
        return 'dan'

    def get_non_registered_frank(self):
        return 'frank'

    def register_alice_account(self, rating=None, moderation_points=None):
        return self._register_account('alice', rating, moderation_points)

    def register_bob_account(self, rating=None, moderation_points=None):
        return self._register_account('bob', rating, moderation_points)

    def register_carol_account(self, rating=None, moderation_points=None):
        return self._register_account('carol', rating, moderation_points)

    def register_ted_account(self, rating=None, moderation_points=None):
        return self._register_account('ted', rating, moderation_points)

    def register_dan_account(self, rating=None, moderation_points=None):
        return self._register_account('dan', rating, moderation_points)

    def register_frank_account(self, rating=None, moderation_points=None):
        return self._register_account('frank', rating, moderation_points)

    def get_token_contract(self):
        return 'token'

    def _register_account(self, user, rating, moderation_points):
        self.action('registeracc', {'user': str(user), 'display_name': str(
            user) + 'DispName', 'ipfs_profile': str(user) + '_IPFS'},
            user, 'Register {} account'.format(user))
        if rating is None:
            rating=self.DEFAULT_RATING
        if moderation_points is None:
            moderation_points=self.DEFAULT_MDP
        self.action('setaccrtmpc', {'user': str(user), 'rating': rating, 'moderation_points': moderation_points},
                    user, 'Set {} rating to {} and give {} moderation points'.format(str(user), rating, moderation_points))
        return user

def get_expected_account_body(user):
    return {
        'user': str(user),
        'display_name': str(user) + 'DispName',
        'ipfs_profile': str(user) + '_IPFS',
        'registration_time': '#ignore',
        'moderation_points': '#var ' + str(user) + '_mdp',
        'rating': '#var ' + str(user) + '_rating',
        'string_properties': [],
        'integer_properties': []
    }


def get_tag_scope(community_id):
    charmap = ".12345abcdefghijklmnopqrstuvwxyz"
    mask = 0xF800000000000000
    v = 3774731489195851776 + community_id
    ret = ""
    for i in range(13):
        v &= 0xFFFFFFFFFFFFFFFF
        if v == 0:
            break
        indx = (v & mask) >> (60 if i == 12 else 59)
        ret+=charmap[indx]
        v <<=5
    return ret

def time_sec():
    return round(time())

def get_period_scope(time):
  alphabet = 'abcdefjhijklmnopqrstuvwxyz'
  time -= monday_1_october_2018
  week_number = time // PERIOD
  scope = ''
  while week_number != 0:
      scope += alphabet[week_number % 26]
      week_number //= 26
  return scope

def load_defines(filepath):
    defs={}
    with open(filepath, 'r') as ins:
        for line in ins:
            spl=line.split(' ')
            if len(spl) > 2 and spl[0] == '#define':
                try:
                    defs[spl[1]]=int(spl[2])
                except:
                    continue
    return defs


def begin(text, error_expected=False):
    cprint(text + ('- Error expected.' if error_expected else ''), color='cyan')

def end():
    cprint('Test ', end='', color='cyan')
    cprint('OK\n\n', color='green')