# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.db import models
from django.test import TestCase
from django.core.management import call_command

from turbion import options
from turbion.options.models import Option

now = datetime.now().replace(microsecond=0)

class Pet( models.Model ):
    ages = models.IntegerField()

class Animal( models.Model ):
    name = models.CharField( max_length = 20 )

class ModelOptions( options.OptionSet ):
    class Meta:
        model = Pet

    per_page = options.IntegerOption( default = 10 )

class ObjectOptions( options.OptionSet ):
    class Meta:
        model = Animal
        to_object = True

    color = options.CharOption( default = "red" )

class TestOptions( options.OptionSet ):
    str_option     = options.CharOption( default = "foobar" )
    int_option     = options.IntegerOption( default = 23 )
    float_option   = options.FloatOption( default = 1. )

    time_option    = options.TimeOption( default = now )
    boolean_option = options.BooleanOption( default = False )

class FreeOptionsTestCase( TestCase ):
    def setUp( self ):
        call_command( "syncoptions" )

    def test_option_count( self ):
        self.assertEqual( Option.objects.filter(connection_ct = None,
                                                connection_id = None,
                                                descriptor__contains = "options.tests" ).count(), 5 )

    def test_defaults( self ):
        self.assertEqual( TestOptions.instance.str_option,    "foobar" )
        self.assertEqual( TestOptions.instance.int_option,     23 )
        self.assertEqual( TestOptions.instance.float_option,   1.0 )
        self.assertEqual( TestOptions.instance.time_option,    now )
        self.assertEqual( TestOptions.instance.boolean_option, False )

    def test_assign_str( self ):
        TestOptions.instance.str_option = "barfoo"
        self.assertEqual( TestOptions.instance.str_option, "barfoo" )

    def test_assign_int( self ):
        TestOptions.instance.int_option = 777
        self.assertEqual( TestOptions.instance.int_option, 777 )

    def test_assign_float( self ):
        TestOptions.instance.float_option = 777.
        self.assertEqual( TestOptions.instance.float_option, 777. )

    def test_assign_time( self ):
        new_now = datetime.now().replace( microsecond = 0 )

        TestOptions.instance.time_option = new_now
        self.assertEqual( TestOptions.instance.time_option, new_now )

    def test_assign_boolean( self ):
        TestOptions.instance.boolean_option = True
        self.assertEqual( TestOptions.instance.boolean_option, True )


class ModelOptionsTest( TestCase ):
    def setUp( self ):
        call_command( "syncoptions" )

    def test_option_get( self ):
        self.assertEqual( Pet.options.per_page, 10 )

    def test_option_set( self ):
        Pet.options.per_page = 25
        self.assertEqual( Pet.options.per_page, 25 )


class ObjectOptionsTest( TestCase ):
    def setUp( self ):
        Animal.objects.create( name = "shark" )
        call_command( "syncoptions" )

    def test_option_get( self ):
        animal = Animal.objects.get()

        self.assertEqual( animal.options.color, "red" )

    def test_option_set( self ):
        animal = Animal.objects.get()

        animal.options.color = "green"
        self.assertEqual( animal.options.color, "green" )

class NewObjectOptionsTest( TestCase ):
    def setUp( self ):
        Animal.objects.create( name = "shark" )
        call_command( "syncoptions" )

        Animal.objects.create( name = "dog" )

    @property
    def object( self ):
        return Animal.objects.get( name = "dog" )

    def test_option_get( self ):
        self.assertEqual( self.object.options.color, "red" )

    def test_option_set( self ):
        animal = self.object

        animal.options.color = "green"
        self.assertEqual( animal.options.color, "green" )

class TemplateGlobalsTest( TestCase ):
    def setUp( self ):
        call_command( "syncoptions" )

    def test_variable( self ):
        from django.template import Template, Context
        from turbion.options.context_processors import OptionsProvider

        template = Template( "{{options.turbion__options__tests__TestOptions__float_option}}" )

        result = template.render( Context( { "options" : OptionsProvider() } ) )

        self.assertEqual( result, "1.0" )

#TODO:
# - test options with custom names
# - test multiple options sets to one model/instance
#
