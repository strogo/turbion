# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

class FeedbackPageTest( TestCase ):
    def test_submit_feedback(self):
        response = self.client.get( reverse( "feedback" ) )
        self.assertEqual( response.status_code, 200 )

        USERNAME = "daevaorn"

        data = {}
        data[ "subject"] = "Test subject"
        data[ "name"]    = USERNAME
        data[ "e_mail" ] = "foobar@bar.com"
        data[ "text" ]   = "some feedback"

        #registering user
        response = self.client.post(reverse( "feedback" ), data = data )
        self.assertEqual( response.status_code, 200 )

        self.assertEqual( len( mail.outbox ), 1 )
