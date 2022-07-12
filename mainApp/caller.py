# from models import Event

import sys, os
from dotenv import load_dotenv
load_dotenv()
# from mainApp.deploy import BLOCKCHAIN
from django.conf import settings
BLOCKCHAIN = sys.argv[1] #settings.BLOCKCHAIN
if BLOCKCHAIN == 'ganache':
  blockchain_address = 'http://127.0.0.1:7545'
  chain_id = 1337 # ganache
  private_key = os.getenv("PRIVATE_KEY_GANACHE")
elif BLOCKCHAIN == 'ropsten':
  blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
  chain_id = 3
  private_key = os.getenv("PRIVATE_KEY_ROPSTEN")
else:
  sys.exit('No valid blockchain provided: exiting...')

from web3 import Web3

# connect
w3 = Web3(Web3.HTTPProvider(blockchain_address))

# set the deafult account
# w3.eth.defaultAccount = w3.eth.accounts[0]
# print(f'Attempting to interact with contract from account: { w3.eth.defaultAccount }')
acct = w3.eth.account.privateKeyToAccount(private_key)

# retrieve contract vars and create contract instance
import json
deployed_contract_address = '0xDaa0db926b98FBB1De4752dA73cc8b6FAEDeBc5D'
compiled_contract_path = '../startup_token/build/contracts/NotaryCOntract.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
message = contract.functions.numContract_().call()
print(f'Total number of created contracts : {message}')

# Calling function: store(string memory,string memory) and making state change
import time
now = int(time.time()) # unix epoch
deadline = now + 14*24*3600 # 2 weeks
new_contract_txn = contract.functions.newContract(
  "0xc85e78A5CBdE92ae1B9848AB1B3D6C0EBbb88187",
  "0x2a61c6f70c84eAd46b054746C1B7C7aAA12269cd",
  "The first contract",
  100,
  deadline
  ).buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gasPrice': w3.eth.gas_price,
    'chainId': chain_id
  })
signed = w3.eth.account.sign_transaction(new_contract_txn, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


message = contract.functions.numContract_().call()
print(f'Total number of created contracts : {message}')