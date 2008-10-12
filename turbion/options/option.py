# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode

class BaseOption(object):
    def __init__(self, default=None):
        self.default = default

    def to_python(self, value):
        return value

    def to_db(self, value):
        return value

class CharOption( BaseOption ):
    to_python = models.CharField.to_python.im_func
    to_db     = models.CharField.get_db_prep_save.im_func
    get_db_prep_value = models.CharField.get_db_prep_value.im_func

class IntegerOption( BaseOption ):
    def to_python( self, value ):
        try:
            return value is not None and int( value ) or None
        except ValueError:
            return 0

    to_db     = models.IntegerField.get_db_prep_save.im_func
    get_db_prep_value = models.IntegerField.get_db_prep_value.im_func

class FloatOption( BaseOption ):
    def to_python( self, value ):
        try:
            return value is not None and float( value ) or None
        except ValueError:
            return 0.

    to_db     = models.FloatField.get_db_prep_save.im_func
    get_db_prep_value = models.FloatField.get_db_prep_value.im_func

class BooleanOption( BaseOption ):
    to_python = models.BooleanField.to_python.im_func
    to_db     = models.BooleanField.get_db_prep_save.im_func
    get_db_prep_value = models.BooleanField.get_db_prep_value.im_func

class TimeOption( BaseOption ):
    def to_python( self, value ):
        if isinstance( value, basestring ):
            i = value.rfind( "." )
            if i >= 0:
                value = value[ : i + 1 ]
        return models.DateTimeField.to_python.im_func( self, value )

    def to_db( self, value ):
        return force_unicode( value )
