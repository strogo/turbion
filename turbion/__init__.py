# -*- coding: utf-8 -*-
from turbion.conf import GenericConfigurator

class TurbionConfigurator(GenericConfigurator):
    def handle_installed_apps(self, value, options):
        if not options.get("use_djapian".upper(), False) and value == "djapian":
            return False
        return True

from turbion import settings

configure = TurbionConfigurator(settings, "TURBION_")
