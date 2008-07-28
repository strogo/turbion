# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import forms
from django.utils.safestring import mark_safe

from turbion.tags.models import Tag, TaggedItem

class TagsWidget( forms.MultiWidget ):
    def decompress(self, value):
        #if value is not None:
        #    return ( [ key for key, v in value ], )
        if value is None:
            return []
        return value, None

    def _get_choices( self ):
        return self.widgets[ 0 ].choices

    def _set_choices( self, choices ):
        self.widgets[ 0 ].choices = choices

    choices = property( _get_choices, _set_choices )

class TagsField( forms.ModelMultipleChoiceField ):
    def __init__( self, form, required = False, *args, **kwargs ):
        self.form = form
        model = form.instance.__class__

        queryset   = Tag.objects.filter_for_model( model )

        if form.instance._get_pk_val():
            initial = form.instance.tags.all().values_list( "id", flat = True )
        else:
            initial = None

        widget     = TagsWidget( widgets = ( forms.SelectMultiple(),
                                             forms.CharField.widget() ) )

        super( TagsField, self ).__init__( queryset = queryset,
                                           widget = widget,
                                           initial = initial,
                                           required = required,
                                           *args, **kwargs
                                           )

    def clean(self, value):
        def save_tags():
            str_list = value[1].strip()
            if len( str_list ):
                str_values = [ t.strip() for t in str_list.split( "," ) ]
            else:
                str_values = []
            self.form.instance.tags.replace( *( list( Tag.objects.filter( pk__in = value[ 0 ] ) ) + str_values ) )
        self.form.save_tags = save_tags

        return value
