from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token as default_token_generator


def send__activation_mail(user, use_https=False):
    subject_template_name = 'users/registration/my_account_activation_subject.txt'
    email_template_name = 'users/registration/my_account_activation_email.html'
    from_email = "activation@smdonline.net"
    to_email = user.email
    html_email_template_name = None
    current_site = Site.objects.get_current()
    context = {
        "email": user.email,
        "domain": current_site.domain,
        "site_name": current_site.name,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": default_token_generator.make_token(user),
        "protocol": "https" if use_https else "http",
        "port": ":8000" if settings.DEBUG else ""
    }
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

    email_message.attach_alternative(body, "text/html")
    email_message.send()
