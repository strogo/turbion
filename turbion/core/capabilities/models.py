from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.descriptor import DescriptorField, GenericForeignKey
from turbion.core.profiles.models import Profile

class Capability(models.Model):
    connection_dscr = DescriptorField(null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_dscr", "connection_id")

    user = models.ForeignKey(Profile, related_name="capabilities")

    set = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s.%s" % (self.set, self.name)

    class Meta:
        app_label = "turbion"
        unique_together = ("connection_dscr", "connection_id", "set", "name")

        verbose_name = _("capability")
        verbose_name_plural = _("capabilities")

def grant_capability(profile, cap=None, set=None, instance=None):
    from turbion.core.capabilities import CapabilitySet, sets

    assert(cap is not None or set is not None)

    if cap is not None:
        if not isinstance(cap, (list, tuple)):
            cap = [cap]

        for c in cap:
            set_name = CapabilitySet.extract_name(c)
            sets.get(set_name).grant(profile, cap=c, instance=instance)

    else:
        if not isinstance(set, (list, tuple)):
            set = [set]

        for s in set:
            sets.get(s).grant(profile, instance=instance)

def has_capability(profile, cap=None, set=None, instance=None, all=True):
    import operator
    from turbion.core.capabilities import CapabilitySet, sets

    assert(cap is not None or set is not None)
    res = []

    if cap is not None:
        if not isinstance(cap, (list, tuple)):
            cap = [cap]

        for c in cap:
            set_name = CapabilitySet.extract_name(c)
            res.append(sets.get(set_name).check(profile, cap=c, instance=instance))

    else:
        if not isinstance(set, (list, tuple)):
            set = [set]

        for s in set:
            res.append(sets.get(s).check(profile, instance=instance, all=all))

    op = all and operator.and_ or operator.or_

    return reduce(op, res) == True

Profile.add_to_class("grant_capability", grant_capability)
Profile.add_to_class("has_capability", has_capability)
