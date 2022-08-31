from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from cinema.models import Movie
from newsletter.models import SubscribedUser


@receiver(post_save, sender=Movie)
def new_movie_added(sender, instance, created, **kwargs):
    recipients = SubscribedUser.objects.all()
    subject, from_email = 'New movie added', 'office@silverscreen.com'
    email_text = get_template('newsletter/new_movie_email.html')

    for recipient in recipients:

        context = {
            'name': instance.name,
            'user': recipient.id,
        }

        html_content = email_text.render(context)

        msg = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=(recipient.email, )
        )
        msg.send()
