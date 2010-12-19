from django import template
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from urlparse import urljoin

register = template.Library()

@register.simple_tag
def pingback_gateway(post):
    url = reverse("turbion_pingback_gateway", args=(post.pk,))

    return '<link rel="pingback" href="%s" />' % urljoin("http://" + Site.objects.get_current().domain, url)
