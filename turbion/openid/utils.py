# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from turbion.profiles.models import Profile
from turbion.openid.models import Identity

def get_consumer(session):
    from openid.consumer import consumer
    from turbion.openid.store import DatabaseStore

    return consumer.Consumer(session, DatabaseStore())

def complete(request):
    data = dict(request.GET.items())
    if request.method=="POST":
        data.update(dict(request.POST.items()))

    consumer = get_consumer(request.session)

    trust_url, return_to = get_auth_urls(request)
    response = consumer.complete(data, return_to)

    return consumer, response

def complete_sreg(response):
    from openid.extensions import sreg
    return sreg.SRegResponse.fromSuccessResponse(response)

def get_auth_urls(request):
    site_url =  "http://%s" % Site.objects.get_current().domain
    trust_url = getattr(settings, "TURBION_OPENID_TRUST_URL", (site_url + '/'))
    return_to = site_url + reverse('openid_authenticate')

    return trust_url, return_to

def create_user(username, email, response):
    user = Profile.objects.create_user(
                                    username.lower(),
                                    email,
                                    Profile.objects.make_random_password()
                                )
    user.nickname = user.username
    user.save()

    connection = Identity.objects.create(
                        user=user,
                        url=response.identity_url
                    )
    return connection
