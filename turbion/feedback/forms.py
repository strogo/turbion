# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import forms

from turbion.visitors import forms as visitors_forms
from turbion.feedback.models import Feedback

class _FeedbackForm( forms.ModelForm ):
    class Meta:
        model = Feedback
        fields = ( "subject", "text" )

class FeedbackForm( forms.Form ):
    def __init__(self, request, blog, *args, **kwargs ):
        self.__class__ = visitors_forms.combine_user_form_with( _FeedbackForm,
                                                 user         = request.generic_user,
                                                 raw_user     = request.user,
                                                 visitor_data = visitors_forms.extract_visitor_data( request ),
                                                 user_data    = visitors_forms.extract_user_data( request ),
                                                 field        = "created_by",
                                                 need_captcha = False
                                               )

        self.__class__.__init__( self, *args, **kwargs )
