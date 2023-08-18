from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect
from shop.models import Category, MyUser, Product, PurchaseCard, PurchaseLine, Options
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()

def login_page(request):
    print("login page function entered !!!")
    return render(request, "login.html")

def login_user(request):
    print("login function entered !!!")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        
        print(f"username={username}. passowrd={password}")        
         # Authenticate the user - validating user password. return user object if valid
        user = authenticate(request, username=username, password=password)
        print(f"authenticate passed. user is:{user.username}")

        if user is not None:
            # If the credentials are correct, log in the user
            login(request, user)
            print(f"** login passed. user is:{user}")
            return redirect('all_products')        
        else:
            print(f"!! error login. user is:{user}")
            # If authentication fails, show an error message or redirect back to the login page
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
        
    return redirect('login_page')

def create_new_user(username, password, phone_number, address):
    try:
        new_user = User.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            address=address,
        )
        return new_user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

def user_register(request):
    print("register function entered !!!")
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address') 
             # Check if phone_number is empty or not provided
            if not phone_number:
                phone_number = None            
            # Check if address is empty or not provided
            if not address:
                address = None           
            #create new user function
            new_user = create_new_user(
                username=username,
                password=password,
                phone_number=phone_number,
                address=address,
            )
            print(f"{new_user.username} - user created")
            messages.success(request, f"Welcome {new_user.username}- You have successfully registered, please Login")            
        else:
            messages.error(request, "Invalid request method.")
    except Exception as e:
        messages.error(request, f"Error occurred on registration: {e}")
        
    return redirect("login_page")


def logout_user(request):
    print("logout function entered !!!")
    logout(request)
    return redirect('all_products')

def products(request):   
    print("products function entered !!!") 
    
    purchase_cart = get_customer_cart(request)
    
    category_name = request.GET.get('category_name')
    product_name = request.GET.get('product_name')
    # Get all categories & products
    all_categories = Category.objects.all()
    all_products = Product.objects.all()   
           
    # Filter products by category_name if provided
    if category_name and category_name!="None":        
        try:
            selected_category = all_categories.get(name__iexact=category_name)
        except Category.DoesNotExist:
            selected_category = None
            all_products = Product.objects.none()
        else:
            # Filter products within the selected category
            all_products = selected_category.product_set.all()
    else:
        selected_category = None
        all_products = Product.objects.all()
    # Filter products by product_name if provided
    if product_name:        
        all_products = all_products.filter(name__icontains=product_name)

    context = {
        'products': all_products,
        'categories': all_categories,
        'selected_category': category_name, 
        'selected_product': product_name, 
        'purchase_cart': purchase_cart,        
    }
    return render(request, 'products.html', context)


def add_to_cart(request, product_id):
    print("add product function entered !!!")
    
    if request.method == 'POST':
        number = int(request.POST.get('number'))
        print("NUMBER IS", number)
        
        # Get the customer's PurchaseCard using the get_customer_cart function
        purchase_cart = get_customer_cart(request)
        
        if purchase_cart:
            try:
                # Get the product
                product = Product.objects.get(id=product_id)
                if product.stock > 0:
                    # Check if a PurchaseLine with the same product already exists in the cart
                    existing_purchase_line = PurchaseLine.objects.filter(product=product, purchase=purchase_cart).first()
                
                    if existing_purchase_line:
                        # If it exists, update the amount
                        existing_purchase_line.amount += number                    
                        existing_purchase_line.save()
                        print(f"Updated {number} {product.name} in PurchaseCard {purchase_cart.id}")
                    else:
                        # If it doesn't exist, create a new PurchaseLine instance
                        purchase_line = PurchaseLine.objects.create(
                            product=product,
                            amount=number,
                            purchase=purchase_cart
                        )
                        print(f"Added {number} {product.name} to PurchaseCard {purchase_cart.id}")
                    product.stock = product.stock - number
                    product.save()
                else:
                    print("no stock for product")    
            except Exception as e:
                print(f"Error adding product to PurchaseCard: {e}")
        
        return redirect('all_products')

def create_purchase_card(request):
    print("create purchase cart function entered !!!")
    try:       
        #checking if user loged in 
        if request.user.is_authenticated:
            print(f"Logged-in user: {request.user.username}")
            customer = request.user
        else:
            # Replace with the actual username of your default user
            default_user = MyUser.objects.get(username='default')
            customer = default_user       
       
        purchase_card = PurchaseCard.objects.create(
            date=datetime.now(),
            customer=customer,
            status=Options.OPTION_TWO.value # Set the initial status to 'Open'
        )
        request.session['cart_id'] = purchase_card.id  # Store the purchase card ID in the session
        print(request.session.get('cart_id'))
        return purchase_card
    except Exception as e:
        # Handle any exceptions that may occur during creation
        print(f"Error creating purchase cart: {e}")
        return None

def get_session_cart(request):
    print("get session function entered !!!")   
    cart_id = request.session.get('cart_id')
    if cart_id:
        purchase_cart = PurchaseCard.objects.get(id=cart_id, status=Options.OPTION_TWO.value)
        print(f"pending purchase cart is: {purchase_cart}")
        return purchase_cart                   
    else:
        print("no cart ID in session, creating new purchase cart")
        # If no cart ID in session, create a new purchase cart
        return create_purchase_card(request)
            
def get_customer_cart(request):
    
    if request.user.is_authenticated:        
        customer = request.user        
        try:
            purchase_cart = PurchaseCard.objects.get(customer=customer, status=Options.OPTION_TWO.value)
            print(f"pending purchase cart is: {purchase_cart}")
            return purchase_cart        
        except Exception as e:               
            print("no pending purchase cart - new purchase cart created to login user")
            return create_purchase_card(request)        
    else:
        return get_session_cart(request)        

from .models import PurchaseLine

def view_purchase_cart(request):
    print("view_purchase_cart function entered !!!")
    
    purchase_cart = get_customer_cart(request)
    
    # Get category_name and product_name from the GET request
    category_name = request.GET.get('category_name')
    product_name = request.GET.get('product_name')
    
    # Get all categories
    all_categories = Category.objects.all()
    
    # Get all PurchaseLine instances associated with the purchase cart
    purchase_lines = purchase_cart.purchaseline_set.all()
    
    # Filter products by category_name if provided
    if category_name:
        try:
            selected_category = all_categories.get(name__iexact=category_name)
        except Category.DoesNotExist:
            selected_category = None
            all_products = PurchaseLine.objects.none()
        else:
            all_products = purchase_lines.filter(product__category=selected_category)
    else:
        selected_category = None
        all_products = purchase_lines
    
    # Filter products by product_name if provided
    if product_name:
        all_products = all_products.filter(product__name__icontains=product_name)
    
    context = {
        'products': all_products,
        'categories': all_categories,
        'selected_category': category_name,
        'selected_product': product_name,
        'purchase_cart': purchase_cart,
    }
    print(f"{context}")
    return render(request, 'cart.html', context)

def delete_product_from_cart(request, product_id):
    print("deleteing product from cart")
    if request.method == 'POST':
        try:
            # Get the customer's PurchaseCard using the get_customer_cart function
            purchase_cart = get_customer_cart(request)
            
            # Get the product to be deleted
            product_to_delete = PurchaseLine.objects.filter(id=product_id, purchase=purchase_cart).first()
            
            if product_to_delete:
                product_to_delete.delete()
                print(f"Product {product_to_delete.product.name} deleted from cart")
            else:
                print(f"Product with ID {product_id} not found in cart")
        except Exception as e:
            print(f"Error deleting product from cart: {e}")
    
    return redirect('view_purchase_cart')







