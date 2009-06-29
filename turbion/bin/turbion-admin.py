#!/usr/bin/env python
import os
from optparse import make_option

import django
from django.core import management
from django.core.management.base import LabelCommand

# file shortcuts
get_lines = lambda filename: file(filename, "r").readlines()
save_lines = lambda filename, lines: file(filename, "w").writelines(lines)

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

        lines = get_lines(urls_file_name)
        lines.insert(-1,
            "\n"
            "    (r'^blog/', include('turbion.urls')),\n"
        )

        save_lines(urls_file_name, lines)

    def _patch_settings(self, label, **options):
        settings_file_name = os.path.join(label, "settings.py")
        defaults_file_name = os.path.join(os.path.dirname(django.__file__), "conf/global_settings.py")

        options_list = []
        if options.get("name", None):
            options_list += [("BLOG_NAME", "'%s'" % options["name"])]

        lines = get_lines(settings_file_name)

        self._append_to_lists(
            lines,
            {
                "INSTALLED_APPS": 'turbion',
                "CONTEXT_PROCESSORS": 'turbion.bits.blogs.context_processors.blog_globals',
            },
            get_lines(defaults_file_name)
        )

        lines.append(
            "\n" +
            "from turbion.settings import *\n\n" +
            "\n".join(["TURBION_%s=%s" % opt for opt in options_list]) +
            "\n"
        )

        save_lines(settings_file_name, lines)

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

    def _append_to_lists(self, lines, lists, defaults=[]):
        mark = None
        i = 0

        for line in lines[:]:
            if not mark: # no list processing yet
                for name in lists.keys():
                    if name in line:
                        mark = name
                        break
            elif ")" in line: # in list right now and check for end
                lines.insert(i, "\n    '%s',\n" % lists[mark])
                i += 1
                del lists[mark]

                if not lists:
                    break

                mark = None
            i += 1

        if lists and defaults: # extrack lists from defaults
            for name, value in lists.iteritems():
                start = 0
                for i, line in enumerate(defaults):
                    if name in line: # match list start
                        start = i
                    elif start and ")" in line: # find list end and extract it with append
                        lines += ["\n"]\
                            + defaults[start:i - 1]\
                            + ["\n    '%s',\n" % value]\
                            + [line]
                        break

management.get_commands()
management._commands["startblogproject"] = BlogProjectCommand()

if __name__ == "__main__":
    management.execute_from_command_line()
