# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import newforms as forms
from django.utils.datastructures import SortedDict

from turbion.blogs.models import Comment
from turbion.visitors import forms as visitors_forms

class _CommentForm( forms.ModelForm ):
    class Meta:
        model = Comment
        fields = ( "text", "notify" )

class CommentForm( forms.Form ):
    def __init__(self, request, *args, **kwargs ):
        self.__class__ = visitors_forms.combine_user_form_with( _CommentForm,
                                                 user         = request.generic_user,
                                                 visitor_data = visitors_forms.extract_visitor_data( request ),
                                                 user_data    = visitors_forms.extract_user_data( request ),
                                                 field        = "created_by",
                                                 need_captcha = True
                                               )

        self.__class__.__init__( self, *args, **kwargs )

    def _clean_notify(self):
        notify = self.cleaned_data[ "notify" ]
        if "email" in self.cleaned_data:
            email = self.cleaned_data[ "email" ]

            if notify and not email:
                raise forms.ValidationError("Для получения уведомлений должен буть указан адрес почты")
        return notify
