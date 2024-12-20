import random
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from datetime import timedelta

def send_reset_code(email):
    # Generate a random 6-digit code
    reset_code = random.randint(100000, 999999)

    # Store the reset code in cache for 10 minutes
    cache.set(f'password_reset_code_{email}', reset_code, timeout=600)

    # Send the reset code via email
    send_mail(
        'Password Reset Code',
        f'Your password reset code is: {reset_code}',
        settings.DEFAULT_FROM_EMAIL,  # Using Django's default email sender
        [email],
        fail_silently=False,
    )

    return reset_code
