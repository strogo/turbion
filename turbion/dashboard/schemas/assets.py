# -*- coding: utf-8 -*-
from turbion.dashboard.schemas import Schema

from turbion.assets.models import Asset

class AssetsSchema(Schema):
    name = "asset"
    model = Asset
    fields = ['id', 'name', 'type', 'get_file_url', 'created_on']

    def get_query_set(self):
        return Asset.objects.for_object(self.blog)
