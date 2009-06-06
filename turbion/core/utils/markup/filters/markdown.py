from turbion.core.utils.markup.filters import Filter

class Markdown(Filter):
    def to_html(self, value):
        import markdown2
        return markdown2.markdown(value)
