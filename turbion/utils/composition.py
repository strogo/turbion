# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import curry

class CompositionMeta(object):
    def __init__(self, model, field, name, trigger, commons,\
                 commit, update_method_queryset, update_method_name):
        self.model = model
        self.name = name
        self.trigger = []

        if not commons:
            commons = {}
        self.commons = commons

        self.commit = commit
        self.update_method_queryset = update_method_queryset

        if not update_method_name:
            update_method_name = "update_%s" % name

        if hasattr(model, update_method_name):
            raise AttributeError("Method with name `%s` already exists in model" % update_method_name)

        setattr(model, update_method_name, lambda instance: self._update_method(instance))

        if not isinstance(trigger, (list, tuple)):
            trigger = [trigger]

        trigger_defaults = dict(
                sender_model=model,
                on=[models.signals.post_save],
                field_holder_getter=lambda instance: instance,
                on_update=False,
                on_update_initial=None
        )
        trigger_defaults.update(commons)

        for t in trigger:
            full_trigger = trigger_defaults.copy()
            full_trigger.update(t)

            if "sender_model" in full_trigger and "sender" not in full_trigger:
                sender_model = full_trigger["sender_model"]
                if isinstance(sender_model, basestring):
                    sender_model = None
                full_trigger["sender"] = sender_model

            if "do" not in full_trigger:
                raise ValueError("`do` action not defined for trigger")

            if not isinstance(full_trigger["on"], (tuple, list)):
                full_trigger["on"] = [full_trigger["on"]]

            for signal in full_trigger["on"]:
                def _handler(instance, **kwargs):
                    obj = full_trigger["field_holder_getter"](instance)

                    setattr(obj, self.name, full_trigger["do"](obj, instance, signal))

                signal.connect(_handler, sender=full_trigger["sender_model"])

            self.trigger.append(full_trigger)

    def _update_method(self, instance):
        if self.update_method_queryset:
            qs_getter = self.update_method_queryset
        else:
            qs_getter = [instance]

        for trigger in self.trigger:
            if trigger["on_update"]:
                setattr(instance, self.name, trigger["on_update_initial"])
                if callable(qs_getter):
                    qs = qs_getter(instance)

                for obj in qs:
                    trigger["do"](instance, obj, trigger["on"])

        if self.commit:
            instance.save()

def CompositionField(native, trigger=None, commons={}, commit=True,\
                     update_method_queryset=None, update_method_name=None):

    native_contribute_to_class = native.contribute_to_class
    def contribute_to_class(cls, name):
        native._composition_meta = CompositionMeta(cls, native, name, trigger, commons, \
                                                   commit, update_method_queryset, update_method_name)
        return native_contribute_to_class(cls, name)

    native.contribute_to_class = contribute_to_class

    return native
