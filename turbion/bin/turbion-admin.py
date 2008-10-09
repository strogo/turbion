#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import make_option

from django.core import management
from django.core.management.base import LabelCommand

class Command(LabelCommand):
    help = "Creates Django project with Turbion blog enabled"
    args = "blog_project_name"

    can_import_settings = False
    requires_model_validation = False

    option_list = LabelCommand.option_list + (
        make_option('--disable-djapian', action='store_true', default=False,
            help="Don't use Djapian", dest="disable_djapian"),
        make_option('--disable-openid', action='store_true', default=False,
            help="Don't use turbion openid infrasructure", dest="disable_openid"),
        make_option('--allow-multiple', action='store_true', default=False,
            help="Allow multiple blogs", dest="allow_multiple"),
    )

    def handle_label(self, label, **options):
        """
        - пропатчить settings.py
        - пропатчить urls.py
        """
        if not self._check_modules(**options):
            print "Cannot create project"
            return

        management.call_command("startproject", label)

        self._patch_urls()
        self._patch_settings(**options)

    def _patch_urls(self):
        pass

    def _patch_settings(self, **options):
        pass

    def _check_modules(self, disable_djapian, disable_openid, **options):
        modules = ["turbion"]

        if not disable_djapian:
            pass#modules += ["djapian"]

        if not disable_openid:
            modules += ["openid"]

        res = True

        for m in modules:
            try:
                __import__(m)
            except ImportError, e:
                print "Cannot import required module '%s': %s" % (m.split(".")[0], e)
                res = False

        return res

management.get_commands()
management._commands["startblogproject"] = Command()

if __name__ == "__main__":
    management.execute_from_command_line()
