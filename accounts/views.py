import os
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from accounts.tokens import account_activation_token, password_reset_token
from accounts.forms import UserSignUpForm, UserForgotPasswordForm, UserPasswordResetForm
from accounts.models import NewUser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def register(request):
    """Register new users and send verification mails to their email addresses."""
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():  # checking the form
            email = request.POST.get('email')
            user = form.save(commit=False) # add all information from the form in the User model
            user.is_active = False  # user is only active after confirming the email!
            user.save() # save the User model 
            site = get_current_site(request) # for the domain
            message = render_to_string('accounts/activate_account_email.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })  # filling the  activation mail template w/ all the variables 

            # This part can be found in the SendGrid setup guide as well
            message = Mail(
                from_email='jutardpierre@gmail.com',
                to_emails=email,
                subject='Activate account for domain.com',
                html_content=message)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY')) 
                response = sg.send(message)  # .status_code, .body, .headers
                messages.add_message(request, messages.SUCCESS, 'A verification email has been sent.')
                messages.add_message(request, messages.WARNING, 'Please also check your SPAM inbox!')
            except Exception as e:
                print(e)  # e.message
                print(e.body)
                messages.add_message(request, messages.WARNING, str(e))
            return render(request, 'accounts/account_activation_sent.html')
        else:
            return render(request, 'accounts/register.html', {'form': form})

    return render(request, 'accounts/register.html', {'form': UserSignUpForm()})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('ophtalmo_center_index')
    else:
        return render(request, 'accounts/account_activation_invalid.html')

def login_user(request):
    if request.method == "POST":
        if "Connexion" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")  
            user = authenticate(request,email=email, password=password)
            if user:
                login(request, user)
                return redirect('ophtalmo_center_index')
            else:
                return render(request, 'accounts/error_login.html')
        else:
            return redirect('/login/password_reset')
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('ophtalmo_center_index')

def password_reset(request):
    msg = ''
    if request.method == "POST":
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            qs = NewUser.objects.filter(email=email)
            site = get_current_site(request)

            if len(qs) > 0:
                user = qs[0]
                user.is_active = False  # User needs to be inactive for the reset password duration
                user.profile.reset_password = True
                user.save()

                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                message = Mail(
                    from_email='jutardpierre@gmail.com',
                    to_emails=email,
                    subject='Reset password for domain.com',
                    html_content=message)
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                except Exception as e:
                    print(e)

            messages.add_message(request, messages.SUCCESS, 'Email {0} submitted.'.format(email))
            msg = 'If this mail address is known to us, an email will be sent to your account.'
            return render(request, 'accounts/password_reset_done.html')
        else:
            messages.add_message(request, messages.WARNING, 'Email not submitted.')
            return render(request, 'accounts/password_reset.html', {'form': form})
    return render(request, 'accounts/password_reset.html', {'form': UserForgotPasswordForm, 'msg': msg})

def reset(request, uidb64, token):

    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = UserPasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                user.is_active = True
                user.profile.reset_password = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return render(request, 'accounts/password_reset_success.html')
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Password could not be reset.')
                return render(request, 'accounts/password_reset_confirm.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
            messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': UserPasswordResetForm(user),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
        messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    return redirect('ophtalmo_center_index')