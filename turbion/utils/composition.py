# -*- coding: utf-8 -*-
from django.db import models
from django.utils.itercompat import is_iterable


# TODO: add pre_save signal handler for initial value

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
            do=self.trigger[0],
            queryset=None
        )
        update_method_defaults.update(update_method)

        if isinstance(update_method_defaults["do"], (int, long)):
            n = update_method_defaults["do"]
            if n >= len(self.trigger):
                raise ValueError("Update method trigger must be index of trigger list")
            update_method_defaults["do"] = self.trigger[update_method_defaults["do"]]

        self.update_method = update_method_defaults

        setattr(model, self.update_method["name"], lambda instance: self._update_method(instance))
        setattr(model, "freeze_%s" % name, lambda instance: self._freeze_method(instance))

    def _update_method(self, instance):
        """
            Generic `update_FOO` method that is connected to model
        """
        qs_getter = self.update_method["queryset"]
        if qs_getter is None:
            qs_getter = [instance]

        trigger = self.update_method["do"]

        setattr(instance, trigger.field_name, self.update_method["initial"])
        if callable(qs_getter):
            qs = qs_getter(instance)
        else:
            qs = qs_getter

        if not is_iterable(qs):
            qs = [qs]

        for obj in qs:
            setattr(
                instance,
                trigger.field_name,
                trigger.do(instance, obj, trigger.on[0])
            )
        if self.commit:
            instance.save()

    def _freeze_method(self, instance):
        """
            Generic `freeze_FOO` method that is connected to model
        """
        pass

class CompositionField(object):
    def __init__(self, native, trigger=None, commons={},\
                     commit=True, update_method={}):
        self.internal_init(native, trigger, commons, commit, update_method)

    def internal_init(self, native=None, trigger=None, commons={},\
                     commit=True, update_method={}):
        """
            CompositionField class that patches native field
            with custom `contribute_to_class` method

            Params:
                 * native - Django field instance for current compostion field
                 * trigger - one or some numberr of triggers that handle composition.
                    Trigger is a dict with allowed keys:
                      * on - signal or list of signals that this field handles
                      * do - signals handler, with 3 params:
                               * related instance
                               * instance (that comes with signal send)
                               * concrete signal (one from `on` value)
                      * field_holder_getter - function that gets instance(that comes with signal send)\
                                              as parameter and returns field holder
                                              object (related instance)
                      * sender - signal sender
                      * sender_model - model instance or model name that send signal
                 * commons - a trigger like field with common settings
                             for all given triggers
                 * commit - flag that indicates save instance after trigger appliance or not
                 * update_method - dict for customization of update_method. Allowed params:
                        * initial - initial value to field before applince of method
                        * do - index of update trigger or trigger itself
                        * queryset - query set or callable(with one param - `instance` of an holder model)
                                that have to retun something iterable
                        * name - custom method name instead of `update_FOO`
        """
        if native:
            import new
            self.__class__ = new.classobj(
                                    self.__class__.__name__,
                                    tuple([self.__class__, native.__class__] + list(self.__class__.__mro__[1:])),
                                    {}
                                )

        self._c_native = native
        self.__dict__.update(native.__dict__)

        self._c_trigger = trigger
        self._c_commons = commons
        self._c_commit = commit
        self._c_update_method = update_method

    def contribute_to_class(self, cls, name):
        self.introspect_class(cls, name)
        self._composition_meta = self.create_meta(cls, name)
        return self._c_native.__class__.contribute_to_class(self, cls, name)

    def create_meta(self, cls, name):
        return CompositionMeta(
                    cls, self._c_native, name, self._c_trigger,\
                    self._c_commons, self._c_commit, self._c_update_method
                )

    def introspect_class(self, cls, name):
        pass

class ForeignAttribute(CompositionField):
    def __init__(self, field, native=None):
        self.field = field
        self.native = native

    def introspect_class(self, cls, name):
        """
        - По полю определить модель к которой относится атрибут
        - определить как из объекта этой модели найти объект холдер
        - повесить сигналы на сохранение и добавлени к модели
        - сгенерировать функцию сеттер для атрибута
        """
        bits = self.field.split(".")

        if len(bits) < 2:
            raise ValueError("Illegal path to foreign field")

        foreign_field = None
        foreign_model = cls
        prev_model = None# for related_name generation

        related_names_chain = []

        for bit in bits:
            meta = foreign_model._meta

            try:
                foreign_field = meta.get_field(bit)
            except models.FieldDoesNotExist:
                raise ValueError("Field '%s' does not exist" % bit)

            if isinstance(foreign_field, models.ForeignKey):
                foreign_rel = foreign_field.rel
                prev_model = foreign_model
                foreign_model = foreign_rel.to

                if isinstance(foreign_rel.to, basestring):
                    raise ValueError("Model with name '%s' must be class instance not string" % foreign_rel.to)

                related_name = foreign_rel.related_name
                if not related_name and prev_model:
                    related_name = "%s_set" % prev_model.__name__.lower()#FIXME
                    #for rel_object in foreign_field.rel.to._meta.get_all_related_objects():
                    #    if rel_object.field == foreign_field:
                    #        related_name = rel_object.get_accessor_name()

                related_names_chain.append(related_name)


        native = self.native
        if not native:
            native = foreign_field

        def get_root_instances(instance, chain):
            attr = getattr(instance, chain.pop()).all()

            if chain:
                for obj in attr:
                    for inst in get_root_instances(
                                        obj,
                                        rchain
                                    ):
                        yield inst
            else:
                for obj in attr:
                    yield obj

        def get_leaf_instance(instance, chain):
            for bit in chain:
                instance = getattr(instance, bit)

            return instance

        self.internal_init(
            native=native,
            trigger=dict(
                on=(models.signals.post_save, models.signals.post_delete),
                sender_model=foreign_model,
                do=lambda holder, foreign, signal: getattr(foreign, bits[-1]),
                field_holder_getter=lambda foreign: get_root_instances(foreign, related_names_chain[:])
            ),
            update_method=dict(
                queryset=lambda holder: get_leaf_instance(holder, bits[:-1])#FIXME: rename queryset
            ),
            commit=True,
        )
        
ForeignAttributeField = ForeignAttribute

class AttributesAggregation(CompositionField):
    def __init__(self, field, do, native=None):
        self.field = field
        self.do = do
        self.native = native
        
AttributesAggregationField = AttributesAggregation

class ChildsAggregation(CompositionField):
    def __init__(self, field, do, native=None, signal=None, instance_getter=None):
        self.field = field
        self.do = do
        self.native = native
        self.signal = signal
        self.instance_getter = instance_getter
        
ChildsAggregationField = ChildsAggregation
