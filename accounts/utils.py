import random
from django.core.mail import send_mail

def send_reset_code(email):
    # Generate a random 6-digit code
    reset_code = random.randint(100000, 999999)

    # You should implement email sending logic here
    send_mail(
        'Password Reset Code',
        f'Your password reset code is: {reset_code}',
        'from@example.com',  # You need to replace this with the sender email
        [email],
        fail_silently=False,
    )

    return reset_code
