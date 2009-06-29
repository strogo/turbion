from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django import forms, http
from django.utils.http import urlencode

from turbion.bits.antispam import Filter
from turbion.bits.utils.urlfetch import fetch

site = Site.objects.get_current()
site_url = 'http://%s' % site.domain

class Akismet(Filter):
    """
    Akismet filter. API docs: http://akismet.com/development/api/
    """
    method_map = {
        'verify-key': 'http://%(domain)s/1.1/verify-key',
        'comment-check': 'http://%(api-key)s.%(domain)s/1.1/comment-check',
        'submit-spam': 'http://%(api-key)s.%(domain)s/1.1/submit-spam',
        'submit-ham': 'http://%(api-key)s.%(domain)s/1.1/submit-ham'
    }
    domain = 'rest.akismet.com'
    key = settings.TURBION_AKISMET_API_KEY
        
    # filter functions
    
    def process_form_submit(self, request, form, child, parent=None):
        data = self._get_data(child)

        if data:
            data.update({
                'user_ip': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'referrer': request.META.get('HTTP_REFERER'),
            })
            response = self._make_request('comment-check', data)

            if response.status_code == '200':
                if response.content == 'true':
                    return self._get_spam_status()

        return None

    def action_submit(self, status, obj):
        data = self._get_data(obj)

        if status.startswith('spam'):
            self._make_request('submit-ham', data)
            if self._get_spam_status():
                return True
        elif status == 'ham':
            self._make_request('submit-spam', data)

    # helpers

    def _make_request(self, method, data):
        result = fetch(
            self.method_map[method] % {'api-key': self.key, 'domain': self.domain},
            data,
            headers={
                'Content-type': 'application/x-www-form-urlencoded',
            },
            timeout=5,
        )
        return result

    def _get_data(self, obj, *args, **kwargs):
        data = obj.get_antispam_data()
        data.update({
            'blog': site_url,
            'permalink': site_url + data['permalink']
        })
        return data
        
    def _get_spam_status(self):
        return 'spam:%s' % self.name

