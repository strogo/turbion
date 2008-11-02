# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django import http, forms

from turbion.profiles.models import Profile
from turbion.notifications.models import Event
from turbion.notifications.eventdescriptor import EventSpot
from turbion.utils.views import status_redirect
from turbion.utils.descriptor import to_object

class UnsubscribeForm(forms.Form):
    connection_dscr = forms.CharField(required=True)
    connection_id = forms.IntegerField(required=True)
    code = forms.CharField(required=True)

    def __init__(self, event_descriptor, user, *args, **kwargs):
        self.user = user
        self.event_descriptor = event_descriptor
        super(UnsubscribeForm, self).__init__(*args, **kwargs)

    def clean_connection_dscr(self):
        connection_dscr = self.cleaned_data["connection_dscr"]

        return to_object(connection_dscr)

    def clean_code(self):
        code = self.cleaned_data["code"]

        hash = self.event_descriptor.get_user_hash(self.user)

        if hash != code:
            raise forms.ValidationError("Wrong code")

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

    desc = event.descriptor.instance

    form = UnsubscribeForm(data=request.GET, user=user, event_descriptor=desc)

    if form.is_valid():
        connection = form.cleaned_data["connection"]

        desc.unsubscribe(user, connection)

        return status_redirect(
                    request,
                    title=u"Отписка",
                    section=u"Оповещения",
                    message=u'Вы отписаны от уведомлений в теме "%s"' % desc.name,
                    next="/"
            )
    raise http.Http404
