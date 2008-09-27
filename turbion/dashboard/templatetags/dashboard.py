# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def add_turbion_media( url ):
    return "%sturbion/%s" % ( settings.MEDIA_URL, url )

@register.simple_tag
def dashboard_yui_load(modules, success="",optional=True):
    return """<!-- Load the YUI Loader script: -->
<script src="%(MEDIA_URL)sturbion/yui/yuiloader/yuiloader-beta-min.js"></script>
<script>
var loader = new YAHOO.util.YUILoader({
    require: [%(modules)s],
    base: '%(MEDIA_URL)sturbion/yui/',
    loadOptional: %(optional)s,
    onSuccess: %(success)s
});
loader.insert();
</script>
    """ % {"modules": modules,
           "MEDIA_URL": settings.MEDIA_URL,
           "optional": str(bool(optional)).lower(),
           "success": success
    }

@register.inclusion_tag("turbion/dashboard/include/table_def.html", takes_context=True)
def dashboard_create_table(context, name):
    from turbion.dashboard.schemas import SchemaSpot
    blog = context["blog"]
    schema = SchemaSpot.schemas[name](blog)

    return {"blog": blog,
            "schema": schema,
            "name": name}
