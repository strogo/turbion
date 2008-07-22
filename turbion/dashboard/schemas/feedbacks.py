# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from turbion.dashboard.schemas import Schema

from turbion.feedback.models import Feedback

class FeedbackSchema(Schema):
    name = "feedback"
    model = Feedback
    fields = ['id', 'status', 'subject', 'created_on', 'created_by',]

    def get_query_set(self):
        return Feedback.objects.filter(blog=self.blog)