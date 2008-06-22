# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

from django.conf import settings
from django.contrib.sites.models import Site

site = "http://" + Site.objects.get_current().domain


 #def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
#            connection=None, attachments=None, headers=None):

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
    template = 'registration/messages/confirm_mail.html'
        
class RestorePasswordRequestMessage( Mail ):
    subject = u'Запрос востановления пароля на сайте %s' % site
    template = "registration/messages/restore_password_request.html"

class RestorePasswordMessage( Mail ):
    subject = u'Новый пароля на сайте %s' % site
    template = "registration/messages/restore_password.html"
    
class ChangeEmailMessage( Mail ):
    subject = u'Подтверждение почтового адреса %s' % site
    template = "registration/messages/change_email.html"