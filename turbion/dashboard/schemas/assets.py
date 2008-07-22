# -*- coding: utf-8 -*-
#--------------------------------
#$Date: 2008-07-20 23:05:21 +0400 (Sun, 20 Jul 2008) $
#$Author: daev $
#$Revision: 58 $
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from turbion.dashboard.schemas import Schema

from turbion.assets.models import Asset

class PostsSchame(Schema):
    name = "asset"
    model = Asset
    fields = ['id', 'name', 'type', 'get_file_filename', 'created_on']

    def get_query_set(self):
        return Asset.objects.for_object(self.blog)
