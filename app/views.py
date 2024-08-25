from django.shortcuts import render,redirect
from django.views import View
from .models import (
    Customer,
    Product,
    OrderPlaced,
    Cart
)
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages


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
    
    
       
# def home(request):
#  return render(request, 'app/home.html')

def product_detail(request):
 return render(request, 'app/productdetail.html')

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
        return render(request,'app/addtocart.html',{'carts':cart})

def buy_now(request):
 return render(request, 'app/buynow.html')

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


def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

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
        
        

def checkout(request):
 return render(request, 'app/checkout.html')
