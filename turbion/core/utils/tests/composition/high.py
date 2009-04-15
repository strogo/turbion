from django.test import TestCase

from turbion.core.utils.tests.composition.generic import *

from turbion.core.utils.tests.composition.models import HLMovie#, HLPost, HLComment

class HighMovieTest(GenericMovieTest, TestCase):
    movie_model = HLMovie

    def test_movie_director_name(self):
        self.renew_object("movie")
        self.assertEqual(
                        self.movie.director_name,
                        "George Lucas"
                    )

        self.assertEqual(
                        self.movie.director_country,
                        "USA"
                    )

        self.person.name = "George W. Lucas"
        self.person.save()

        self.person.country.name = "United States"
        self.person.country.save()

        self.renew_object("movie")
        self.assertEqual(
                        self.movie.director_name,
                        "George W. Lucas"
                    )
        self.assertEqual(
                        self.movie.director_country,
                        "United States"
                    )
"""
class HighPostTest(GenericPostTest, TestCase):
    post_model = HLPost
    comment_model = HLComment
"""
