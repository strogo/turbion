from django.utils.html import strip_tags
from django.utils.encoding import force_unicode

from urlparse import urlsplit
from BeautifulSoup import BeautifulSoup

def parse_html_links(text, domain):
    def is_external(external):
        if not href.startswith('http://') and not href.startswith('https://'):
            return False

        path_e = urlsplit(external)[2]
        return path_e != domain

    soup = BeautifulSoup(text)

    return [a['href'] for a in soup.findAll('a') if is_external(a['href'])]

class PingError(Exception):
    def __init__(self, code):
        self.code = code
        super(PingError, self).__init__('pingback.ping: error with code %s' % code)

class SourceParser(object):
    def __init__(self, content):
        self.soup = BeautifulSoup(content)

    def get_title(self):
        try:
            title = self.soup.find('title').contents[0]
            return strip_tags(force_unicode(title))
        except AttributeError:
            return ""

    def get_paragraph(self, target_uri, max_length=200):
        mylink = self.soup.find('a', href=target_uri)
        if not mylink:
            # The source URI does not contain a link to the target URI, and so cannot be used as a source.
            raise PingError(0x0011)

        content = force_unicode(mylink.findParent())
        mylink = force_unicode(mylink)
        i = content.index(mylink)
        content = strip_tags(content)

        if len(content) > max_length:
            start = i - max_length / 2
            if start < 0:
                start = 0
            end = i + len(mylink) + max_length / 2
            if end > len(content):
                end = len(content)
            content = content[start:end]
        mark = "[...]"
        return mark + content.strip() + mark
