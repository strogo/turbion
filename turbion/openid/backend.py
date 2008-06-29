# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from turbion.openid import utils
from turbion.openid.models import Identity

def gen_username( identity_url ):
    import md5
    unique = md5.new( identity_url).hexdigest()[:30 - len('opend_')]
    return 'openid_%s' % unique

class OpenidBackend( ModelBackend ):
    def authenticate( self, request ):
        consumer, response = utils.complete(request )

        if response.status != consumer.SUCCESS:
            return None

        sreg_response = utils.complete_sreg( response )

        try:
            connection = Identity.objects.get( openid = response.identity_url )
        except Identity.DoesNotExist:
            username = sreg_response.has_key( "nickname" ) and sreg_response[ "nickname" ] or gen_username()
            email = sreg_response.has_key( "email" ) and sreg_response[ "email" ] or gen_username

            user = User.objects.create_user( username,
                                             email,
                                             User.objects.make_random_password()
                                            )
            connection = Identity.objects.create( user = user, openid = response.identity_url )
        return connection.user
