from django.contrib.auth.models import User, Group
from django.conf import settings

from django.contrib import admin
from turbion.bits.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    exclude = ['password', 'last_login', 'user_permissions', 'groups']
    list_display  = (
        'id', 'nickname', 'email', 'full_name', 'site', 'openid',
        'trusted', 'ip', 'filter',
    )
    list_per_page = 50
    list_display_links = ('id', 'nickname')
    list_filter   = (
        'trusted', 'is_superuser', 'is_staff', 'filter'
    )
    search_fields = ('username', 'nickname', 'email', 'site')

admin.site.register(Profile, ProfileAdmin)
