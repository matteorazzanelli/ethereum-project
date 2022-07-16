# Fetch deployed conract
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
deployed_contract_address = '0xDaa0db926b98FBB1De4752dA73cc8b6FAEDeBc5D'
compiled_contract_path = 'startup_token/build/contracts/NotaryContract.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)


#######################################################################################################################


from .models import Event
from .forms import ActForm
from django.shortcuts import  render, redirect

# Create your views here.
def homepage(request):
  form = OrderForm()
  #if there is an incoming submitted form
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid():
      processOrder(form, request)
      return redirect('app:homepage')
    
  context = {
    "user": request.user,
    # "open_orders": Order.objects.filter(profile=request.user, status="pending").order_by('datetime'),
    # "closed_orders": Order.objects.filter(profile=request.user, status="executed").order_by('-datetime'),
    "gas_price": w3.eth.gasPrice,
    "block_number": w3.eth.blockNumber
    # "profit": wallet.profit,
    # "form": form
  }
  return render(request=request, template_name='mainapp/home.html', context=context)



#######################################################################################################################


# import json
# from web3 import Web3
# from .render import Render
# from .models import Rec_Model
# from django.http import HttpResponseRedirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.sessions.models import Session

# url = 'https://ropsten.infura.io/v3/<PASTE YOUR API KEY HERE>'
# web3 = Web3(Web3.HTTPProvider(url))

# address = web3.toChecksumAddress("0x0231CE2f680d4986DE84E55f2a72cBade878B774")
# abi = json.loads('''[...]''')
	
# contract = web3.eth.contract(address=address,abi=abi)

# def connect(request):
# 	return render(request,'main_app/index.html')

# #CONNECTING TO SMART CONTRACT FOR POST,PAYMENTS etc
# def get_posts_from_contract():
# 	func_to_call = 'postCount'
# 	contract_func = contract.functions[func_to_call]
# 	postCount = contract_func().call()

# 	posts=[]
# 	for i in range(postCount):
# 		p = contract.functions.posts(i+1).call()
# 		posts.append(p)	
# 	return posts


# def append(request):
# 	return render(request, 'main_app/submit.html')


# #ACCESSING AND DISPLAY OF POSTS
# def posts(request):
	
# 	posts = get_posts_from_contract()
# 	# print(f'{posts}\n\n')

# 	posts.sort(key = lambda x: x[2], reverse=True)

# 	paginator = Paginator(posts,5)
# 	page_number =  request.GET.get('page')
# 	page_obj = paginator.get_page(page_number)

# 	context={
# 		'page':page_obj,
# 		'posts':posts,
# 		# 'author':account_address
# 	}

# 	return render(request,'main_app/posts.html',context)

# def get_free_post(request,pid):
# 	posts=[]
# 	posts_list=get_posts_from_contract()
# 	for p in posts_list:
# 		if p[0] == pid:
# 			if p[1] == False:
# 				posts.append(p)
# 	if len(posts)==0:
# 		messages.warning(request,'THIS POST IS NOT FOR SALE')
# 		return redirect('posts')

# 	context={
# 		'posts':posts[0],
# 		'pid':pid
# 	}
# 	return render(request, 'main_app/get_post.html',context)
			
# def get_receipt(request,pid):
# 	if request.method=='POST':
# 		global receipt
# 		receipt = request.POST.get('receipt')
# 		check = Rec_Model.objects.filter(receipt=receipt).exists()
# 		if check:
# 			messages.warning(request,'THIS RECEIPT HAS BEEN USED EARLIER')
# 			return redirect('receipt', pid=pid)
# 		else:
# 			if (receipt.startswith("0x") and len(receipt)==66):
# 				rec=web3.eth.waitForTransactionReceipt(receipt)
# 				rec=dict(rec)
# 				status = rec["status"]
# 				if status==1:
# 					request.session['has_receipt']=True
# 					rec = Rec_Model.objects.create(receipt=receipt)
# 					if rec:
# 						return redirect('get_post', pid=pid)
# 				else:
# 					messages.warning(request,'INVALID TRANSACTION RECEIPT')
# 					return redirect('payment',pid=pid)
# 			else:
# 				messages.warning(request,'INVALID RECEIPT')
# 				return redirect('receipt', pid=pid)
			
# 	return render(request, "main_app/receipt.html")

# def get_post(request,pid):
# 	if request.session.has_key('has_receipt'):
# 		posts=[]
# 		posts_list=get_posts_from_contract()
# 		for p in posts_list:
# 			if p[0] == pid:
# 				posts.append(p)
# 		print(posts[0][0])
# 		context={
# 			'posts':posts[0],
# 			'pid':pid
# 		}

# 		return render(request, 'main_app/get_post.html',context)
# 	else:
# 		return redirect('receipt',pid=pid)



# def payment(request, pid):
# 	context ={
# 		'pid':pid
# 	}
# 	return render(request, 'main_app/payment.html',context)


# #DOWNLOADING THE CONTENT ON SYSTEM
# def get_pdf(request,pid, *args, **kwargs):
# 	posts=[]
# 	posts_list=get_posts_from_contract()
# 	for p in posts_list:
# 		if p[0] == pid:
# 			posts.append(p)
# 	print(posts[0])
# 	context={
# 		'posts':posts[0]
# 	}

# 	return Render.render('main_app/get_post.html', context)

# def buy_content(request):
# 	posts = []
# 	all_posts = get_posts_from_contract()
# 	# print(f'{posts[1][1]}\n\n')
# 	for post in all_posts:
# 		if post[1]:
# 			posts.append(post)

# 	posts.sort(key = lambda x: x[2], reverse=True)
# 	total = len(posts)

# 	paginator = Paginator(posts,5)
# 	page_number =  request.GET.get('page')
# 	page_obj = paginator.get_page(page_number)

# 	context={
# 		'page':page_obj,
# 		'posts':posts,
# 		'total':total
# 	}

# 	return render(request,'main_app/buy_content.html',context)


