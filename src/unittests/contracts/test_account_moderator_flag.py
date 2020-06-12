import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

economy = load_defines('src/contracts/peeranha.main/economy.h')

MODERATOR_FLG_INFINITE_ENERGY = 1 << 0
MODERATOR_FLG_INFINITE_IMPACT = 1 << 1
MODERATOR_FLG_IGNORE_RATING = 1 << 2
MODERATOR_FLG_CREATE_COMMUNITY = 1 << 3
MODERATOR_FLG_CREATE_TAG = 1 << 4
MODERATOR_FLG_ALL = 31


class AccountModerationTests(peeranhatest.peeranhaTest):
    def test_set_moderator_flag_non_deployer_failed(self):
        begin('Not a deploer trying to give moderator rights', True)
        alice = self.register_alice_account()
        self.failed_action('givemoderflg', {
            'user': alice, 'flags': 1}, alice, 'Alice attempt to get moderator rules', 'auth')
        end()

    def test_create_tag(self):
        begin('Test create tag permission')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(alice, MODERATOR_FLG_ALL)
        self._give_moderator_flag(
            bob, MODERATOR_FLG_ALL ^ MODERATOR_FLG_CREATE_TAG)
        self.action('crtag', {'user': alice, 'name': 'Alice tag',
                              'ipfs_description': 'undefined', 'community_id': 1}, alice, 'Alice create tag')
        self.action('crtag', {'user': bob, 'name': 'Bob tag', 'ipfs_description': 'undefined',
                              'community_id': 1}, bob, 'Bob attempt to create tag')
        bt = self.table('crtagtb', get_tag_scope(1))
        be = [{
            'creator': 'bob',
            'name': 'Bob tag',
            'ipfs_description': 'undefined',
        }]
        self.assertTrue(compare(be, bt, ignore_excess=True))
        at = self.table('tags', get_tag_scope(1))
        ae = {
            'name': 'Alice tag',
            'ipfs_description': 'undefined',
        }
        self.assertTrue(compare(ae, at[6], ignore_excess=True))
        end()

    def test_infinite_energy(self):
        begin('Test use infinite energy')
        alice = self.register_alice_account(100, 0)
        self._give_moderator_flag(alice, MODERATOR_FLG_INFINITE_ENERGY)
        for i in range(10):
            self.action('postquestion', {'user': 'alice', 'title': f'AQ{i}', 'ipfs_link': 'undefined', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                        f'Register {i} question from alice')
        end()

    def test_inifinite_impact_delete_forum_items(self):
        begin('Delete forum items with moderator')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'alice', 'title': 'undefined', 'ipfs_link': 'undefined',  'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Register question from alice')
        AQ_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': AQ_id, 'ipfs_link': 'undefined', 'official_answer': False},
                    bob, 'Register Bob answer to Alice')
        AQ_BA_id = self.table('question', 'allquestions')[
            0]['answers'][0]['id']
        self.action('postcomment', {'user': 'carol', 'question_id': AQ_id, 'answer_id': AQ_BA_id,
                                    'ipfs_link': 'undefined'}, carol, 'Register Carol comment to Bob answer')
        AQ_BA_CC_id = self.table('question', 'allquestions')[
            0]['answers'][0]['comments'][0]['id']
        ted = self.register_ted_account()
        self._give_moderator_flag(ted, MODERATOR_FLG_INFINITE_IMPACT)
        account_e = ['#ignoreorder',
                     {'user': 'alice', 'rating': '#var alice_rating'},
                     {'user': 'bob', 'rating': '#var bob_rating'},
                     {'user': 'carol', 'rating': '#var carol_rating'},
                     {'user': 'ted', 'rating':  '#var ted_rating'}
                     ]
        base_rating = {}
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), base_rating, True))
        self.action('reportforum', {'user': 'ted', 'question_id': AQ_id, 'answer_id': AQ_BA_id, 'comment_id': AQ_BA_CC_id},
                    ted, 'Ted delete Alice question->Bob answer->Carol comment')
        self.action('reportforum', {'user': 'ted', 'question_id': AQ_id, 'answer_id': AQ_BA_id, 'comment_id': 0},
                    ted, 'Ted delete Alice question->Bob answer->Carol comment')
        self.action('reportforum', {'user': 'ted', 'question_id': AQ_id, 'answer_id': 0, 'comment_id': 0},
                    ted, 'Ted delete Alice question->Bob answer->Carol comment')
        new_rating = base_rating
        new_rating['alice_rating'] += economy['QUESTION_DELETED_REWARD']
        new_rating['bob_rating'] += economy['ANSWER_DELETED_REWARD']
        new_rating['carol_rating'] += economy['COMMENT_DELETED_REWARD']
        setvar(account_e, new_rating)
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        self.assertTrue(len(self.table('question', 'allquestions')) == 0)
        end()

    def infinite_impact_freze_account(self):
        begin('Freze profile with moderator')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self._give_moderator_flag(bob, MODERATOR_FLG_INFINITE_IMPACT)
        self.action('reportprof', {
                    'user': bob, 'user_to_report': 'alice'}, bob, 'Bob report alice account')
        account_e = [{
            'user': alice,
            'reports': [{
                'user': 'bob',
                'report_points': 6
            }, {
                'user': 'carol',
                'report_points': 6
            }],
            'report_power': 1,
            'is_frozen': 1
        }, {'user': bob}]
        self.assertTrue(compare(account_e, self.table(
            'account', 'allaccounts'), ignore_excess=True))
        end()

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')


if __name__ == '__main__':
    main()
