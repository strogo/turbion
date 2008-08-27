# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

#FIXME: repair tests
class ProfilePageTest:#( TestCase ):
    def setUp(self):
        pass

    def test_profile(self):
        response = self.client.get( reverse( "turbion.profiles.views.profile", kwargs = { "profile_user":user.username } ) )
        self.assertEqual( response.status_code, 200 )

    #def test_registration(self):
    def foo(self):
        response = self.client.get( reverse( "turbion.registration.views.registration" ) )
        self.assertEqual( response.status_code, 200 )

        context = None
        for c in response.context:
            if "registration_action" in c:# in c and "captcha" in c["form"]:
                context = c

        form = context[ "form" ]

        cm = CaptchaManager()
        key = cm.get_solution( form[ "captcha" ].field.widget.get_id() )

        USERNAME = "daevaorn"
        PASSWORD = "pocha"

        data = {}
        data[ "username"] = USERNAME
        data[ "email" ] = "foobar@bar.com"
        data[ "password" ] = PASSWORD
        data[ "password_confirm" ] = "pocha"
        data[ "captcha_2" ] = key
        data[ "captcha_0" ] = form[ "captcha" ].field.widget.get_id()

        #registering user
        response = self.client.post(reverse( "turbion.registration.views.registration" ), data = data )
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( len( mail.outbox ), 1 )
        del mail.outbox[0]

        #process confirm
        tu = TempUser.objects.get( username = USERNAME )

        response = self.client.get(reverse( "turbion.registration.views.registration_confirm" ), data = { "code" : tu.code } )
        self.assertEqual( response.status_code, 200 )

        #try to log in
        response = self.client.post( reverse( "turbion.registration.views.login" ), data = { "username" : USERNAME, "password": PASSWORD } )
        self.assertEqual( response.status_code, 302 )
