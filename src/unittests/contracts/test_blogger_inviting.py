import peeranhatest
from peeranhatest import *
from jsonutils import *
from unittest import main

MODERATOR_FLG_ALL = 31

defs = load_defines('./src/contracts/peeranha.main/economy.h')


class CommunityQuestionsTypeTest(peeranhatest.peeranhaTest):

    def test_ask_and_modify_questions(self):
        begin("Testing work of asking and modifying questionst in community with general/expert/any type")
        alice = self.register_alice_account(100000, 400)
        self._give_invited_blogger_flag(alice)
        self.action('crcommunity', {'user': alice, 'name': 'alice bloger community1', 'type': 1,
                                    'ipfs_description': 'ACM1', 'suggested_tags': self.get_stub_suggested_tags()}, alice, 'Alice create community with EXPERT type')
       
        # communities = self.table('communities', 'allcomm')
        # for com in communities:
        #     print(com)
        #     print("\n")
        end()

    def get_stub_suggested_tags(self):
        tags = []
        for i in range(0, 10):
            tags.append({
                'name': f'Tag {i}',
                'ipfs_description': f'IPFS of tag {i}'
            })
        return tags

    def _give_invited_blogger_flag(self, acc):
        print(acc)
        admin = self.get_contract_deployer(self.get_default_contract())
        print(admin)
        self.action('invtblogger', {
                    'user': acc}, admin, f'Give invited blogger flags to {acc}')

    def _give_moderator_flag(self, acc, flg):
        admin = self.get_contract_deployer(self.get_default_contract())
        self.action('givemoderflg', {
                    'user': acc, 'flags': flg}, admin, f'Give moderator flags to {acc}')

if __name__ == '__main__':
    main()