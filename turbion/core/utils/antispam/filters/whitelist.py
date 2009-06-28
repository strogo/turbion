# Trying to find user in OpenID whitelist
from turbion.core.utils.antispam import Filter
from turbion.core.whitelist.models import Identity

class Whitelist(Filter):
    def process_form_submit(self, request, form, child, parent=None):
        if child.created_by.openid\
            and Identity.objects.filter(openid=child.created_by.openid).count() > 0:
                return 'ham'
        return None
