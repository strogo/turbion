from django import http, forms
from django.views.decorators.http import require_POST
from django.utils.encoding import force_unicode

from turbion.bits.markup.filters import Filter

class PreviewForm(forms.Form):
    filter = forms.CharField(required=True)
    text = forms.CharField()

    def clean_filter(self):
        filter = self.cleaned_data['filter']

        if filter not in set([name for name, _ in Filter.manager.all()]):
            raise forms.ValidationError('Unkown filter `%s`' % filter)

        return filter

    def render(self):
        filter = Filter.manager.get(self.cleaned_data['filter'])

        return filter.to_html(self.cleaned_data['text'])

@require_POST
def preview(request):
    form = PreviewForm(request.POST)

    if form.is_valid():
        return http.HttpResponse(form.render())

    return http.HttpReponseBadRequest(force_unicode(form.errors))
