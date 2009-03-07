# -*- coding: utf-8 -*-
from django.dispatch import Signal

pingback_recieved = Signal()
send_pingback = Signal()

trackback_recieved = Signal()
send_trackback = Signal()
