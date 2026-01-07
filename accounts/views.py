from django.shortcuts import render, redirect
from .forms import RegistrationForm
from.models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, 
                                               username=username, password=password) # in models.py from where this methiod is coming, we havent given the phone_number so not here as well
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request) #if anything else is required in palce of localhost. diff kind of domain
            mail_subjct = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user, #pk
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encoding pk so that nobody would see it
                'token': default_token_generator.make_token(user),          
            })
            to_email = email
            send_email = EmailMessage(mail_subjct,message,to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering! A verification link has been sent to your email. Please check your inbox to verify your account.')
            return redirect('/accounts/login?command=verification&email='+email)
        
    else: # if its a get requets on;y the registration form is rendered
        form = RegistrationForm() 
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)

def login(request):
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, "accounts/login.html")

@login_required(login_url= 'login')
def logout(request):
    # return render(request, "accounts/logout.html")
    auth.logout(request)
    messages.success(request, "You're successfully logged out.")
    return redirect('login')

def activate(request, uidb64, token):
    # return HttpResponse("ok")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active= True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')

@login_required 
def dashboard(request): # only availalbe when you're logged in so the decorator
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method=="POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) # __exact will chekc if the email is mathcing iwth the email with what we have in db
           
            # Reset Password email 
            current_site = get_current_site(request) #if anything else is required in palce of localhost. diff kind of domain
            mail_subjct = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user, #pk
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encoding pk so that nobody would see it
                'token': default_token_generator.make_token(user),          
            })
            to_email = email
            send_email = EmailMessage(mail_subjct,message,to=[to_email])
            send_email.send()
           
            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect('login')
        
        else:
            messages.error(request, "Account doesn't exist")
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64,token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'The Password Reset link has been expired!')
        return redirect('login')

# def resetPassword(request):
#     if request.method == "POST":
#         password =  request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password == confirm_password:
#             uid = request.session.get('uid')
#             user = Account.objects.get(pk=uid)
#             user.set_password(password) # save password will give error. django's inbuilt func will take the passsord and hash it
#             user.save()
#             messages.success(request, 'Password reset successful')
#             return redirect('login')
        
#         else:
#             messages.error(request, 'Password do not match')
#             return redirect('resetPassword')
#     else:
#         return render(request, 'accounts/resetPassword.html')

def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('resetPassword')

        uid = request.session.get('uid')

        if uid is None:
            messages.error(request, "Session expired. Please reset your password again.")
            return redirect('forgotPassword')

        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()

        # 🔐 IMPORTANT: clear session
        del request.session['uid']

        messages.success(request, 'Password reset successful. Please login.')
        return redirect('login')

    return render(request, 'accounts/resetPassword.html')

