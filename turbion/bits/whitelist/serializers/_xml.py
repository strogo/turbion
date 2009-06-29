from cStringIO import StringIO
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import elementtree.ElementTree as ET

from django.conf import settings

mime_types = ['application/xml', 'text/xml']

def generator(openids, buf):
    root = ET.Element('whitelist')
    for openid in openids:
        ET.SubElement(root, 'openid').text = openid
    xml = ET.ElementTree(root)
    xml.write(buf, encoding=settings.DEFAULT_CHARSET)

def parser(content):
    xml = ET.parse(StringIO(content))

    return [o.text for o in xml.findall('openid')]
