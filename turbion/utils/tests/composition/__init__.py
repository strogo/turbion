# -*- coding: utf-8 -*-
from django.test import TestCase


from turbion.utils.tests.composition.models import Event
from turbion.utils.tests.composition.low import *
from turbion.utils.tests.composition.high import *

class CompositionFieldTest(TestCase):
    def test_model_attribute_exist(self):
        self.assert_(hasattr(Event._meta.get_field("visit_count"), "_composition_meta"), "Field`s composition meta does not exist")

        self.assert_(hasattr(Event, "sync_visit_count"), "Update method does not exist")
        self.assert_(hasattr(Event, "freeze_visit_count"), "Freeze method does not exist")
