# -*- coding: utf-8 -*-
from django.test import TestCase

from turbion.utils.tests.composition.generic import *

from turbion.utils.tests.composition.models import HLMovie, HLVisit, HLPerson,\
                                                   HLEvent, HLPost, HlComment

class HighEventTest(GenericEventTest, TestCase):
    event_model = HLEvent
    visit_model = HLVisit

class HighMovieTest(GenericMovieTest, TestCase):
    movie_test = HLMovie
    person_test = HLPerson

class HighPostTest(GenericPostTest, TestCase):
    post_model = HLPost
    comment_model = HLComment
