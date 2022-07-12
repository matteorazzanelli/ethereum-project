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

# set the deafult account
w3.eth.defaultAccount = w3.eth.accounts[0]

# retrieve contract vars and create contract instance
deployed_contract_address = '0xb7afC8dB8EEf302cd30553B39cEa0599093FDE3C'
compiled_contract_path = '../startup_token/build/contracts/NotaryCOntract.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
message = contract.functions.sayHello().call()

print(message)
