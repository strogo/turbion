# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from pantheon.supernovaforms.captcha import manager

from turbion.registration.models import Code

USERNAME = "daevaorn"
PASSWORD = "pocha"
EMAIL    = "foobar@bar.com"

def make_reg_data( ):
    # cm = CaptchaManager()
    #key = cm.get_solution( form[ "captcha" ].field.widget.get_id() )

    data = {}
    data[ "username"] = USERNAME
    data[ "email" ] = EMAIL
    data[ "password" ] = PASSWORD
    data[ "password_confirm" ] = PASSWORD
    #data[ "captcha_2" ] = key
    #data[ "captcha_0" ] = form[ "captcha" ].field.widget.get_id()

    return data

class NewUserRegistrationTest( TestCase ):
    def setUp(self):
        pass#prepare()

    def test_registration(self):
        response = self.client.get( reverse( "turbion.registration.views.registration" ) )
        self.assertEqual( response.status_code, 200 )

        data = make_reg_data()

        #registering user
        response = self.client.post(reverse( "turbion.registration.views.registration" ), data = data )
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( len( mail.outbox ), 1 )
        del mail.outbox[0]

        #try find our new user
        user = User.objects.get( username = USERNAME )
        self.assertEqual( user.is_active, False )

        #process confirm
        tu = Code.objects.get( user = user )

        response = self.client.get(reverse( "turbion.registration.views.registration_confirm" ), data = { "code" : tu.code } )
        self.assertEqual( response.status_code, 200 )

        user = User.objects.get( username = USERNAME )
        self.assertEqual( user.is_active, True )

        #try to login
        response = self.client.post( reverse( "turbion.registration.views.login" ), data = { "username" : USERNAME, "password": PASSWORD } )
        self.assertEqual( response.status_code, 302 )
        #self.assertRedirects( response, "/" )

class RegTestBase( object ):
    def setUp(self):
        self.user = User.objects.create_user( USERNAME, EMAIL, PASSWORD )
        self.user.save()

class InactiveUserLoginTest( RegTestBase, TestCase ):
    def setUp(self):
        super( InactiveUserLoginTest, self ).setUp()
        self.user.is_active = False
        self.user.save()

    def test_login(self):
        self.assertEqual( self.client.login( username = USERNAME, password = PASSWORD ), False )

class PasswordRestoreTest( RegTestBase, TestCase ):
    def test_password_restore(self):
        response = self.client.get( reverse( "turbion.registration.views.restore_password_request" ) )
        self.assertEqual( response.status_code, 200 )

        data = {}
        data[ "email" ] = EMAIL
        response = self.client.post( reverse( "turbion.registration.views.restore_password_request" ), data = data )
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( len( mail.outbox ), 1 )
        del mail.outbox[0]

        request = Code.objects.get( user = self.user )
        response = self.client.get( reverse( "turbion.registration.views.restore_password" ), data = { "code" : request.code } )
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( Code.objects.count(), 0 )

class ChangePasswordTest( RegTestBase, TestCase ):
    def test_good_change(self):
        NEW_PASSWORD = "foobar"
        data = { "old_password" : PASSWORD,
                 "password": NEW_PASSWORD,
                 "password_confirm" : NEW_PASSWORD }

        self.assertEqual( self.client.login( username = USERNAME, password = PASSWORD ), True )
        response = self.client.post( reverse( "turbion.registration.views.change_password" ), data = data )
        self.assertEqual( response.status_code, 302 )

    def test_bad_change(self):
        NEW_PASSWORD = "foobar"
        data = { "old_password" : PASSWORD+"12",
                 "password": NEW_PASSWORD,
                 "password_confirm" : NEW_PASSWORD }

        self.assertEqual( self.client.login( username = USERNAME, password = PASSWORD ), True )
        response = self.client.post( reverse( "turbion.registration.views.change_password" ), data = data )
        self.assertFormError( response, "change_password_form", "old_password", [ u"Указан неверный пароль" ] )
        self.assertEqual( response.status_code, 200 )

class ChangeEmailTest( RegTestBase, TestCase ):
    def test_good_change(self):
        data = { "email" : "fuck@the.ass"}

        self.assertEqual( self.client.login( username = USERNAME, password = PASSWORD ), True )
        response = self.client.post(reverse( "turbion.registration.views.change_email" ), data = data )
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( len( mail.outbox ), 1 )
        del mail.outbox[0]

        code = ""
        data = { "code" : code }
        response = self.client.get(reverse( "turbion.registration.views.change_email_confirm" ), data = data )
        self.assertEqual( response.status_code, 200 )

class SameUsernameTest( RegTestBase, TestCase ):
    def test_newuser(self):
        data = make_reg_data()
        response = self.client.post(reverse( "turbion.registration.views.registration" ), data = data )
        self.assertFormError( response, "registration_form", "username", [ u"Пользователь с именем %s уже существует. Выберете другое имя." % USERNAME ] )
        self.assertEqual( response.status_code, 200 )

class SameEmailTest( RegTestBase, TestCase ):
    def test_newuser(self):
        data = make_reg_data()
        response = self.client.post(reverse( "turbion.registration.views.registration" ), data = data )
        self.assertFormError( response, "registration_form", "email", [ u"Данный адрес почты %s уже существует в системе" % EMAIL ] )
        self.assertEqual( response.status_code, 200 )
