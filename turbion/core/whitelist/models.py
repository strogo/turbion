from django.db import models
from django.utils.translation import ugettext_lazy as _

class Source(models.Model):
    url = models.URLField(verify_exists=False, verbose_name=_('url'))

    def __unicode__(self):
        return self.url

    class Meta:
        app_label = 'turbion'
        db_table = 'turbion_whitelist_source'
        verbose_name = _('source')
        verbose_name_plural = _('sources')

class Identity(models.Model):
    source = models.ForeignKey(Source, related_name='identities')
    openid = models.CharField(max_length=250, db_index=True)

    def __unicode__(self):
        return u'%s: %s' % (self.source, self.openid)

    class Meta:
        app_label = 'turbion'
        db_table = 'turbion_whitelist_identity'
