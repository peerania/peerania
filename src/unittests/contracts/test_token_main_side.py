import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
from threading import Timer


class TestTokenIntegration(peeranhatest.peeranhaTest):
    PERIOD_LENGTH = 3

    def test_simple_rating_up(self):
        begin('One user, rating rises on each week')
        scenario = [{'users': [{'name': 'alice', 'rating_change': [1, -2, 3]}]},  # week 1
                    {'users': [{'name': 'alice', 'rating_change': [4, -2, -1]}]}, # week 2
                    {'users': [{'name': 'alice', 'rating_change': [-5, 7, -1]}]}, # week 3
                    {'users': [{'name': 'alice', 'rating_change': [-3, 8, 2]}]}]  # week 4
        self._run_scenario(scenario)
        end()

    def test_rating_loosage(self):
        begin('One user, rating loosage')
        scenario = [{'users': [{'name': 'alice', 'rating_change': [10, 9, 8]}]},    # week 1
                    {'users': [{'name': 'alice', 'rating_change': [-10, -9, -8]}]}, # week 2
                    {'users': [{'name': 'alice', 'rating_change': [10, 10, 10]}]},  # week 3
                    {'users': [{'name': 'alice', 'rating_change': [10, 11, 12]}]}]  # week 4
        self._run_scenario(scenario)
        end()

    def test_rose_fell_rose(self):
        begin('Rating rose, fell, then rose again')
        scenario = [{'users': [{'name': 'alice', 'rating_change': [3, -2, 3]}]},   # week 1
                    {'users': [{'name': 'alice', 'rating_change': [-5, 10, -1]}]}, # week 2
                    {'users': [{'name': 'alice', 'rating_change': [-10, -9, 8]}]}, # week 3
                    {'users': [{'name': 'alice', 'rating_change': [10, 9, -8]}]},  # week 4
                    {'users': [{'name': 'alice', 'rating_change': [1, 1, 1]}]}]    # week 5
        self._run_scenario(scenario)
        end()

    def test_multiple_user_losage(self):
        begin('Test scenario with many users(the second user loose his rating)')
        scenario = [{'users': [{'name': 'alice', 'rating_change': [10, 9, 8]},
                               {'name': 'bob', 'rating_change': [10, 9, 8, 1]}]},      # week 1
                    {'users': [{'name': 'alice', 'rating_change': [-10, -9, -8]},
                               {'name': 'bob', 'rating_change': [-10, -9, -8, 1]}]},   # week 2
                    {'users': [{'name': 'alice', 'rating_change': [10, 10, 10]},
                               {'name': 'bob', 'rating_change': [10, -10, 0, 1]}]},    # week 3
                    {'users': [{'name': 'alice', 'rating_change': [10, 11, 12, 1]}]}]  # week 4
        self._run_scenario(scenario)
        end()

    def test_multiple_user_rose(self):
        begin('Many users, rating rises on each week')
        scenario = scenario = [{'users': [{'name': 'alice', 'rating_change': [1, 2, -1]},
                                          {'name': 'bob', 'rating_change': [2, 3, -1, 2]}]},     # week 1
                               {'users': [{'name': 'alice', 'rating_change': [-1, 3, 2]},
                                          {'name': 'bob', 'rating_change': [3, -3, 0, 0]}]},     # week 2
                               {'users': [{'name': 'alice', 'rating_change': [0, -1, 1]},
                                          {'name': 'bob', 'rating_change': [1, -1, 2, 1]}]},     # week 3
                               {'users': [{'name': 'alice', 'rating_change': [3, 4, 2]},
                                          {'name': 'bob', 'rating_change': [-10, 15, 10, 1]}]}]  # week 4
        self._run_scenario(scenario)
        end()

    def _build_user_rating_element(self, period):
        return {
            'period': period,
            'rating': '#var rating',
            'rating_to_award': '#var rating_to_award'
        }

    def _build_total_rating_element(self, period):
        return {
            'period': period,
            'total_rating_to_reward': '#var total_rating_to_reward'
        }

    def _fing_item_with_period(self, period, array):
        for item in array:
            if item != '#ignoreorder' and item['period'] == period:
                return item
        return None

    def _update_rating(self, user, rating_change):
        self.action('chnguserrt', {
            'user': user, 'rating_change': rating_change}, self.admin, user + ' rating change ' + str(rating_change))

    def _run_scenario(self, rating_change_scenario):
        all_users = [self.register_alice_account(10, 10),
                     self.register_bob_account(10, 10),
                     self.register_carol_account(10, 10)]
        e_total_rating = ['#ignoreorder']
        e_user_rating = {'alice': ['#ignoreorder'],
                         'bob': ['#ignoreorder'],
                         'carol': ['#ignoreorder']}
        user_paid_out_rating = {'alice': 10,
                                'bob': 10,
                                'carol': 10}
        user_rating = {'alice': 10,
                       'bob': 10,
                       'carol': 10}
        period_id = 0
        for period in rating_change_scenario:
            for user in period['users']:
                #Bottleneck place
                #How to synchronize period end in contract with test class
                pause = self.PERIOD_LENGTH / (len(user['rating_change']) + 3)
                tick_in = pause / 6
                for rating_change in user['rating_change']:
                    user_rating[user['name']] += rating_change
                    Timer(tick_in, self._update_rating,
                          (user['name'], rating_change)).start()
                    tick_in += pause
                e_user_rating[user['name']].append(
                    self._build_user_rating_element(period_id))
            sleep(self.PERIOD_LENGTH)
            total = 0
            info('Rewards')
            for user in period['users']:
                name = user['name']
                user_rating_var = {}
                self.assertTrue(compare(e_user_rating[name], self.table(
                    'periodrating', name), user_rating_var))
                setvar(e_user_rating[name], user_rating_var)
                info(name + ' rating is ' + str(user_rating_var['rating']))
                previous_week = self._fing_item_with_period(
                    period_id - 1, e_user_rating[name])
                this_week = self._fing_item_with_period(
                    period_id, e_user_rating[name])
                self.assertTrue(this_week['rating'] == user_rating[name])
                if not previous_week is None:
                    base = min(previous_week['rating'], this_week['rating'])
                    rating_to_award = base - user_paid_out_rating[name]
                    if rating_to_award > 0:
                        info(name + ' reward rating is ' + str(rating_to_award))
                        total += rating_to_award
                        user_paid_out_rating[name] += rating_to_award
                        self.assertTrue(
                            this_week['rating_to_award'] == rating_to_award)
                    else:
                        info(name + ' reward rating is 0')
                        self.assertTrue(this_week['rating_to_award'] == 0)
                else:
                    info(name + ' reward rating is 0')
                    self.assertTrue(this_week['rating_to_award'] == 0)
            e_total_rating.append(self._build_total_rating_element(period_id))
            total_get = self._fing_item_with_period(
                period_id, self.table('totalrating', 'allperiods'))
            if total_get is None:
                self.assertTrue(total == 0)
            else:
                self.assertTrue(total_get['total_rating_to_reward'] == total)
            info('Period finished!!\n')
            period_id += 1
        info('table all periods', self.table('totalrating', 'allperiods'))


if __name__ == '__main__':
    main()
