# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.utils.translation import ugettext_lazy as _
from django.dispatch import dispatcher

from pantheon.utils.decorators import *
from pantheon.utils.views import info_page

from turbion.feedback.forms import FeedbackForm
from turbion.feedback.models import Feedback
from turbion.feedback import signals
from turbion.blogs.decorators import blog_view

@render_to( "feedback/index.html" )
@title_bits( page=_(u"Write"), section=_(u"Feedback") )
@blog_view
def index( request, blog ):
    if request.method == 'POST':
        feedback_form = FeedbackForm( request.POST )
        if feedback_form.is_valid():
            feedback = feedback_form.save( False )
            feedback.blog = blog
            feedback.ip = request.META.get( "REMOTE_ADDR", "0.0.0.0" )
            feedback.save()

            dispatcher.send( signals.feedback_added,
                             sender = Feedback,
                             instance = feedback )

            return info_page( request,
                              title=_(u"Thanks"),
                              section= _(u"Feedback"),
                              next = "/",
                              message= _( u"Thanks. Your request will be handled by the administrator." ),
                              template="info_page.html" )
    else:
        initial = {}
        if request.user.is_authenticated():
            initial[ 'name' ] = request.user.username
            initial[ 'e_mail' ] = request.user.email

        feedback_form = FeedbackForm( initial = initial )
    feedback_action = './'

    return { "feedback_action" : feedback_action,
             "feedback_form": feedback_form,
             "blog" : blog }
