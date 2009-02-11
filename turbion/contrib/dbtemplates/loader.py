# -*- coding: utf-8 -*-
from django.template import TemplateDoesNotExist

from turbion.dbtemplates.models import Template

def load_template_source(template_name, template_dirs=None):
    try:
        return ( Template.active.get( path = template_name ).text, template_name )
    except Template.DoesNotExist:
        raise TemplateDoesNotExist, "Does not a datebase template"
load_template_source.is_usable = True