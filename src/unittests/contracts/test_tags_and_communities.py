import peeraniatest
from peeraniatest import *
from jsonutils import *
from unittest import main
#NOT IMPLEMENTED YET
class TagsAndCommunitiesTests(peeraniatest.PeeraniaTest):

    def test_popularity_rewrite(self):
        self._create_basic_hierarchy()
        info('communities:', self.table('tagandcomm', 'allcomm'))
        info('tags of 1 community:', self.table('tagandcomm', get_tag_scope(1)))

    def test_vote_rewrite(self):
        alice = self.register_alice_account(30000, 10)
        bob = self.register_bob_account(30000, 10)
        self.action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'Alice tag', 'ipfs_description': 'Alice tag description'}, alice,
                    'Alice create tag')
        info('Tags to be created for 1 community:', self.table('crtagcomm', get_tag_scope(1)))
        self.action('vtcrtag', {'user': bob, 'community_id': 1, 'tag_id': 4294967295}, bob, 'Bob wants to add tag', True)
        info('Tags to be created for 1 community:', self.table('crtagcomm', get_tag_scope(1)))
        info('tags of 1 community:', self.table('tagandcomm', get_tag_scope(1), limit = 11))

    def _create_basic_hierarchy(self):
        alice = self.register_alice_account()
        self.action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [1, 2, 3, 4], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
                    'Alice asking question')
        self.forum_e = ['#ignoreorder',
                        {
                            'id': '#var aq',
                            'community_id': 1,
                            'tags': [1, 2, 3, 4],
                            'user': 'alice',
                            'title': 'Title alice question',
                            'ipfs_link': 'AQ',
                            'correct_answer_id': '#var aq_caid',
                            'rating': '#var aq_rating',
                            'answers': [],
                            'comments':[]
                        }]
        t = self.table('question', 'allquestions')

        self.var = {}
        self.assertTrue(compare(self.forum_e, t, self.var, True))
        return alice


if __name__ == '__main__':
    main()
