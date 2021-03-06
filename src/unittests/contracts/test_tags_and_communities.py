import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main
# NOT IMPLEMENTED YET


class TagsAndCommunitiesTests(peeranhatest.peeranhaTest):

    def test_modify_question(self):
        begin("Testing work of tags and communities, when question modified")
        alice, bob, e, var = self._create_basic_hierarchy()
        c = self.table('communities', 'allcomm')
        self.assertTrue(c[0]['questions_asked'] ==
                        2 and c[1]['questions_asked'] == 0)
        t = self.table('tags', get_tag_scope(c[0]['id']))
        pupularity1 = [1, 2, 2, 1, 1, 0]
        for i in range(6):
            self.assertTrue(t[i]['questions_asked'] == pupularity1[i])
        self.action('modquestion', {'user': 'alice', 'question_id': var['aq'], 'community_id': 1, 'tags': [1, 4, 6], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
                    'Alice modify own question')
        e[1]['tags'] = [1, 4, 6]
        self.assertTrue(compare(e, self.table(
            'question', 'allquestions'), var, True))
        pupularity1 = [2, 1, 1, 1, 0, 1]
        t = self.table('tags', get_tag_scope(c[0]['id']))
        for i in range(6):
            self.assertTrue(t[i]['questions_asked'] == pupularity1[i])
        self.action('modquestion', {'user': 'bob', 'question_id': var['bq'], 'community_id': 2, 'tags': [1, 3], 'title': 'Title bob question', 'ipfs_link': 'BQ'}, bob,
                    'Bob modify own question')
        c = self.table('communities', 'allcomm')
        e[2]['community_id'] = c[1]['id']
        e[2]['tags'] = [1, 3]
        self.assertTrue(compare(e, self.table(
            'question', 'allquestions'), var, True))
        pupularity1 = [1, 0, 0, 1, 0, 1]
        t = self.table('tags', get_tag_scope(c[0]['id']))
        self.assertTrue(c[0]['questions_asked'] == 1 and c[1]['questions_asked'] == 1)
        for i in range(6):
            self.assertTrue(t[i]['questions_asked'] == pupularity1[i])
        pupularity2 = [1, 0, 1]
        t = self.table('tags', get_tag_scope(c[1]['id']))
        for i in range(3):
            self.assertTrue(t[i]['questions_asked'] == pupularity2[i])
        end()

    def test_delete_question(self):
        begin("Testing work of tags and communities, when question deleted")
        alice, bob, e, var = self._create_basic_hierarchy()
        carol = self.register_carol_account(30000, 10)
        dan = self.register_dan_account(10000)
        self.action('delquestion', {
                    'user': 'alice', 'question_id': var['aq']}, alice, 'Alice delete own question')
        c = self.table('communities', 'allcomm')
        self.assertTrue(c[0]['questions_asked'] ==
                        1 and c[1]['questions_asked'] == 0)
        t = self.table('tags', get_tag_scope(c[0]['id']))
        pupularity1 = [1, 1, 1, 0, 0, 0]
        for i in range(6):
            self.assertTrue(t[i]['questions_asked'] == pupularity1[i])
        self.action('reportforum', {
                    'user': carol, 'question_id': var['bq'], 'answer_id': 0, 'comment_id': 0}, carol, 'Carol delete Bob question')
        self.action('reportforum', {
                    'user': dan, 'question_id': var['bq'], 'answer_id': 0, 'comment_id': 0}, dan, 'Dan delete Bob question')
        c = self.table('communities', 'allcomm')
        self.assertTrue(c[0]['questions_asked'] ==
                        0 and c[1]['questions_asked'] == 0)
        t = self.table('tags', get_tag_scope(c[0]['id']))
        for i in range(6):
            self.assertTrue(t[i]['questions_asked'] == 0)
        end()

    def test_unique_tag_assert_failed(self):
        begin('Test tag unique constraint', True)
        alice = self.register_alice_account()
        self.failed_action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [1, 2, 1, 4], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                           'Alice attempt ask question with tags [1, 2, 1, 4] - 1 is duplicate', 'assert')
        # self.failed_action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
        #                   'Alice attempt to ask question with no tags', 'assert')
        self.action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                    'Alice ask question')
        var = {}
        self.assertTrue(compare([{'id': '#var aq',
                                  'user': 'alice'}], self.table('question', 'allquestions'), var, True))
        self.failed_action('modquestion', {'user': 'alice', 'question_id': var['aq'], 'community_id': 1, 'tags': [1, 3, 2, 1], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
                           'Alice attempt to modify own question - set duplicate tag [1, 3, 2, 1]', 'assert')
        # self.failed_action('postquestion', {'user': 'alice', 'question_id': var['aq'],  'community_id': 1, 'tags': [], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
        #                   'Alice attempt to modify own question - set no tags', 'assert')
        end()

    def test_non_existing_tag_community_failed(self):
        begin('Test register question with not existing tag or community', True)
        alice = self.register_alice_account()
        self.failed_action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [1, 9], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                           'Alice attempt ask question with non-existing tag [1, 9] - 9 non-exist', 'assert')
        self.failed_action('postquestion', {'user': 'alice', 'community_id': 5, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                           'Alice attempt to ask question with non-existing community - 5', 'assert')
        self.table('question', 'allquestions')
        self.action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                    'Alice ask question')
        var = {}
        self.assertTrue(compare([{'id': '#var aq',
                                  'user': 'alice'}], self.table('question', 'allquestions'), var, True))
        self.failed_action('modquestion', {'user': 'alice', 'question_id': var['aq'], 'community_id': 1, 'tags': [1, 9], 'title': 'Title alice question', 'ipfs_link': 'AQ'}, alice,
                           'Alice attempt to modify own question - set non-existing tag [1, 9] - 9 non-exist', 'assert')
        self.failed_action('postquestion', {'user': 'alice', 'question_id': var['aq'],  'community_id': 5, 'tags': [1], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                           'Alice attempt to modify own question - set non-existing community - 5', 'assert')
        end()

    def test_create_tag_or_community_str_assert(self):
        begin('Test input string parameters limits')
        alice = self.register_alice_account(10000, 200)
        self.failed_action('crcommunity', {'user': 'alice', 'name': ''.join(['a' for i in range(51)]), 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                           'Alice attempt to create community winth name length > 25', 'assert')
        self.failed_action('crtag', {'user': 'alice', 'community_id': 1, 'name': ''.join(['a' for i in range(31)]), 'ipfs_description': 'Alice tag description'}, alice,
                           'Alice attempt to create tag winth name length > 30', 'assert')
        self.failed_action('crcommunity', {'user': 'alice', 'name': 'Hi? mark', 'type': 2, 'ipfs_description': ''.join(['a' for i in range(65)]), 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                           'Alice attempt to create community with invalid IPFS', 'assert')
        self.failed_action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'Hi? mark', 'ipfs_description': ''.join(['a' for i in range(65)])}, alice,
                           'Alice attempt to create tag with invalid IPFS', 'assert')
        self.action('crcommunity', {'user': 'alice', 'name': ''.join(['a' for i in range(50)]), 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                    'Alice create community winth name length 50')
        self.action('crtag', {'user': 'alice', 'community_id': 1, 'name': ''.join(['a' for i in range(30)]), 'ipfs_description': 'Alice tag description'}, alice,
                    'Alice create tag winth name length 30')
        end()

    def test_create_community_and_tag(self):
        begin('Test create community and tag')
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000, 200)
        self.action('crcommunity', {'user': alice, 'name': 'alice community', 'type': 2,
                                    'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags() }, alice, 'Alice create community')

        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                              'ipfs_description': 'BCM'}, bob, 'Bob create ')
        voters = [self.register_carol_account(), self.register_dan_account(),
                  self.register_frank_account(), self.register_ted_account()]
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))

        self.action('vtdeltag', {'user': voters[3], 'community_id': 1,
                                 'tag_id': t[0]['id']}, voters[3], f'Ted won\' bob tag to be created')

        for i in range(4):
            if i < 3:
                self.action('vtcrtag', {
                            'user': voters[i], 'community_id': 1, 'tag_id': t[0]['id']}, voters[i], f'{voters[i]} vote create tag')
            else:
                self.assertTrue(self.table(
                    'crtagtb', get_tag_scope(1)) == [])
                self.assertTrue({'id': 7, 'name': 'bob tag', 'ipfs_description': 'BCM',
                                 'questions_asked': 0} in self.table('tags', get_tag_scope(1)))
            self.action('vtcrcomm', {
                        'user': voters[i], 'community_id': c[0]['id']}, voters[i], f'{voters[i]} vote create community')
        self.assertTrue(self.table('crcommtb', 'allcomm') == [])
        c = self.table('communities', 'allcomm')
        for comm in c:
            if comm['id'] == 4:
                self.assertTrue(comm['name'] == 'alice community' and comm['ipfs_description'] == 'AC')

    def test_community_and_tag_vote_non_existent(self):
        begin('Test vote non exisent item, create tag with non-existen community', True)
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(1000, 100)
        carol = self.register_carol_account(10000)
        self.action('crcommunity', {'user': alice, 'name': 'alice community', 'type': 2,
                                    'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                              'ipfs_description': 'BCM'}, bob, 'Bob create ')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.failed_action('crtag', {'user': carol, 'name': 'carol tag',  'community_id': c[0]['id'],
                                     'ipfs_description': 'CCM'}, carol, 'Carol attempt to create tag with invaid community', 'assert')

        self.failed_action('vtcrcomm', {
                           'user': carol, 'community_id': c[0]['id'] - 1}, carol, 'Carol vote create non-existent community', 'assert')
        self.failed_action('vtdelcomm', {
                           'user': carol, 'community_id': c[0]['id'] - 1}, carol, 'Carol vote delete non-existent community', 'assert')
        self.failed_action('vtcrtag', {'user': carol, 'community_id': 1,
                                       'tag_id': t[0]['id'] - 1}, carol, 'Carol vote create non-existent tag', 'assert')
        self.failed_action('vtdeltag', {'user': carol, 'community_id': 3,
                                        'tag_id': t[0]['id']}, carol, 'Carol vote create non-existent tag', 'assert')
        self.failed_action('vtcrtag', {'user': carol, 'community_id': 1,
                                       'tag_id': t[0]['id'] - 1}, carol, 'Carol vote delete non-existent tag', 'assert')
        self.failed_action('vtdeltag', {'user': carol, 'community_id': 3,
                                        'tag_id': t[0]['id']}, carol, 'Carol vote delete non-existent tag', 'assert')
        end()

    def test_energy_point_limit(self):
        begin('Test energy points assert', True)
        defs = load_defines(
            './src/contracts/peeranha.main/economy.h')
        alice = self.register_alice_account(
            10000, defs['ENERGY_CREATE_COMMUNITY'])
        bob = self.register_bob_account(
            10000, defs['ENERGY_CREATE_TAG'])
        carol = self.register_carol_account(
            10000, defs['ENERGY_CREATE_COMMUNITY'] - 1)
        dan = self.register_dan_account(
            10000, defs['ENERGY_CREATE_TAG'] - 1)
        self.action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                    'Alice create community')
        self.action('crtag', {'user': 'bob', 'community_id': 1, 'name': 'BT', 'ipfs_description': 'Bob tag description'}, bob,
                    'Bob create tag')
        accounts_e = [
            {'user': 'alice', 'rating': '#var alice_rt',
                'energy': '#var alice_energy'},
            {'user': 'bob', 'rating': '#var bob_rt',
                'energy': '#var bob_energy'},
            {}, {}
        ]
        var = {}
        self.assertTrue(compare(accounts_e, self.table(
            'account', 'allaccounts'), var, True))
        self.assertTrue(var['alice_energy'] == 0)
        self.assertTrue(var['bob_energy'] == 0)
        self.failed_action('crcommunity', {'user': 'carol', 'name': 'CCM', 'type': 2, 'ipfs_description': 'Carol community description', 'suggested_tags': self.get_stub_suggested_tags()}, carol,
                           'Carol attempt to create community', 'assert')
        self.failed_action('crtag', {'user': 'dan', 'community_id': 1, 'name': 'DT', 'ipfs_description': 'Dan tag description'}, dan,
                           'Dan attempt to create tag', 'assert')
        end()

    def test_delete_own_vote(self):
        begin('Test delete own upvote or downvote')
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000, 200)
        self.action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                    'Alice create community')
        self.action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'AT', 'ipfs_description': 'Alice tag description'}, alice,
                    'Alice create tag')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.action('vtcrtag', {'user': bob, 'community_id': 1,
                                'tag_id': t[0]['id']}, bob, 'Bob vote create tag')
        self.action('vtcrcomm', {
            'user': bob, 'community_id': c[0]['id']}, bob, 'Bob vote create community')

        self.assertTrue(compare([{'upvotes': ['bob'], 'downvotes': []}], self.table(
            'crcommtb', 'allcomm'), ignore_excess=True))
        self.assertTrue(compare([{'upvotes': ['bob'], 'downvotes': []}], self.table(
            'crtagtb', get_tag_scope(1)), ignore_excess=True))

        self.wait()
        self.action('vtcrtag', {'user': bob, 'community_id': 1,
                                'tag_id': t[0]['id']}, bob, 'Bob remove vote create tag')
        self.action('vtcrcomm', {
            'user': bob, 'community_id': c[0]['id']}, bob, 'Bob remove vote create community')

        self.assertTrue(compare(c, self.table('crcommtb', 'allcomm')))
        self.assertTrue(compare(t, self.table('crtagtb', get_tag_scope(1))))

        self.wait()
        self.action('vtdeltag', {'user': bob, 'community_id': 1,
                                 'tag_id': t[0]['id']}, bob, 'Bob vote delete tag')
        self.action('vtdelcomm', {'user': bob, 'community_id': c[0]['id']},
                    bob, 'Bob vote delete community')
        self.assertTrue(compare([{'downvotes': ['bob'], 'upvotes': []}], self.table(
            'crcommtb', 'allcomm'), ignore_excess=True))
        self.assertTrue(compare([{'downvotes': ['bob'], 'upvotes': []}], self.table(
            'crtagtb', get_tag_scope(1)), ignore_excess=True))
        self.wait()
        self.action('vtdeltag', {'user': bob, 'community_id': 1,
                                 'tag_id': t[0]['id']}, bob, 'Bob vote delete tag')
        self.action('vtdelcomm', {'user': bob, 'community_id': c[0]['id']},
                    bob, 'Bob vote delete community')
        self.assertTrue(compare(c, self.table('crcommtb', 'allcomm')))
        self.assertTrue(compare(t, self.table('crtagtb', get_tag_scope(1))))
        end()

    def test_upvote_own_community_or_tag(self):
        begin('Upvote own community or tag', True)
        alice = self.register_alice_account(10000, 200)
        self.action('crcommunity', {'user': alice, 'name': 'alice community', 'type': 2,
                              'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': alice, 'name': 'alice tag',  'community_id': 1,
                                    'ipfs_description': 'ACM'}, alice, 'Alice create tag')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.failed_action('vtcrtag', {'user': alice, 'community_id': 1,
                                       'tag_id': t[0]['id']}, alice, 'Allice attempt to upvote own tag', 'assert')
        self.failed_action('vtcrcomm', {
                           'user': alice, 'community_id': c[0]['id']}, alice, 'Allice attempt to upvote own community', 'assert')
        end()

    def test_delete_with_downvotes_own(self):
        begin('Test delete own tag and community with downvote')
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000, 200)
        carol =  self.register_carol_account()
        self.action('crcommunity', {'user': alice, 'name': 'alice community', 'type': 2,
                              'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                                    'ipfs_description': 'BCM'}, bob, 'Bob create ')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        
        self.action('vtdeltag', {'user': carol, 'community_id': 1, 'tag_id': t[0]['id']}, carol, 'carol upvote alice tag')
        self.action('vtdelcomm', {'user': carol, 'community_id': c[0]['id']}, carol, 'carol downvote alice community')

        self.action('vtdelcomm', {'user': alice, 'community_id': c[0]['id']}, alice, 'Alice vote delete own community')
        self.action('vtdeltag', {'user': bob, 'community_id': 1, 'tag_id': t[0]['id']}, bob, 'Bob vote delete own tag')
        self.assertTrue(self.table('crcommtb', 'allcomm') == [])
        self.assertTrue(self.table('crtagtb', get_tag_scope(1)) == [])
        #Couldn't load int values, loaddefines method
        account_e = ["#ignoreorder", {'user': 'alice', 'rating' : 10000 - (150//3)}, {'user': 'bob', 'rating' : 10000- (50//2)}, {'user': 'carol', 'rating' : 200}]
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), ignore_excess=True))
        end() 

    def test_delete_with_downvotes_own_with_upvotes(self):
        begin('Test delete own tag and community with downvote')
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000, 200)
        carol =  self.register_carol_account()
        dan = self.register_dan_account()
        
        self.action('crcommunity', {'user': alice, 'name': 'alice community', 'type': 2,
                              'ipfs_description': 'AC', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community')
        self.action('crtag', {'user': bob, 'name': 'bob tag',  'community_id': 1,
                                    'ipfs_description': 'BCM'}, bob, 'Bob create ')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        
        self.action('vtdeltag', {'user': carol, 'community_id': 1, 'tag_id': t[0]['id']}, carol, 'carol downvote alice tag')
        self.action('vtdelcomm', {'user': carol, 'community_id': c[0]['id']}, carol, 'carol downvote alice community')

        self.action('vtcrtag', {'user': dan, 'community_id': 1, 'tag_id': t[0]['id']}, dan, 'carol upvote alice tag')
        self.action('vtcrcomm', {'user': dan, 'community_id': c[0]['id']}, dan, 'carol upvote alice community')

        self.action('vtdelcomm', {'user': alice, 'community_id': c[0]['id']}, alice, 'Alice vote delete own community')
        self.action('vtdeltag', {'user': bob, 'community_id': 1, 'tag_id': t[0]['id']}, bob, 'Bob vote delete own tag')
        self.assertTrue(self.table('crcommtb', 'allcomm') == [])
        self.assertTrue(self.table('crtagtb', get_tag_scope(1)) == [])
        #Couldn't load int values, loaddefines method
        account_e = ["#ignoreorder", {'user': 'alice', 'rating' : 10000}, {'user': 'bob', 'rating' : 10000}, {'user': 'carol', 'rating' : 200}, {'user': 'dan', 'rating': 200}]
        self.assertTrue(compare(account_e, self.table('account', 'allaccounts'), account_e, ignore_excess=True))
        end() 


    def test_change_own_vote(self):
        begin('Test upvote after downvote and downvote after upvote - change vote')
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000)
        carol = self.register_carol_account(10000)
        self.action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                    'Alice create community')
        self.action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'AT', 'ipfs_description': 'Alice tag description'}, alice,
                    'Alice create tag')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.action('vtcrtag', {'user': bob, 'community_id': 1,
                                'tag_id': t[0]['id']}, bob, 'Bob vote create tag')
        self.action('vtcrcomm', {
            'user': bob, 'community_id': c[0]['id']}, bob, 'Bob vote create community')

        self.action('vtdeltag', {'user': carol, 'community_id': 1,
                                 'tag_id': t[0]['id']}, carol, 'Carol vote delete tag')
        self.action('vtdelcomm', {'user': carol, 'community_id': c[0]['id']},
                    carol, 'Carol vote delete community')

        c[0]['upvotes'] = ['bob']
        c[0]['downvotes'] = ['carol']
        t[0]['upvotes'] = ['bob']
        t[0]['downvotes'] = ['carol']
        self.assertTrue(compare(c, self.table(
            'crcommtb', 'allcomm')))
        self.assertTrue(compare(t, self.table(
            'crtagtb', get_tag_scope(1))))

        self.wait()

        self.action('vtcrtag', {'user': carol, 'community_id': 1,
                                'tag_id': t[0]['id']}, carol, 'Carol change downvote to upvote tag')
        self.action('vtcrcomm', {'user': carol, 'community_id': c[0]['id']},
                    carol, 'Carol change downvote to upvote community')
        
        self.action('vtdeltag', {'user': bob, 'community_id': 1,
                                 'tag_id': t[0]['id']}, bob, 'Bob change upvote to downvote tag')
        self.action('vtdelcomm', {'user': bob, 'community_id': c[0]['id']},
                    bob, 'Bob change upvote to downvote community')

        c[0]['upvotes'] = ['carol']
        c[0]['downvotes'] = ['bob']
        t[0]['upvotes'] = ['carol']
        t[0]['downvotes'] = ['bob']
        self.assertTrue(compare(c, self.table(
            'crcommtb', 'allcomm'), ignore_excess=True))
        self.assertTrue(compare(t, self.table(
            'crtagtb', get_tag_scope(1)), ignore_excess=True))
        end()

    def test_another_user(self):
        begin('Test vote assert another user', True)
        alice = self.register_alice_account(10000, 200)
        bob = self.register_bob_account(10000, 200)
        carol = self.register_carol_account(10000, 200)
        self.failed_action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, bob,
                           'Alice attempt to create community with bob auth', 'auth')
        self.failed_action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'AT', 'ipfs_description': 'Alice tag description'}, bob,
                           'Alice attempt to create tag with bob auth', 'auth')
        self.action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags()}, alice,
                    'Alice create community')
        self.action('crtag', {'user': 'alice', 'community_id': 1, 'name': 'AT', 'ipfs_description': 'Alice tag description'}, alice,
                    'Alice create tag')
        c = self.table('crcommtb', 'allcomm')
        t = self.table('crtagtb', get_tag_scope(1))
        self.failed_action('vtcrtag', {'user': bob, 'community_id': 1,
                                       'tag_id': t[0]['id']}, carol, f'Bob vote create tag with carol auth', 'auth')
        self.failed_action('vtcrcomm', {
                           'user': bob, 'community_id': c[0]['id']}, carol, 'Bob vote create community with carol auth', 'auth')
        self.failed_action('vtdeltag', {'user': bob, 'community_id': 1,
                                        'tag_id': t[0]['id']}, carol, f'Bob vote delete tag with carol auth', 'auth')
        self.failed_action('vtdelcomm', {
                           'user': bob, 'community_id': c[0]['id']}, carol, 'Bob vote delete community with carol auth', 'auth')
        end()

    def test_create_community_with_invalid_tag_count(self):
        begin('Attempt to create community with invalid tag count', True)
        alice = self.register_alice_account(10000, 10)
        self.failed_action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags(4)}, alice,
                           'Alice attempt to create community with bob auth', 'assert')
        self.failed_action('crcommunity', {'user': 'alice', 'name': 'ACM', 'type': 2, 'ipfs_description': 'Alice community description', 'suggested_tags': self.get_stub_suggested_tags(26)}, alice,
                           'Alice attempt to create community with bob auth', 'assert')
        end()

    def test_edit_tag_without_rights(self):
        begin('edit tag without rights', True)
        alice = self.register_alice_account(10000, 10)
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag without rights')
        end()
    
    def test_edit_tag_global_mod(self):
        begin('edit tag global moderator', True)
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account(20, 10)
        self.action('givemoderflg', {
                    'user': 'alice', 'flags': 16}, admin, 'Give moderator flags to alice (create tag)')
        
        self.action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag with global moderator rights')
        example_tag = {'id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs', 'questions_asked': 0}
        self.assertTrue(compare(example_tag, self.table('tags', get_tag_scope(1))[0], ignore_excess=True))
        
        self.failed_action('edittag', {'user': 'alice', 'community_id': 5, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong community id')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 10, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong tag id')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'e', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong name tag')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'n'}, alice,
                           'Alice edit tag, wrong name ipfs')
        end()
    
    def test_edit_tag_community_mod(self):
        begin('edit tag community moderator', True)
        admin = self.get_contract_deployer(self.get_default_contract())
        alice = self.register_alice_account(20, 10)
        self.action('givecommuflg', {
            'user': alice, 'flags': 16, 'community_id': 1}, admin, 'Give community moderator flags to alice (create tag)')
        
        self.action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag with global moderator rights')
        example_tag = {'id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs', 'questions_asked': 0};
        self.assertTrue(compare(example_tag, self.table('tags', get_tag_scope(1))[0], ignore_excess=True))
        
        self.failed_action('edittag', {'user': 'alice', 'community_id': 5, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong community id')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 10, 'name': 'new name', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong tag id')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'e', 'ipfs_description': 'new ipfs'}, alice,
                           'Alice edit tag, wrong name tag')
        self.failed_action('edittag', {'user': 'alice', 'community_id': 1, 'tag_id': 1, 'name': 'new name', 'ipfs_description': 'n'}, alice,
                           'Alice edit tag, wrong name ipfs')
        end()

    def _create_basic_hierarchy(self):
        alice = self.register_alice_account()
        bob = self.register_bob_account()
        self.action('postquestion', {'user': 'alice', 'community_id': 1, 'tags': [2, 3, 4, 5], 'title': 'Title alice question', 'ipfs_link': 'AQ', 'type': 0}, alice,
                    'Alice asking question')
        self.action('postquestion', {'user': 'bob', 'community_id': 1, 'tags': [1, 2, 3], 'title': 'Title bob question', 'ipfs_link': 'BQ', 'type': 0}, bob,
                    'Bob asking question')
        e = ['#ignoreorder', {
            'id': '#var aq',
            'community_id': 1,
            'tags': [2, 3, 4, 5],
            'user': 'alice',
            'title': 'Title alice question',
            'ipfs_link': 'AQ'
        }, {
            'id': '#var bq',
            'community_id': 1,
            'tags': [1, 2, 3],
            'user': 'bob',
            'title': 'Title bob question',
            'ipfs_link': 'BQ'
        }]
        t = self.table('question', 'allquestions')
        var = {}
        self.assertTrue(compare(e, t, var, True))
        return (alice, bob, e, var)

    def get_stub_suggested_tags(self, count=10):
        tags = []
        for i in range(0, count):
            tags.append({
                'name': f'Tag {i}',
                'ipfs_description': f'IPFS of tag {i}'
            })
        return tags

if __name__ == '__main__':
    main()
