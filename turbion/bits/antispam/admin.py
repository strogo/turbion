from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django import http

from turbion.bits.antispam import action_submit

class ActionModelAdmin(object):
    additinal_fields = ['antispam']
    batch_actions = ['antispam_action_spam', 'antispam_action_ham']

    def get_antispam_url_name(self):
        """Creates antispam action url name"""
        return '%s_%s_antispam_action' % (self.model._meta.app_label, self.model._meta.module_name)

    def get_urls(self):
        """Updates default ModelAdmin urls"""
        from django.conf.urls.defaults import patterns, url

        urls = super(ActionModelAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(.+)/antispam/$', self.antispam_view, name=self.get_antispam_url_name())
        )
        return my_urls + urls

    def antispam_submit_action_for_object(self, request, obj, action):
        action_submit(action, obj)

        obj.antispam_status = action == 'spam' and 'manual' or None
        obj.handle_antispam_decision(action)
        obj.save()

        self.message_user(
            request,
            _("`%(obj)s` successfully marked as %(action)s.") % {
                'obj': obj,
                'action': action
            }
        )

    def antispam_view(self, request, object_id):
        """Processes action form for object"""
        if request.method == 'POST':
            obj = self.model._default_manager.get(pk=object_id)
            action = request.POST.get('action')

            self.antispam_submit_action_for_object(request, obj, action)

            return http.HttpResponseRedirect(
                request.META.get('HTTP_REFERER')
            )
        return http.HttpResponseBadRequest('No action or illegal object')

    def antispam(self, obj):
        """Creates button with action url and proper label"""
        action = obj.antispam_status and 'ham' or 'spam'
        name = action == 'spam' and ugettext('Spam') or ugettext('Ham')
        url = reverse('admin:%s' % self.get_antispam_url_name(), args=(obj.pk,), current_app=self.admin_site.name)

        return """<form action="%s" method="POST">
        <input type="hidden" name="action" value="%s"/>
        <input class="button" type="submit" style="font-size:10px; padding:1px 2px;" value="%s"/>
        </form>""" % (url, action, name)
    antispam.allow_tags = True
    antispam.short_description = _('antispam')

    def _antispam_batch_action(self, request, queryset, status):
        """Generic admin batch action"""
        for obj in queryset:
            self.antispam_submit_action_for_object(request, obj, status)

    antispam_action_spam = lambda self, request, queryset: self._antispam_batch_action(request, queryset, 'spam')
    antispam_action_spam.short_description = _("mark selected as spam")

    antispam_action_ham = lambda self, request, queryset: self._antispam_batch_action(request, queryset, 'ham')
    antispam_action_ham.short_description = _("mark selected as ham")
