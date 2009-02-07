from django.db import models

from turbion.core.utils.models import GenericManager

class PostManager(GenericManager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().select_related("created_by")
