# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
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
                                from_email="%s <%s>" % (self.site, settings.EMAIL_HOST_USER),
                                body=body
                        )

class RegistrationConfirmMessage(Mail):
    subject = _('Registration on %(site)s')
    template = 'turbion/registration/messages/confirm_mail.html'

class RestorePasswordRequestMessage(Mail):
    subject = _('Password restore request on %(site)s')
    template = "turbion/registration/messages/restore_password_request.html"

class RestorePasswordMessage(Mail):
    subject = _('New password on %(site)s')
    template = "turbion/registration/messages/restore_password.html"

class ChangeEmailMessage(Mail):
    subject = _('Email confirm on %(site)s')
    template = "turbion/registration/messages/change_email.html"
