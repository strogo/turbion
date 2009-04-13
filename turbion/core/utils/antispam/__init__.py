from django.conf import settings

from turbion.core.utils import loading
from turbion.core.profiles import get_profile

decisions = ['spam', 'ham', 'unknown']

filters = []
urlpatterns = []

for filter_name in settings.TURBION_ANTISPAM_FILTERS:
    mod = None
    try:
        mod = loading.get_module('turbion.core.utils.antispam' , filter_name)
    except loading.NoModuleError:
        if '.' in filter_name:
            try:
                mod = loading.get_module(filter_name.rsplit('.', 1))
            except loading.NoModuleError:
                pass
    if mod:
        if hasattr(mod, 'urlpatterns'):
            urlpatterns.extend(mod.urlpatterns)
        filters.append(mod)
    else:
        raise ValueError("Cannot load filter '%s'" % filter_name)

def anonymous_only(func):
    def _decorator(request, *args, **kwargs):
        if not get_profile(request).is_confirmed:
            return func(request, *args, **kwargs)
    return _decorator

@anonymous_only
def process_form_init(request, form, parent=None):
    for filter in filters:
        if hasattr(filter, 'process_form_init'):
            filter.process_form_init(request, form, parent)

@anonymous_only
def process_form_submit(request, form, child, parent=None):
    decision = 'unknown'
    for filter in filters:
        if hasattr(filter, 'process_form_submit'):
            decision = filter.process_form_submit(request, form, child, parent)
            if decision == 'spam':
                break
    return decision
