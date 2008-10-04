# -*- coding: utf-8 -*-

class GenericEventTest(object):
    def test_event(self):
        event = self.event_model.objects.create()

        for i in range(5):
            self.visit_model.objects.create(event=event)

        event = self.event_model.objects.get(pk=event._get_pk_val())
        self.assertEqual(event.visit_count, 5)

        event.visit_count = 0
        event.save()

        event.sync_visit_count()

        event = self.event_model.objects.get(pk=event._get_pk_val())
        self.assertEqual(event.visit_count, 5)

class GenericMovieTest(object):
    def test_movie(self):
        person = self.person_model.objects.create(name="George Lucas")

        movie = self.movie_model(title="Star Wars Episode IV: A New Hope", director=person)
        movie.save()
        movie.update_headline()

        movie = self.movie_model.objects.get(pk=movie._get_pk_val())
        self.assertEqual(
                        movie.headline,
                        "Star Wars Episode IV: A New Hope, by George Lucas"
                    )

        person.name = "George W. Lucas"
        person.save()

        movie = self.movie_model.objects.get(pk=movie._get_pk_val())
        self.assertEqual(
                        movie.headline,
                        "Star Wars Episode IV: A New Hope, by George W. Lucas"
                    )

class GenericPostTest(object):
    def test_post(self):
        post = self.post_model.objects.create()

        for i in range(5):
            self.comment_model.objects.create(post=post)

        post = self.post_model.objects.get(pk=post._get_pk_val())
        self.assertEqual(post.comment_count, 5)

        post.comment_count = 0
        post.save()

        post.update_comment_count()

        post = self.post_model.objects.get(pk=post._get_pk_val())
        self.assertEqual(post.comment_count, 5)
