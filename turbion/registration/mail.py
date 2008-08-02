# -*- coding: utf-8 -*-
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

from django.conf import settings
from django.contrib.sites.models import Site

site = "http://" + Site.objects.get_current().domain

class Mail( EmailMessage ):
    def __init__( self, to, context ):
        template = get_template( self.template )
        context = Context( context )
        context.update( { "site" : site,
                          })
        body = template.render( context )

        super( Mail, self ).__init__( to = [to],
                                      subject = self.subject,
                                      from_email = "%s <%s>" % ( site, settings.EMAIL_HOST_USER ),
                                      body = body )

class RegistrationConfirmMessage( Mail ):
    subject = u'Регистрация на сайте %s' % site
    template = 'turbion/registration/messages/confirm_mail.html'

class RestorePasswordRequestMessage( Mail ):
    subject = u'Запрос востановления пароля на сайте %s' % site
    template = "turbion/registration/messages/restore_password_request.html"

class RestorePasswordMessage( Mail ):
    subject = u'Новый пароля на сайте %s' % site
    template = "turbion/registration/messages/restore_password.html"

class ChangeEmailMessage( Mail ):
    subject = u'Подтверждение почтового адреса %s' % site
    template = "turbion/registration/messages/change_email.html"
