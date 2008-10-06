# -*- coding: utf-8 -*-
from django.test import TestCase

from turbion.utils.tests.composition.generic import *

from turbion.utils.tests.composition.models import HLMovie, HLPerson,\
                                                   HLPost, HLComment

class HighMovieTest(GenericMovieTest, TestCase):
    movie_model = HLMovie
    person_model = HLPerson

    def test_movie_director_name(self):
        person = self.person_model.objects.create(name="George Lucas")
        
        movie = self.movie_model(title="Star Wars Episode IV: A New Hope", director=person)
        movie.save()
        #person.save()
        movie.update_director_name()

        movie = self.renew_object(movie)
        self.assertEqual(
                        movie.director_name,
                        "George Lucas"
                    )

        person.name = "George W. Lucas"
        person.save()

        movie = self.renew_object(movie)
        self.assertEqual(
                        movie.director_name,
                        "George W. Lucas"
                    )


class HighPostTest(GenericPostTest, TestCase):
    post_model = HLPost
    comment_model = HLComment
