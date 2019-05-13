import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class RatingRewardsTests(peeraniatest.PeeraniaTest):

    def test_account_create_rating(self):
        begin('Test rating value for new account')
        defs = load_defines('./src/contracts/peerania/economy.h')
        alice = self.get_non_registered_alice()
        self.action('registeracc', {'user': 'alice', 'display_name': 'test',
                                    'ipfs_profile': 'test'}, alice, 'Register alice account')
        self.assertTrue(self.table(
            'account', 'allaccounts')[0]['rating'] == defs['RATING_ON_CREATE'])
        end()

    def test_vote_question(self):
        begin('Test vote for question')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account()
        self.account_e.append(
            {'user': 'ted', 'moderation_points': '#var ted_mdp', 'rating': '#var ted_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0}, ted, 'Ted upvote Alice question')
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol upvote Alice question')
        self.action('downvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': 0}, alice, 'Alice downvote bob question')
        self.var['alice_rating'] += self.defs['QUESTION_UPVOTED_REWARD'] * \
            2 + self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['bob_rating'] += self.defs['QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0}, ted, 'Ted remove upvote from Alice question')
        self.var['alice_rating'] -= self.defs['QUESTION_UPVOTED_REWARD']
        self._verify_acc()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol change her upvote to downvote')
        self.var['carol_rating'] += self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['alice_rating'] += self.defs['QUESTION_DOWNVOTED_REWARD'] - \
            self.defs['QUESTION_UPVOTED_REWARD']
        self._verify_acc()
        self.action('upvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': 0}, alice, 'Alice change her downvote to upvote')
        self.var['alice_rating'] -= self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['bob_rating'] += self.defs['QUESTION_UPVOTED_REWARD'] - \
            self.defs['QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol remove downvote')
        self.var['carol_rating'] -= self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['alice_rating'] -= self.defs['QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        info('Test history not empty')
        self.action('votedelete', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0, 'comment_id': 0},
                    bob, 'Bob vote for Alice question deletion')
        self.action('downvote', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0},
                    bob, 'Bob downvote alice question')
        self.var['alice_rating'] += self.defs['QUESTION_DOWNVOTED_REWARD']
        self.var['bob_rating'] += self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['bob_mdp'] -= 1
        self._verify_acc()
        end()

    def test_vote_answer(self):
        begin('Test vote for answer')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account()
        self.account_e.append(
            {'user': 'ted', 'moderation_points': '#var ted_mdp', 'rating': '#var ted_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, ted, 'Ted upvote Alice question->Bob answer')
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol upvote Alice question->Bob answer')
        self.action('downvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, alice, 'Alice downvote Bob question->Carol answer')
        self.var['bob_rating'] += self.defs['ANSWER_UPVOTED_REWARD'] * 2
        self.var['alice_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['carol_rating'] += self.defs['ANSWER_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, ted, 'Ted remove upvote from Alice question->Bob answer')
        self.var['bob_rating'] -= self.defs['ANSWER_UPVOTED_REWARD']
        self._verify_acc()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol change her upvote to downvote Alice question->Bob answer')
        self.var['carol_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_DOWNVOTED_REWARD'] - \
            self.defs['ANSWER_UPVOTED_REWARD']
        self._verify_acc()
        self.action('upvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, alice, 'Alice change her downvote to upvote Bob question->Carol answer')
        self.var['alice_rating'] -= self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['carol_rating'] += self.defs['ANSWER_UPVOTED_REWARD'] - \
            self.defs['ANSWER_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol remove downvote Alice question->Bob answer')
        self.var['carol_rating'] -= self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['bob_rating'] -= self.defs['ANSWER_DOWNVOTED_REWARD']
        self._verify_acc()
        info('Test history not empty')
        self.action('votedelete', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca'], 'comment_id': 0},
                    bob, 'Bob vote for Alice question->Carol Answer deletion')
        self.action('downvote', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']},
                    bob, 'Bob downvote Alice question->Carol Answer')
        self.var['carol_rating'] += self.defs['ANSWER_DOWNVOTED_REWARD']
        self.var['bob_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['bob_mdp'] -= 1
        self._verify_acc()
        end()

    def test_mark_as_correct_reward(self):
        begin('Mark answer as correct rating change')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account(3000, 1)
        self.account_e.append(
            {'user': 'ted', 'moderation_points': '#var ted_mdp', 'rating': '#var ted_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.var['alice_rating'] += self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']}, alice, "Alice mark Carol answer as correct")
        self.var['carol_rating'] += self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['bob_rating'] -= self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.wait()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': 0}, alice, "Alice unmark Bob answer as correct")
        self.var['alice_rating'] -= self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['carol_rating'] -= self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct again")
        self.var['alice_rating'] += self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.action('votedelete', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'], 'comment_id': 0}, ted, "Ted delete bob answer")
        self.var['ted_mdp'] -= 1
        self.var['alice_rating'] -= self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_DELETED_REWARD'] - \
            self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        end()

    def test_mark_as_correct_own_reward(self):
        begin('Mark own answer as correct rating change')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1]}, alice,
                    'Alice asking question')
        self.forum_e = [{
            'id': '#var aq',
            'user': 'alice',
            'ipfs_link': 'AQ',
            'correct_answer_id': '#var aq_caid',
            'answers': [],
        }]
        t = self.table('question', 'allquestions')
        self.var = {}
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        self.action('postanswer', {'user': 'alice', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->AA'},
                    alice, 'Alice answering Alice')
        self.action('postanswer', {'user': 'bob', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Bob answering Alice')

        self.forum_e[0]['answers'].append({
            'id': '#var aq_aa',
            'user': 'alice',
            'ipfs_link': 'AQ->AA'})
        self.forum_e[0]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA'})

        t = self.table('question', 'allquestions')
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        self.defs = {**load_defines('./src/contracts/peerania/economy.h')}
        self.account_e = ['#ignoreorder',
                          {'user': 'alice', 'moderation_points': '#var alice_mdp',
                           'rating': '#var alice_rating'},
                          {'user': 'bob', 'moderation_points': '#var bob_mdp',
                              'rating': '#var bob_rating'}]
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        info('hierarchy')
        info('Alice question')
        info('  |-->Alice answer')
        info('   `->Bob answer')

        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_aa']}, alice, "Alice mark Own answer as correct")
        self._verify_acc()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.var['alice_rating'] += self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.wait()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': 0}, alice, "Alice unmark Bob answer as correct")
        self.var['alice_rating'] -= self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] -= self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct again")
        self.var['alice_rating'] += self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] += self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self._verify_acc()

        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_aa']}, alice, "Alice mark Own answer as correct")
        self.var['alice_rating'] -= self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] -= self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.wait()
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': 0}, alice, "Alice unmark own answer as correct")
        self._verify_acc()
        end()

    def test_delete_own_item_reward(self):
        begin('Delete own item reward')
        (alice, bob, carol) = self._create_basic_hierarchy()
        self.action('delcomment', {'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'],
                                   'comment_id': self.var['aq_ba_ac']}, alice, "Delete Alice question->Bob answer->Alice comment")
        self.var['alice_rating'] += self.defs['DELETE_OWN_COMMENT_REWARD']
        self.action('delanswer', {
                    'user': 'carol', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, carol, "Delete Bob question->Carol answer")
        self.var['carol_rating'] += self.defs['DELETE_OWN_ANSWER_REWARD']
        self.action('delquestion', {
                    'user': 'bob', 'question_id': self.var['bq']}, bob, "Delete Bob question")
        self.var['bob_rating'] += self.defs['DELETE_OWN_QUESTION_REWARD']
        self._verify_acc()
        end()

    def test_delete_question_reward(self):
        begin('Reward when question was deleted by vote')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account(3000, 3)  # man who will delte
        self.account_e.append(
            {'user': 'ted', 'moderation_points': '#var ted_mdp', 'rating': '#var ted_rating'})
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'moderation_points': '#var dan_mdp', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        (bob_old_rt, alice_old_rt, carol_old_rt) = (
            self.var['bob_rating'], self.var['alice_rating'], self.var['carol_rating'])
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark bob answer as correct")
        self.action('upvote', {
                    'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0}, bob, "Bob upvote alice question")
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']}, alice, "Alice upvote carol answer")
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, "Carol upvote alice question")
        self.action('upvote', {
                    'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']}, bob, "Bob upvote carol answer")
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, "Carol upvote bob answer")
        self.action('upvote', {
                    'user': 'dan', 'question_id': self.var['aq'], 'answer_id': 0}, dan, "Dan upvote alice question")
        self.action('upvote', {
                    'user': 'dan', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, dan, "Dan upvote bob answer")
        self.action('upvote', {
                    'user': 'dan', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']}, dan, "Dan upvote carol answer")
        self.var['bob_rating'] += 3 * self.defs['ANSWER_UPVOTED_REWARD'] + \
            self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['alice_rating'] += 3 * self.defs['QUESTION_UPVOTED_REWARD'] + \
            self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['carol_rating'] += 3 * self.defs['ANSWER_UPVOTED_REWARD']
        self._verify_acc()
        self.action('votedelete', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0, 'comment_id': 0}, ted, "Ted delete alice question")
        self.var['ted_mdp'] -= 1
        (self.var['bob_rating'], self.var['alice_rating'], self.var['carol_rating']) = (
            bob_old_rt, alice_old_rt, carol_old_rt)
        self.var['alice_rating'] += self.defs['QUESTION_DELETED_REWARD']
        self._verify_acc()
        end()

    def test_delete_answer_reward(self):
        begin('Reward when answer was deleted by vote')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account(3000, 3)  # man who will delte
        self.account_e.append(
            {'user': 'ted', 'moderation_points': '#var ted_mdp', 'rating': '#var ted_rating'})
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'moderation_points': '#var dan_mdp', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        bob_old_rt = self.var['bob_rating']
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark bob answer as correct")
        self.action('upvote', {
                    'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0}, bob, "Bob upvote alice question")
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, "Carol upvote alice question")
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, "Carol upvote bob answer")
        self.action('upvote', {
                    'user': 'dan', 'question_id': self.var['aq'], 'answer_id': 0}, dan, "Dan upvote alice question")
        self.action('upvote', {
                    'user': 'dan', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, dan, "Dan upvote bob answer")
        self.var['bob_rating'] += 3 * self.defs['ANSWER_UPVOTED_REWARD'] + \
            self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['alice_rating'] += 3 * self.defs['QUESTION_UPVOTED_REWARD'] + \
            self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self._verify_acc()
        self.action('votedelete', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'], 'comment_id': 0}, ted, "Ted delete alice question->bob answer")
        self.var['ted_mdp'] -= 1
        self.var['alice_rating'] -= self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']
        self.var['bob_rating'] = bob_old_rt + \
            self.defs['ANSWER_DELETED_REWARD']
        self._verify_acc()
        end()

    def test_tag_or_community_created_reward(self):
        begin('Reward when tag or community created')
        defs = {**load_defines('./src/contracts/peerania/economy.h'), 
                **load_defines('./src/contracts/peerania/communities_and_tags.hpp')}
        alice = self.register_alice_account(defs['CREATE_COMMUNITY_ALLOWED'], defs['MODERATION_POINTS_CREATE_COMMUNITY'])
        bob = self.register_bob_account(defs['CREATE_TAG_ALLOWED'], defs['MODERATION_POINTS_CREATE_TAG'])
        self.action('crcommunity', {'user': alice, 'name': 'alice community',
                              'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                                    'ipfs_description': 'BCM'}, bob, 'Bob create ')
        voters = [self.register_carol_account(), self.register_dan_account(),
                  self.register_frank_account(), self.register_ted_account()]
        accounts_e = [
            {'user': 'alice', 'rating': '#var alice_rt', 'moderation_points': '#var alice_mdp'},
            {'user': 'bob', 'rating': '#var bob_rt', 'moderation_points': '#var bob_mdp'},
            {}, {}, {}, {}
        ]
        var = {}
        self.assertTrue(compare(accounts_e, self.table('account', 'allaccounts'), var, True))
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.assertTrue(var['alice_mdp'] == 0)
        self.assertTrue(var['bob_mdp'] == 0)
        for i in range(4):
            if i < 3:
                self.assertTrue(var['bob_rt'] == defs['CREATE_TAG_ALLOWED'])
                self.action('vtcrtag', {'user': voters[i], 'community_id': 1, 'tag_id': t[0]['id']}, voters[i], f'{voters[i]} vote create tag')
            else:
                self.assertTrue(var['bob_rt'] == defs['CREATE_TAG_ALLOWED'] + defs['TAG_CREATED_REWARD'])
            self.assertTrue(var['alice_rt'] == defs['CREATE_COMMUNITY_ALLOWED'])
            self.action('vtcrcomm', {'user': voters[i], 'community_id': c[0]['id']}, voters[i], f'{voters[i]} vote create community')
            compare(accounts_e, self.table('account', 'allaccounts'), var, True)
        self.assertTrue(var['alice_rt'] == defs['CREATE_COMMUNITY_ALLOWED'] + defs['COMMUNITY_CREATED_REWARD'])
        end()


    def test_tag_or_community_deleted_reward(self):
        begin('Reward when tag or community deleted')
        defs = {**load_defines('./src/contracts/peerania/economy.h'), 
                **load_defines('./src/contracts/peerania/communities_and_tags.hpp')}
        alice = self.register_alice_account(defs['CREATE_COMMUNITY_ALLOWED'], defs['MODERATION_POINTS_CREATE_COMMUNITY'])
        bob = self.register_bob_account(defs['CREATE_TAG_ALLOWED'], defs['MODERATION_POINTS_CREATE_TAG'])
        self.action('crcommunity', {'user': alice, 'name': 'alice community',
                              'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                                    'ipfs_description': 'BCM'}, bob, 'Bob create ')
        voters = [self.register_carol_account(), self.register_dan_account(),
                  self.register_frank_account(), self.register_ted_account()]
        accounts_e = [
            {'user': 'alice', 'rating': '#var alice_rt', 'moderation_points': '#var alice_mdp'},
            {'user': 'bob', 'rating': '#var bob_rt', 'moderation_points': '#var bob_mdp'},
            {}, {}, {}, {}
        ]
        var = {}
        self.assertTrue(compare(accounts_e, self.table('account', 'allaccounts'), var, True))
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        for i in range(3):
            if i < 2:
                print(var['bob_rt'])
                self.assertTrue(var['bob_rt'] == defs['CREATE_TAG_ALLOWED'])
                self.action('vtdeltag', {'user': voters[i], 'community_id': 1, 'tag_id': t[0]['id']}, voters[i], f'{voters[i]} vote delete tag')
            else:
                print(var['bob_rt'])
                self.assertTrue(var['bob_rt'] == defs['CREATE_TAG_ALLOWED'] + defs['TAG_DELETED_REWARD'])
            self.assertTrue(var['alice_rt'] == defs['CREATE_COMMUNITY_ALLOWED'])
            self.action('vtdelcomm', {'user': voters[i], 'community_id': c[0]['id']}, voters[i], f'{voters[i]} vote delete community')
            compare(accounts_e, self.table('account', 'allaccounts'), var, True)
        self.assertTrue(var['alice_rt'] == defs['CREATE_COMMUNITY_ALLOWED'] + defs['COMMUNITY_DELETED_REWARD'])
        end()

    def _create_basic_hierarchy(self):
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1]}, alice,
                    'Alice asking question')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'BQ', 'community_id': 1, 'tags': [1]}, bob,
                    'Bob asking question')
        self.forum_e = ['#ignoreorder',
                        {
                            'id': '#var aq',
                            'user': 'alice',
                            'title': 'Title alice question',
                            'ipfs_link': 'AQ',
                            'correct_answer_id': '#var aq_caid',
                            'rating': '#var aq_rating',
                            'answers': [],
                            'comments':[]
                        }, {
                            'id': '#var bq',
                            'user': 'bob',
                            'title': 'Title bob question',
                            'ipfs_link': 'BQ',
                            'correct_answer_id': '#var bq_caid',
                            'rating': '#var bq_rating',
                            'answers': [],
                            'comments':[]
                        }]
        t = self.table('question', 'allquestions')
        self.var = {}
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Bob answering Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': self.var['aq'], 'ipfs_link': 'AQ->CA'},
                    carol, 'Carol answering Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': self.var['bq'], 'ipfs_link': 'BQ->CA'},
                    carol, 'Carol answering Bob')
        self.forum_e[1]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA',
            'rating': '#var aq_aa_rating',
            'comments': []})
        self.forum_e[1]['answers'].append({
            'id': '#var aq_ca',
            'user': 'carol',
            'ipfs_link': 'AQ->CA',
            'rating': '#var aq_ca_rating',
            'comments': []})
        self.forum_e[2]['answers'].append({
            'id': '#var bq_ca',
            'user': 'carol',
            'ipfs_link': 'BQ->CA',
            'rating': '#var bq_ca_rating',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        self.action('postcomment', {'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'],
                                    'ipfs_link': 'AQ->BA->AC'}, alice, 'Register Alice comment to Alice question->Bob answer')
        self.action('postcomment', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'],
                                    'ipfs_link': 'AQ->BA->BC'}, bob, 'Register Bob comment to Alice question->Bob answer')
        self.action('postcomment', {'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0,
                                    'ipfs_link': 'AQ->CC'}, carol, 'Register Carol comment to Alice question')
        self.action('postcomment', {'user': 'alice', 'question_id': self.var['aq'], 'answer_id': 0,
                                    'ipfs_link': 'AQ->AC'}, alice, 'Register Alice comment to Alice question')
        self.forum_e[1]['answers'][0]['comments'].append({'id': '#var aq_ba_ac', 'user': 'alice', 'ipfs_link': 'AQ->BA->AC',
                                                          'properties': '#var aq_ba_ac_prop', 'history': '#var aq_ba_ac_hst'})
        self.forum_e[1]['answers'][0]['comments'].append({'id': '#var aq_ba_bc', 'user': 'bob', 'ipfs_link': 'AQ->BA->BC',
                                                          'properties': '#var aq_ba_bc_prop', 'history': '#var aq_ba_bc_hst'})
        self.forum_e[1]['comments'].append({'id': '#var aq_cc', 'user': 'carol', 'ipfs_link': 'AQ->CC',
                                            'properties': '#var aq_cc_prop', 'history': '#var aq_cc_hst'})
        self.forum_e[1]['comments'].append({'id': '#var aq_ac', 'user': 'alice', 'ipfs_link': 'AQ->AC',
                                            'properties': '#var aq_ac_prop', 'history': '#var aq_ac_hst'})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(self.forum_e, t, self.var, True))

        self.defs = {**load_defines('./src/contracts/peerania/economy.h'),
                     **load_defines('./src/contracts/peerania/question_container.hpp')}
        self.account_e = ['#ignoreorder',
                          {'user': 'alice', 'moderation_points': '#var alice_mdp',
                           'rating': '#var alice_rating'},
                          {'user': 'bob', 'moderation_points': '#var bob_mdp',
                              'rating': '#var bob_rating'},
                          {'user': 'carol', 'moderation_points': '#var carol_mdp',
                              'rating': '#var carol_rating'}]
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        info('hierarchy')
        info('Alice question')
        info('  |-->Bob answer')
        info('  |     |-->Alice comment')
        info('  |      `->Bob comment')
        info('  |-->Carol answer')
        info('  |')
        info('   `->Comments')
        info('        |-->Carol comment')
        info('         `->Alice comment')
        info('Bob question')
        info('   `->Carol answer')
        return alice, bob, carol

    def _verify_acc(self):
        buf_var = {}
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), buf_var, ignore_excess=True))
        #print(self.table('account', 'allaccounts'))
        # print(self.var)
        for key, value in buf_var.items():
            #print(self.var[key], value)
            self.assertTrue(self.var[key] == value)


    def get_stub_suggested_tags(self):
        tags = []
        for i in range(0, 10):
            tags.append({
                'name': f'Tag {i}',
                'ipfs_description': f'IPFS of tag {i}'
            })
        return tags

if __name__ == '__main__':
    main()
