from django.contrib import admin

from turbion.contrib.dbtemplates.models import Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ("path", "is_active",)
    list_filter = ("is_active",)

admin.site.register(Template, TemplateAdmin)
