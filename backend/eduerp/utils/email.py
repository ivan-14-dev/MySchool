from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email,username):
    subject = "Bienvenu sur EDUERP"
    message = f"Bonjour M/Mme {username}, \n\n Merci de vous etre inscrit sur EDUERP. \nNous sommes ravis de vous compter parmi nous !"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject,message,from_email,recipient_list)
    return f"Email sent to {user_email}"

@shared_task
def send_password_reset_email(user_email, reset_link):
    subject = "Réinitialisation de votre mot de passe"
    message = f"Bonjour,\n\n Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant : {reset_link} \n\n Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject,message,from_email,recipient_list)
    return f"Email sent to {user_email}"

@shared_task
def send_custom_email(subject, message, recipient_list):
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list)
    return f"Email sent to {', '.join(recipient_list)}"

@shared_task