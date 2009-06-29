from django import template

from turbion.bits.utils.markup.filters import Filter

register = template.Library()

for name, func in Filter.manager.all():
    register.filter(name, func.to_html)

@register.filter
def markup(text, filter="markdown"):
    return Filter.manager.get(filter).to_html(text)

@register.filter
def sanitize(value):
    from BeautifulSoup import BeautifulSoup, Comment#TODO: design decision needed
    valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
    valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                     if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')
