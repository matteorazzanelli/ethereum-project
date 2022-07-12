
# Compile the contract
# import solcx
from solcx import compile_standard, install_solc

# Compile our Solidity

install_solc("0.6.0")

print(compile_sol)
# If you haven't already installed the Solidity compiler
solcx.install_solc()
# Compile
temp_file = solcx.compile_files('../startup_token/contracts/NotaryAct.sol')
# Export contract data
abi = temp_file['NotaryAct.sol:NotaryContract']['abi']
bytecode = temp_file['NotaryAct.sol:NotaryContract']['bin']

from web3 import Web3
# connect to a node: ganache or ropsten
blockchain_address = 'http://127.0.0.1:7545'
chain_id = 1337 # ganache
# blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
# chain_id = 3
w3 = Web3(Web3.HTTPProvider(blockchain_address))
# create contract in python
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# retrieve private key
import os
from dotenv import load_dotenv
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
acct = w3.eth.account.privateKeyToAccount(private_key)

# deploy contract
construct_txn = contract.constructor().build_transaction({
  'from': acct.address,
  'nonce': w3.eth.getTransactionCount(acct.address),
  'gasPrice': w3.eth.gas_price,
  'chainId': chain_id
})
signed = w3.eth.account.sign_transaction(construct_txn,private_key)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['contractAddress'])