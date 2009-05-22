from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django import forms, http
from django.utils.http import urlencode

from turbion.core.utils.urlfetch import fetch

"""
API specifications:
 - http://akismet.com/development/api/
 - http://antispam.typepad.com/info/developers.html
"""

site = Site.objects.get_current()
site_url = 'http://%s' % site.domain

def get_antispam_data(self):
    return {
        'permalink': reverse('turbion_feedback'),
        'comment_type': 'feedback',
        'comment_author': self.created_by.name,
        'comment_author_email': self.created_by.email,
        'comment_author_url': self.created_by.site or self.created_by.openid,
        'comment_content': self.text,
        'user_ip': self.created_by.ip,
    }

def get_data(obj, *args, **kwargs):
    data = obj.get_antispam_data()
    data.update({
        'blog': site_url,
        'permalink': site_url + data['permalink']
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
                return 'spam:akismet'

    return 'unknown'

def _make_request(method, data, method_map=settings.TURBION_AKISMET_API_METHODS,
                  key=settings.TURBION_AKISMET_API_KEY):
    result = fetch(
        method_map[method] % {'api-key': key},
        data,
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
        },
        timeout=5,
    )
    return result

def action_submit(action, obj):
    data = get_data(obj)

    return _make_request('submit-%s' % action, data)
