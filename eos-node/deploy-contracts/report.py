import json
import requests
import subprocess
import math
from random import randrange
from time import sleep

verbose = True

peeranamain = {
    "name": "main",
    "deployer": "peeranhamain",
    "private-key": "5JUnu1jgVifdznEHpc9eVedpLXsyDPwu69xziMm9ZvbRSkVKEda",
    "public-key": "EOS5hhovSUZFZQPdvVvtCU9JjjZuuoyyQLG8EoY83UTELZtNMRz1b",
    "contract": "../../src/contracts/peeranha.main"
}

eosNameAlphabet = "abcdefghijklmnopqrstuvwxyz12345."

def finish(msg):
    subprocess.call(['pkill', 'nodeos'])
    print('Info: program exit with msg={}'.format(msg))
    exit()


def execute(command): 
    with subprocess.Popen(command, shell=True, stdout=-1, stderr=-1) as process:
        process.wait()
        if process.returncode != 0:
            finish('Error: unable to execute {}'.format(command))

def action(action_name, body, auth):
    cmd = "cleos push action {} {} '{}' -p {}".format(peeranamain['deployer'], action_name, json.dumps(body), auth)
    execute(cmd)


def generateRandomEosName():
    eosName = ""
    firstSymbol = randrange(0, 26)
    eosName += eosNameAlphabet[firstSymbol]
    for _ in range(10):
        middleSymbol = randrange(0, len(eosNameAlphabet))
        eosName += eosNameAlphabet[middleSymbol]
    lastSymbol = randrange(0, 31)
    eosName += eosNameAlphabet[lastSymbol]
    return eosName

def get_ram(account = peeranamain['deployer']): 
    data = {'account_name': account}
    with requests.post('http://127.0.0.1:8888/v1/chain/get_account', json.dumps(data)) as t:
        if t.status_code == 200:
            tb = t.json()
            return tb['ram_usage']
        else:
            print(t.text)
            print('Info: Failed to get RAM\n' + str(t))
    return None

def table(table, scope):
    data = {'table': table,
            'scope': scope,
            'code': peeranamain['deployer'],
            'limit': 30000,
            'json': True}
    with requests.post('http://127.0.0.1:8888/v1/chain/get_table_rows', json.dumps(data)) as t:
        if t.status_code == 200:
            tb = t.json()
            return tb['rows']
        else:
            print('Error fetching table data:\n' + str(t))
    return None
            
print('Info: Start EOS node')
eosnode = subprocess.Popen('./run', cwd='./..', stdout=-1, stderr=-1, shell=True)
count = 7
while count != 0:
    try:
        count -= 1
        sleep(1)
        req = requests.get('http://127.0.0.1:8888/v1/chain/get_info')
        if req.status_code == 200:
            print('Info: Node succesfully started!')
            break
    except:
        pass
if count == 0: 
    finish("Error: unable to start EOS")

accounts = [generateRandomEosName() for _ in range(100)]

to_execute = [
    'cleos wallet create --name default --to-console',
    'cleos wallet import --private-key 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3',
    'cleos set contract eosio $EOSIO_BUILD_DIR/contracts/eosio.bios -p eosio',
    'cleos wallet import --private-key {}'.format(peeranamain['private-key']),
    'cleos create account eosio {0} {1} {1}'.format(peeranamain['deployer'], peeranamain['public-key'])
]

for account in accounts:
    to_execute.append('cleos create account eosio {0} {1} {1}'.format(account, peeranamain['public-key']))

for command in to_execute:
    execute(command)

testIpfsLink = 'QmarHSr9aSNaPSR6G9KFPbuLV9aEqJfTk1y9B8pdwqK4Rq'
testArrayIpfsLink = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
currentRam = get_ram(peeranamain['deployer'])
print('Report: Ram before deployment {}'.format(currentRam))
execute('cleos set contract {0} {1} -p {0}'.format(peeranamain['deployer'], peeranamain['contract']))
action('init', {}, peeranamain['deployer'])
deploymentRam = get_ram(peeranamain['deployer'])
print('Report: Deployment {}'.format(deploymentRam - currentRam))
for account in accounts:
    action('registeracc', {'user': account, 'display_name': account + 'DispName', 'ipfs_profile': testIpfsLink, 'ipfs_avatar': testIpfsLink}, account)
accountRam = get_ram(peeranamain['deployer'])
print('Report: 100 Account {}'.format(accountRam - deploymentRam))
action('givemoderflg', {'user': accounts[0], 'flags': 31}, peeranamain['deployer'])
giveModerFlgRam = get_ram(peeranamain['deployer'])
print('Report: Give moderator flg for one {}'.format(giveModerFlgRam - accountRam))
for i in range(100):
    action('crcommunity', {
        'user': accounts[0], 
        'name': f'Long name {i+1}', 
        'ipfs_description': testIpfsLink, 
        'suggested_tags': [{
             'name': f'Community {i+1} tag {j+1}', 
             'ipfs_description': testIpfsLink
            } for j in range(6)]
        }, accounts[0])
communityAndTagRam = get_ram(peeranamain['deployer'])
print('Report: 100 Community and 600 Tags {}'.format(communityAndTagRam - giveModerFlgRam))

for i in range(100):
    action('postquestion', {'user': accounts[i], 'title': 'Title of question', 'ipfs_link': testIpfsLink, 'community_id': i + 1, 'tags': [2, 3, 4, 5]}, accounts[i])
postQuestionRam = get_ram(peeranamain['deployer'])
print('Report: 100 questions {}'.format(postQuestionRam - communityAndTagRam))

for i in range(100):
    action('setaccrten', {'user': accounts[i], 'rating': 100 + i, 'energy': 200}, accounts[i])

increaseRatingRam = get_ram(peeranamain['deployer'])
print('Report: Increase reating for all users {}'.format(increaseRatingRam - postQuestionRam))

map_account_to_question = {}
all_questions = table('question', 'allquestions')
for question in all_questions:
    map_account_to_question[question['user']] = question['id'] 
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 1) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 2) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 3) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 4) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 5) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 6) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 7) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 8) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 9) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 10) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])
for i in range(100):
    action('postanswer', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 11) % 100]]), 'ipfs_link': testArrayIpfsLink}, accounts[i])



postAnsewrRam = get_ram(peeranamain['deployer'])
print('Report: Post 200 answers {}'.format(postAnsewrRam - increaseRatingRam))

for i in range(100):
    action('postcomment', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 7) % 100]]), 'answer_id':0, 'ipfs_link': testArrayIpfsLink}, accounts[i])

for i in range(100):
    action('postcomment', {'user': accounts[i], 'question_id': str(map_account_to_question[accounts[(i + 3) % 100]]), 'answer_id':1, 'ipfs_link': testArrayIpfsLink}, accounts[i])

postCommentsRam = get_ram(peeranamain['deployer'])
print('Report: Post 200 comments {}'.format(postCommentsRam - postAnsewrRam))

print('Total: ', get_ram(peeranamain['deployer']))

action('resettables', {}, peeranamain['deployer'])
print('Total: ', get_ram(peeranamain['deployer']))
input()