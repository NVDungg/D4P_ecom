from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#for email vefication
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests

from .forms import RegistrationForm
from .models import Account
from carts.models import Cart, CartItem
from carts.views import _cart_id

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #render username by add to email
            username = email.split("@")[0] 
            #create user have all the information in fields
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'ANow active your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #encode for user pk
                'token': default_token_generator.make_token(user)   #create token for user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Welcome to the site. We sent you a verification email to your email address. Please verify it')

            #if verify is success redirect to login form had email = email
            return redirect('login/?command=verification&email='+email) 
    else:
        form =  RegistrationForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    '''get uid and token from request. Decode uid to get pk user,
    by that uid and token now active user'''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is acctivated!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email, password = password)

        if user is not None:
            try:
                '''Take the cart session and if it had item in it b4 login.
                Then assign user to that cart if u logged.'''
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() 
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    #store all variation product in here
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    '''If the user is authenticated, the code retrieves all the CartItem objects associated with the user 
                    and stores their variations and IDs in the exists_variation and id lists.'''
                    cart_item = CartItem.objects.filter(user=user)
                    exists_variation = []
                    id = []
                    for item in cart_item:  
                        existing_variation = item.variations.all()
                        exists_variation.append(list(existing_variation))
                        id.append(item.id)

                    '''compares the product_variation list with the exists_variation. If a variation in product_variation exists 
                    in exists_variation, the code retrieves the id of the corresponding CartItem object and increments its quantity byone. 
                    The user associated with the CartItem object is also updated with the current user and the changes are saved to the database.'''
                    for pr in product_variation:
                        if pr in exists_variation:
                            index = exists_variation.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1 # increase after click
                            item.user = user
                            item.save()

                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
      
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now login')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #out put query it: next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                #out put params it: {'next': '/cart/checkout/'}

                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashbroad')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #send email reset
            current_site = get_current_site(request)    #get the site host
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #encode for user pk
                'token': default_token_generator.make_token(user)   #create token for user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Email has been send to your email!')

        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    '''get uid and token from request. Decode uid to get pk user,
    by that uid and token now reset password'''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Now reset your password!')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('login')
    
def resetpassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get['uid']
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset success!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetpassword')

    return render(request, 'accounts/resetpasswrod.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logout')
    return redirect('login')

@login_required(login_url= 'login')
def dashbroad(request):
    return render(request, 'accounts/dashbroad.html')

    
