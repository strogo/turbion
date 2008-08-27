# -*- coding: utf-8 -*-

class OptionsProvider( object ):
    def __getattr__( self, name ):
        bits = name.split( "__" )

        value_name = bits[ -1 ]
        options_set = bits[ -2 ]

        path = ".".join( bits[:-2] )

        mod = __import__( path, {}, {}, [ '' ] )

        options_set = getattr( mod, options_set )
        instance = getattr( options_set, "instance" )

        return getattr( instance, value_name )

def options_globals( request ):
    return { "options" : OptionsProvider() }
