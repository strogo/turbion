#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from optparse import make_option

from django.core import management
from django.core.management.base import LabelCommand

class BlogProjectCommand(LabelCommand):
    help = "Creates Django project with Turbion blog enabled"
    args = "blog_project_name"

    can_import_settings = False
    requires_model_validation = False

    local_options_list = (
        make_option('--use-djapian', action='store_true', default=False,
            help="Don't use Djapian", dest="use_djapian"),
        make_option('--disable-openid', action='store_true', default=False,
            help="Don't use Turbion openid infrasructure", dest="disable_openid"),
        make_option('--blogs-multiple', action='store_true', default=False,
            help="Allow multiple blogs", dest="blogs_multiple"),
    )

    option_list = LabelCommand.option_list + local_options_list

    def handle_label(self, label, **options):
        if not self._check_modules(**options):
            return "Cannot create project"

        management.call_command("startproject", label)

        self._patch_urls(label, **options)
        self._patch_settings(label, **options)

    def _patch_urls(self, label, **options):
        urls_file_name = os.path.join(label, "urls.py")

        pattern = "blog"
        if options["blogs_multiple"]:
            pattern += "s"

        lines = file(urls_file_name, "r").readlines()
        lines.insert(-1,
            "\n"
            "    (r'^%s/', include('turbion.urls')),\n" % pattern
        )

        file(urls_file_name, "w").writelines(lines)

    def _patch_settings(self, label, **options):
        settings_file_name = os.path.join(label, "settings.py")

        valid_options = dict([(opt.dest, opt.default) for opt in self.local_options_list])
        options = [(name, value) for name, value in options.iteritems()\
                            if (name in valid_options and valid_options[name] != value)]

        lines = file(settings_file_name, "r").readlines()
        lines.append(
            "\n"
            "from turbion import configure\n\n"
            "configure(%s)\n" % ", ".join(["%s=%s" % opt for opt in options])
        )

        file(settings_file_name, "w").writelines(lines)

    def _check_modules(self, use_djapian, disable_openid, **options):
        modules = ["turbion"]

        if use_djapian:
            modules += ["djapian"]

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
management._commands["startblogproject"] = BlogProjectCommand()

if __name__ == "__main__":
    management.execute_from_command_line()
