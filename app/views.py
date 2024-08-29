from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import (
    Customer,
    Product,
    OrderPlaced,
    Cart
)
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self,request):
        totalitem=0
        topwear=Product.objects.filter(category='TW')
        bottomwear=Product.objects.filter(category='BW')
        mobile=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile,'totalitem':totalitem})

class ProductDetailsView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})
    

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amt=50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        
        if cart_product:
            for p in cart_product:
                temp_amt=(p.quantity* p.product.discounted_price)
                amount+=temp_amt
            total_amount=amount+shipping_amt
            return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'total_amount':total_amount})
        else:
            return render(request,'app/emptycart.html')
        
@login_required     
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amt=50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        if cart_product:
            for p in cart_product:
                temp_amt=(p.quantity* p.product.discounted_price)
                amount+=temp_amt
            total_amount=amount+shipping_amt
            
            data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':total_amount
            }
            return JsonResponse(data)
            
@login_required      
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amt=50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        if cart_product:
            for p in cart_product:
                temp_amt=(p.quantity* p.product.discounted_price)
                amount+=temp_amt
            total_amount=amount+shipping_amt
            
            data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':total_amount
            }
            return JsonResponse(data)       


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.delete()

        amount = 0.0
        shipping_amt = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        if cart_product:
            for p in cart_product:
                temp_amt = p.quantity * p.product.discounted_price
                amount += temp_amt
            total_amount = amount + shipping_amt
            
            data = {
                'amount': amount,
                'total_amount': total_amount,
                'is_cart_empty': False
            }
        else:
            # Render the empty cart template
            empty_cart_html = render_to_string('app/emptycart1.html', {})
            data = {
                'is_cart_empty': True,
                'empty_cart_html': empty_cart_html
            }

        return JsonResponse(data)

                      
@login_required          
def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Address added successfully!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    user=request.user
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op,'user':user})

def change_password(request):
 return render(request, 'app/changepassword.html')

@login_required
def mobile(request, data=None):
    if data:
        # Use `__in` lookup to handle multiple brand names
        valid_brands = ['Vivo', 'Oppo', 'Samsung']
        if data in valid_brands:
            mobiles = Product.objects.filter(category='M', brand=data)
        else:
            # Handle cases where the brand is not valid, optionally return all products or an empty queryset
            mobiles = Product.objects.filter(category='M')
        if data=='below':
            mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
        elif data=='Above':
            mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    else:
        mobiles = Product.objects.filter(category='M')
    
    return render(request, 'app/mobile.html', {'mobiles': mobiles})
        

class CustomRegistrationForm(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations! You have been successfully registered!")
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})
        
        
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    amount = 0.0
    shipping_amt = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amt = p.quantity * p.product.discounted_price
            amount += temp_amt
        total_amount = amount + shipping_amt
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_product':cart_product})

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	# print("Customer ID", custid)
	user = request.user
	carts = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	# print(customer)
	for cid in carts:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		cid.delete()
	return redirect("orders")
    
