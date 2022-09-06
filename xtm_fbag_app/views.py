from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import get_template
from .forms import *
import uuid

'''------------for maintaining logs----------------------------------------------------------------------'''
# from logging import *

# LOG_FORMAT = '%(asctime)s  //  %(message)s  //  %(lineno)d'
# basicConfig(filename='logfile.log', level=DEBUG, filemode='a+', format=LOG_FORMAT)

# link = settings.MEDIA_URL
'''-------------------------------------------------------------------------------------------------------'''

def signup(request):
    """---------SignUp functionality is provided----------"""

    try:
        if request.method == 'POST':
            password = request.POST['password2']
            password1 = request.POST['password1']
            if password != password1:
                messages.success(request, "Password and confirm password should be same")
            form = UserRegisterForm(request.POST)
            email = request.POST['email']

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email already registered')
            if form.is_valid():
                obj = form.save()
                messages.success(request, 'You have registered successfully.')
                first_name = request.POST.get("first_name")
                email_from = settings.EMAIL_HOST_USER
                context = {"first_name": first_name, "email_from": email_from}
                message = get_template("email/email_register.html").render(context)
                mail = EmailMessage(
                    subject="Registration successfully at XTM FBAG application",
                    body=message,
                    from_email=email_from,
                    to=[email],
                    reply_to=[],
                )
                mail.content_subtype = "html"
                mail.send()
                return redirect('sign_in')

            else:
                return render(request, 'xtm_fbag_app/Register.html', {'form': form})
    except Exception as error:
        messages.error(request, error)
        return render(request, 'xtm_fbag_app/Register.html')
    else:
        form = UserRegisterForm()
    return render(request, 'xtm_fbag_app/Register.html', {'form': form})

@login_required(login_url='/')
def home(request):
    try:
        return render(request, 'xtm_fbag_app/index.html')
    except Exception as error:
        messages.success(request, error)
        return render(request, 'xtm_fbag_app/index.html')


def sign_in(request):
    """-----------------------Login functionality is provided--------------------------------------------"""

    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            if not email or not password:
                messages.success(request, f'Enter Both email and password')
                return redirect('sign_in')
            user_obj = User.objects.filter(email=email).first()
            if user_obj is None:
                messages.success(request, f'User not found')
                return render(request, 'xtm_fbag_app/Login.html', )
            user = authenticate(request, email=email, password=password)
            if user is not None:
                form = login(request, user)
                messages.success(request, f'Welcome {user.first_name.capitalize()} {user.last_name.capitalize()} ')
                return redirect('home')
            else:
                messages.info(request, f'Wrong password')
        return render(request, 'xtm_fbag_app/Login.html')
    except Exception as error:
        messages.error(request, error)
        return render(request, 'xtm_fbag_app/Login.html')





@login_required(login_url='/')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('sign_in')


def forgot_password(request):
    """---------forgot password functionality is provided----------"""

    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email__exact=email).exists():
                messages.info(request, f'No user found with {email}')
                return render(request, 'xtm_fbag_app/forgot-password.html')
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            link = f'{request.scheme}://{request.get_host()}/reset_password/{token}/'
            if user_obj.first_name:
                first_name = user_obj.first_name
                context = {"first_name": first_name, 'link': link}
            else:
                context = {'link': link}
            message = get_template("email/email_forgot.html").render(context)
            mail = EmailMessage(
                subject="Forgot password link",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
                reply_to=[],
            )
            mail.content_subtype = "html"
            mail.send()
            messages.success(request, 'An email is sent.')
            return redirect('forgot_password')
        else:
            return render(request, 'xtm_fbag_app/forgot-password.html')
    except Exception as error:
        messages.error(request, error)
        return render(request, 'xtm_fbag_app/forgot-password.html')


def reset_password(request, token):
    """-------------------------------Reset password functionality is provided------------------------------------"""

    context = {}
    try:
        user_obj = User.objects.filter(forget_password_token=token).first()
        context = {'user_id': user_obj.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('new_password1')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.success(request, 'No user id found.')
                return render(request, 'xtm_fbag_app/reset-password.html')

            if new_password != confirm_password:
                messages.success(request, f'Both passwords should  be same.')
                return render(request, 'xtm_fbag_app/reset-password.html', context)

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'you have successfullly changed your password')
            return redirect('sign_in')
    except Exception as error:
        return HttpResponse(status=404)
    return render(request, 'xtm_fbag_app/reset-password.html', context)


@login_required(login_url='/')
def change_password(request):
    """---------Change password functionality is provided----------"""

    try:
        if request.method == "POST":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('new_password1')
            user_obj = User.objects.get(id=request.user.id)
            if not user_obj.check_password(old_password):
                messages.success(request, f'Incorrect old password')
                return render(request, 'xtm_fbag_app/change-password.html')
            if not new_password == confirm_password:
                messages.success(request, 'New password and confirm password must be same')
            else:
                user_obj.set_password(str(new_password))
                user_obj.save()
                messages.success(request, 'Password changed successfully')
                return render(request, 'xtm_fbag_app/index.html')

        return render(request, 'xtm_fbag_app/change-password.html')
    except Exception as error:
        messages.error(request, error)
        return render(request, 'xtm_fbag_app/change-password.html')




# here is starting with POSt


@login_required(login_url='/')
def create_post(request):

    
    # if request.user.is_authenticated:

    if request.method == "POST":
            req = request.POST.get
            title1 = req("title1")
            comment1 = req("comment1")

            post_data = Post.objects.create(title=title1,author=request.user,content=comment1)
            post_data.save()
            return redirect("home")

    return render(request,'post/create_post.html')


@login_required(login_url='/')
def list_post(request):
    latest_post_list = Post.objects.filter(author=request.user).order_by('-updated_on')[:5]
    return render(request,'xtm_fbag_app/index.html',{'latest_post_list': latest_post_list})



def delete_post(request,pk):
    dlt_post = Post.objects.get(id=pk)
    dlt_post.delete()
    latest_post_list = Post.objects.filter(author=request.user).order_by('-updated_on')[:5]
    return render(request,'post/list_post.html',{'latest_post_list': latest_post_list})