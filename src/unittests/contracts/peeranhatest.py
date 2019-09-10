import json
from termcolor import cprint
from eostest import *
from time import time


PERIOD = 604800
monday_1_october_2018 = 1538341200


class peeranhaTest(EOSTest):
    DEFAULT_RATING = 200
    DEFAULT_ENERGY = 50
    WAIT_FOR_NEW_BLOCK = 0.51
    contracts = {}

    def setUp(self):
        self.action('create', {'issuer': 'peeranha.tkn', 'maximum_supply': '100.000000 PEER'},
                    'peeranha.tkn', 'Create token PEER', contract='token', suppress_output=True)
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('init', {}, admin, 'Init contract', suppress_output=True)
        self.action('registeracc', {'user': admin, 'display_name': 'admin', 'ipfs_profile': 'undefined', 'ipfs_avatar': 'undefined'},
            admin, 'Register admin account', suppress_output=True)
        self.action('givemoderflg', {'user': admin, 'flags': 31}, admin, "Give admin permisson", suppress_output=True)
        for i in range(3):
            self.action('crcommunity', {'user': admin, 'name': f'Community {i+1}', 'ipfs_description': 'undefined', 'suggested_tags': 
                [{'name': f'Community {i+1} tag {j+1}', 'ipfs_description': 'undefined'} for j in range(6)]}, admin, f'Create community {i+1}', suppress_output=True)
        self.action('setaccrten', {'user': admin, 'rating': -1, 'energy': -1}, admin, 'Delete admin account', suppress_output=True)

    def tearDown(self):
        self.action('resettables', {}, self.get_contract_deployer(
            'token'), 'Reset all token tables', contract='token', suppress_output=True)
        self.action('resettables', {}, self.get_contract_deployer(
            self.get_default_contract()), 'Reset all tables', suppress_output=True)
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

    def register_alice_account(self, rating=None, energy=None):
        return self._register_account('alice', rating, energy)

    def register_bob_account(self, rating=None, energy=None):
        return self._register_account('bob', rating, energy)

    def register_carol_account(self, rating=None, energy=None):
        return self._register_account('carol', rating, energy)

    def register_ted_account(self, rating=None, energy=None):
        return self._register_account('ted', rating, energy)

    def register_dan_account(self, rating=None, energy=None):
        return self._register_account('dan', rating, energy)

    def register_frank_account(self, rating=None, energy=None):
        return self._register_account('frank', rating, energy)

    def get_token_contract(self):
        return 'token'

    def _register_account(self, user, rating, energy):
        self.action('registeracc', {'user': str(user), 'display_name': str(
            user) + 'DispName', 'ipfs_profile': str(user) + '_IPFS', 'ipfs_avatar': str(user) + '_avatar'},
            user, 'Register {} account'.format(user))
        if rating is None:
            rating = self.DEFAULT_RATING
        if energy is None:
            energy = self.DEFAULT_ENERGY
        self.action('setaccrten', {'user': str(user), 'rating': rating, 'energy': energy},
                    user, 'Set {} rating to {} and give {} energy'.format(str(user), rating, energy))
        return user


def get_expected_account_body(user):
    return {
        'user': str(user),
        'display_name': str(user) + 'DispName',
        'ipfs_profile': str(user) + '_IPFS',
        'ipfs_avatar': str(user) + '_avatar',
        'registration_time': '#ignore',
        'rating': '#var ' + str(user) + '_rating',
        'string_properties': [],
        'integer_properties': [],
        'energy': 50,  # probably better to load from defines
        'reports': [],
        'report_power': 0,
        'is_frozen': False,
        'followed_communities': []
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
        ret += charmap[indx]
        v <<= 5
    return ret


def time_sec():
    return round(time())

def get_moderation_impact(rating):
    if rating < 99:
        return 0
    elif rating < 499:
        return 1
    elif rating < 999:
        return 2
    elif rating < 2499:
        return 3
    elif rating < 4999:
        return 4
    elif rating < 9999:
        return 5
    else:
        return 6


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
    defs = {}
    with open(filepath, 'r') as ins:
        for line in ins:
            spl = line.split(' ')
            if len(spl) > 2 and spl[0] == '#define':
                try:
                    defs[spl[1]] = int(spl[2])
                except:
                    continue
    return defs


def begin(text, error_expected=False):
    cprint(text + ('- Error expected.' if error_expected else ''), color='cyan')


def end():
    cprint('Test ', end='', color='cyan')
    cprint('OK\n\n', color='green')
