from distutils.config import PyPIRCCommand
from itertools import product
from unicodedata import category
from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages

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

# def product_detail(request):
#  return render(request, 'ecomapp/productdetail.html')


class ProductDetailView(View):
	def get(self, request, pk):
		product = Product.objects.get(pk=pk)
		context = {
			'product': product
		}
		return render(request, 'ecomapp/productdetail.html', context)


def add_to_cart(request):
 return render(request, 'ecomapp/addtocart.html')


def buy_now(request):
 return render(request, 'ecomapp/buynow.html')


def profile(request):
 return render(request, 'ecomapp/profile.html')


def address(request):
 return render(request, 'ecomapp/address.html')


def orders(request):
 return render(request, 'ecomapp/orders.html')


def change_password(request):
 return render(request, 'ecomapp/changepassword.html')


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
