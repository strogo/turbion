# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.db.models import signals

from turbion.utils.composition import CompositionField

D = dict

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
                    commit=True, # save field host after appling of doers
                    update_method_queryset=lambda event: event.visit_set.all(),
                    update_method_name="sync_visit_count"
                )

    class Meta:
        app_label="utils"

class Visit(models.Model):
    date = models.DateField()
    event = models.ForeignKey(Event)

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
                                on=signals.pre_save,
                                do=lambda movie, signal: "%s, by %s" % (movie.title, movie.director.name)
                        )
            )

    class Meta:
        app_label="utils"

    def update_headline(self):
        pass

class CompositionFieldTest(TestCase):
    def test_model_field_meta_exists(self):
        self.assert_(hasattr(Event._meta.get_field("visit_count"), "_composition_meta"), "Field`s composition meta does not exist")

    def test_model_update_method_exists(self):
        self.assert_(hasattr(Event, "sync_visit_count"), "Update method does not exist")

    def test_model_update_method(self):
        e = Event()
        e.sync_visit_count()
