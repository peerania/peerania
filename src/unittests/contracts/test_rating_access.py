import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main


class ForumRatingRewardsTests(peeraniatest.PeeraniaTest):
    
    def test_post_question(self):
        begin('Testing assertion rating for question post')
        defs = self._get_defs()
        alice = self.register_alice_account(defs['POST_QUESTION_ALLOWED'], 1)
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1, 2, 3]}, alice,
                    'Register question from alice')
        self.action('setaccrtmpc', {'user': 'alice', 'rating': defs['POST_QUESTION_ALLOWED'] - 1, 'moderation_points': 1}, alice, "Reduce alice rating for 1")
        self.failed_action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ2', 'community_id': 1, 'tags': [1, 2, 3]}, alice,
            'Attempt to register question from alice', 'assert')
        end()
    
    def test_post_answer(self):
        begin('Testing assertion rating for posting answer')
        defs = self._get_defs()
        alice = self.register_alice_account(defs['POST_QUESTION_ALLOWED'], 1)
        bob = self.register_bob_account(defs['POST_ANSWER_ALLOWED'], 1)
        carol = self.register_carol_account(defs['POST_ANSWER_ALLOWED'] - 1, 1)
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.action('setaccrtmpc', {'user': 'alice', 'rating': defs['POST_ANSWER_OWN_ALLOWED'] - 1, 'moderation_points': 1}, alice, "Set alice rating to { POST_ANSWR_OWN_ALLOWED - 1 }")
        self.failed_action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'AQ->AA failed'},
            alice, 'Attemp to register Alice answer to Alice', 'assert')
        self.wait() #why???
        self.action('setaccrtmpc', {'user': 'alice', 'rating': defs['POST_ANSWER_OWN_ALLOWED'], 'moderation_points': 1}, alice, "Set alice rating to { POST_ANSWR_OWN_ALLOWED }")
        self.action('postanswer', {'user': 'alice', 'question_id': var['aq'], 'ipfs_link': 'AQ->AA'},
            alice, 'Register Alice answer to Alice')
        self.failed_action('postanswer', {'user': 'carol', 'question_id': var['aq'], 'ipfs_link': 'AQ->CA'},
            carol, 'Carol attempt to answer alice', 'assert')
        end()

    def test_post_comment(self):
        begin('Testing assertion rating for posting comment')
        defs = self._get_defs()
        alice = self.register_alice_account(defs['POST_QUESTION_ALLOWED'], 1)
        bob = self.register_bob_account(defs['POST_ANSWER_ALLOWED'], 1)
        carol = self.register_carol_account(defs['POST_COMMENT_ALLOWED'] - 1, 1)
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.action('setaccrtmpc', {'user': 'alice', 'rating': defs['POST_COMMENT_OWN_ALLOWED'] - 1, 'moderation_points': 1}, alice, "Set alice rating to { POST_COMMENT_OWN_ALLOWED - 1 }")
        self.action('setaccrtmpc', {'user': 'bob', 'rating': defs['POST_COMMENT_OWN_ALLOWED'] - 1, 'moderation_points': 1}, bob, "Set bob rating to { POST_COMMENT_OWN_ALLOWED - 1 }")
        self.failed_action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'test'}, alice, 'Alice attempt to comment bob answer', 'assert')
        self.failed_action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'test'}, alice, 'Alice attempt to comment own question', 'assert')
        self.failed_action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'test'}, bob, 'Bob attempt to comment own answer', 'assert')
        self.failed_action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'test'}, carol, 'Carol attempt to comment bob answer', 'assert')
        self.failed_action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'test'}, carol, 'Carol attempt to comment alice question', 'assert')
        self.wait() #why should I wait?
        self.action('setaccrtmpc', {'user': 'alice', 'rating': defs['POST_COMMENT_OWN_ALLOWED'], 'moderation_points': 1}, alice, "Set alice rating to { POST_COMMENT_OWN_ALLOWED }")
        self.action('setaccrtmpc', {'user': 'bob', 'rating': defs['POST_COMMENT_OWN_ALLOWED'], 'moderation_points': 1}, bob, "Set bob rating to { POST_COMMENT_OWN_ALLOWED }")
        self.action('setaccrtmpc', {'user': 'carol', 'rating': defs['POST_COMMENT_ALLOWED'], 'moderation_points': 1}, carol, "Set carol rating to { POST_COMMENT_ALLOWED }")
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'AQ->BA->AC'}, alice, 'Alice comment bob answer')
        self.action('postcomment', {'user': 'alice', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'AQ->AC'}, alice, 'Alice comment own question')
        self.action('postcomment', {'user': 'bob', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'AQ->BA->BC'}, bob, 'Bob comment own answer')
        self.action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba'], 'ipfs_link': 'AQ->BA->CC'}, carol, 'Carol comment bob answer', )
        self.action('postcomment', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0, 'ipfs_link': 'AQ->CC'}, carol, 'Carol comment alice question',)
        end()

    def test_upvote(self):
        begin('Testing assertion for upvote')
        defs = self._get_defs()
        alice = self.register_alice_account(defs['POST_QUESTION_ALLOWED'], 1)
        bob = self.register_bob_account(defs['POST_ANSWER_ALLOWED'], 1)
        carol = self.register_carol_account(defs['UPVOTE_ALLOWED'] - 1, 1)
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol attempt to upvote Alice question', 'assert')
        self.failed_action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol attempt to upvote Alice question -> Bob answer', 'assert')
        self.action('setaccrtmpc', {'user': 'carol', 'rating': defs['UPVOTE_ALLOWED'], 'moderation_points': 1}, carol, "Set carol rating to { UPVOTE_ALLOWED }")
        self.wait()
        self.action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol upvote Alice question')
        self.action('upvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol upvote Alice question -> Bob answer')
        end()

    def test_downvote(self):
        begin('Testing assertion for downvote')
        defs = self._get_defs()
        alice = self.register_alice_account(defs['POST_QUESTION_ALLOWED'], 1)
        bob = self.register_bob_account(defs['POST_ANSWER_ALLOWED'], 1)
        carol = self.register_carol_account(defs['DOWNVOTE_ALLOWED'] - 1, 1)
        (e, var) = self._create_simple_hierarchy(alice, bob)
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol attempt to downvote Alice question', 'assert')
        self.failed_action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol attempt to downvote Alice question -> Bob answer', 'assert')
        self.action('setaccrtmpc', {'user': 'carol', 'rating': defs['DOWNVOTE_ALLOWED'], 'moderation_points': 1}, carol, "Set carol rating to { DOWNVOTE_ALLOWED }")
        self.wait()
        self.action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': 0}, carol, 'Carol downvote Alice question')
        self.action('setaccrtmpc', {'user': 'carol', 'rating': defs['DOWNVOTE_ALLOWED'], 'moderation_points': 1}, carol, "Set carol rating to { DOWNVOTE_ALLOWED }")
        self.action('downvote', {'user': 'carol', 'question_id': var['aq'], 'answer_id': var['aq_ba']}, carol, 'Carol downvote Alice question -> Bob answer')
        end()

    def test_create_tag_or_community(self):
        begin('Testing assertion for create tag or community', True)
        defs = self._get_defs()
        alice = self.register_alice_account(defs['CREATE_TAG_ALLOWED'], 10)
        bob = self.register_bob_account(defs['CREATE_TAG_ALLOWED'] -1, 10)
        carol = self.register_carol_account(defs['CREATE_COMMUNITY_ALLOWED'], 10)
        dan = self.register_dan_account(defs['CREATE_COMMUNITY_ALLOWED'] -1, 10)
        self.action('crtag', {'user': alice, 'name': 'alice tag', 'ipfs_description': 'AT', 'community_id': 1}, alice, 'Alice create tag')
        self.failed_action('crtag', {'user': bob, 'name': 'bob tag', 'ipfs_description': 'BT', 'community_id': 1}, bob, 'Bob attempt to create tag', 'assert')
        self.action('crcommunity', {'user': carol, 'name': 'alice community', 'ipfs_description': 'ACM'}, carol, 'Carol create community')
        self.failed_action('crcommunity', {'user': dan, 'name': 'bob community', 'ipfs_description': 'BCM'}, dan, 'Dan attempt to create community', 'assert')
        end()

    def test_vote_create_tag_or_community(self):
        begin('Testing assertion for vote create tag or community', True)
        defs = self._get_defs()
        ted = self.register_ted_account(30000, 10)
        self.action('crtag', {'user': ted, 'community_id': 1, 'name': 'ted tag', 'ipfs_description': 'TT'}, ted, 'Ted create tag')
        self.action('crcommunity', {'user': ted, 'name': 'ted community', 'ipfs_description': 'TCM'}, ted, 'Ted create community')
        c = self.table('crtagcomm', 'allcomm')
        t = self.table('crtagcomm', get_tag_scope(1))
        alice = self.register_alice_account(defs['VOTE_CREATE_TAG_ALLOWED'], 10)
        bob = self.register_bob_account(defs['VOTE_CREATE_TAG_ALLOWED'] -1, 10)
        carol = self.register_carol_account(defs['VOTE_CREATE_COMMUNITY_ALLOWED'], 10)
        dan = self.register_dan_account(defs['VOTE_CREATE_COMMUNITY_ALLOWED'] -1, 10)
        self.action('vtcrtag', {'user': alice, 'community_id': 1, 'tag_id': t[0]['id']}, alice, 'Alice vote create tag')
        self.failed_action('vtcrtag', {'user': bob, 'community_id': 1, 'tag_id': t[0]['id']}, bob, 'Tad attempt to vote create tag', 'assert')
        self.action('vtcrcomm', {'user': carol, 'community_id': c[0]['id']}, carol, 'Carol vote create community')
        self.failed_action('vtcrcomm', {'user': dan, 'community_id': c[0]['id']}, dan, 'Dan attempt to vote create community', 'assert')
        end()
    
    def test_vote_delete_tag_or_community(self):
        begin('Testing assertion for vote delete tag or community', True)
        defs = self._get_defs()
        ted = self.register_ted_account(30000, 10)
        self.action('crtag', {'user': ted, 'community_id': 1, 'name': 'ted tag', 'ipfs_description': 'TT'}, ted, 'Ted create tag')
        self.action('crcommunity', {'user': ted, 'name': 'ted community', 'ipfs_description': 'TCM'}, ted, 'Ted create community')
        c = self.table('crtagcomm', 'allcomm')
        t = self.table('crtagcomm', get_tag_scope(1))
        alice = self.register_alice_account(defs['VOTE_DELETE_TAG_ALLOWED'], 10)
        bob = self.register_bob_account(defs['VOTE_DELETE_TAG_ALLOWED'] -1, 10)
        carol = self.register_carol_account(defs['VOTE_DELETE_COMMUNITY_ALLOWED'], 10)
        dan = self.register_dan_account(defs['VOTE_DELETE_COMMUNITY_ALLOWED'] -1, 10)
        self.action('vtdeltag', {'user': alice, 'community_id': 1, 'tag_id': t[0]['id']}, alice, 'Alice vote delete tag')
        self.failed_action('vtdeltag', {'user': bob, 'community_id': 1, 'tag_id': t[0]['id']}, bob, 'Tad attempt to vote delete tag', 'assert')
        self.action('vtdelcomm', {'user': carol, 'community_id': c[0]['id']}, carol, 'Carol vote delete community')
        self.failed_action('vtdelcomm', {'user': dan, 'community_id': c[0]['id']}, dan, 'Dan attempt to vote delete community', 'assert')
        end()

    def _get_defs(self):
        return load_defines('./src/contracts/peerania/economy.h')

    def _create_simple_hierarchy(self, alice, bob):
        self.action('postquestion', {'user': 'alice', 'title': 'Title alice question', 'ipfs_link': 'AQ', 'community_id': 1, 'tags': [1, 2, 3]}, alice,
                    'Register question from alice')
        e = [{
            'id': '#var aq',
            'user': 'alice',
            'title': 'Title alice question', 
            'ipfs_link': 'AQ',
            'properties': '#var aq_prop',
            'history': '#var aq_hst',
            'correct_answer_id': '#var aq_caid',
            'answers': [],
            'comments': []}]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        self.action('postanswer', {'user': 'bob', 'question_id': var['aq'], 'ipfs_link': 'AQ->BA'},
                    bob, 'Register Bob answer to Alice')
        e[0]['answers'].append({
            'id': '#var aq_ba',
            'user': 'bob',
            'ipfs_link': 'AQ->BA',
            'properties': '#var aq_ba_prop',
            'history': '#var aq_ba_hst',
            'comments': []})
        t = self.table('question', 'allquestions')
        self.assertTrue(compare(e, t, var, True))
        info('Hierarchy look like')
        info('Alice question')
        info('  `-->Bob answer')
        return (e, var)

if __name__ == '__main__':
    main()
