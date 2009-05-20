from django.conf import settings

from turbion.core.utils import loading
from turbion.core.profiles import get_profile

decisions = set(['spam', 'ham', 'unknown'])

filters = []

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
        filters.append(mod)
    else:
        raise ValueError("Cannot load filter '%s'" % filter_name)

def process_form_init(request, form, parent=None):
    for filter in filters:
        if hasattr(filter, 'process_form_init'):
            filter.process_form_init(request, form, parent)

def process_form_submit(request, form, child, parent=None):
    decision = 'unknown'
    for filter in filters:
        if not hasattr(filter, 'process_form_submit'):
            continue
        decision = filter.process_form_submit(request, form, child, parent)

        if isinstance(decision, tuple):
            decision, need_break = decision
        else:
            need_break = False

        if decision not in decisions:
            decision = 'unknown'

        if decision == 'spam' or need_break:
            break
    return decision

class AntispamModel(object):
    def get_antispam_data(self):
        raise NotImplementedError

    def get_antispam_status(self):
        raise NotImplementedError

    def get_antispam_action(self):
        raise NotImplementedError

    def set_antispam_status(self, action):
        raise NotImplementedError
