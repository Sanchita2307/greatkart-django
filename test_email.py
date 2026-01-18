import os
from django.conf import settings
from django.core.mail import send_mail
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
django.setup()

try:
    send_mail(
        'Test Email',
        'This is a test email from Django.',
        settings.DEFAULT_FROM_EMAIL,
        ['sanchitajainjbp23@gmail.com'],  # Replace with your actual email
        fail_silently=False,
    )
    print('Test email sent successfully!')
except Exception as e:
    print(f'Email failed: {e}')