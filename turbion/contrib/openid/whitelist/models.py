from django.db import models

class Source(models.Model):
    url = models.URLField()

    def __unicode__(self):
        return self.url

class Identity(models.Model):
    source = models.ForeignKey(Source)
    openid = models.CharField(max_length=200, db_index=True)

    def __unicode__(self):
        return self.openid
