from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy
from account.models import CustomUser
from account.forms import *
from jobapp.permission import user_is_employee 
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from .tokens import account_activation_token
from django.conf import settings
import logging
import traceback

logger = logging.getLogger(__name__)

def get_success_url(request):
    """
    Handle Success Url After LogIN
    """
    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        return next_url
    return reverse('jobapp:home')



def employee_registration(request):
    """
    Handle Employee Registration
    """
    form = EmployeeRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Email verification
        current_site = get_current_site(request)
        mail_subject = 'Activate your Job Portal account'
        message = render_to_string('emails/account_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        try:
            email = EmailMessage(
                mail_subject,
                message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.content_subtype = "html"  # Make the email HTML
            email.send(fail_silently=False)
            messages.success(request, 'Please check your email to complete registration.')
        except Exception as e:
            messages.error(request, f'Problem sending email: {e}')
            user.delete()  # Delete user if email fails
            return redirect('account:employee-registration')

        return redirect('account:login')

    context = {'form': form}
    return render(request, 'account/employee-registration.html', context)


def employer_registration(request):
    """
    Handle Employee Registration 

    """
    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        try:
            # 1. Save the user
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            logger.info(f"User created successfully: {user.email}")

            # 2. Prepare email data
            current_site = get_current_site(request)
            mail_subject = 'Activate your Job Portal Employer Account'
            
            # 3. Generate activation token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            logger.info(f"Generated activation token for user {user.email}")
            logger.info(f"UID: {uid}")
            logger.info(f"Token: {token}")
            logger.info(f"Domain: {current_site.domain}")

            # 4. Render email template
            try:
                html_message = render_to_string('emails/employer_activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                logger.info("Email template rendered successfully")
            except Exception as template_error:
                logger.error(f"Template rendering error: {str(template_error)}")
                logger.error(traceback.format_exc())
                raise

            # 5. Send email
            try:
                # First try with EmailMessage
                email = EmailMessage(
                    subject=mail_subject,
                    body=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                logger.info(f"Activation email sent successfully to {user.email}")

            except Exception as email_error:
                logger.error(f"EmailMessage failed: {str(email_error)}")
                logger.error(traceback.format_exc())
                
                # Try with send_mail as fallback
                try:
                    send_mail(
                        subject=mail_subject,
                        message='',
                        html_message=html_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Activation email sent successfully using send_mail to {user.email}")
                except Exception as send_mail_error:
                    logger.error(f"send_mail failed: {str(send_mail_error)}")
                    logger.error(traceback.format_exc())
                    raise

            messages.success(request, 'Please check your email to complete registration.')
            return redirect('account:login')

        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            logger.error(traceback.format_exc())
            if 'user' in locals() and user.pk:
                user.delete()
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('account:employer-registration')

    context = {'form': form}
    return render(request, 'account/employer-registration.html', context)

def send_test_email():
    """Test email configuration"""
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employee
def employee_edit_profile(request, id=id):
    """
    Handle Employee Profile Update Functionality
    """
    user = get_object_or_404(CustomUser, id=id)
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={'id': form.id}))
    context={'form':form}
    return render(request,'account/employee-edit-profile.html',context)



def user_logIn(request):
    """
    Provides users to logIn

    """
    if request.user.is_authenticated:
        return redirect('jobapp:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                return redirect('jobapp:home')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        # Send welcome email based on role
        welcome_template = 'emails/employer_welcome.html' if user.role == 'employer' else 'emails/employee_welcome.html'
        mail_subject = f'Welcome to Job Portal - Your {"Employer" if user.role == "employer" else "Employee"} Account is Active'
        message = render_to_string(welcome_template, {'user': user})
        
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()
        
        messages.success(request, 'Thank you for confirming your email. You can now login.')
        return redirect('account:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('account:login')

def test_email(request):
    try:
        send_mail(
            'Test Subject',
            'Test Message',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Error sending email: {str(e)}")

def test_activation_template(request):
    """Test view to check if the activation template renders correctly"""
    from django.contrib.sites.shortcuts import get_current_site
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    
    try:
        # Use the first user in the database for testing
        user = CustomUser.objects.first()
        if not user:
            return HttpResponse("No users in database to test with")
            
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        
        html = render_to_string('emails/employer_activation.html', context)
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error rendering template: {str(e)}")

def test_email_config(request):
    try:
        # Test email configuration
        test_email = EmailMessage(
            subject='Test Email Configuration',
            body='<h1>This is a test email.</h1>',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER]
        )
        test_email.content_subtype = "html"
        test_email.send(fail_silently=False)
        
        # Log configuration details
        logger.info("Email Configuration:")
        logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        logger.info(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        return HttpResponse("""
            <h1>Email Test Successful</h1>
            <p>Test email has been sent. Please check your inbox.</p>
            <p>Check the debug.log file for configuration details.</p>
        """)
    except Exception as e:
        logger.error(f"Email test failed: {str(e)}")
        logger.error(traceback.format_exc())
        return HttpResponse(f"""
            <h1>Email Test Failed</h1>
            <p>Error: {str(e)}</p>
            <p>Check the debug.log file for more details.</p>
        """)