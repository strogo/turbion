# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.conf import settings
from django.contrib.sites.models import Site

class Mail(EmailMessage):
    @property
    def site(self):
        return "http://" + Site.objects.get_current().domain

    def __init__(self, to, context):
        context = context.copy()

        context.update({
            "site" : self.site,
        })
        body = render_to_string(self.template, context)

        super(Mail, self).__init__(
                                to=[to],
                                subject=self.subject % {"site": self.site},
                                from_email="%s <%s>" % (site, settings.EMAIL_HOST_USER),
                                body=body
                        )

class RegistrationConfirmMessage(Mail):
    subject = u'Регистрация на сайте %(site)s' % site
    template = 'turbion/registration/messages/confirm_mail.html'

class RestorePasswordRequestMessage(Mail):
    subject = u'Запрос востановления пароля на сайте %(site)s'
    template = "turbion/registration/messages/restore_password_request.html"

class RestorePasswordMessage(Mail):
    subject = u'Новый пароля на сайте %(site)s'
    template = "turbion/registration/messages/restore_password.html"

class ChangeEmailMessage(Mail):
    subject = u'Подтверждение почтового адреса %(site)s'
    template = "turbion/registration/messages/change_email.html"
