from django.conf import settings

from turbion.core.utils import loading, spot
from turbion.core.profiles import get_profile

decisions = set(['spam', 'ham', 'unknown'])

urlpatterns = []

class AntispamModel(object):
    def get_antispam_data(self):
        raise NotImplementedError

    def get_antispam_status(self):
        raise NotImplementedError

    def set_antispam_status(self, action):
        raise NotImplementedError

class BaseFilter(object):
    def process_form_init(self, request, form, parent=None):
        raise NotImplementedError
    
    def process_form_submit(self, request, form, child, parent=None):
        raise NotImplementedError
        
    def action_submit(self, action, obj):
        raise NotImplementedError

class FilterManager(spot.SpotManager):
    def load(self):
        for filter_name in settings.TURBION_ANTISPAM_FILTERS:
            mod = None
            try:
                mod = loading.get_module('turbion.core.utils.antispam.filters', filter_name)
            except loading.NoModuleError:
                if '.' in filter_name:
                    try:
                        mod = loading.get_module(filter_name.rsplit('.', 1))
                    except loading.NoModuleError:
                        pass
            if mod:
                if hasattr(mod, 'urlpatterns'):
                    urlpatterns.extend(mod.urlpatterns)
            else:
                raise ValueError("Cannot load filter '%s'" % filter_name)

Filter = spot.create(BaseFilter, manager=FilterManager, cache=False)

def process_form_init(request, form, parent=None):
    for name, filter in Filter.manager.all():
        try:
            filter.process_form_init(request, form, parent)
        except NotImplementedError:
            pass

def process_form_submit(request, form, child, parent=None):
    decision = 'unknown'
    for name, filter in Filter.manager.all():
        try:
            decision = filter.process_form_submit(request, form, child, parent)

            if decision:
                break
        except NotImplementedError:
            pass
    return decision

def action_submit(action, obj):
    for name, filter in Filter.manager.all():
        try:
            if filter.action_submit(action, obj):
                return
        except NotImplementedError:
            pass

