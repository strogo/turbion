# -*- coding: utf-8 -*-
from django.dispatch import Signal

post_published = Signal(providing_args=["post"])

comment_added = Signal()
comment_edited = Signal()
