
import sys
import os
from dotenv import load_dotenv
load_dotenv()
BLOCKCHAIN = sys.argv[1]
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
  
# Compile the contract
import solcx
# If you haven't already installed the Solidity compiler
# solcx.install_solc("0.8.0")
# Compile
temp_file  = solcx.compile_files('../startup_token/contracts/NotaryAct.sol', solc_version='0.8.0')
# Export contract data
abi = temp_file['../startup_token/contracts/NotaryAct.sol:NotaryContract']['abi']
bytecode = temp_file['../startup_token/contracts/NotaryAct.sol:NotaryContract']['bin']

from web3 import Web3
# connect to a node: ganache or ropsten
w3 = Web3(Web3.HTTPProvider(blockchain_address))
# create contract in python
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# retrieve private key

acct = w3.eth.account.privateKeyToAccount(private_key)

# deploy
print(f'Attempting to deploy from account: { acct.address }')
# deploy contract
construct_txn = contract.constructor().buildTransaction({
  'from': acct.address,
  'nonce': w3.eth.getTransactionCount(acct.address),
  'gasPrice': w3.eth.gas_price,
  'chainId': chain_id
})
signed = w3.eth.account.sign_transaction(construct_txn,private_key)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt['contractAddress'])
# 0xDaa0db926b98FBB1De4752dA73cc8b6FAEDeBc5D