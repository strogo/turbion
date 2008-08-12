# -*- coding: utf-8 -*-
from django.dispatch import Signal

post_add = Signal()
post_edit = Signal()
post_status_change = Signal()
post_delete = Signal()

comment_add = Signal()
comment_edit = Signal()
comment_delete = Signal()