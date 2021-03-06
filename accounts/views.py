from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth, messages
from .forms import UserLoginForm, UserRegistrationForm, get_user_model

from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect

from checkout.models import Transaction, LineItem

# import in the login_required annotation
from django.contrib.auth.decorators import login_required

from cart.views import view_cart_amount
from cart.models import CartItem



# Create your views here.
def index(request):
    cart_amount = None
    if request.user.is_authenticated:
        cart_amount = CartItem.objects.filter(owner=request.user).count()
    return render(request, 'accounts/index.template.html', {
        'cart_amount': cart_amount
    })

# Logout function
def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    # creating a custom logout view that calls the LOGOUT_URL function and defines a redirect page
    return redirect('%s?userAction=%s' % (settings.LOGOUT_URL, request.path))

# Login function
def login(request):
    """Returns the login page"""
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST) # populate the form from what the user has keyed in
        if login_form.is_valid():
            # attempt to check the username and password is valid
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                # log in the user
                auth.login(user=user, request=request)
                # creating a custom login view that calls the LOGIN_URL function and defines a redirect page
                messages.success(request, "You have successfully logged in")
                return redirect('%s?userAction=%s' % (settings.LOGIN_URL, request.path))
            else:
                login_form.add_error(None, "Invalid username or password")
    else:
        login_form = UserLoginForm()
    return render(request, 'accounts/login.template.html', {
        'form':login_form
    })

@login_required    
def profile(request):
    User = get_user_model()
    user = User.objects.get(email=request.user.email)
    all_transactions = list(Transaction.objects.filter(owner=user))
    all_transactions.reverse()
    cart_amount = None
    if request.user.is_authenticated:
        cart_amount = CartItem.objects.filter(owner=request.user).count()
    # line_items = LineItem.objects.filter(all_transactions=all_transactions)
    return render(request, 'accounts/profile.template.html', {
    'all_transactions': all_transactions,
    'cart_amount': cart_amount
    # 'line_items': line_items
    })
    return render(request, 'accounts/profile.template.html', {
        'user' : user
    })
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #check if the username and password matches
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                #acutally log the user in
                auth.login(user=user, request=request)
                messages.success(request, "You have registered successfully")
            else:
                messages.error(request, "You failed to register")
            # creating a custom login view that calls the REGISTER_URL function and defines a redirect page
            return redirect('%s?userAction=%s' % (settings.REGISTER_URL, request.path))
        else:
            return render(request, "accounts/register.template.html", {
                'form': form
            })
    else:
        register_form = UserRegistrationForm()
        return render(request, "accounts/register.template.html", {
            'form': register_form
    })



# view all transactions and order summary in profile page
def view_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    line_items = LineItem.objects.filter(transaction=transaction)
    cart_amount = None
    if request.user.is_authenticated:
        cart_amount = CartItem.objects.filter(owner=request.user).count()
    return render(request, 'accounts/view_transaction.template.html', {
    'transaction': transaction,
    'line_items': line_items,
    'cart_amount': cart_amount
    })