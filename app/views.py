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
from django.http import JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache



class ProductView(View):
    def get(self,request):
        totalitem=0
        topwear=Product.objects.filter(category='TW')
        bottomwear=Product.objects.filter(category='BW')
        mobile=Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile,'totalitem':totalitem})

class ProductDetailsView(View):
    @method_decorator(never_cache)
    def get(self,request,pk):
        user=request.user
        totalitem=0
        product = get_object_or_404(Product, pk=pk)
        in_cart=False
        if request.user.is_authenticated:
            in_cart = Cart.objects.filter(user=user, product=product).exists()
            totalitem = len(Cart.objects.filter(user=request.user))
        
        return render(request,'app/productdetail.html',{'product':product,'in_cart':in_cart,'totalitem':totalitem})
    

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
        totalitem=0
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amt=50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        totalitem=len(Cart.objects.filter(user=user))
        
        if cart_product:
            for p in cart_product:
                temp_amt=(p.quantity* p.product.discounted_price)
                amount+=temp_amt
            total_amount=amount+shipping_amt
            return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'total_amount':total_amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',{'totalitem':totalitem})
        
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
    if request.user.is_authenticated:
        user=request.user
        totalitem=0
        totalitem=len(Cart.objects.filter(user=user))
        
    if request.method == 'POST':
        product_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product is already in the cart for the current user
        existing_cart_item = Cart.objects.filter(user=request.user, product=product).first()
        
        if existing_cart_item:
            # Product is already in the cart, don't add a duplicate entry
            return redirect('/checkout',{'totalitem':totalitem})
        
        # Add the product to the cart if it's not already present
        Cart(user=request.user, product=product).save()
        
        return redirect('/checkout',{'totalitem':totalitem})
    else:
        return redirect('/')


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
    totalitem=0
    user=request.user
    op = OrderPlaced.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed':op,'user':user,'totalitem':totalitem})

def change_password(request):
 return render(request, 'app/changepassword.html')


@login_required
def cancel_order(request,pk):
    if request.method=='POST':
        order=get_object_or_404(OrderPlaced,id=pk,user=request.user)
        order.delete()
        return redirect('orders')
    else:
        return redirect('/')
        
        
        
    


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
    totalitem=0
    totalitem=len(Cart.objects.filter(user=user))
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
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_product':cart_product,'totalitem':totalitem})



@login_required
def payment_done(request):
    custid = request.GET.get('custid')
    user = request.user

    if not custid:
        messages.error(request, 'Please select a shipping address.')
        return redirect('/checkout')

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        messages.error(request, 'Selected address is invalid. Please select a valid address.')
        return redirect('/checkout')

    # Process the cart items
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        OrderPlaced(user=user, customer=customer, product=item.product, quantity=item.quantity).save()
        item.delete()

    return redirect("orders")





def product_list(request):
    query = request.GET.get('query','').strip()
    products = Product.objects.all()

    if query:
        products = products.filter(title__icontains=query)
        return render(request, 'app/product_list.html', {'products':products})
    else:
        return redirect('/')
