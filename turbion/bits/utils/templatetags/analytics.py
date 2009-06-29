from django.conf import settings
from django import template
from django.contrib.sites.models import Site

register = template.Library()

domain = Site.objects.get_current().domain

@register.simple_tag
def google_urchin(uacct):
    if not settings.DEBUG:
        return """<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("%(uacct)s");
pageTracker._addOrganic("mail.ru", "q");
pageTracker._addOrganic("rambler.ru", "query");
pageTracker._addOrganic("go.mail.ru", "q");
pageTracker._addOrganic("nova.rambler.ru", "query");
pageTracker._addOrganic("nigma.ru", "s");
pageTracker._addOrganic("blogs.yandex.ru", "text");
pageTracker._addOrganic("webalta.ru", "q");
pageTracker._addOrganic("aport.ru", "r");
pageTracker._addOrganic("meta.ua", "q");
pageTracker._addOrganic("bigmir.net", "q");
pageTracker._addOrganic("tut.by", "query");
pageTracker._addOrganic("ukr.net", "search_query");
pageTracker._addOrganic("poisk.ru", "text");
pageTracker._addOrganic("liveinternet.ru", "ask");
pageTracker._addOrganic("gogo.ru", "q");
pageTracker._addOrganic("gde.ru", "keywords");
pageTracker._addOrganic("quintura.ru", "request");
pageTracker._addOrganic("qip.ru", "query");
pageTracker._addOrganic("metabot.ru","st");
pageTracker._trackPageview();
} catch(err) {}</script>""" % {'uacct': uacct}
    else:
        return ""

@register.simple_tag
def google_webtools_meta( meta ):
    return """<meta name="verify-v1" content="%s" />""" % meta

@register.simple_tag
def yandex_webmaster( code ):
    return """<meta name='yandex-verification' content='%s' />""" % code

@register.simple_tag
def feedburner_stats( name, url ):
    if not settings.DEBUG:
        return """<script src="http://feeds.feedburner.com/~s/%s?i=http://%s%s" type="text/javascript" charset="utf-8"></script>""" % ( name, domain, url )
    return ""

@register.simple_tag
def feedburner_count(feed):
    from urllib2 import urlopen
    from xml.dom import minidom
    try:
        stats = urlopen( "http://api.feedburner.com/awareness/1.0/GetFeedData?uri=%s" % feed )

        doc = minidom.parse( stats )
        entry = doc.getElementsByTagName( "entry" )[0]
        return entry.getAttribute( "circulation" )
    except:
        if settings.DEBUG:
            raise
        return ""
