# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.db.models import signals

from turbion.utils.composition import CompositionField

D = dict

class Visit(models.Model):
    event = models.ForeignKey("Event")

    class Meta:
        app_label="utils"

class Event(models.Model):
    visit_count=CompositionField(
                    native=models.IntegerField(default=0),
                    trigger=[
                        D(
                            on=signals.post_save,
                            do=lambda event, visit, signal: event.visit_count + 1
                        ),
                        D(
                            on=signals.post_delete,
                            do=lambda event, visit, signal: event.visit_count - 1
                        )
                    ],
                    commons=D(
                        sender_model="utils.Visit",
                        field_holder_getter=lambda visit: visit.event,
                    ),
                    commit=True,
                    update_method=D(
                        do=0,
                        initial=0,
                        queryset=lambda event: event.visit_set.all(),
                        name="sync_visit_count"
                    )
                )

    class Meta:
        app_label="utils"

class Person(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        app_label="utils"

class Movie(models.Model):
    title = models.CharField(max_length=250)
    director = models.ForeignKey(Person)

    headline=CompositionField(
                    native=models.CharField(max_length=250),
                    trigger=D(
                                sender_model=Person,
                                field_holder_getter=lambda director: director.movie_set.all(),
                                do=lambda movie, _, signal: "%s, by %s" % (movie.title, movie.director.name)
                    )
            )

    class Meta:
        app_label="utils"

class Comment(models.Model):
    post = models.ForeignKey("Post")

    class Meta:
        app_label="utils"

class Post(models.Model):
    comment_count=CompositionField(
                    native=models.IntegerField(default=0),
                    trigger=D(
                            on=(signals.post_save, signals.post_delete),
                            do=lambda post, comment, signal: post.comment_set.count()
                        ),
                    commons=D(
                        sender_model=Comment,
                        field_holder_getter=lambda comment: comment.post,
                    )
                )

    class Meta:
        app_label="utils"

class CompositionFieldTest(TestCase):
    def test_model_field_meta_exists(self):
        self.assert_(hasattr(Event._meta.get_field("visit_count"), "_composition_meta"), "Field`s composition meta does not exist")

    def test_model_update_method_exists(self):
        self.assert_(hasattr(Event, "sync_visit_count"), "Update method does not exist")

    def test_event(self):
        event = Event.objects.create()

        for i in range(5):
            Visit.objects.create(event=event)

        event = Event.objects.get(pk=event._get_pk_val())
        self.assertEqual(event.visit_count, 5)

        event.visit_count = 0
        event.save()

        event.sync_visit_count()

        event = Event.objects.get(pk=event._get_pk_val())
        self.assertEqual(event.visit_count, 5)

    def test_movie(self):
        person = Person.objects.create(name="George Lucas")

        movie = Movie(title="Star Wars Episode IV: A New Hope", director=person)
        movie.save()
        movie.update_headline()

        movie = Movie.objects.get(pk=movie._get_pk_val())
        self.assertEqual(movie.headline, "Star Wars Episode IV: A New Hope, by George Lucas")

        person.name = "George W. Lucas"
        person.save()

        movie = Movie.objects.get(pk=movie._get_pk_val())
        self.assertEqual(movie.headline, "Star Wars Episode IV: A New Hope, by George W. Lucas")

    def test_post(self):
        post = Post.objects.create()

        for i in range(5):
            Comment.objects.create(post=post)

        post = Post.objects.get(pk=post._get_pk_val())
        self.assertEqual(post.comment_count, 5)

        post.comment_count = 0
        post.save()

        post.update_comment_count()

        post = Post.objects.get(pk=post._get_pk_val())
        self.assertEqual(post.comment_count, 5)
