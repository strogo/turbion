# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf import settings

from turbion.comments.models import Comment

from dxapian.backend.xap import XapianIndexer

indexer = XapianIndexer( model = Comment,
                         fields = ( "text",
                                  ),
                         attributes = { "author" : "author",  },
                         )