# -*- coding: utf-8 -*-
from django import http

from turbion.aliases.models import Alias

import re

class AliasesMiddleware(object):
    def process_request(self, request):
        try:
            alias = Alias.active.get(from_url=request.path)

            if alias.exclude_user_agent:
                regexpr = re.compile(alias.exclude_user_agent, re.I)
                if regexpr.match(request.META.get("HTTP_USER_AGENT", "")):
                   return

            response = http.HttpResponseRedirect(alias.to_url)
            response.status_code = alias.status_code
            return response
        except Alias.DoesNotExist:
            pass
