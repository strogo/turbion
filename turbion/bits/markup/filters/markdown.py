from turbion.bits.markup.filters import Filter

class Markdown(Filter):
    def to_html(self, value):
        import markdown2
        return unicode(markdown2.markdown(value))
