# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from datetime import date

from django.newforms.extras import SelectDateWidget

from pantheon.utils.decorators import render_to, paged

from turbion.blogs import forms
from turbion.blogs.decorators import blog_view, login_required, title_bits

@blog_view
@login_required
@title_bits( page = u'Редактирование настроек' )
@render_to( 'blogs/edit_preference.html' )
def edit( request, blog ):
    blogpref_form_action = './'

    if request.POST and 'blog_pref_button' in request.POST:
        blogpref_form = forms.BlogPrefForm( request.POST,
                                            instance = blog )
        if blogpref_form.is_valid():
            blogpref_form.save()
    else:
        blogpref_form = forms.BlogPrefForm( instance = blog )

    return { "blog" : blog,
             "blogpref_form_action" : blogpref_form_action,
             "blogpref_form" : blogpref_form }
