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
        make_option('--name', action='store', default=None,
            help="Blog name", dest="name"),
    )

    option_list = LabelCommand.option_list + local_options_list

    def handle_label(self, label, name=None, **options):
        if not self._check_modules(name=name, **options):
            return "Cannot create project"

        management.call_command("startproject", label)

        self._patch_urls(label)
        self._patch_settings(label, name=name)

    def _patch_urls(self, label):
        urls_file_name = os.path.join(label, "urls.py")

        lines = file(urls_file_name, "r").readlines()
        lines.insert(-1,
            "\n"
            "    (r'^blog/', include('turbion.urls')),\n"
        )

        file(urls_file_name, "w").writelines(lines)

    def _patch_settings(self, label, **options):
        settings_file_name = os.path.join(label, "settings.py")

        valid_options = dict([(opt.dest, opt.default) for opt in self.local_options_list])
        options = [(name.upper(), value) for name, value in options.iteritems()\
                            if (name in valid_options and valid_options[name] != value and value is not None)]

        lines = file(settings_file_name, "r").readlines()

        mark = False
        for i, line in enumerate(lines[:]):
            if "INSTALLED_APPS" in line:
                mark = True
            if mark and ")" in line:
                lines.insert(i, "    'turbion',\n")
                break

        lines.append(
            "\n" +
            "from turbion.settings import *\n\n" +
            "\n".join(["TURBION_%s=%s" % opt for opt in options]) +
            "\n"
        )

        file(settings_file_name, "w").writelines(lines)

    def _check_modules(self, **options):
        modules = ["turbion"]

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
