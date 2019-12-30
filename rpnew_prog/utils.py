from django.conf import settings
from django.core.mail import send_mail, get_connection

def send_rp_mail(subject, message, mailto):
    con = get_connection(settings.EMAIL_BACKEND)
    send_mail(
        subject,
        message,
        'no-reply@rifondazionepodistica.it',
        mailto,
        connection = con,
    )
