# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import exceptions
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from turbion.profiles.models import Profile
from turbion.openid import models

def get_consumer(session):
    from openid.consumer import consumer
    from openid.store.filestore import FileOpenIDStore

    if not hasattr( settings, "TURBION_OPENID_STORE_ROOT" ):
        raise exceptions.ImproperlyConfigured('TURBION_OPENID_STORE_ROOT is not set')
    return consumer.Consumer(session, FileOpenIDStore(settings.TURBION_OPENID_STORE_ROOT))

def complete( request ):
    data = request.GET.copy()
    data.update( request.POST )

    consumer = get_consumer( request.session )

    trust_url, return_to = get_auth_urls( request )
    response = consumer.complete( dict( data.items() ), return_to )

    return consumer, response

def complete_sreg( response ):
    from openid.extensions import sreg
    return sreg.SRegResponse.fromSuccessResponse( response )

def get_auth_urls( request ):
    site_url =  "http://%s" % Site.objects.get_current().domain
    trust_url = getattr( settings, "TURBION_OPENID_TRUST_URL", None ) or (site_url + '/')
    return_to = site_url + reverse('openid_authenticate')

    return trust_url, return_to

def create_user( username, email, response ):
    user = Profile.objects.create_user( username,
                                    email,
                                    User.objects.make_random_password()
                                )
    connection = models.Identity.objects.create( user = user, url = response.identity_url )
    return connection
