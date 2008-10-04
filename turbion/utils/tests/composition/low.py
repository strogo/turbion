# -*- coding: utf-8 -*-
from django.test import TestCase

from turbion.utils.tests.composition.generic import *

from turbion.utils.tests.composition.models import Movie, Visit, Person, Event,\
                                                  Post, Comment

class LowEventTest(GenericEventTest, TestCase):
    event_model = Event
    visit_model = Visit

class LowMovieTest(GenericMovieTest, TestCase):
    movie_test = Movie
    person_test = Person

class LowPostTest(GenericPostTest, TestCase):
    post_model = Post
    comment_model = Comment
