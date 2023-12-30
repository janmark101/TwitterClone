from django.core.mail import send_mail
from django.conf import settings
from .models import User
import random

def send_verify_email(email):
    subcject = 'DjangoProjectJanMarkowicz'
    email_from = settings.EMAIL_HOST_USER
    code = random.randint(100000, 999999)
    message = f'Your code to verify is : {code}'
    send_mail(subcject,message,email_from,[email])
    user = User.objects.get(email=email)
    user.verify_code = code
    user.save()