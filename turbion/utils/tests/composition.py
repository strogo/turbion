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
                            on_update=True,
                            on_update_initial=0,
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
                    commit=True, # save field holder after appling of doers
                    update_method_queryset=lambda event: event.visit_set.all(),
                    update_method_name="sync_visit_count"
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
                                field_holder_getter=lambda visit: visit.movie_set.all(),
                                do=lambda movie, _, signal: "%s, by %s" % (movie.title, movie.director.name)
                        ),
                    commit=True
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

    def test_model_update_method(self):
        e = Event()
        e.sync_visit_count()
