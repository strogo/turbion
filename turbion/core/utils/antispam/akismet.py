from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.urls.defaults import patterns, url

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

def get_comment_data(comment, parent):
    return {
        'permalink': '%s%s' % (site_url, parent.get_absolute_url()),
        'comment_type': 'comment',
        'comment_author': comment.created_by.name,
        'comment_author_email': comment.created_by.email,
        'comment_author_url': comment.created_by.site or comment.created_by.openid,
        'comment_content': comment.text,
    }

def get_feedback_data(feedback, parent=None):
    return {
        'permalink': _,
        'comment_type': 'feedback',
        'comment_author': feedback.created_by.name,
        'comment_author_email': feedback.created_by.email,
        'comment_author_url': feedback.created_by.site or feedback.created_by.openid,
        'comment_content': feedback.text,
    }

model_map = {
    Comment: get_comment_data,
    Feedback: get_feedback_data,
}

def process_form_submit(request, form, child, parent=None):
    model = child.__class__

    if model in model_map:
        data = model_map[model](child, parent)
        data.update({
            'blog': site_url,
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

def submit_spam(request, ct, pk):
    pass

def submit_ham(request, ct, pk):
    pass

urlpatters = patterns(
    url('submit_spam', submit_spam, name='akismet_submit_spam'),
    url('submit_ham', submit_ham, name='akismet_submit_ham'),
)
