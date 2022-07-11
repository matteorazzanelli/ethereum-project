from web3 import Web3
from .models import Event
import json
import time

# connect to a node
blockchain_address = 'http://127.0.0.1:7545'
chain_id = 1337 # ganache
# blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
# chain_id = 3
w3 = Web3(Web3.HTTPProvider(blockchain_address))


# retrieve contract
contractAddress = '0x86D219D65452b013912B2af7b2E65E903fa3777d'
contractAbi = json.loads('');
contract = web3.eth.contract(address=contractAddress, abi=contractAbi)

# connect to redis server
client = redis.StrictRedis(host='localhost', port=6379, db=0)

