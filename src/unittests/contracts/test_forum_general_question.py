import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main


class RatingRewardsTestsGeneralQuestion(peeranhatest.peeranhaTest):
    def test_change_question_type_to_general(self):
        begin('Change question type to general')
        (alice, bob, carol) = self._create_basic_hierarchy(0)
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'energy': '#var dan_energy', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        bob_old_rt = self.var['bob_rating']
        self.action('mrkascorrect', {
            'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
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
        self.var['bob_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER'] + \
            self.defs['ENERGY_MARK_ANSWER_AS_CORRECT']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['dan_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['bob_rating'] += 3 * self.defs['COMMON_ANSWER_UPVOTED_REWARD'] + \
            self.defs['COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['alice_rating'] += 3 * \
            self.defs['COMMON_QUESTION_UPVOTED_REWARD'] + self.defs['ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD']

        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': 'dan', 'flags': 32}, admin, "Give moderator flags to ted")
        self.action('chgqsttype', {
                    'user': 'dan', 'question_id': self.var['aq'], 'type': 1, 'restore_rating': True}, dan, "Change question type to general")
        self._verify_acc()
        end()

    def test_change_question_type_to_expert(self):
        begin('Change question type to expert')
        (alice, bob, carol) = self._create_basic_hierarchy()
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'energy': '#var dan_energy', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        bob_old_rt = self.var['bob_rating']
        self.action('mrkascorrect', {
            'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
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
        self.var['bob_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER'] + \
            self.defs['ENERGY_MARK_ANSWER_AS_CORRECT']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['dan_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['bob_rating'] += 3 * self.defs['ANSWER_UPVOTED_REWARD'] + \
            self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['alice_rating'] += 3 * \
            self.defs['QUESTION_UPVOTED_REWARD'] + self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']

        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': 'dan', 'flags': 32}, admin, "Give moderator flags to ted")
        self.action('chgqsttype', {
                    'user': 'dan', 'question_id': self.var['aq'], 'type': 0, 'restore_rating': True}, dan, "Change question type to expert")
        self._verify_acc()
        end()

    def test_change_question_type_without_rating_restore(self):
        begin('Change question type', True)
        (alice, bob, carol) = self._create_basic_hierarchy(0)
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'energy': '#var dan_energy', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        bob_old_rt = self.var['bob_rating']
        self.action('mrkascorrect', {
            'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice mark Bob answer as correct")
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
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
        self.var['bob_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER'] + \
            self.defs['ENERGY_MARK_ANSWER_AS_CORRECT']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['dan_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['bob_rating'] += 3 * self.defs['ANSWER_UPVOTED_REWARD'] + \
            self.defs['ANSWER_ACCEPTED_AS_CORRECT_REWARD']
        self.var['alice_rating'] += 3 * self.defs['QUESTION_UPVOTED_REWARD'] + \
            self.defs['ACCEPT_ANSWER_AS_CORRECT_REWARD']

        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': 'dan', 'flags': 32}, admin, "Give moderator flags to ted")
        self.action('chgqsttype', {
                    'user': 'dan', 'question_id': self.var['aq'], 'type': 1, 'restore_rating': False}, dan, "Change question type to general")
        self._verify_acc()
        end()

    def test_vote_question(self):
        begin('Test vote for question')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account()
        self.account_e.append(
            {'user': 'ted', 'energy': '#var ted_energy', 'rating': '#var ted_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0}, ted, 'Ted upvote Alice question')
        self.var['ted_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol upvote Alice question')
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.action('downvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': 0}, alice, 'Alice downvote bob question')
        self.var['alice_energy'] -= self.defs['ENERGY_DOWNVOTE_QUESTION']
        self.var['alice_rating'] += self.defs['COMMON_QUESTION_UPVOTED_REWARD'] * \
            2 + self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['bob_rating'] += self.defs['COMMON_QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0}, ted, 'Ted remove upvote from Alice question')
        self.var['alice_rating'] -= self.defs['COMMON_QUESTION_UPVOTED_REWARD']
        self.var['ted_energy'] -= self.defs['ENERGY_FORUM_VOTE_CHANGE']
        self._verify_acc()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol change her upvote to downvote')
        self.var['carol_rating'] += self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_DOWNVOTE_QUESTION']
        self.var['alice_rating'] += self.defs['COMMON_QUESTION_DOWNVOTED_REWARD'] - \
            self.defs['COMMON_QUESTION_UPVOTED_REWARD']
        self._verify_acc()
        self.action('upvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': 0}, alice, 'Alice change her downvote to upvote')
        self.var['alice_rating'] -= self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.var['bob_rating'] += self.defs['COMMON_QUESTION_UPVOTED_REWARD'] - \
            self.defs['COMMON_QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': 0}, carol, 'Carol remove downvote')
        self.var['carol_rating'] -= self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_FORUM_VOTE_CHANGE']
        self.var['alice_rating'] -= self.defs['COMMON_QUESTION_DOWNVOTED_REWARD']
        self._verify_acc()
        info('Test history not empty')
        self.action('reportforum', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0, 'comment_id': 0},
                    bob, 'Bob vote for Alice question deletion')
        self.action('downvote', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': 0},
                    bob, 'Bob downvote alice question')
        self.var['alice_rating'] += self.defs['COMMON_QUESTION_DOWNVOTED_REWARD']
        self.var['bob_rating'] += self.defs['DOWNVOTE_QUESTION_REWARD']
        self.var['bob_energy'] -= self.defs['ENERGY_DOWNVOTE_QUESTION'] + \
            self.defs['ENERGY_REPORT_QUESTION']
        self._verify_acc()
        end()

    def test_vote_answer(self):
        begin('Test vote for answer')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account()
        self.account_e.append(
            {'user': 'ted', 'energy': '#var ted_energy', 'rating': '#var ted_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, ted, 'Ted upvote Alice question->Bob answer')
        self.action('upvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol upvote Alice question->Bob answer')
        self.action('downvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, alice, 'Alice downvote Bob question->Carol answer')
        self.var['bob_rating'] += self.defs['COMMON_ANSWER_UPVOTED_REWARD'] * 2
        self.var['ted_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['alice_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['alice_energy'] -= self.defs['ENERGY_DOWNVOTE_ANSWER']
        self.var['carol_rating'] += self.defs['COMMON_ANSWER_DOWNVOTED_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER']
        self._verify_acc()
        self.wait()
        self.action('upvote', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, ted, 'Ted remove upvote from Alice question->Bob answer')
        self.var['ted_energy'] -= self.defs['ENERGY_FORUM_VOTE_CHANGE']
        self.var['bob_rating'] -= self.defs['COMMON_ANSWER_UPVOTED_REWARD']
        self._verify_acc()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol change her upvote to downvote Alice question->Bob answer')
        self.var['carol_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_DOWNVOTE_ANSWER']
        self.var['bob_rating'] += self.defs['COMMON_ANSWER_DOWNVOTED_REWARD'] - \
            self.defs['COMMON_ANSWER_UPVOTED_REWARD']
        self._verify_acc()
        self.action('upvote', {
            'user': 'alice', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, alice, 'Alice change her downvote to upvote Bob question->Carol answer')
        self.var['alice_rating'] -= self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['carol_rating'] += self.defs['COMMON_ANSWER_UPVOTED_REWARD'] - \
            self.defs['COMMON_ANSWER_DOWNVOTED_REWARD']
        self._verify_acc()
        self.wait()
        self.action('downvote', {
                    'user': 'carol', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, carol, 'Carol remove downvote Alice question->Bob answer')
        self.var['carol_rating'] -= self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_FORUM_VOTE_CHANGE']
        self.var['bob_rating'] -= self.defs['COMMON_ANSWER_DOWNVOTED_REWARD']
        self._verify_acc()
        info('Test history not empty')
        self.action('reportforum', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca'], 'comment_id': 0},
                    bob, 'Bob vote for Alice question->Carol Answer deletion')
        self.action('downvote', {'user': 'bob', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ca']},
                    bob, 'Bob downvote Alice question->Carol Answer')
        self.var['carol_rating'] += self.defs['COMMON_ANSWER_DOWNVOTED_REWARD']
        self.var['bob_rating'] += self.defs['DOWNVOTE_ANSWER_REWARD']
        self.var['bob_energy'] -= self.defs['ENERGY_REPORT_ANSWER'] + \
            self.defs['ENERGY_DOWNVOTE_ANSWER']
        self._verify_acc()
        end()

    def test_delete_own_item_reward(self):
        begin('Delete own item reward')
        (alice, bob, carol) = self._create_basic_hierarchy()
        self.action('delcomment', {'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'],
                                   'comment_id': self.var['aq_ba_ac']}, alice, "Delete Alice question->Bob answer->Alice comment")
        self.var['alice_rating'] += self.defs['DELETE_OWN_COMMENT_REWARD']
        self.var['alice_energy'] -= self.defs['ENERGY_DELETE_COMMENT']
        self.action('delanswer', {
                    'user': 'carol', 'question_id': self.var['bq'], 'answer_id': self.var['bq_ca']}, carol, "Delete Bob question->Carol answer")
        self.var['carol_rating'] += self.defs['DELETE_OWN_ANSWER_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_DELETE_ANSWER']
        self.action('delquestion', {
                    'user': 'bob', 'question_id': self.var['bq']}, bob, "Delete Bob question")
        self.var['bob_rating'] += self.defs['DELETE_OWN_QUESTION_REWARD']
        self.var['bob_energy'] -= self.defs['ENERGY_DELETE_QUESTION']
        self._verify_acc()
        end()

    def test_delete_question_reward(self):
        begin('Reward when question was deleted by vote')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account(10000, 3)  # man who will delte
        frank = self.register_frank_account(10000)  # man who help delete
        self.account_e.append(
            {'user': 'ted', 'energy': '#var ted_energy', 'rating': '#var ted_rating'})
        self.account_e.append({'user': 'frank'})
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'energy': '#var dan_energy', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        (bob_old_rt, alice_old_rt, carol_old_rt) = (
            self.var['bob_rating'], self.var['alice_rating'], self.var['carol_rating'])
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
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
        self.var['bob_rating'] += 3 * self.defs['COMMON_ANSWER_UPVOTED_REWARD']
        self.var['bob_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['alice_rating'] += 3 * \
            self.defs['COMMON_QUESTION_UPVOTED_REWARD']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER']*2
        self.var['carol_rating'] += 3 * \
            self.defs['COMMON_ANSWER_UPVOTED_REWARD']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['dan_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER'] * 2
        self._verify_acc()
        self.action('reportforum', {
                    'user': 'frank', 'question_id': self.var['aq'], 'answer_id': 0, 'comment_id': 0}, frank, "Frank report alice question")
        self.action('reportforum', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': 0, 'comment_id': 0}, ted, "Ted (report)delete alice question")
        self.var['ted_energy'] -= self.defs['ENERGY_REPORT_QUESTION']
        (self.var['bob_rating'], self.var['alice_rating'], self.var['carol_rating']) = (
            bob_old_rt, alice_old_rt, carol_old_rt)
        self.var['alice_rating'] += self.defs['QUESTION_DELETED_REWARD']
        self._verify_acc()
        end()

    def test_delete_answer_reward(self):
        begin('Reward when answer was deleted by vote')
        (alice, bob, carol) = self._create_basic_hierarchy()
        ted = self.register_ted_account(10000, 3)  # man who will delte
        self.account_e.append(
            {'user': 'ted', 'energy': '#var ted_energy', 'rating': '#var ted_rating'})
        dan = self.register_dan_account()
        self.account_e.append(
            {'user': 'dan', 'energy': '#var dan_energy', 'rating': '#var dan_rating'})
        self.assertTrue(compare(self.account_e, self.table(
            'account', 'allaccounts'), self.var, ignore_excess=True))
        bob_old_rt = self.var['bob_rating']
        self.action('upvote', {
                    'user': 'alice', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba']}, alice, "Alice upvote bob answer")
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
        self.var['bob_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION']
        self.var['alice_energy'] -= self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['carol_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['dan_energy'] -= self.defs['ENERGY_UPVOTE_QUESTION'] + \
            self.defs['ENERGY_UPVOTE_ANSWER']
        self.var['bob_rating'] += 3 * self.defs['COMMON_ANSWER_UPVOTED_REWARD']
        self.var['alice_rating'] += 3 * \
            self.defs['COMMON_QUESTION_UPVOTED_REWARD']
        self._verify_acc()
        self.action('reportforum', {
                    'user': 'ted', 'question_id': self.var['aq'], 'answer_id': self.var['aq_ba'], 'comment_id': 0}, ted, "Ted report alice question->bob answer")
        self.var['ted_energy'] -= self.defs['ENERGY_REPORT_ANSWER']
        self.var['bob_rating'] = bob_old_rt + \
            self.defs['ANSWER_DELETED_REWARD']
        self._verify_acc()
        end()

    def _create_basic_hierarchy(self, tp=1):
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': tp}, alice,
                    'Alice asking question')
        self.action('postquestion', {'user': 'bob', 'title': 'Title bob question', 'ipfs_link': 'BQ', 'community_id': 1, 'tags': [1], 'type': tp}, bob,
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

        self.defs = {**load_defines('./src/contracts/peeranha.main/economy.h'),
                     **load_defines('./src/contracts/peeranha.main/question_container.hpp')}
        self.account_e = ['#ignoreorder',
                          {'user': 'alice', 'energy': '#var alice_energy',
                           'rating': '#var alice_rating'},
                          {'user': 'bob', 'energy': '#var bob_energy',
                              'rating': '#var bob_rating'},
                          {'user': 'carol', 'energy': '#var carol_energy',
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
        for key, value in buf_var.items():
            #print(key, self.var[key], value)
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
