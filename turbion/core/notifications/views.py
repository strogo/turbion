from django.shortcuts import get_object_or_404
from django import http, forms
from django.utils.translation import ugettext_lazy as _

from turbion.core.profiles.models import Profile
from turbion.core.notifications.models import Event
from turbion.core.notifications.event import EventSpot
from turbion.core.utils.views import status_redirect
from turbion.core.utils.descriptor import to_object

class UnsubscribeForm(forms.Form):
    connection_dscr = forms.CharField(required=True)
    connection_id = forms.IntegerField(required=True)
    code = forms.CharField(required=True)

    def __init__(self, manager, user, *args, **kwargs):
        self.user = user
        self.manager = manager
        super(UnsubscribeForm, self).__init__(*args, **kwargs)

    def clean_connection_dscr(self):
        connection_dscr = self.cleaned_data["connection_dscr"]

        return to_object(connection_dscr)

    def clean_code(self):
        code = self.cleaned_data["code"]

        hash = self.manager.get_user_hash(self.user)

        if hash != code:
            raise forms.ValidationError(_("Wrong code"))

        return code

    def clean(self):
        data = self.cleaned_data

        connection_dscr = data["connection_dscr"]
        connection_id = data["connection_id"]

        data["connection"] = connection_dscr._default_manager.get(pk=connection_id)

        return data

def unsubscribe(request, user_id, event_id):
    user  = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)

    manager = event.descriptor.manager

    form = UnsubscribeForm(
        data=request.GET,
        user=user,
        manager=manager
    )

    if not form.is_valid():
        return http.HttpResponseBadRequest("Incorrect request params")

    connection = form.cleaned_data["connection"]

    manager.unsubscribe(user, connection)

    return status_redirect(
                request,
                title=_("Unsubscribe"),
                section=_("Notifications"),
                message=_("You've been unsubscribed from \"%s\"") % event.descriptor.meta.name,
                next="/"
        )
