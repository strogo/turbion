# Trying to find user in OpenID whitelist

from turbion.contrib.openid.whitelist.models import Identity

def process_form_submit(request, form, child, parent=None):
    if child.created_by.openid\
        and Identity.objects.filter(openid=child.created_by.openid).count() > 0:
            return 'ham', True
    return 'unknown'
