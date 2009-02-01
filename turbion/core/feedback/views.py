# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.decorators import templated, titled
from turbion.core.utils.views import status_redirect

from turbion.core.feedback.forms import FeedbackForm
from turbion.core.feedback.models import Feedback
from turbion.core.feedback import signals

@templated("turbion/feedback/index.html")
@titled(page=_(u"Write"), section=_(u"Feedback"))
def index(request):
    if request.method == 'POST':
        form = FeedbackForm(request=request, data=request.POST)

        if form.is_valid():
            feedback = form.save()

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
        form = FeedbackForm(request=request)

    return {
        "form": form
    }
