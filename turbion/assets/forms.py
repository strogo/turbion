# -*- coding: utf-8 -*-
import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.assets.models import Asset
from turbion.tags.forms import TagsField

class AssetForm( forms.ModelForm ):
    class Meta:
        model = Asset
        exclude = ["created_by", "created_on", "edited_by", "edited_on"]

    resize_to    = forms.CharField(required=False)
    thumbnail_to = forms.CharField(required=False)

    def __init__( self, *args, **kwargs ):
        super( AssetForm, self ).__init__( *args, **kwargs )

        self.fields["filename"].required = False
        self.fields["mime_type"].required = False
        self.fields["type"].required = False

        self.fields["tags"] = TagsField( form = self )

    def _guess_mime_type(self, filename):
        import mimetypes

        type, _ = mimetypes.guess_type("image.pdf")

        if not type:
            type = "unknown"

        if not self.cleaned_data.get("mime_type"):
            self.cleaned_data["mime_type"] = type

    def _guess_type(self):
        mime = self.cleaned_data["mime_type"].split('/')[0]

        if mime in Asset.types.__dict__:
            type = mime
        else:
            type = "unknown"

        if not self.cleaned_data.get("type"):
            self.cleaned_data["type"] = type

    def clean_file(self):
        data = self.cleaned_data["file"]
        filename = self.cleaned_data.get("filename")
        if not filename:
            self.cleaned_data["filename"] = data._name
        else:
            data._name = filename

        #TODO: add file existance check

        self._guess_mime_type(data._name)
        self._guess_type()

        return data

    def clean(self):
        return self.cleaned_data

    def postprocess(self):
        import Image

        resize_to = self.cleaned_data.get("resize_to")
        thumbnail_to = self.cleaned_data.get("thumbnail_to")

        if resize_to:
            pass

        if thumbnail_to:
            dimentions = map(int, thumbnail_to.split(':'))

            image = Image.open(self.instance.get_file_filename())
            image.thumbnail(dimentions, Image.ANTIALIAS)

            image.save(self.instance.get_thumbnail_url())
