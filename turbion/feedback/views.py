# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from turbion.utils.decorators import templated, titled
from pantheon.utils.views import info_page

from turbion.feedback.forms import FeedbackForm
from turbion.feedback.models import Feedback
from turbion.feedback import signals
from turbion.blogs.decorators import blog_view

@templated( "turbion/feedback/index.html" )
@titled( page=_(u"Write"), section=_(u"Feedback") )
@blog_view
def index( request, blog ):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request=request, blog=blog, data=request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save( False )
            feedback.blog = blog
            feedback.save()

            signals.feedback_added.send(
                             sender=Feedback,
                             instance=feedback
                    )

            return info_page( request,
                              title=_(u"Thanks"),
                              section= _(u"Feedback"),
                              next = "/",
                              message= _( u"Thanks. Your request will be handled by the administrator." ),
                              template="info_page.html" )
    else:
        feedback_form = FeedbackForm(request=request, blog=blog)

    return { "feedback_form": feedback_form,
             "blog" : blog }
