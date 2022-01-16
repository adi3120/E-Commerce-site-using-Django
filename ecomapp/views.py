from distutils.config import PyPIRCCommand
from itertools import product
from sre_constants import SUCCESS
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


# def home(request):
#  return render(request, 'ecomapp/home.html')


class ProductView(View):
	def get(self, request):
		topwears = Product.objects.filter(category='TW')
		bottomwears = Product.objects.filter(category='BW')
		mobiles = Product.objects.filter(category='M')
		laptops = Product.objects.filter(category='L')
		context = {
			'topwears': topwears,
			'bottomwears': bottomwears,
			'mobiles': mobiles,
			'laptops': laptops,
		}
		return render(request, 'ecomapp/home.html', context)


class ProductDetailView(View):
	def get(self, request, pk):
		product = Product.objects.get(pk=pk)
		context = {
			'product': product
		}
		return render(request, 'ecomapp/productdetail.html', context)


def add_to_cart(request):
	user=request.user
	product_id=request.GET.get('prod_id')
	product=Product.objects.get(id=product_id)
	Cart(user=user,product=product).save()

	return redirect('/cart')

def show_cart(request):
	if request.user.is_authenticated:
		user=request.user
		cart=Cart.objects.filter(user=user)
		amount=0.0

		shipping_amount=70.0

		total_amount=0.0

		# cart_product=[p for p in Cart.objects.all() if p.user == user]
		cart_product=[]

		for p in Cart.objects.all():
			if p.user==user:
				cart_product.append(p)
				amount+=p.product.discounted_price*p.quantity+shipping_amount

		total_amount=amount

		print(cart_product)
		print(amount)


		context={
			'carts':cart,
			'amount':amount,
			'total':total_amount,
			'shipping':shipping_amount,
		}
		return render(request, 'ecomapp/addtocart.html',context)

def plus_cart(request):
	if request.method=="GET":
		prod_id=request.GET['prod_id']
		c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1;
		c.save()
		amount=0.0
		shipping_amount=70.0
		user=request.user
		cart_product=[p for p in Cart.objects.all() if p.user==user]

		for p in cart_product:
			tempamount=(p.quantity * p.product.discounted_price)
			amount+=tempamount
			totalamount=amount+shipping_amount

		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':totalamount,
		}

		return JsonResponse(data)


def minus_cart(request):
	if request.method=="GET":
		prod_id=request.GET['prod_id']
		c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1;
		c.save()
		amount=0.0
		shipping_amount=70.0
		user=request.user
		cart_product=[p for p in Cart.objects.all() if p.user==user]

		for p in cart_product:
			tempamount=(p.quantity * p.product.discounted_price)
			amount+=tempamount
			totalamount=amount+shipping_amount

		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':totalamount,
		}

		return JsonResponse(data)

	

def buy_now(request):
 return render(request, 'ecomapp/buynow.html')


def profile(request):
 return render(request, 'ecomapp/profile.html')


def address(request):
	add=Customer.objects.filter(user=request.user)
	context={
		'address':add,
		'active':'btn-primary',
	}
	return render(request, 'ecomapp/address.html',context)


def orders(request):
 return render(request, 'ecomapp/orders.html')


def mobile(request,data=None):
	context={}
	if data==None:
		mobiles=Product.objects.filter(category='M')

	elif data=='Redmi' or data=='Samsung':
		mobiles=Product.objects.filter(category='M').filter(brand=data)
	elif data=='below':
		mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)

	elif data=='above':
		mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)


	context={
			'mobiles':mobiles
		}
	return render(request, 'ecomapp/mobile.html',context)


def laptop(request,data=None):
	context={}
	if data==None:
		laptops=Product.objects.filter(category='L')

	elif data=='Lenovo' or data=='Acer':
		laptops=Product.objects.filter(category='L').filter(brand=data)
	elif data=='below':
		laptops=Product.objects.filter(category='L').filter(discounted_price__lt=40000)

	elif data=='above':
		laptops=Product.objects.filter(category='L').filter(discounted_price__gt=40000)


	context={
			'laptops':laptops
		}
	return render(request, 'ecomapp/laptop.html',context)

def topwear(request,data=None):
	context={}
	if data==None:
		topwears=Product.objects.filter(category='TW')

	elif data=='Park' or data=='Polo':
		topwears=Product.objects.filter(category='TW').filter(brand=data)
	elif data=='below':
		topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=500)

	elif data=='above':
		topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=500)


	context={
			'topwears':topwears
		}
	return render(request, 'ecomapp/topwear.html',context)


def bottomwear(request,data=None):
	context={}
	if data==None:
		bottomwears=Product.objects.filter(category='BW')

	elif data=='Spykar' or data=='Lee':
		bottomwears=Product.objects.filter(category='BW').filter(brand=data)
	elif data=='below':
		bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=500)

	elif data=='above':
		bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=500)


	context={
			'bottomwears':bottomwears
		}
	return render(request, 'ecomapp/bottomwear.html',context)


class CustomerRegistrationView(View):

	def get(self,request):
		form=CustomerRegistrationForm()
		context={
			'form':form
		}
		return render(request, 'ecomapp/customerregistration.html',context)
	def post(self,request):
		form=CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request,"Congratulations!! Registered Successfully")
			form.save()
		context={
			'form':form
		}
		return render(request, 'ecomapp/customerregistration.html',context)
		


def checkout(request):
	return render(request, 'ecomapp/checkout.html')


class ProfileView(View):
	def get(self,request):
		form=CustomerProfileForm()
		context={
			'form':form,
			'active':'btn-primary',
		}
		return render(request,'ecomapp/profile.html',context)
	def post(self,request):
		form=CustomerProfileForm(request.POST)
		if form.is_valid():
			usr=request.user
			name=form.cleaned_data['name']
			locality=form.cleaned_data['locality']
			city=form.cleaned_data['city']
			state=form.cleaned_data['state']
			zipcode=form.cleaned_data['zipcode']

			reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)

			reg.save()

			messages.success(request,'Congratulations!! Profile Updated Successfully')
		context={
			'form':form,
			'active':'btn-primary',
		}
		return render(request,'ecomapp/profile.html',context)
