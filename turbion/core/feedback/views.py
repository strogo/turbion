from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.decorators import templated, titled
from turbion.core.utils.views import status_redirect

from turbion.core.feedback.forms import FeedbackForm
from turbion.core.feedback.models import Feedback
from turbion.core.feedback import signals
from turbion.core.utils import antispam

@templated("turbion/feedback/index.html")
@titled(page=_(u"Write"), section=_(u"Feedback"))
def index(request):
    if request.method == 'POST':
        form = FeedbackForm(request=request, data=request.POST)
        antispam.process_form_init(request, form)

        if form.is_valid():
            feedback = form.save(False)

            if antispam.process_form_submit(request, form, feedback) == "spam":
                feedback.status = Feedback.statuses.rejected

            feedback.save()

            signals.feedback_added.send(
                sender=Feedback,
                instance=feedback
            )

            response = status_redirect(
                request,
                title=_(u"Thanks"),
                section=_(u"Feedback"),
                next="/",
                message=_(u"Thanks. Your request will be handled by the administrator.")
            )

            if form.need_auth_redirect():
                return form.auth_redirect(
                    response["Location"]
                )
            return response
    else:
        form = FeedbackForm(request=request)
        antispam.process_form_init(request, form)

    return {
        "form": form
    }