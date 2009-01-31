from django.utils.translation import ugettext_lazy as _

from turbion.core.capabilities.models import Capability
from turbion.core.utils.descriptor import to_descriptor

class AlreadyRegistered(Exception):
    pass

class CapabilitySet(object):
    @staticmethod
    def extract_name(cap_name):
        bits = cap_name.split('.')

        return ".".join(bits[:2])

    def __init__(self, name):
        self.name = name

    def get_instance(self, instance):
        return instance

    def _create_connection(self, instance=None):
        if instance:
            instance = self.get_instance(instance)
            return {
                "connection_dscr": to_descriptor(instance.__class__),
                "connection_id": instance.pk
            }
        else:
            return {
                "connection_dscr": None,
                "connection_id": None
            }

    def grant(self, profile, cap=None, instance=None):
        if cap:
            cap = '.'.join(cap.split('.')[2:])
            if cap not in self.defs.keys():
                raise ValueError(cap)
            caps = [cap]
        else:
            caps = self.defs.keys()

        for cap in caps:
            Capability.objects.get_or_create(
                user=profile,
                set=self.name,
                name=cap,
                **self._create_connection(instance)
            )

    def check(self, profile, cap=None, instance=None, all=True):
        if cap:
            cap = '.'.join(cap.split('.')[2:])
            if cap not in self.defs.keys():
                raise ValueError(cap)
            caps = [cap]
        else:
            caps = self.defs.keys()

        res = Capability.objects.filter(
            user=profile,
            set=self.name,
            name__in=caps,
            **self._create_connection(instance)
        ).count()

        return all and res == len(caps) or res > 1

class CapabilitySetManager(object):
    def __init__(self):
        self._sets = {}

    def add(self, name, model, set):
        if name in self._sets:
            raise AlreadyRegistered(name)

        self._sets[name] = (model, set(name))

    def get(self, name):
        return self._sets[name][1]

sets = CapabilitySetManager()

def register(model, capability_set, name=None):
    if name is None:
        name = "%s.%s" % (model._meta.object_name, capability_set.__name__.lower())

    sets.add(name, model, capability_set)

def generate_triple(name, label=None):
    if not label:
        label = name

    actions = [_("add"), _("edit"), _("delete")]

    return [("%s_%s" % (action, name), _("Can %s %s") % (action, label)) for action in actions]
