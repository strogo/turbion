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

# filter functions

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

    return None

def action_submit(status, obj):
    data = get_data(obj)

    if status.startswith('spam'):
        _make_request('submit-ham', data)
        if 'spam:akismet':
            return True
    elif status == 'ham':
        _make_request('submit-spam', data)

# helper

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


