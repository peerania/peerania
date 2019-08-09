import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from threading import Timer

PERIOD_LENGTH = 3

INFLATION_PERIOD = 2
POOL_REDUSE = 100000
START_POOL = 200000

SCOPE = '......2mcp2p'
class TestTokenIntegration(peeranhatest.peeranhaTest):

    def test_pick_up_future_reward_failed(self):
        begin("Test call pick up reward with period is not yet come", True)
        alice = self.register_alice_account()
        self.failed_action('pickupreward', {'user': 'alice', 'period': 100},
                           'alice', 'Alice attempt to pickuprewerd', 'assert', contract='token')
        end()

    def test_pick_up_reward_another_owner_failed(self):
        begin("Test call pick up reward with period is not yet come", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.wait(PERIOD_LENGTH)
        self.failed_action('pickupreward', {'user': 'alice', 'period': 0},
                           'bob', 'Alice attempt to pickuprewerd', 'auth', contract='token')
        end()

    def test_pick_up_reward(self):
        begin("Test puckupreward")
        scenario = [[0, 1, 1],      # week 0
                    [1, 0, 1],      # week 1
                    [1, 1, 0],      # week 2
                    [0, 1, 1],      # week 3
                    [1, 15, 1],     # week 4
                    [1, 1, 1]]      # week 5
        self._run_scenario(scenario)
        end()

    def test_pick_up_reward_failed(self):
        begin('Test pick up this week, pick up twice', True)
        alice = self.register_alice_account(10, 10)
        bob = self.register_bob_account(10, 10)
        for i in range(4):
            self.action('chnguserrt', {'user': alice, 'rating_change': 1},
                        alice, alice + ' rating change 1')
            if i == 2:
                self.failed_action('pickupreward', {'user': alice, 'period': i},
                        alice, alice + ' attempt to pickup reward this period ' + str(i) + ' preiod', 'assert',contract='token')
            self.wait(PERIOD_LENGTH)
        self.action('pickupreward', {'user': alice, 'period': 2},
                                alice, alice + ' pick up her reward for 2 preiod', contract='token')
        self.wait()
        self.failed_action('pickupreward', {'user': alice, 'period': 2},
                        alice, alice + ' attempt to pickup reward this period 2 preiod', 'assert', contract='token')

        for i in range(3):
            self.failed_action('pickupreward', {'user': bob, 'period': i},
                        bob, f'{bob} attempt to pickup reward this period {i} preiod', 'assert', contract='token')

        carol = self.get_non_registered_carol()
        self.failed_action('pickupreward', {'user': carol, 'period': 2},
                    carol, 'Craol attempt to pickuprewerd with no registred acount', 'assert', contract='token')
        end()

    def _build_rating_element(self, period, owner=None):
        if owner is None:
            return {
                'period': period,
                'total_rating_to_reward': '#var total_rating_to_reward'
            }
        else:
            return {
                'period': period,
                'rating': '#ignore',
                'rating_to_award': '#var rating_to_award_' + owner
            }

    def _get_inflation(self, period_id):
        inf = START_POOL - (period_id//INFLATION_PERIOD) * POOL_REDUSE
        if (inf < 0):
            inf = 0
        return inf

    def _get_reward(self, period_id, total_rating, user_rating):
        return self._get_inflation(period_id) * user_rating / total_rating

    def _compare_rewards(self, expected, received, accuracy = 2):
        self.assertTrue((abs(float(received.split(" ")[0]) - expected)) < accuracy*10**-6)

    # Takes matrix
    ## row - week; column - actor(alice, bob, carol)
    def _run_scenario(self, rating_change_scenario):
        all_users = [self.register_alice_account(10, 10),
                     self.register_bob_account(10, 10),
                     self.register_carol_account(10, 10)]
        period_id = 0
        var = {}
        e_total_rating = ['#ignoreorder']
        e_user_rating = [['#ignoreorder'],
                         ['#ignoreorder'],
                         ['#ignoreorder']]
        user_reward = [0, 0, 0]
        for period in rating_change_scenario:
            info(f'Period {period_id} started')
            for i in range(3):
                self.action('chnguserrt', {'user': all_users[i], 'rating_change': period[i]},
                            all_users[i], all_users[i] + ' rating change ' + str(period[i]))
                if(period[i] != 0):
                    e_user_rating[i].append(
                        self._build_rating_element(period_id, all_users[i]))
            sleep(PERIOD_LENGTH)
            total = 0
            if period_id > 1:
                for i in range(3):
                    name = all_users[i]
                    if  rating_change_scenario[period_id-1][i] != 0:
                        self.action('pickupreward', {'user': name, 'period': period_id-1},
                                name, name + ' pick up his reward for ' + str(period_id-1) + ' preiod', contract='token')
                        if 'total_rating_to_reward' in var:
                            user_rating = int(var['rating_to_award_'+name])
                            total_rating = int(var['total_rating_to_reward'])
                            user_reward[i] += self._get_reward(
                                period_id-1, total_rating, user_rating)
                            info(f'{all_users[i]} pick up {self._get_reward(period_id-1, total_rating, user_rating)}')
                            self._compare_rewards(user_reward[i], self.table(
                                'accounts', name, contract='token')[0]["balance"])
                    else:
                        self.failed_action('pickupreward', {'user': name, 'period': period_id-1},
                                name, name + ' pick up his reward for ' + str(period_id-1) + ' preiod', 'assert',contract='token')
                residue = self.table('accounts', 'peeranha.dev', contract='token')[0]["balance"]
                self._compare_rewards(0, residue, 2*period_id)
                info('Period: ' + str(period_id-1))
                info('Pool residue: ' + str(residue))
                info('Inflation: ' + str(self._get_inflation(period_id-1)))
            for i in range(3):
                self.assertTrue(compare(e_user_rating[i], self.table(
                    'periodrating', all_users[i]), var))
                setvar(e_user_rating[i], var)
            if period_id > 0:
                e_total_rating.append(self._build_rating_element(period_id))
                self.assertTrue(compare(e_total_rating, self.table(
                    'totalrating', 'allperiods'), var))
                setvar(e_total_rating, var)
            info('Period finished!!\n')
            period_id += 1

    def _fing_item_with_period(self, period, array):
        for item in array:
            if item != '#ignoreorder' and item['period'] == period:
                return item
        return None


if __name__ == '__main__':
    main()
