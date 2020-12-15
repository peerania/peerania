import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main


class StatisticUserCommunityTagTests(peeranhatest.peeranhaTest):

    def test_ask_question(self):
        begin('Test ask question')
        alice = self.register_alice_account()
        self.assertTrue(self.table('account', 'allaccounts')
                        [0]['questions_asked'] == 0)
        for comm in self.table('communities', 'allcomm'):
            for tag in self.table('tags', get_tag_scope(comm['id'])):
                self.assertTrue(tag['questions_asked'] == 0)
            self.assertTrue(comm['questions_asked'] == 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        self.assertTrue(self.table('account', 'allaccounts')
                        [0]['questions_asked'] == 1)
        for comm in self.table('communities', 'allcomm'):
            if comm['id'] == 1:
                for tag in self.table('tags', get_tag_scope(comm['id'])):
                    self.assertTrue(tag['questions_asked']
                                    == (1 if tag['id'] == 1 else 0))
                self.assertTrue(comm['questions_asked'] == 1)
            else:
                for tag in self.table('tags', get_tag_scope(comm['id'])):
                    self.assertTrue(tag['questions_asked'] == 0)
                self.assertTrue(comm['questions_asked'] == 0)
        end()

    def test_answer_question(self):
        begin('Test answer question')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'bob')['answers_given'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'bob', 'question_id': question_id, 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'bob')['answers_given'] == 1)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_answer_own_question(self):
        begin('Test answer own question')
        alice = self.register_alice_account()
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'alice')['answers_given'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question_id = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'alice', 'question_id': question_id, 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    alice, 'Bob answering Alice')
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'alice')['answers_given'] == 1)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_mark_as_correct(self):
        begin('Test ark answer as correct')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'bob')['correct_answers'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] == 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'bob')['correct_answers'] == 1)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_mark_yourself_as_correct(self):
        begin('test mark yourself as correct')
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'carol', 'title': 'Title alice question', 'ipfs_link': 'Alice question', 'community_id': 1, 'tags': [1, 2, 3], 'type': 0}, carol,
                    'Carol post question')
        id_question = self.table('question', 'allquestions')[0]['id']
        self.action('postanswer', {'user': 'carol', 'question_id': id_question, 'ipfs_link': 'Alice answer to herself', 'official_answer': False},
                    carol, 'Carol post answer')
        self.assertTrue(compare([{'user': 'carol', 'correct_answers': 0}], self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('mrkascorrect', {
                    'user': 'carol', 'question_id': id_question, 'answer_id': 1}, carol, "Carol mark Carol answer as correct")

        self.wait(3)
        self.assertTrue(compare([{'user': 'carol', 'rating': 200, 'correct_answers': 0}], self.table('account', 'allaccounts'), ignore_excess=True))
        self.action('mrkascorrect', {
                    'user': 'carol', 'question_id': id_question, 'answer_id': 0}, carol, "Carol dismark Carol answer as correct")
        self.assertTrue(compare([{'user': 'carol', 'rating': 200, 'correct_answers': 0}], self.table('account', 'allaccounts'), ignore_excess=True))
        end()
    
    def test_mark_as_correct_own(self):
        begin('Test answer question')
        alice = self.register_alice_account()
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'alice')['correct_answers'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] == 0)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'alice', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    alice, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        self.assertTrue(self._find_by_id(self.table(
            'account', 'allaccounts'), 'user', 'alice')['correct_answers'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_mark_as_correct_to_own(self):
        begin('Test mark answer as correct change to own')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        self.action('postanswer', {'user': 'alice', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    alice, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][1]['id']}, alice, "Alice mark Own answer as correct")
        acc = self.table('account', 'allaccounts')
        self.assertTrue(self._find_by_id(acc, 'user', 'bob')
                        ['correct_answers'] == 0)
        self.assertTrue(self._find_by_id(acc, 'user', 'alice')
                        ['correct_answers'] == 1)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_mark_as_correct_from_own(self):
        begin('Test mark answer as correct change from own')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        self.action('postanswer', {'user': 'alice', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    alice, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][1]['id']}, alice, "Alice mark Own answer as correct")
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        acc = self.table('account', 'allaccounts')
        self.assertTrue(self._find_by_id(acc, 'user', 'bob')
                        ['correct_answers'] == 1)
        self.assertTrue(self._find_by_id(acc, 'user', 'alice')
                        ['correct_answers'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_mark_as_correct_to_another(self):
        begin('Test ark answer as correct change to own')
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        carol = self.register_carol_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        self.action('postanswer', {'user': 'carol', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    carol, 'Carol answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][1]['id']}, alice, "Alice mark Carol answer as correct")
        acc = self.table('account', 'allaccounts')
        self.assertTrue(self._find_by_id(acc, 'user', 'carol')
                        ['correct_answers'] == 1)
        self.assertTrue(self._find_by_id(acc, 'user', 'bob')
                        ['correct_answers'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['correct_answers'] ==
                            (1 if comm['id'] == 1 else 0))
        end()

    def test_subscribe_stat(self):
        begin('Test subscribe stat')
        alice = self.register_alice_account()
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['users_subscribed'] == 0)
        self.action('followcomm', {
                    'user': alice, 'community_id': 1}, alice, 'Alice now following community 1')
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['users_subscribed'] ==
                            (1 if comm['id'] == 1 else 0))
        self.action('unfollowcomm', {
                    'user': alice, 'community_id': 1}, alice, 'Alice now following community 1')
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['users_subscribed'] == 0)
        end()

    def test_delete_own_question(self):
        begin("Delete own question")
        alice = self.register_alice_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        q = self.table('question', 'allquestions')
        self.action('delquestion', {
                    'user': 'alice', 'question_id': q[0]['id']}, alice, "Alice delete own question")
        self.assertTrue(self.table('account', 'allaccounts')
                        [0]['questions_asked'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['questions_asked'] == 0)
        self.assertTrue(self._find_by_id(self.table('tags', get_tag_scope(1)), 'id', 1)['questions_asked'] == 0)
        end()

    def test_delete_own_answer(self):
        begin("Delete own question")
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        q = self.table('question', 'allquestions')
        self.action('postanswer', {'user': 'bob', 'question_id': q[0]['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        q = self.table('question', 'allquestions')
        self.action('delanswer', {
                    'user': 'bob', 'question_id': q[0]['id'], 'answer_id': q[0]['answers'][0]['id']}, bob, "Bob delete own answer")
        self.assertTrue(self._find_by_id(self.table('account', 'allaccounts'), 'user', 'bob')['answers_given'] == 0)
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
        end()

    def test_delete_question_with_correct_answer_by_vote(self):
        begin("Delete question with correct answer by vote")
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        ted = self.register_ted_account(10000, 3)  # man who will delte
        dan = self.register_dan_account(10000) # man who helps delete
        self.action('reportforum', {
                    'user': 'ted', 'question_id': question['id'], 'answer_id': 0, 'comment_id': 0}, ted, "Ted report alice question")
        self.action('reportforum', {
                    'user': 'dan', 'question_id': question['id'], 'answer_id': 0, 'comment_id': 0}, dan, "Dan also report alice question")
        accounts = ["#ignoreorder",{
            'user': 'alice',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'bob',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'ted',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        }, {'user': 'dan'}]
        self.assertTrue(accounts, compare(self.table('account', 'allaccounts'), {}, True))
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
            self.assertTrue(comm['questions_asked'] == 0)
            self.assertTrue(comm['correct_answers'] == 0)
        self.assertTrue(self._find_by_id(self.table('tags', get_tag_scope(1)), 'id', 1)['questions_asked'] == 0)
        end()

    def test_delete_correct_answer_by_vote(self):
        begin("Delete correct answer by vote")
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        self.action('mrkascorrect', {
                    'user': 'alice', 'question_id': question['id'], 'answer_id': question['answers'][0]['id']}, alice, "Alice mark Bob answer as correct")
        ted = self.register_ted_account(10000, 3)  # man who will delte
        self.action('reportforum', {
                    'user': 'ted', 'question_id': question['id'], 'answer_id': question['answers'][0]['id'], 'comment_id': 0}, ted, "Ted delete alice question")
        accounts = ["#ignoreorder",{
            'user': 'alice',
            'questions_asked': 1,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'bob',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'ted',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        }]
        self.assertTrue(accounts, compare(self.table('account', 'allaccounts'), {}, True))
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
            self.assertTrue(comm['questions_asked'] == (1 if comm['id'] == 1 else 0))
            self.assertTrue(comm['correct_answers'] == 0)
        self.assertTrue(self._find_by_id(self.table('tags', get_tag_scope(1)), 'id', 1)['questions_asked'] == 1)
        end()

    def test_delete_question_by_vote(self):
        begin("Delete question by vote")
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        ted = self.register_ted_account(10000, 3)  # man who will delte
        dan = self.register_dan_account(10000) # man who helps delete
        self.action('reportforum', {
                    'user': 'ted', 'question_id': question['id'], 'answer_id': 0, 'comment_id': 0}, ted, "Ted report alice question")
        self.action('reportforum', {
                    'user': 'dan', 'question_id': question['id'], 'answer_id': 0, 'comment_id': 0}, dan, "Dan also report alice question")
        accounts = ["#ignoreorder",{
            'user': 'alice',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'bob',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'ted',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        }, {'user': 'dan'}]
        self.assertTrue(accounts, compare(self.table('account', 'allaccounts'), {}, True))
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
            self.assertTrue(comm['questions_asked'] == 0)
            self.assertTrue(comm['correct_answers'] == 0)
        self.assertTrue(self._find_by_id(self.table('tags', get_tag_scope(1)), 'id', 1)['questions_asked'] == 0)
        end()

    def test_delete_by_vote(self):
        begin("Delete answer by vote")
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1], 'type': 0}, alice,
                    'Alice asking question')
        question = self.table('question', 'allquestions')[0]
        self.action('postanswer', {'user': 'bob', 'question_id': question['id'], 'ipfs_link': 'AQ->BA', 'official_answer': False},
                    bob, 'Bob answering Alice')
        question = self.table('question', 'allquestions')[0]
        ted = self.register_ted_account(10000, 3)  # man who will delte
        self.action('reportforum', {
                    'user': 'ted', 'question_id': question['id'], 'answer_id': question['answers'][0]['id'], 'comment_id': 0}, ted, "Ted delete alice question")
        accounts = ["#ignoreorder",{
            'user': 'alice',
            'questions_asked': 1,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'bob',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        },{
            'user': 'ted',
            'questions_asked': 0,
            'answers_given': 0,
            'correct_answers': 0
        }]
        self.assertTrue(accounts, compare(self.table('account', 'allaccounts'), {}, True))
        for comm in self.table('communities', 'allcomm'):
            self.assertTrue(comm['answers_given'] == 0)
            self.assertTrue(comm['questions_asked'] == (1 if comm['id'] == 1 else 0))
            self.assertTrue(comm['correct_answers'] == 0)
        self.assertTrue(self._find_by_id(self.table('tags', get_tag_scope(1)), 'id', 1)['questions_asked'] == 1)
        end()


    def _find_by_id(self, arr, id_name, id_val):
        for item in arr:
            if item[id_name] == id_val:
                return item
        return None


if __name__ == '__main__':
    main()
