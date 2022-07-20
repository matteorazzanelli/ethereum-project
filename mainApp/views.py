#######################################################################################################################
################################# Fetch deployed conract
import sys, os
from dotenv import load_dotenv
load_dotenv()
from django.conf import settings
BLOCKCHAIN = settings.BLOCKCHAIN
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
w3 = Web3(Web3.HTTPProvider(blockchain_address))
acct = w3.eth.account.privateKeyToAccount(private_key)

# retrieve contract vars and create contract instance
import json
deployed_contract_address = '0x4E04C5726059B0DB3A9Be3619E4BC1524D63215a'
compiled_contract_path = 'startup_token/build/NotaryContract.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

#######################################################################################################################
################################# Create MongoDB initial setup

from .models import Event, NotaryModelForm

# create mongodb records for each event
events = ['NewContractCreated', 'NewContribution', 'GoalReached', 'ActFailed']
for event in events:
  record = Event.objects.create(type=event)
  record.save()

# set filters and counters for each event
newContractFilter = contract.events.NewContractCreated.createFilter(fromBlock='0x0')
newContributionFilter = contract.events.NewContribution.createFilter(fromBlock='0x0')
goalReachedFilter = contract.events.GoalReached.createFilter(fromBlock='0x0')
actFailedFilter = contract.events.ActFailed.createFilter(fromBlock='0x0')
filters = [newContractFilter, newContributionFilter, goalReachedFilter, actFailedFilter]

#######################################################################################################################


from .forms import NotaryForm
from django.shortcuts import  render, redirect
from datetime import datetime
from django.contrib import messages
import time
from pprint import pprint

def process_new_contract(form, request):
  # verify all params are ok
  buyer = form.cleaned_data['buyer']
  seller = form.cleaned_data['seller']
  amount = Web3.toWei(form.cleaned_data['amount'], 'ether')
  deadline = form.cleaned_data['deadline']*7*24*3600
  description = form.cleaned_data['description']
  if (not w3.isAddress(buyer)) or (not w3.isAddress(seller)) or (amount <= 0) or (deadline < contract.functions.minPeriodOfDeadline_().call()+1):
    return
  # vars are ok
  now = int(time.time()) # unix epoch
  deadline += now
  print(acct.address, w3.eth.get_balance(acct.address))
  new_contract_txn = contract.functions.newContract(buyer, seller, description, amount, deadline).buildTransaction({
      'from': acct.address,
      'nonce': w3.eth.getTransactionCount(acct.address),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
  signed = w3.eth.account.sign_transaction(new_contract_txn, private_key)
  tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print('Transaction receipt for new contract method:')
  pprint(dict(tx_receipt))
  
def process_contribute_contract(form, request):
  id = int(form.cleaned_data['id'])
  amount = Web3.toWei(form.cleaned_data['amount'], 'ether')
  t = contract.functions.getTitleDeed(id).call()
  print(id, amount, t)
  if (amount <= 0) or (t[6] is True): 
    print('Amount should be greater than 0 or contract already closed')
    return
  new_contribution_txn = contract.functions.newPayment(id).buildTransaction({
      'from': acct.address,
      'value': amount,
      'nonce': w3.eth.getTransactionCount(acct.address),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
  signed = w3.eth.account.sign_transaction(new_contribution_txn, private_key)
  tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print('Transaction receipt for new contract method:')
  pprint(dict(tx_receipt))
      
  
def process_delete_contract(form, request):
  id = int(form.cleaned_data['id'])
  t = contract.functions.getTitleDeed(id).call()
  if t[6] is True:
    print('Contract already completeed or archived')
    return
  new_delete_txn = contract.functions.deletedNotaryAct(id).buildTransaction({
      'from': acct.address,
      'nonce': w3.eth.getTransactionCount(acct.address),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
  signed = w3.eth.account.sign_transaction(new_delete_txn, private_key)
  tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print('Transaction receipt for new contract method:')
  pprint(dict(tx_receipt))

def processForm(form, request):
  type = form.cleaned_data["type"]
  if type == 'new':
    process_new_contract(form, request)
  elif type == 'contribute':
    process_contribute_contract(form, request)
  elif type == 'delete':
    process_delete_contract(form, request)
  else:
    messages.error(request, "Operation not allowed.")
  return redirect("mainApp:homepage")

###############################################################

def get_acts_from_contract():
  acts = []
  # check if contract has been completed, and eventually make its status to 'closed'
  # closed contracts are not shown
  num_of_contracts = contract.functions.numContract_().call()
  for i in range(num_of_contracts):
    t = contract.functions.getTitleDeed(i).call()
    if t[6] is True:
      record = NotaryModelForm.objects.filter(id=i).first()
      if record is not None:
        record.status = 'closed' # todo: this is redundant for already closed contracts
    else:
      acts.append({'id': i, 'buyer':t[0], 'seller':t[1], 'description':t[2],
                 'amount': t[3], 'amount_for_now': t[4],
                 'deadline':round((t[5]-time.time())/(7*24*3600))})
  return acts

def get_events_from_contract():
  for filter in filters:
    for event in filter.get_new_entries():
      # update records in db
      record = Event.objects.filter(type=event['event']).first()
      if record is not None:
        record.times += 1
        record.date = datetime.now()
        record.save()
  # db is updated, now retrieve info we need
  output = []
  for event in events:
    record = Event.objects.filter(type=event).first()
    output.append({'type':record.type, 'times':record.times, 'date':record.date})
  return output

###############################################################

def homepage(request):
  form = NotaryForm()
  #if there is an incoming submitted form
  if request.method == "POST":
    form = NotaryForm(request.POST)
    if form.is_valid():
      processForm(form, request)
      return redirect('mainApp:homepage')
  
  list_of_contracts = get_acts_from_contract()
  list_of_events = get_events_from_contract()
  context = {
    "list_of_contracts": list_of_contracts,
    "list_of_events": list_of_events,
    "form": form
  }
  return render(request=request, template_name='mainapp/home.html', context=context)
