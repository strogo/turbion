# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.visitors.models import Visitor, User

from pantheon.supernovaforms.fields import CaptchaField

def extract_user_data( request ):
    return { "ip" : request.META.get( "REMOTE_ADDR", "0.0.0.0" ) }

def extract_visitor_data( request ):
    return { "session_key" : request.session.session_key }

def combine_user_form_with( form_class, visitor_data, user_data, user = None, raw_user = None, field = "created_by", need_captcha = True ):
    if ( not user or user.is_guest ) and ( not raw_user or not raw_user.is_authenticated() ):
        class UserForm( form_class, forms.ModelForm ):
            #class Meta:
            #    model = Visitor
            #    exclude = ( "session_key", )
            name  = forms.CharField( required = True, label = _ ( "name" ) )
            email = forms.EmailField( required = False, label = _( "email" ) )
            site  = forms.URLField( required = False, label = _( "site" ) )

            if need_captcha:
                captcha = CaptchaField( required = True, label = _( "check" ) )

            def __init__(self, initial = None, *args, **kwargs ):
                if not initial:
                    initial = {}
                if user:
                    initial.update( user.raw_user.__dict__ )
                super( UserForm, self ).__init__( initial = initial, *args, **kwargs )

            def get_user( self ):
                form_data = dict( [ ( key, value ) for key, value in self.cleaned_data.iteritems()\
                                                    if key in self.fields.keys() ] )
                if not user:
                    session_key = visitor_data[ "session_key" ]
                    try:
                        visitor = Visitor.objects.get( session_key = session_key )
                    except Visitor.DoesNotExist:
                        visitor = Visitor( **visitor_data )

                    visitor.__dict__.update( form_data )
                    visitor.save()

                    return User.objects.get_or_create_for( visitor, defaults = user_data )[ 0 ]

                user.raw_user.__dict__.update( form_data )
                user.raw_user.save()

                return user

            def save( self, commit = True ):
                obj = super( UserForm, self ).save( False )

                user = self.get_user()

                setattr( obj, field, user )
                if commit:
                    obj.save()

                return obj

        return UserForm

    form_save = form_class.save

    def save( self, commit = True ):
        if not user and raw_user.is_authenticated():
            new_user, _ = User.objects.get_or_create_for( raw_user.profile )
        else:
            new_user = user
        obj = form_save( self, commit = False )
        setattr( obj, field, new_user )
        if commit:
            obj.save()

        return obj

    form_class.save = save

    return form_class
