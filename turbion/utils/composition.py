# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import curry
from django.utils.itercompat import is_iterable

class Trigger(object):
    def __init__(self, do, on, field_name, sender, sender_model,\
                 commit, field_holder_getter):
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
        
        if not is_iterable(on):
            on = [on]
        self.on = on
        
        self.field_holder_getter = field_holder_getter
        
    def connect(self):
        """
           Connects trigger's handler to all of its signals
        """
        for signal in self.on:
            signal.connect(self.handler, sender=self.sender)
        
    def handler(self, signal, instance=None, **kwargs):
        """
            Signal handler
        """
        objects = self.field_holder_getter(instance)
        if not is_iterable(objects):
            objects = [objects]
            
        for obj in objects:
            setattr(obj, self.field_name, self.do(obj, instance, signal))
        
            if self.commit:
                obj.save()

class CompositionMeta(object):
    def __init__(self, model, field, name, trigger,\
                  commons, commit, update_method):
        self.model = model
        self.name = name
        self.trigger = []

        if not commons:
            commons = {}
        self.commons = commons

        self.commit = commit

        if not is_iterable(trigger) or isinstance(trigger, dict):
            trigger = [trigger]

        trigger_defaults = dict(
                sender_model=model,
                sender=None,
                on=[models.signals.post_save],
                field_holder_getter=lambda instance: instance,
                field_name=name,
                commit=commit
        )
        trigger_defaults.update(commons)
        
        if not len(trigger):
            raise ValueError("At least one trigger must be specefied")
        
        for t in trigger:
            trigger_meta = trigger_defaults.copy()
            trigger_meta.update(t)

            trigger_obj = Trigger(**trigger_meta)
            trigger_obj.connect()
            
            self.trigger.append(trigger_obj)
            
        update_method_defaults = dict(
            initial=None,
            name="update_%s" % name,
            trigger=self.trigger[0],
            queryset=None
        )
        update_method_defaults.update(update_method)
        
        if isinstance(update_method_defaults["trigger"], (int, long)):
            n = update_method_defaults["trigger"]
            if n >= len(self.trigger):
                raise ValueError("Update method trigger must be index of trigger list")
            update_method_defaults["trigger"] = self.trigger[update_method_defaults["trigger"]]
        
        self.update_method = update_method_defaults
        
        setattr(model, self.update_method["name"], lambda instance: self._update_method(instance))

    def _update_method(self, instance):
        """
            Generic `update_FOO` method that is connected to model
        """
        qs_getter = self.update_method["queryset"]
        if qs_getter is None:
            qs_getter = [instance]
        
        trigger = self.update_method["trigger"]
        
        setattr(instance, trigger.field_name, self.update_method["initial"])
        if callable(qs_getter):
            qs = qs_getter(instance)
        else:
            qs = qs_getter
    
        for obj in qs:
            setattr(
                instance,
                trigger.field_name,
                trigger.do(instance, obj, trigger.on[0])
            )
        if self.commit:
            instance.save()

def CompositionField(native, trigger=None, commons={},\
                     commit=True, update_method={}):
    """
        CompositionField funtiction that patches native field
        with custom `contribute_to_class` method and returns it
        
        Params:
             * native - Django field instance for current compostion field
             * trigger - one or some numberr of triggers that handle composition.
                Trigger is a dict with allowed keys:
                  * on - signal or list of signals that this field handles
                  * do - signals handler, with 3 params:
                           * related instance
                           * instance (that comes with signal send)
                           * concrete signal (one from `on` value)
                  * on_update - flag that indicates use or not
                                this trigger for `update_FOO` method
                  * on_update_initial - initial value to field before applince
                                        of `update_FOO` method
                  * field_holder_getter - function that gets instance(that comes with signal send)\
                                          as parameter and returns field holder
                                          object (related instance)
                  * sender
                  * sender_model
             * commons - a trigger like field with common settings
                         for all given triggers
             * commit - flag that indicates save instance after trigger appliance or not
             * update_method_queryset - query set or
                        callable(with one param - `instance` of an holder model)
                        that have to retun something iterable
             * update_method_name - custom `update_FOO` method name
    """
    native_contribute_to_class = native.contribute_to_class
    def contribute_to_class(cls, name):
        native._composition_meta = CompositionMeta(
                                        cls, native, name, trigger,\
                                        commons, commit,update_method)
        return native_contribute_to_class(cls, name)

    native.contribute_to_class = contribute_to_class

    return native
