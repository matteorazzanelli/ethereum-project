# 1. Import solcx
import solcx
import os
# 2. If you haven't already installed the Solidity compiler, uncomment the following line
# solcx.install_solc()

# 3. Compile contract
temp_file = solcx.compile_files('Incrementer.sol')

# 4. Export contract data
abi = temp_file['Incrementer.sol:Incrementer']['abi']
bytecode = temp_file['Incrementer.sol:Incrementer']['bin']

##############################################################################################

import json
from web3 import Web3, HTTPProvider

# EXECUTE IN AN OTHER TERMINAL WRT TRUFFLE CONSOLE

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'

# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))

# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0] # 0x92D7A711F97027702fCdc11c8B470e03ABef7c0F

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/Adoption.json'

# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x29bE94C6f67e3E8D0b7773E14C676B4922958eaA'

with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
  contract_bytecode = contract_json['bytecode']

# Fetch deployed contract reference (create an instance that refers to, links, and allows you to interact with the contract itself on the blockchain)
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# if you want to deploy it directly
construct_txn = contract.constructor(1000, 3600*24).buildTransaction({
    'from': acct.address,
    'nonce': web3.eth.getTransactionCount(acct.address),
    'gas': 4679352,
    'gasPrice': web3.toWei('50', 'gwei')})

signed = acct.signTransaction(construct_txn)

tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)

# Call contract function (this is not persisted to the blockchain)
message = contract.functions.sayHello().call()

print(message)

# executes setPayload function
tx_hash = contract.functions.setPayload('abc').transact()
# waits for the specified transaction (tx_hash) to be confirmed
# (included in a mined block)
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print('tx_hash: {}'.format(tx_hash.hex()))


################################
# from metamask
public_key = '0xB73844B5a1D1539a5185FD92A2Ac8EEDEc7c5Dde'
# private_key = 'df2710d474fc23f0a8cd92686ecea12245e3827f6427324ee022124addf66048'
from dotenv import load_dotenv
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")

# create an account from an external private key
acct = web3.eth.account.privateKeyToAccount(private_key)


####################################
# from hosted node
w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'))
account = w3.eth.account.create()
private_key = account.privateKey.hex()
address = account.address

