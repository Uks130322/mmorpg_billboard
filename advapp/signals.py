from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from billboard.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .models import Advert, Respond


@receiver(post_save, sender=Respond)
def get_respond(sender, instance, created, **kwargs):
    if created:
        destination = [instance.advert_id.user_id.email]
        title = 'Новый отклик на Ваше объявление!'
        text = f'Пользователь {instance.user_id.username} оставил отклик на Ваше объявление:'

    else:
        destination = [instance.user_id.email]
        title = 'Ваш отклик принят!'
        text = f'Пользователь {instance.advert_id.user_id.username} принял Ваш отклик:'

    send_notification(instance, title, text, destination)


def send_notification(respond, title, text, destination):
    html_content = render_to_string(
        'email.html',
        {
            'title': title,
            'advert': respond.advert_id.title,
            'respond': respond.content,
            'text': text,
            'link': f'{SITE_URL}/advert/{respond.advert_id.id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        from_email=DEFAULT_FROM_EMAIL,
        to=destination
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
