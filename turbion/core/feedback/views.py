# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.decorators import templated, titled
from turbion.core.utils.views import status_redirect

from turbion.core.feedback.forms import FeedbackForm
from turbion.core.feedback.models import Feedback
from turbion.core.feedback import signals
from turbion.core.blogs.decorators import blog_view

@templated("turbion/feedback/index.html")
@titled(page=_(u"Write"), section=_(u"Feedback"))
@blog_view
def index(request, blog):
    if request.method == 'POST':
        form = FeedbackForm(request=request, blog=blog, data=request.POST)

        if form.is_valid():
            feedback = form.save(False)
            feedback.blog = blog
            feedback.save()

            signals.feedback_added.send(
                            sender=Feedback,
                            instance=feedback
                    )
            
            return status_redirect(
                            request,
                            title=_(u"Thanks"),
                            section=_(u"Feedback"),
                            next="/",
                            message=_(u"Thanks. Your request will be handled by the administrator.")
                        )
    else:
        form = FeedbackForm(request=request, blog=blog)

    return {
        "form": form,
        "blog": blog
    }
