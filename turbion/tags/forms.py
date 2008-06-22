# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import newforms as forms
from django.utils.safestring import mark_safe

from turbion.tags.models import Tag, TaggedItem

class TagsWidget( forms.MultiWidget ):
    def decompress(self, value):
        if value is None:
            return []
        return value

class TagsField( forms.MultiValueField ):
    def __init__( self, form, initial = None, required = False, *args, **kwargs ):
        self.form = form
        model = form.instance.__class__

        queryset   = Tag.objects.filter_for_model( model )
        if form.instance._get_pk_val():
            initial = form.instance.tags.all().values_list( "id", "name" )
        else:
            initial = None

        widget     = TagsWidget( widgets = ( forms.SelectMultiple,
                                             forms.CharField.widget ) )

        fields = ( forms.ModelMultipleChoiceField( queryset = queryset,
                                            initial = initial,
                                           required = required,
                                           *args, **kwargs),
                   forms.CharField( required = False ) )

        super( TagsField, self ).__init__( fields = fields,
                                           widget = widget )

    def compress( self, value ):
        return value

    def clean(self, value):
        def save_tags():
            self.form.instance.tags.replace( *( value[ 0 ] + [ t.strip() for t in value[ 1 ].split( "," ) ] ) )
        self.form.save_tags = save_tags

        return value
