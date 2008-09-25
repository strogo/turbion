# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import curry
from django.utils.itercompat import is_iterable

class Trigger(object):
    def __init__(self, do, on, field_name, sender, sender_model,\
                 commit, field_holder_getter, on_update, on_update_initial):
        self.field_name = field_name
        self.commit = commit
        
        if sender_model and not sender:
            if isinstance(sender_model, basestring):
                
                sender_model = models.get_model(*sender_model.split(".", 1))
            self.sender = self.sender_model = sender_model
        else:
            self.sender = sender
            self.sender_model = sender_model
        
        if not do:
            raise ValueError("`do` action not defined for trigger")
        self.do = do
        
        if not isinstance(on, (tuple, list)):
            on = [on]
        self.on = on
        
        self.field_holder_getter = field_holder_getter
        self.on_update= on_update
        self.on_update_initial = on_update_initial
        
    def connect(self):
        for signal in self.on:
            signal.connect(self.handler, sender=self.sender)
        
    def handler(self, signal, instance=None, **kwargs):
        objects = self.field_holder_getter(instance)
        if not is_iterable(objects):
            objects = [objects]
            
        for obj in objects:
            setattr(obj, self.field_name, self.do(obj, instance, signal))
        
            if self.commit:
                obj.save()

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
                sender=None,
                on=[models.signals.post_save],
                field_holder_getter=lambda instance: instance,
                on_update=False,#Fixme: make allow only one on_update method
                on_update_initial=None,
                field_name=name,
                commit=commit
        )
        trigger_defaults.update(commons)
        
        on_update = False
    
        for count, t in enumerate(trigger):
            trigger_meta = trigger_defaults.copy()
            trigger_meta.update(t)
            
            if trigger_meta["on_update"]:
                if not on_update:
                    on_update = True
                else:
                    raise ValueError("Only one trigger may be marked as `on_update`")
            else:
                if count == len(trigger) - 1 and not on_update:#last trigger
                    trigger_meta["on_update"] = True

            trigger_obj = Trigger(**trigger_meta)
            trigger_obj.connect()
            
            self.trigger.append(trigger_obj)

    def _update_method(self, instance):
        if self.update_method_queryset:
            qs_getter = self.update_method_queryset
        else:
            qs_getter = [instance]
        for trigger in self.trigger:
            if trigger.on_update:
                setattr(instance, trigger.field_name, trigger.on_update_initial)
                if callable(qs_getter):
                    qs = qs_getter(instance)
                else:
                    qs = qs_getter
        
                for obj in qs:
                    setattr(instance, trigger.field_name, trigger.do(instance, obj, trigger.on))

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
