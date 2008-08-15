# -*- coding: utf-8 -*-
from django.db import models

from turbion.utils.postprocessing import ProcessorSpot

class PostprocessField(models.CharField):
    __metaclass__ = models.SubfieldBase

    default_choices = [ ( desc, desc.rsplit(".",2)[1] ) for desc, processor in ProcessorSpot.processors.iteritems() ]

    def __init__(self, limit_choices_to = None, *args, **kwargs ):
        self.limit_choices_to = limit_choices_to

        defaults = { "choices" : [ ( desc, proc ) for desc, proc in self.default_choices if limit_choices_to and desc in limit_choices_to or True ],
                    "max_length" : 150,
                    "default" : "turbion.utils.postprocessing.backends.dummy.Processor" }

        defaults.update( kwargs )

        super( PostprocessField, self ).__init__( *args, **defaults )

    def to_python( self, value ):
        return ProcessorSpot.get_processor( value )

    def get_db_prep_save(self, value):
        return value.descriptor

_postprocess_field_name = lambda name: "%s_processor"%name

class ProcessTextField( models.TextField ):
    def contribute_to_class(self, cls, name):
        postprocess_field = PostprocessField()
        postprocess_field.creation_counter = self.creation_counter
        cls.add_to_class(_postprocess_field_name(name), postprocess_field)

        #add processed field data getter
        cls.add_to_class( "get_%s_postprocess" % name, self.get_FIELD_postprocess )
        # add the text field normally
        super(ProcessTextField, self).contribute_to_class(cls, name)

    def pre_save(self, model_instance, add):
        value = super(ProcessTextField,self ).pre_save( model_instance, add )

        processor= getattr( model_instance, _postprocess_field_name(self.name) )

        return processor.preprocess( value )
