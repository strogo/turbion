# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import date

from django.newforms.extras import SelectDateWidget

from pantheon.utils.decorators import templated, paged

from turbion.blogs import forms
from turbion.blogs.decorators import blog_view, login_required, titled

@blog_view
@login_required
@templated( 'turbion/blogs/edit_preference.html' )
@titled( page = u'Редактирование настроек' )
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
