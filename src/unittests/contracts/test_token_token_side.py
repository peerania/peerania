import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from threading import Timer

PERIOD_LENGTH = 3

INFLATION_PERIOD = 2
RATING_TOKEN_COEFFICIENT = 8
POOL_REDUSE_COEFFICIENT = 0.5
START_POOL = 40
TOTAL_USER_SUPPLY = 60

SCOPE = '......2mcp2p'


class TestTokenIntegration(peeranhatest.peeranhaTest):

    def test_pick_up_future_reward_failed(self):
        begin("Test call pick up reward with period is not yet come", True)
        alice = self.register_alice_account()
        self.failed_action('pickupreward', {'user': 'alice', 'period': 100},
                           'alice', 'Alice attempt to pickuprewerd', 'assert', contract='token')
        end()

    def test_get_inflation_method(self):
        begin("Test get inflation", True)
        alice = self.register_alice_account()
        data = [
            {
                'period': 0,
                'total_rating': 10,
                'expected': 40,
            }, {
                'period': 1,
                'total_rating': 10,
                'expected': 40,
            }, {
                'period': 2,
                'total_rating': 10,
                'expected': 20,
            }, {
                'period': 3,
                'total_rating': 10,
                'expected': 20,
            }, {
                'period': 0,
                'total_rating': 2,
                'expected': 16,
            }, {
                'period': 1,
                'total_rating': 2,
                'expected': 16,
            }, {
                'period': 2,
                'total_rating': 2,
                'expected': 16,
            }, {
                'period': 3,
                'total_rating': 2,
                'expected': 16,
            },
        ]
        for i in range(len(data)):
            self.action('mapcrrwpool', {'id': i, 'period': data[i]['period'], 'total_rating': data[i]['total_rating']},
                           'alice', f'Test with data {data[i]}', contract='token')
            self._compare_rewards(data[0]['expected'], self.table('dbginfl', 'allconstants', contract='token')[0]['inflation'])
            self.action('resettables', {}, self.admin, 'Reset')
            self.wait()
        end()

    def test_pick_up_reward_another_owner_failed(self):
        begin("Test call pick up reward with period is not yet come", True)
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.wait(PERIOD_LENGTH)
        self.failed_action('pickupreward', {'user': 'alice', 'period': 0},
                           'bob', 'Alice attempt to pickuprewerd', 'auth', contract='token')
        end()

    def test_pick_up_reward1(self):
        begin("Test puckupreward 1")
        scenario = [[0, 1, 1],      # week 0
                    [1, 0, 1],      # week 1
                    [1, 1, 0],      # week 2
                    [0, 1, 1],      # week 3
                    [1, 15, 1],     # week 4
                    [1, 1, 1]]      # week 5
        self._run_scenario(scenario)
        end()

    def test_pick_up_reward2(self):
        begin("Test puckupreward 2")
        scenario = [[0, 10, 1],      # week 0
                    [10, 0, 1],      # week 1
                    [1, 10, 0],      # week 2
                    [0, 1, 10],      # week 3
                    [1, 15, 10],     # week 4
                    [1, 15, 10],     # week 5
                    [1, 15, 10]]     # week 7
        self._run_scenario(scenario)
        end()

    def test_pick_up_reward_failed(self):
        begin('Test pick up this week, pick up twice', True)
        alice = self.register_alice_account(10, 10)
        bob = self.register_bob_account(10, 10)
        for i in range(4):
            self.action('chnguserrt', {'user': alice, 'rating_change': 1},
                        self.admin, alice + ' rating change 1')
            if i == 2:
                self.failed_action('pickupreward', {'user': alice, 'period': i},
                                   alice, alice + ' attempt to pickup reward this period ' + str(i) + ' preiod', 'assert', contract='token')
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

    def _get_inflation(self, total_rating_to_reward, period_id, issued_reward):
        max_inflation = START_POOL * \
            (POOL_REDUSE_COEFFICIENT) ** (period_id // INFLATION_PERIOD)
        user_iflation = total_rating_to_reward * RATING_TOKEN_COEFFICIENT
        remaining_tokens = TOTAL_USER_SUPPLY - float(issued_reward[:-5])
        return min(max_inflation, user_iflation, remaining_tokens)

    def _get_reward(self, period_id, total_rating, user_rating, issued_reward):
        return self._get_inflation(total_rating, period_id, issued_reward) * user_rating / total_rating

    def _compare_rewards(self, expected, received, accuracy=2):
        self.assertTrue(
            (abs(float(received.split(" ")[0]) - expected)) < accuracy*10**-6)

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
        total_reward = 0
        issued_reward = '0 PEER'
        #sleep(PERIOD_LENGTH)
        for period in rating_change_scenario:
            info(f'Period {period_id} started')
            for i in range(3):
                self.action('chnguserrt', {'user': all_users[i], 'rating_change': period[i]},
                            self.admin, all_users[i] + ' rating change ' + str(period[i]))
                if(period[i] != 0):
                    e_user_rating[i].append(
                        self._build_rating_element(period_id, all_users[i]))
            sleep(PERIOD_LENGTH)

            if period_id > 1:
                for i in range(3):
                    name = all_users[i]
                    if rating_change_scenario[period_id-1][i] != 0:
                        self.action('pickupreward', {'user': name, 'period': period_id-1},
                                    name, name + ' pick up his reward for ' + str(period_id-1) + ' preiod', contract='token')
                        if 'total_rating_to_reward' in var:
                            user_rating = int(var['rating_to_award_'+name])
                            total_rating = int(var['total_rating_to_reward'])
                            user_reward_this_period = self._get_reward(
                                period_id-1, total_rating, user_rating, issued_reward)
                            total_reward += user_reward_this_period
                            user_reward[i] += user_reward_this_period
                            info(
                                f'{all_users[i]} pick up {user_reward_this_period}')
                            self._compare_rewards(user_reward[i], self.table(
                                'accounts', name, contract='token')[0]["balance"])
                    else:
                        self.failed_action('pickupreward', {'user': name, 'period': period_id-1},
                                           name, name + ' pick up his reward for ' + str(period_id-1) + ' preiod', 'assert', contract='token')
                stat = self.table('stat', '......2mcp2p', contract='token')[0]
                issued_reward = stat['user_supply']
                self._compare_rewards(total_reward, issued_reward, 2*period_id)
                info('Period: ' + str(period_id-1))
                info('Issued reward: ' + str(issued_reward))
                if 'total_rating_to_reward' in var:
                    info(
                        'Inflation: ' + str(self._get_inflation(int(var['total_rating_to_reward']), period_id-1, issued_reward)))
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
