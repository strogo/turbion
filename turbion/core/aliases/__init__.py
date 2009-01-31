import re

from django import http

from turbion.core.aliases.models import Alias

def check_aliases(request, blog):
    try:
        alias = Alias.active.get(blog=blog, from_url=request.path)

        if alias.exclude_user_agent:
            regexpr = re.compile(alias.exclude_user_agent, re.I)
            if regexpr.match(request.META.get("HTTP_USER_AGENT", "")):
               return

        response = http.HttpResponseRedirect(alias.to_url)
        response.status_code = alias.status_code
        return response
    except Alias.DoesNotExist:
        pass
