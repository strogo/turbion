from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django import forms, http
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from turbion import get_version
from turbion.core.blogs.models import Comment
from turbion.contrib.feedback.models import Feedback
from turbion.core.utils.urlfetch import fetch

"""
API specifications:
 - http://akismet.com/development/api/
 - http://antispam.typepad.com/info/developers.html
"""

site = Site.objects.get_current()
site_url = 'http://%s' % site.domain

def get_comment_data(comment, parent=None):
    if not parent:
        parent = comment.post

    return {
        'permalink': '%s%s' % (site_url, parent.get_absolute_url()),
        'comment_type': 'comment',
        'comment_author': comment.created_by.name,
        'comment_author_email': comment.created_by.email,
        'comment_author_url': comment.created_by.site or comment.created_by.openid,
        'comment_content': comment.text,
        'user_ip': comment.created_by.ip,
    }

def get_feedback_data(feedback, parent=None):
    return {
        'permalink': '%s%s' % (site_url, reverse('turbion_feedback')),
        'comment_type': 'feedback',
        'comment_author': feedback.created_by.name,
        'comment_author_email': feedback.created_by.email,
        'comment_author_url': feedback.created_by.site or feedback.created_by.openid,
        'comment_content': feedback.text,
        'user_ip': feedback.created_by.ip,
    }

model_map = {
    Comment: get_comment_data,
    Feedback: get_feedback_data,
}

def get_data(obj, *args, **kwargs):
    model = obj.__class__

    if model in model_map:
        data = model_map[model](obj, *args, **kwargs)
        data.update({
            'blog': site_url,
        })
        return data

def process_form_submit(request, form, child, parent=None):
    data = get_data(child)

    if data:
        data.update({
            'user_ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
        })
        response = _make_request('comment-check', data)

        if response.status_code == '200':
            if response.content == 'true':
                return 'spam'
            elif response.content == 'false':
                return 'ham'

    return 'unknown'

def _make_request(method, data, method_map=settings.TURBION_AKISMET_API_METHODS, key=settings.TURBION_AKISMET_API_KEY):
    result = fetch(
        method_map[method] % {'api-key': key},
        data,
        headers={
            'User-Agent': 'Turbion urlfetcher/%s | Antispam' % get_version(),
            'Content-type': 'application/x-www-form-urlencoded',
        },
        timeout=5,
    )
    return result

class ActionForm(forms.Form):
    action = forms.ChoiceField(required=True, choices=[('spam', 'spam'), ('ham', 'ham')], widget=forms.HiddenInput())
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput())
    pk = forms.CharField(widget=forms.HiddenInput())
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    @classmethod
    def for_object(cls, obj, action, next):
        form = cls(
            initial={
                'action': action,
                'content_type': ContentType.objects.get_for_model(obj.__class__).pk,
                'pk': obj.pk,
                'next': next
            }
        )
        form.action_url = reverse('akismet_action')
        return form

def do_action_submit(action, obj):
    data = get_data(obj)

    return _make_request('submit-%s' % action, data)

def submit_action(request):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            ct = form.cleaned_data['content_type']
            obj = ct.get_for_id(form.cleaned_data['pk'])

            response = do_action_submit(form.cleaned_data['action'], obj)

            next = form.cleaned_data['next'] or request.META['HTTP_REFERER']
            next += '?' in next and '&' or '?'

            if response.status_code == '200':
                return http.HttpResponseRedirect(
                    next + urlencode({'result': response.content})
                )

    return http.HttpResponseBadRequest('No action or illegal object')

class ActionModelAdmin(object):
    def get_antispam_url_name(self):
        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.module_name
        return '%sadmin_%s_%s_antispam_action' % info

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urls = super(ActionModelAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(.+)/antispam/$', self.antispam_view, name=self.get_antispam_url_name())
        )
        return my_urls + urls

    def antispam_submit_action(self, request, obj, action):
        response = do_action_submit(action, obj)
        if response.status_code == '200':
            result = response.content

            self.antispam_do_action(action, obj)
            self.message_user(request, u"`%s` successfully marked as %s." % (obj, action))
        else:
            self.message_user(
                request,
                u"`%s` connot be marked %s" % (comment, response.content and u'because %s.' % response.content or '.')
            )

    def antispam_view(self, request, object_id):
        if request.method == 'POST':
            obj = self.model._default_manager.get(pk=object_id)
            action = request.POST.get('action')
            self.antispam_submit_action(request, obj, action)

            return http.HttpResponseRedirect(
                request.META.get('HTTP_REFERER')
            )
        return http.HttpResponseBadRequest('No action or illegal object')

    def antispam(self, obj):
        action = self.antispam_map_action(obj)
        name = action == 'spam' and 'Spam' or 'Ham'

        return """<form action="%s" method="POST">
        <input type="hidden" name="action" value="%s"/>
        <input class="button" type="submit" style="font-size:10px; padding:1px 2px;" value="%s"/>
        </form>""" % (reverse(self.get_antispam_url_name(), args=(obj.pk,)), action, name)
    antispam.allow_tags = True

    def antispam_action_spam(self, request, queryset):
        for obj in queryset:
            self.antispam_submit_action(request, obj, 'spam')
    antispam_action_spam.short_description = _("Mark selected as spam")

urlpatterns = patterns('',
    url('akismet/submit_action', submit_action, name='akismet_action'),
)
