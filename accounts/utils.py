from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_activation_email(user):
    subject = 'Activate your account'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'domain': settings.SITE_ID,
        'token': user.activation_token,
    })
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])