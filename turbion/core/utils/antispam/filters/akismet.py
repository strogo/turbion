from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django import forms, http
from django.utils.http import urlencode

from turbion.core.utils.antispam import Filter
from turbion.core.utils.urlfetch import fetch

"""
API specifications:
 - http://akismet.com/development/api/
 - http://antispam.typepad.com/info/developers.html
"""

site = Site.objects.get_current()
site_url = 'http://%s' % site.domain

# filter functions
class Akismet(Filter):
    method_map = {
        'verify-key': 'http://rest.akismet.com/1.1/verify-key',
        'comment-check': 'http://%(api-key)s.rest.akismet.com/1.1/comment-check',
        'submit-spam': 'http://%(api-key)s.rest.akismet.com/1.1/submit-spam',
        'submit-ham': 'http://%(api-key)s.rest.akismet.com/1.1/submit-ham'
    }
    key = settings.TURBION_AKISMET_API_KEY

    def get_data(self, obj, *args, **kwargs):
        data = obj.get_antispam_data()
        data.update({
            'blog': site_url,
            'permalink': site_url + data['permalink']
        })
        return data

    def process_form_submit(self, request, form, child, parent=None):
        data = self.get_data(child)

        if data:
            data.update({
                'user_ip': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'referrer': request.META.get('HTTP_REFERER'),
            })
            response = self._make_request('comment-check', data)

            if response.status_code == '200':
                if response.content == 'true':
                    return 'spam:akismet'

        return None

    def action_submit(self, status, obj):
        data = self.get_data(obj)

        if status.startswith('spam'):
            self._make_request('submit-ham', data)
            if 'spam:akismet':
                return True
        elif status == 'ham':
            self._make_request('submit-spam', data)

    # helper

    def _make_request(self, method, data):
        result = fetch(
            self.method_map[method] % {'api-key': self.key},
            data,
            headers={
                'Content-type': 'application/x-www-form-urlencoded',
            },
            timeout=5,
        )
        return result


