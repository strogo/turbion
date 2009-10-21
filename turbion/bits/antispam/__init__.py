from django.conf import settings
from django.db import models

from turbion.bits.utils import loading, spot
from turbion.bits.profiles import get_profile

class StopChecking(Exception):
    pass

class AntispamModel(models.Model):
    antispam_status = models.CharField(max_length=20, null=True, blank=True,
                                       editable=False)

    def get_antispam_data(self):
        raise NotImplementedError

    def handle_antispam_decision(self, decision):
        raise NotImplementedError

    class Meta:
        abstract = True

class BaseFilter(object):
    def process_form_init(self, request, form, parent=None):
        raise NotImplementedError

    def process_form_submit(self, request, form, child, parent=None):
        """
        Makes decision about child.
        Returns:
            True - spam detected
            False - cannot decide
            raise StopChecking - stop pipeline with not spam decision
        """
        raise NotImplementedError

    def action_submit(self, action, obj):
        raise NotImplementedError

class FilterManager(spot.Manager):
    def load(self):
        for filter_name in settings.TURBION_ANTISPAM_FILTERS:
            mod = None
            try:
                mod = loading.get_module('turbion.bits.antispam.filters', filter_name)
            except loading.NoModuleError:
                if '.' in filter_name:
                    try:
                        mod = loading.get_module(filter_name.rsplit('.', 1))
                    except loading.NoModuleError:
                        pass
            if not mod:
                raise ValueError("Cannot load filter '%s'" % filter_name)

Filter = spot.create(BaseFilter, manager=FilterManager, cache=False)

def process_form_init(request, form, parent=None):
    for name, filter in Filter.manager.all():
        try:
            filter.process_form_init(request, form, parent)
        except NotImplementedError:
            pass

def process_form_submit(request, form, child, parent=None):
    decisions = []
    for name, filter in Filter.manager.all():
        try:
            filter_decision = filter.process_form_submit(request, form, child, parent)

            if filter_decision:
                decisions.append(name)
        except NotImplementedError:
            pass
        except StopChecking:
            break

    child.antispam_status = ', '.join(decisions)
    child.handle_antispam_decision(decisions and 'spam' or 'ham')

    return child.antispam_status

def action_submit(action, obj):
    for name, filter in Filter.manager.all():
        try:
            filter.action_submit(action, obj)
        except NotImplementedError:
            pass
