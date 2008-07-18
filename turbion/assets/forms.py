# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import newforms as forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.assets.models import Asset
from turbion.tags.forms import TagsField

class AssetForm( forms.ModelForm ):
    class Meta:
        model = Asset

    def __init__( self, *args, **kwargs ):
        super( AssetForm, self ).__init__( *args, **kwargs )

        self.fields["filename"].required = False
        self.fields["tags"] = TagsField( form = self )


    def clean( self ):
        return self.cleaned_data