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
    # session_card = get_session_cart(request)
    # session_card = create_purchase_card(request)    
    # Get category_name and product_name from the GET request
    category_name = request.GET.get('category_name')
    product_name = request.GET.get('product_name')
    # Get all categories
    all_categories = Category.objects.all()
    # Filter products by category_name if provided
    if category_name:
        # Assuming category_name is the name of the Category model field
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
        # Assuming product_name is the name of the Product model field
        all_products = all_products.filter(name__icontains=product_name)

    context = {
        'products': all_products,
        'categories': all_categories,
        'selected_category': category_name,  # Pass the selected category name to highlight in the template
        'selected_product': product_name,    # Pass the selected product name to highlight in the template
        'purchase_cart': purchase_cart,
        # 'session_card': session_card,  # Add the session card to the context
    }
    return render(request, 'products.html', context)

from .models import PurchaseLine

def add_product(request, product_id):
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
                
                # Update the product stock
                product.stock -= number
                product.save()
                
                # Create a new PurchaseLine instance
                purchase_line = PurchaseLine.objects.create(
                    product=product,
                    amount=number,
                    purchase=purchase_cart
                )
                
                print(f"Added {number} {product.name} to PurchaseCard {purchase_cart.id}")
                
            except Exception as e:
                print(f"Error adding product to PurchaseCard: {e}")
    
    return redirect('all_products')

# def add_product(request, product_id):
#     print("add product function entered !!!")
#     if request.method == 'POST':
#         number = request.POST.get('number')
#         print("NUMBER IS", number)
#     product = Product.objects.get(id=product_id)
#     product.stock = product.stock - int(number)
#     product.save()
#     return redirect('all_products')

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

            
    
def single_product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product  # Replace 'data' with the data you want to pass to the template
    }
    # return HttpResponse(f"Single flight {flight}")
    return render(request, 'single_flight.html', context)


#######
##########

    
def buy_products(request):
    # Get category_name and product_name from the GET request
    category_name = request.GET.get('category_name')
    product_name = request.GET.get('product_name')

    # Get all categories
    all_categories = Category.objects.all()

    # Filter products by category_name if provided
    if category_name:
        # Assuming category_name is the name of the Category model field
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
        # Assuming product_name is the name of the Product model field
        all_products = all_products.filter(name__icontains=product_name)

    context = {
        'products': all_products,
        'categories': all_categories,
        'selected_category': category_name,  # Pass the selected category name to highlight in the template
        'selected_product': product_name,    # Pass the selected product name to highlight in the template
    }
    return render(request, 'buy_products.html', context)    



# def get_session_cart(request):
#     print("get session function entered !!!")
#     user = request.user
#     cart_id = request.session.get('cart_id')

#     if user.is_authenticated:
#         print(f"Hi: {user}")
#         try:
#             print("checking if there is a purchase card with pending status")
#             # Retrieve the purchase card with status "Pending"
#             # user = request.user  # Get the current user
#             purchase_card = PurchaseCard.objects.get(customer=user, status=Options.OPTION_TWO.value)
#             # if purchase_card:
#             print(f"pending purchase cart - {purchase_card}")
#             return purchase_card                
#             # else:
#                 # If the user is not authenticated, create a new purchase card
#                 # print("user not authenticated, creating new purchase card")
#                 # return create_purchase_card(request)
#         except PurchaseCard.DoesNotExist:
#             print("purchase card not found with pending status")
#             # If no open session found with the specified status, create a new one
#             return create_purchase_card(request) 
#     else:        
#         cart_id = request.session.get('cart_id')
#         if cart_id:            
#          print(f"Existing cart ID: {cart_id}")
#          return create_purchase_card(request)
#         else:
#             print("no cart ID in session, creating new purchase card")
#             # If no cart ID in session, create a new purchase card
#             return create_purchase_card(request)