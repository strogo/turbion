from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from turbion.core.utils.models import GenericManager
from turbion.core.blogs.fields import PostCountField

class TagManager(GenericManager):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_("slug"))

    post_count = PostCountField(verbose_name=_("post count"))

    objects = models.Manager()
    active = TagManager(post_count__gt=0)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_blog_tag", (self.slug,))

    def get_feed_url(self):
        return {
            "atom": reverse("turbion_blog_atom", args=("tag/%s" % self.pk,)),
            "rss": reverse("turbion_blog_rss", args=("tag/%s" % self.pk,))
        }

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.core.utils.text import slugify
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)

    class Meta:
        app_label           = "turbion"
        ordering            = ("name", "slug")
        verbose_name        = _("tag")
        verbose_name_plural = _("tags")
        db_table            = "turbion_tag"
